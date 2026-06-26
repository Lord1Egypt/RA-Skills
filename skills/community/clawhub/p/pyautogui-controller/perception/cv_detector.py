from typing import List, Optional
from core.types import DetectedElement, ElementType


class CVDetector:
    def __init__(self):
        try:
            import cv2  # noqa: F401
            self.available = True
        except Exception:
            self.available = False

    def detect_inputs(self, image) -> List[DetectedElement]:
        if not self.available:
            return []
        import cv2
        import numpy as np
        arr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidates: List[DetectedElement] = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w < 120 or h < 24:
                continue
            ratio = w / max(h, 1)
            if ratio < 2.5:
                continue
            if h > 90:
                continue
            candidates.append(DetectedElement(
                element_type=ElementType.INPUT,
                bbox=(x, y, w, h),
                center=(x + w // 2, y + h // 2),
                text="",
                source="cv",
                score=min(0.45 + min(ratio / 10.0, 0.35), 0.9),
            ))
        candidates.sort(key=lambda e: (e.score, e.bbox[2] * e.bbox[3]), reverse=True)
        return candidates[:10]

    def detect_buttons(self, image) -> List[DetectedElement]:
        if not self.available:
            return []
        import cv2
        import numpy as np
        arr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        results: List[DetectedElement] = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w < 60 or h < 22:
                continue
            if w > 420 or h > 120:
                continue
            results.append(DetectedElement(
                element_type=ElementType.BUTTON,
                bbox=(x, y, w, h),
                center=(x + w // 2, y + h // 2),
                source="cv",
                score=0.4,
            ))
        results.sort(key=lambda e: e.bbox[2] * e.bbox[3], reverse=True)
        return results[:12]
