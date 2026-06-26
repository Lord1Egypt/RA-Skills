from typing import List, Optional
from app.config import VisionConfig
from core.types import DetectedElement, ElementType
from perception.screen_capture import ScreenCapture
from perception.ocr_engine import OCREngine
from perception.cv_detector import CVDetector
from perception.fusion import PerceptionFusion


class VisionEngine:
    def __init__(self, config: VisionConfig):
        self.capture = ScreenCapture(config.screenshot_dir)
        self.ocr = OCREngine(config.ocr_lang)
        self.cv = CVDetector()
        self.fusion = PerceptionFusion()
        self.config = config

    def locate(self, target_text: Optional[str] = None, target_type: Optional[ElementType] = None,
               position_hint: Optional[str] = None) -> Optional[DetectedElement]:
        ranked = self.locate_candidates(target_text=target_text, target_type=target_type, position_hint=position_hint)
        return ranked[0] if ranked else None

    def locate_candidates(self, target_text: Optional[str] = None, target_type: Optional[ElementType] = None,
                          position_hint: Optional[str] = None) -> List[DetectedElement]:
        image = self.capture.screenshot()
        candidates: List[DetectedElement] = []
        ocr_items: List[DetectedElement] = self.ocr.detect_text(image) if self.config.use_ocr else []
        candidates.extend(self._project_from_ocr(ocr_items, target_text, target_type))

        input_candidates = self.cv.detect_inputs(image) if target_type in {ElementType.INPUT, None} else []
        button_candidates = self.cv.detect_buttons(image) if target_type in {ElementType.BUTTON, None} else []

        if target_type == ElementType.INPUT:
            candidates.extend(self._bind_labels_to_inputs(ocr_items, input_candidates, target_text))
        if target_type == ElementType.BUTTON:
            candidates.extend(self._bind_text_to_buttons(ocr_items, button_candidates, target_text))

        candidates.extend(input_candidates)
        candidates.extend(button_candidates)
        if not candidates:
            return []
        return self.fusion.rank(candidates, target_text=target_text, target_type=target_type, position_hint=position_hint)

    def _project_from_ocr(self, ocr_items: List[DetectedElement], target_text: Optional[str], target_type: Optional[ElementType]) -> List[DetectedElement]:
        out: List[DetectedElement] = []
        for item in ocr_items:
            if not target_text:
                continue
            if target_text not in item.text and item.text not in target_text:
                continue
            x, y, w, h = item.bbox
            if target_type == ElementType.BUTTON:
                bbox = (max(0, x - 20), max(0, y - 10), max(80, w + 40), max(30, h + 20))
                etype = ElementType.BUTTON
            elif target_type == ElementType.INPUT:
                bbox = (max(0, x - 120), max(0, y - 18), max(260, w + 160), max(40, h + 16))
                etype = ElementType.INPUT
            else:
                bbox = item.bbox
                etype = ElementType.TEXT
            out.append(DetectedElement(etype, bbox, (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2), item.text, "ocr-proxy", item.score * 0.92))
        return out

    def _bind_labels_to_inputs(self, ocr_items: List[DetectedElement], inputs: List[DetectedElement], target_text: Optional[str]) -> List[DetectedElement]:
        out: List[DetectedElement] = []
        for inp in inputs:
            ix, iy = inp.center
            best_label = None
            best_dist = None
            for txt in ocr_items:
                tx, ty = txt.center
                dist = abs(tx - ix) + abs(ty - iy)
                if tx < ix and abs(ty - iy) < 80 and dist < 320:
                    if best_dist is None or dist < best_dist:
                        best_label, best_dist = txt, dist
            if best_label:
                cloned = DetectedElement(inp.element_type, inp.bbox, inp.center, inp.text, inp.source, inp.score, attributes=dict(inp.attributes))
                cloned.attributes["label_text"] = best_label.text
                if target_text and (target_text in best_label.text or best_label.text in target_text):
                    cloned.score += 0.28
                out.append(cloned)
        return out

    def _bind_text_to_buttons(self, ocr_items: List[DetectedElement], buttons: List[DetectedElement], target_text: Optional[str]) -> List[DetectedElement]:
        out: List[DetectedElement] = []
        for btn in buttons:
            bx, by = btn.center
            matched = None
            for txt in ocr_items:
                tx, ty = txt.center
                if abs(tx - bx) < max(btn.bbox[2] // 2, 70) and abs(ty - by) < max(btn.bbox[3] // 2, 30):
                    if target_text and (target_text in txt.text or txt.text in target_text):
                        matched = txt
                        break
                    if not matched:
                        matched = txt
            if matched:
                cloned = DetectedElement(btn.element_type, btn.bbox, btn.center, matched.text, btn.source, btn.score + 0.2, attributes=dict(btn.attributes))
                cloned.attributes["label_text"] = matched.text
                out.append(cloned)
        return out
