# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk


class UI(object):
    @staticmethod
    def str(): return tkinter.StringVar()

    @staticmethod
    def int(): return tkinter.IntVar()

    @staticmethod
    def bool(): return tkinter.BooleanVar()

    @staticmethod
    def create(parent, create_entry, create_var):
        var = create_var()
        entry = create_entry(parent, textvariable=var)
        return entry, var

    class Entry(object):
        def get(self): self.var.get()

        def get(self, value): self.var.set(value)

        def pack(self, *args, **kwargs):
            self.entry.pack(*args, **kwargs)
            return self

        def bind(self, name: str, func):
            self.entry.bind(name, lambda e: func(self, e))
            return self

    class Root(Entry):
        def __init__(self):
            self.entry = tkinter.Tk()

        def mainloop(self):
            self.entry.mainloop()
            return self

    class Combobox(Entry):
        def __init__(self, parent):
            self.entry, self.var = UI.create(parent.entry, ttk.Combobox, UI.str)

        def values(self, values):
            self.entry['values'] = values
            return self

        def action(self, func):
            self.bind("<<ComboboxSelected>>", func)
            return self
