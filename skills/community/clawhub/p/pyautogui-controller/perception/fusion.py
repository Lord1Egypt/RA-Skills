from typing import List, Optional
from core.types import DetectedElement, ElementType


class PerceptionFusion:
    def rank(self, candidates: List[DetectedElement], target_text: Optional[str] = None,
             target_type: Optional[ElementType] = None, position_hint: Optional[str] = None) -> List[DetectedElement]:
        scored = []
        for c in candidates:
            score = c.score
            if target_type and c.element_type == target_type:
                score += 0.25
            if target_text:
                text = (c.text or "").strip()
                if text:
                    if target_text == text:
                        score += 0.45
                    elif target_text in text:
                        score += 0.35
                    elif text in target_text:
                        score += 0.15
                if c.attributes.get("label_text"):
                    label = c.attributes["label_text"]
                    if target_text in label or label in target_text:
                        score += 0.22
            if position_hint:
                x, y = c.center
                if position_hint == "右下" and x > 1000 and y > 600:
                    score += 0.12
                elif position_hint == "左上" and x < 500 and y < 300:
                    score += 0.12
                elif position_hint == "中间":
                    score += 0.08
                elif position_hint == "右侧" and x > 900:
                    score += 0.08
                elif position_hint == "左侧" and x < 600:
                    score += 0.08
            score += min((c.bbox[2] * c.bbox[3]) / 50000.0, 0.05)
            scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored]
