import re


class GemConfig:
    __root: dict
    __index: dict

    def __init__(self, filename):
        with open(filename) as file:
            self.__parse(file.read())

    def __parse(self, text):
        self.__text = text
        self.__root: dict = {}
        self.__index: dict = {}
        pos = 0
        pattern = re.compile("\\s*((?P<open>[{(])|(?P<close>[)}])|(?P<comment>;[^\r\n]*))\\s*")
        while pos < len(text):
            match = pattern.search(text, pos)
            if match.group("comment"):
                pos = match.end()
                continue
            if match.group("open"):
                pos = self.__parse_to_end(pattern,
                                          text,
                                          match.start(pattern.groupindex["open"]),
                                          match.end(pattern.groupindex["open"]),
                                          self.__root)
            else:
                raise Exception(f"Format error: {text[pos:pos + 20]}")

    def __parse_to_end(self, pattern: re.Pattern, text: str, pos: int, next_pos: int, parent: dict):
        childs: dict = {}
        while next_pos < len(text):
            match = pattern.search(text, next_pos)
            if not match:
                raise Exception(f"Format error: {text[pos:pos + 20]}")
            if match.group("comment"):
                next_pos = match.end()
                continue
            if match.group("close"):
                self.__index[pos] = parent[pos] = match.end(pattern.groupindex["close"]), childs
                return match.end()
            if match.group("open"):
                next_pos = self.__parse_to_end(pattern,
                                               text,
                                               match.start(pattern.groupindex["open"]),
                                               match.end(pattern.groupindex["open"]),
                                               childs)
        return next_pos

    def find(self, criteria: str):
        return self.__find(self.__root, criteria.split("/"), 0)

    def __find(self, items: dict, patterns: list[str], index: int):
        for item in items:
            text = self.__text[item:items[item][0]]
            if re.match(patterns[index], text):
                if index + 1 < len(patterns):
                    for inner in self.__find(items[item][1], patterns, index + 1):
                        yield inner
                else:
                    yield item

    def get(self, pos: int):
        item = self.__index[pos]
        if item is not None:
            return self.__text[pos:item[0]]

    def find_path(self, path: str):
        return self.__find(self.__root, ["\\s*[{(]" + re.escape(part) for part in path.split("/")], 0)

    def childs(self, pos):
        item = self.__index[pos]
        if item is not None:
            for child in item[1]:
                yield child

    def top(self):
        for item in self.__root:
            yield item

    def set(self, pos, value: str):
        item = self.__index[pos]
        if item is not None:
            self.__parse(self.__text[:pos] + value + self.__text[item[0]:])

    def save(self, filename: str):
        with open(filename, "w") as file:
            file.write(self.__text)
