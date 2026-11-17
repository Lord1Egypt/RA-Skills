"""SkillQA Pro — module registry.

MODULES maps module name -> module class.  Dict order == execution order.
New module = new file in modules/ + one line in MODULES below.
"""
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from modules.static import StaticScan      # noqa: E402
from modules.sandbox import SandboxRun     # noqa: E402
from modules.log import LogAudit           # noqa: E402
from modules.novelty import NoveltyCheck   # noqa: E402
from modules.load import LoadTest          # noqa: E402
from modules.parallel import ParallelTest  # noqa: E402
from modules.compat import CompatCheck     # noqa: E402

MODULES = {
    "static": StaticScan,
    "sandbox": SandboxRun,
    "log": LogAudit,
    "novelty": NoveltyCheck,
    "load": LoadTest,
    "parallel": ParallelTest,
    "compat": CompatCheck,
}

__all__ = ["MODULES"]
