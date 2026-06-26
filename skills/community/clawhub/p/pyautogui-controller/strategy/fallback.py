from typing import List, Optional


def relax_text_match(target_text: Optional[str]) -> List[Optional[str]]:
    if not target_text:
        return [None]
    variants = [target_text]
    stripped = target_text.replace("按钮", "").replace("输入框", "").replace("搜索框", "").strip()
    if stripped and stripped not in variants:
        variants.append(stripped)
    return variants
