# -*- coding: utf-8 -*-

from GemLib import GemConfig
from UILib import UI
from FsLib import FS

"""
root = UI.Root().geometry('300x200').resizable(True, True)

cb = UI.Combobox(root, state='readonly')\
    .values(("Period 1", "Period 2", "Period 3", "Period 4"))\
    .action(lambda s, e: print(e))\
    .pack(expand=True, fill="x")

root.mainloop()

config = GemConfig(r"d:\work\call_to_arms\gho\org\org19\gamelogic\set\stuff\gun\122mm_d25")

config.set(next(config.find_path('from/"shell_data_215"')),
           '("shell_data_215" shell(aphe) range(100500) a(205) b(183) c(162) d(144) e(128))')

print(config.get(next(config.top())))
"""
"""
print(FS.Path.part("d:\\\\work\\\\", -1))
print(FS.Path.part("d:\\\\work\\\\", -1, True))
print(FS.Path.part("\\\\mymy\\\\", 0))
print(FS.Path.part("\\\\mymy\\\\", 0, True))
print(FS.Path.part("single", -1))
print(FS.Path.part("single", -1, True))
print(FS.Path.part("single", 0))
print(FS.Path.part("single", 0, True))

#fs = FS()
#entity = FS.get(r"d:\work\call_to_arms\gho\extended_conquest_build\resource.zip\entity")
#print(entity.list(""))

"""

root = UI.Root().geometry('300x200').resizable(True, True)
scrolls = UI.Scrolls(root).pack(fill='both', expand=True)
tree = UI.TreeView(scrolls).put_to_scrolls(scrolls)\
    .columns({'c': 'column_c', 'b': 'column_b', 'a': 'column_a'})\
    .rows([("c1", "b1", "a1"), ("c2", "b2", "a2")])

root.mainloop()
