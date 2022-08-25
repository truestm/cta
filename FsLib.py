import array
import re
import zipfile
import os


class FS:
    __containers: array

    class Path:
        __split: re = re.compile("[\\\\/]+")

        @staticmethod
        def part(path: str, start: int = 0, alt: bool = False):
            separators = "\\/"
            start_pos = max(0, min(len(path) - 1, start if start >= 0 else len(path) + start))
            end_pos = len(path) if start >= 0 else -1
            delta = 1 if start >= 0 else -1
            pos = start_pos
            while pos != end_pos and separators.find(path[pos]) >= 0:
                pos += delta
            ns_start = pos
            ns_pos = pos
            while pos != end_pos and separators.find(path[pos]) < 0:
                ns_pos = pos
                pos += delta
            if alt:
                return path[pos:] if delta >= 0 else path[:ns_pos]
            return path[ns_start:ns_pos + delta] if delta >= 0 else path[ns_pos:ns_start - delta]

        @staticmethod
        def split(path: str):
            return [part for part in FS.Path.__split.split(path) if part] if path else []

        @staticmethod
        def join(parts):
            return str.join("\\", parts)

        @staticmethod
        def combine(path: str, part:str):
            return path.rstrip("\\/") + part.lstrip("\\/")

        @staticmethod
        def parent(path: str):
            return FS.Path.part(path, -1, True) if path else None

        @staticmethod
        def first(path: str):
            return FS.Path.part(path, 0) if path else None

        @staticmethod
        def last(path: str):
            return FS.Path.part(path, -1) if path else None

        @staticmethod
        def name(path: str):
            return FS.Path.last(path)

        @staticmethod
        def relative(base: str, path: str):
            base_parts = FS.Path.split(base)
            path_parts = FS.Path.split(path)
            if base_parts != path_parts[:len(base_parts)]:
                return None
            return FS.Path.join(path_parts[len(base_parts):])

    class Container(object):
        __path: str
        __parent: object

        def __init__(self, parent, path):
            self.__parent = parent
            self.__path = path

        def fullname(self):
            return FS.Path.combine(self.__parent.fullname(), self.__path)

        def full_path(self, path: str):
            return FS.Path.combine(self.__path, path)

        def is_container(self, path: str):
            return self.__parent.is_container(FS.Path.join(self.full_path(path)))

        def is_file(self, path: str):
            return self.__parent.is_file(FS.Path.join(self.full_path(path)))

        def is_exists(self, path: str):
            return self.__parent.is_exists(FS.Path.join(self.full_path(path)))

        def get(self, path: str):
            if self.is_container(path):
                return FS.Container(self, path)
            if self.is_file(path):
                if FS.Archive.is_archive(self.full_path(path)):
                    return FS.Archive(self.full_path(path))
                return FS.File(self, path)
            return None

        def read(self, path: str):
            return self.__parent.read(FS.Path.join(self.full_path(path)))

        def write(self, path: str, value: str):
            return self.__parent.write(FS.Path.join(self.full_path(path)))

        def list(self, path: str):
            return self.__parent.list(FS.Path.join(self.full_path(path)))

    class Folder(Container):
        def __init__(self, path):
            self.__container = None
            self.__path = path

        def fullname(self):
            return self.__container.fullname() if self.__container else ""

        def fullpath(self, path: str):
            return FS.Path.combine(self.fullname(), path)

        def read(self, path: str):
            with open(self.full_path(path)) as file:
                return file.read()

        def list(self, path: str):
            return os.listdir(self.fullpath(path))

        def is_container(self, path: str):
            full_path = self.full_path(path)
            return os.path.exists(full_path) and os.path.isdir(full_path)

        def is_file(self, path: str):
            full_path = self.full_path(path)
            return os.path.exists(full_path) and os.path.isfile(full_path)

        def is_exists(self, path: str):
            return os.path.exists(self.full_path(path))

    class Archive(Container):

        def __init__(self, path):
            self.__container = None
            self.__path = path

        def fullname(self):
            return self.__container.fullname() if self.__container else ""

        def read(self, path: str):
            with open(self.__path) as file:
                file.read()

        def list(self, path: str):
            with zipfile.ZipFile(self.__path) as z_file:
                return set([name for name in
                            [FS.Path.first(FS.Path.relative(path, full_path)) for full_path in z_file.namelist()] if
                            name])

        def get_all_info(self):
            with zipfile.ZipFile(self.__path) as z_file:
                return z_file.infolist()

        def get_info(self, path: str):
            parts = FS.Path.split(path)
            for info in self.get_all_info():
                if FS.Path.split(info.filename) == parts:
                    return info
            pass

        def is_container(self, path: str):
            info = self.get_info(path)
            return info is not None and info.is_dir()

        def is_file(self, path: str):
            info = self.get_info(path)
            return info is not None and not info.is_dir()

        def is_exists(self, path: str):
            return self.get_info(path) is not None


    class File:
        __container: object
        __path: str

        def __init__(self, container, path):
            self.__container = container
            self.__path = path

        def fullname(self):
            return FS.Path.combine(self.__container.fullname(), self.__path)

        def container(self):
            return self.__container

        def read(self):
            return self.__container.read(self.__path)

        def write(self, value):
            return self.__container.write(self.__path, value)

    def add(self, path: str):
        return self

    def get(self, path: str):
        return self

    def list(self, path: str):
        return self

    @staticmethod
    def is_archive(path: str):
        return FS.is_exists(path) and zipfile.is_zipfile(path)

    @staticmethod
    def is_folder(path: str):
        return FS.is_exists(path) and os.path.isdir(path)

    @staticmethod
    def is_exists(path: str):
        return os.path.exists(path)

    @staticmethod
    def get_exist_path(path: str):
        parts = FS.Path.split(path)
        for part in range(len(parts)):
            if not FS.is_exists(FS.Path.join(parts[:part + 1])):
                return FS.Path.join(parts[:part]), FS.Path.join(parts[part:])
        return FS.Path.join(parts), None

    @staticmethod
    def get(path: str):
        if FS.is_folder(path):
            return FS.Folder(path)
        if FS.is_archive(path):
            return FS.Archive(path)
        if FS.is_exists(path):
            return FS.Folder(FS.Path.parent(path), FS.Path.name(path))
        exist,tail = FS.get_exist_path(path)
        if FS.is_archive(exist):
            archive = FS.Archive(exist)
            if archive.is_container(tail):
                return FS.Container(archive, tail)
            if archive.is_file(tail):
                return FS.File(archive, tail)

