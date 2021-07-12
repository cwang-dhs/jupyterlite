"""A Python kernel backed by Pyodide"""

__version__ = "0.1.0a4"

import sys
import types

# Set the recursion limit, needed for altair
# for more details, see: https://github.com/jupyterlite/jupyterlite/pull/113#issuecomment-851072065
sys.setrecursionlimit(max(175, sys.getrecursionlimit()))

termios_mock = types.ModuleType("termios")
termios_mock.TCSAFLUSH = 2

sys.modules["termios"] = termios_mock
sys.modules["fcntl"] = types.ModuleType("fcntl")
sys.modules["resource"] = types.ModuleType("resource")

# This is needed for some Matplotlib backends (webagg, ipympl)
sys.modules["tornado"] = types.ModuleType("tornados")

from .display import LiteStream
from .interpreter import LitePythonShellApp
from .patches import register_patches

stdout_stream = LiteStream("stdout")
stderr_stream = LiteStream("stderr")

ipython_shell_app = LitePythonShellApp()
ipython_shell_app.initialize()
ipython_shell = ipython_shell_app.shell
kernel_instance = ipython_shell.kernel

sys.stdout = stdout_stream
sys.stderr = stderr_stream

register_patches()
