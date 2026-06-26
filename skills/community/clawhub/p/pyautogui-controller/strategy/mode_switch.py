from core.types import BackendMode


class ModeSwitch:
    def choose_backend(self, has_dom: bool, window_available: bool, target_kind: str = "generic") -> BackendMode:
        if has_dom and target_kind in {"browser", "input", "button"}:
            return BackendMode.BROWSER
        if window_available:
            return BackendMode.HYBRID
        return BackendMode.VISION
