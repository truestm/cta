# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk


class UI(object):
    @staticmethod
    def str():
        return tkinter.StringVar()

    @staticmethod
    def int():
        return tkinter.IntVar()

    @staticmethod
    def bool():
        return tkinter.BooleanVar()

    class Entry(object):
        entry: object
        var: object

        def __init__(self, entry, var=None, var_prop=None):
            self.entry = entry
            self.var = var
            if var_prop:
                self.entry[var_prop] = var

        def get(self):
            self.var.get()

        def set(self, value):
            self.var.set(value)

        def pack(self, *args, **kwargs):
            self.entry.pack(*args, **kwargs)
            return self

        def grid(self, *args, **kwargs):
            self.entry.grid(*args, **kwargs)
            return self

        def bind(self, name: str, func):
            self.entry.bind(name, lambda e: func(self, e))
            return self

        def configure(self, **kwargs):
            self.entry.configure(**kwargs)
            return self

        def put_to_scrolls(self, scrolls: object):
            scrolls.put(self)
            return self

    class Root(Entry):
        def __init__(self, **kwargs):
            super().__init__(tkinter.Tk(**kwargs))

        def geometry(self, *args, **kwargs):
            self.entry.geometry(*args, **kwargs)
            return self

        def resizable(self, *args, **kwargs):
            self.entry.resizable(*args, **kwargs)
            return self

        def title(self, *args, **kwargs):
            self.entry.title(*args, **kwargs)
            return self

        def mainloop(self):
            self.entry.mainloop()
            return self

    class Combobox(Entry):
        def __init__(self, parent, **kwargs):
            super().__init__(ttk.Combobox(parent.entry, **kwargs), UI.str(), "textvariable")

        def values(self, values):
            self.entry['values'] = values
            return self

        def action(self, func):
            self.bind("<<ComboboxSelected>>", func)
            return self

    class TreeView(Entry):
        entry: ttk.Treeview

        def __init__(self, parent, **kwargs):
            super().__init__(ttk.Treeview(parent.entry, **kwargs))

        def columns(self, columns: dict):
            self.configure(columns=[*columns.keys()], show='headings')
            for k, v in columns.items():
                self.entry.heading(k, text=v)
            return self

        def rows(self, rows: list):
            k: int = 0
            for v in rows:
                self.entry.insert("", k, values=v)
                ++k
            return self

        def insert(self, **kwargs):
            self.entry.insert(**kwargs)
            return self

    class Scrolls(Entry):
        def __init__(self, parent, **kwargs):
            super().__init__(ttk.Frame(parent.entry, **kwargs), None)
            self.entry.grid_columnconfigure(0, weight=1)
            self.entry.grid_rowconfigure(0, weight=1)
            self.v_scroll = ttk.Scrollbar(self.entry, orient=tkinter.VERTICAL)
            self.h_scroll = ttk.Scrollbar(self.entry, orient=tkinter.HORIZONTAL)
            self.v_scroll.grid(row=0, column=1, sticky='ns')
            self.h_scroll.grid(row=1, column=0, sticky='ew')

        def put(self, control):
            self.v_scroll["command"] = control.entry.yview
            self.h_scroll["command"] = control.entry.xview
            control.configure(yscroll=self.v_scroll, xscroll=self.h_scroll)
            control.grid(row=0, column=0, sticky='nsew')
            return self
