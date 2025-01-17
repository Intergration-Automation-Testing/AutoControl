import sys

from je_auto_control import hotkey

if sys.platform in ["win32", "cygwin", "msys"]:
    hotkey(["lcontrol", "a", "lcontrol", "c", "lcontrol", "v", "lcontrol", "v"])

elif sys.platform in ["darwin"]:
    hotkey(["command", "a", "command", "c", "command", "v", "command", "v"])

elif sys.platform in ["linux", "linux2"]:
    hotkey(["ctrl", "a", "ctrl", "c", "ctrl", "v", "ctrl", "v"])

