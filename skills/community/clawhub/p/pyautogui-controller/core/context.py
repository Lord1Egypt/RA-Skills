import pyautogui
from core.types import RuntimeContext, BackendMode
from action.window_manager import WindowManager


def build_runtime_context(mode: str = "adaptive") -> RuntimeContext:
    size = pyautogui.size()
    backend = BackendMode.HYBRID if mode == "adaptive" else BackendMode(mode)
    ctx = RuntimeContext(screen_size=size, backend_mode=backend)
    ctx.safety_flags["window_manager_available"] = WindowManager().available
    return ctx
