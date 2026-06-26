from dataclasses import dataclass
from typing import List, Optional


@dataclass
class WindowInfo:
    title: str
    left: int = 0
    top: int = 0
    width: int = 0
    height: int = 0
    active: bool = False


class WindowManager:
    def __init__(self):
        try:
            import pygetwindow  # noqa: F401
            self.available = True
        except Exception:
            self.available = False

    def list_windows(self) -> List[WindowInfo]:
        if not self.available:
            return []
        import pygetwindow as gw
        infos = []
        for w in gw.getAllWindows():
            title = (w.title or "").strip()
            if not title:
                continue
            infos.append(WindowInfo(title=title, left=w.left, top=w.top, width=w.width, height=w.height, active=w.isActive))
        return infos

    def _score_window(self, title: str, keywords: List[str], is_active: bool) -> int:
        t = title.lower()
        score = 0
        for kw in keywords:
            if not kw:
                continue
            k = kw.lower().strip()
            if not k:
                continue
            if t == k:
                score += 100
            elif t.endswith(k):
                score += 60
            elif k in t:
                score += 30 + min(len(k), 20)
        if is_active:
            score += 12
        return score

    def find_window(self, keywords) -> Optional[WindowInfo]:
        if not self.available:
            return None
        import pygetwindow as gw
        lowered = [k.lower() for k in keywords if k]
        if not lowered:
            return None

        best = None
        best_score = 0
        for w in gw.getAllWindows():
            title = (w.title or "").strip()
            if not title:
                continue
            score = self._score_window(title, lowered, w.isActive)
            if score > best_score:
                best_score = score
                best = w

        if not best or best_score <= 0:
            return None

        return WindowInfo(title=best.title.strip(), left=best.left, top=best.top, width=best.width, height=best.height, active=best.isActive)

    def get_active_window(self) -> Optional[WindowInfo]:
        if not self.available:
            return None
        import pygetwindow as gw
        try:
            w = gw.getActiveWindow()
        except Exception:
            return None
        if not w or not (w.title or "").strip():
            return None
        return WindowInfo(title=w.title.strip(), left=w.left, top=w.top, width=w.width, height=w.height, active=True)

    def activate_window(self, keywords) -> bool:
        if not self.available:
            return False
        import pygetwindow as gw
        lowered = [k.lower() for k in keywords if k]
        if not lowered:
            return False

        candidate = None
        best_score = 0
        for w in gw.getAllWindows():
            title = (w.title or "").strip()
            if not title:
                continue
            score = self._score_window(title, lowered, w.isActive)
            if score > best_score:
                best_score = score
                candidate = w

        if not candidate or best_score <= 0:
            return False

        try:
            if candidate.isMinimized:
                candidate.restore()
            candidate.activate()
            return True
        except Exception:
            return False

    def wait_for_window(self, keywords, timeout: float = 6.0, interval: float = 0.25) -> Optional[WindowInfo]:
        import time
        end = time.time() + timeout
        while time.time() < end:
            found = self.find_window(keywords)
            if found:
                return found
            time.sleep(interval)
        return None
