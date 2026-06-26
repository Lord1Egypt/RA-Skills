import os
import shutil
from pathlib import Path
from typing import List
from core.types import DetectedElement, ElementType


class OCREngine:
    def __init__(self, lang: str = "chi_sim+eng"):
        self.lang = lang
        self.available = False
        self.tesseract_path = ""

        try:
            import pytesseract
            self.tesseract_path = self._resolve_tesseract_path()
            if self.tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
            self.available = True
        except Exception:
            self.available = False

    def _resolve_tesseract_path(self) -> str:
        env_path = os.environ.get("TESSERACT_CMD") or os.environ.get("TESSERACT_PATH")
        if env_path and Path(env_path).exists():
            return str(Path(env_path))

        which = shutil.which("tesseract")
        if which:
            return which

        candidates = [
            Path(r"C:\Users\dev\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
            Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
            Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
        ]
        for p in candidates:
            if p.exists():
                return str(p)

        return ""

    def detect_text(self, image) -> List[DetectedElement]:
        if not self.available:
            return []

        try:
            import pytesseract
            data = pytesseract.image_to_data(image, lang=self.lang, output_type=pytesseract.Output.DICT)
        except Exception:
            return []

        results: List[DetectedElement] = []
        for i, txt in enumerate(data.get("text", [])):
            txt = (txt or "").strip()
            if not txt:
                continue
            conf_raw = data.get("conf", [0])[i]
            conf = float(conf_raw) if str(conf_raw).strip() not in {"", "-1"} else 0.0
            if conf < 20:
                continue
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            results.append(DetectedElement(
                element_type=ElementType.TEXT,
                bbox=(x, y, w, h),
                center=(x + w // 2, y + h // 2),
                text=txt,
                source="ocr",
                score=min(conf / 100.0, 0.99),
            ))
        return results
