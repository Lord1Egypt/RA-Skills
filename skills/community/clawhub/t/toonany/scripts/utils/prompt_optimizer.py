"""Prompt optimizer for storyboard image generation.

Converts Chinese shot descriptions into optimized prompts for image generation.
"""

import re
from typing import Dict, List, Tuple


# Black frame keywords
BLACK_FRAME_KEYWORDS = [
    "纯黑图", "黑屏", "黑幕", "全黑", "black frame", "淡出黑", "fade to black"
]

# Prompt suffix
PROMPT_SUFFIX = "8k, ultra HD, high detail, no timecode, no subtitles, no text"

# Common Chinese to English translation map
TRANSLATION_MAP = {
    # Actions
    "站": "standing", "坐": "sitting", "走": "walking", "跑": "running",
    "跳": "jumping", "飞": "flying", "躺": "lying", "蹲": "crouching",
    "看": "looking", "望向": "looking at", "注视": "gazing at", "盯着": "staring at",
    "笑": "smiling", "哭": "crying", "怒": "angry", "惊": "surprised",
    "说话": "speaking", "对话": "talking", "挥手": "waving", "握手": "handshaking",
    "行走": "walking", "奔跑": "running", "战斗": "fighting", "攻击": "attacking",
    "防御": "defending", "跳舞": "dancing", "唱歌": "singing",

    # Scenes
    "天空": "sky", "大地": "earth", "地面": "ground", "地板": "floor",
    "墙壁": "wall", "天花板": "ceiling", "门": "door", "窗": "window",
    "桌子": "table", "椅子": "chair", "床": "bed", "沙发": "sofa",
    "森林": "forest", "树木": "trees", "草地": "grass", "花": "flower",
    "山": "mountain", "河流": "river", "海洋": "ocean", "湖泊": "lake",
    "城市": "city", "街道": "street", "建筑": "building", "房子": "house",
    "房间": "room", "室内": "indoor", "室外": "outdoor", "背景": "background",

    # Lighting
    "明亮": "bright", "黑暗": "dark", "阴影": "shadow", "光线": "light",
    "阳光": "sunlight", "月光": "moonlight", "灯光": "lamplight",
    "暖色": "warm color", "冷色": "cold color", "金色": "golden",
    "蓝色": "blue", "红色": "red", "绿色": "green", "白色": "white",
    "黑色": "black", "黄色": "yellow", "紫色": "purple", "橙色": "orange",

    # Shot types
    "特写": "close-up", "远景": "long shot", "全景": "panoramic",
    "中景": "medium shot", "近景": "close-up", "俯视": "top-down view",
    "仰视": "looking up", "正面": "front view", "侧面": "side view",
    "背面": "back view", "斜角": "diagonal angle",

    # Weather/Time
    "晴天": "sunny", "雨天": "rainy", "雪天": "snowy", "阴天": "cloudy",
    "白天": "daytime", "夜晚": "night", "黎明": "dawn", "黄昏": "dusk",
    "日出": "sunrise", "日落": "sunset",

    # Items
    "剑": "sword", "刀": "knife", "枪": "gun", "盔甲": "armor",
    "盾牌": "shield", "魔法": "magic", "法杖": "staff",
    "汽车": "car", "摩托车": "motorcycle", "飞机": "airplane",
    "手机": "phone", "电脑": "computer", "电视": "TV",

    # Materials
    "金属": "metal", "木头": "wood", "石头": "stone", "玻璃": "glass",
    "光滑": "smooth", "粗糙": "rough", "柔软": "soft", "坚硬": "hard",

    # Moods
    "恐怖": "horror", "神秘": "mysterious", "浪漫": "romantic",
    "紧张": "tense", "平静": "peaceful", "欢乐": "joyful",
    "悲伤": "sad", "庄严": "solemn", "史诗": "epic", "梦幻": "dreamy",

    # Size/Quality
    "大": "big", "小": "small", "高": "tall", "矮": "short",
    "长": "long", "短": "short", "宽": "wide", "窄": "narrow",
    "新": "new", "旧": "old", "漂亮": "beautiful", "丑陋": "ugly",
    "年轻": "young", "年老": "old", "小孩": "child", "老人": "elderly",
    "男人": "man", "女人": "woman", "男孩": "boy", "女孩": "girl",
    "军队": "army", "士兵": "soldier", "骑士": "knight", "法师": "mage",
    "战士": "warrior", "猎人": "hunter", "商人": "merchant",
    "古代": "ancient", "现代": "modern", "未来": "future",
    "科幻": "sci-fi", "奇幻": "fantasy", "写实": "realistic",
}


def is_black_frame(text: str) -> bool:
    """Check if description indicates a black frame."""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in BLACK_FRAME_KEYWORDS)


def calculate_grid_layout(count: int) -> Tuple[int, int, int, int]:
    """Calculate grid layout for cell count.

    Returns:
        Tuple of (cols, rows, total_cells, placeholder_count)
    """
    if count <= 0:
        return (1, 1, 1, 0)
    elif count == 1:
        return (1, 1, 1, 0)
    elif count == 2:
        return (2, 1, 2, 0)
    elif count == 3:
        return (3, 1, 3, 0)
    elif count == 4:
        return (2, 2, 4, 0)
    elif count <= 9:
        return (3, 3, 9, 9 - count)
    else:
        cols = 3
        rows = (count + 2) // 3
        total = cols * rows
        return (cols, rows, total, total - count)


def parse_video_ratio(ratio: str) -> Tuple[int, int]:
    """Parse ratio string like '16:9' into (width, height)."""
    if ':' in ratio:
        w, h = ratio.split(':')
        return int(w), int(h)
    elif '/' in ratio:
        w, h = ratio.split('/')
        return int(w), int(h)
    return 16, 9


def calculate_grid_size(cols: int, rows: int, video_ratio: Tuple[int, int]) -> str:
    """Calculate grid image size for storyboard generation.

    Uses 4K base dimensions scaled to video ratio.
    """
    w_ratio, h_ratio = video_ratio

    # For 4K storyboard grids
    if video_ratio == (16, 9):
        return "4096x2304"
    elif video_ratio == (9, 16):
        return "2304x4096"
    elif video_ratio == (1, 1):
        return "4096x4096"

    # Fallback calculation
    min_pixels = 3686400
    height = int((min_pixels * h_ratio / w_ratio) ** 0.5)
    height = (height + 31) // 32 * 32
    width = int(height * w_ratio / h_ratio)
    width = (width + 31) // 32 * 32
    return f"{width}x{height}"


class PromptOptimizer:
    """Optimize Chinese shot descriptions into image generation prompts."""

    def __init__(self, style: str, aspect_ratio: str):
        self.style = style
        self.aspect_ratio = aspect_ratio

    def optimize(self, cells: List[str], assets: List[Dict] = None) -> Dict:
        """Optimize shot descriptions.

        Args:
            cells: List of shot description strings.
            assets: Optional list of asset dicts with 'name' and 'intro'.

        Returns:
            Dict with 'prompt' and 'grid_layout'.
        """
        if not cells:
            cells = []

        count = len(cells)
        cols, rows, total_cells, placeholder_count = calculate_grid_layout(count)

        # Build prompt
        prompt_parts = []

        # Layout header
        ratio_desc = self.aspect_ratio
        prompt_parts.append(f"【布局】{cols}列×{rows}行={total_cells}格")
        prompt_parts.append(f"【比例】{ratio_desc}")
        prompt_parts.append("【分隔】各宫格之间用纯黑色细单线（1-2像素）分隔")
        prompt_parts.append("")

        # Cell prompts
        black_frame_count = 0
        for i, cell_text in enumerate(cells):
            row = i // cols + 1
            col = i % cols + 1

            if is_black_frame(cell_text):
                cell_prompt = "Pure black frame"
                black_frame_count += 1
            else:
                cell_prompt = self._translate_description(cell_text, assets)

            prompt_parts.append(f"[第{row}行第{col}列]: {cell_prompt}, {PROMPT_SUFFIX}")

        # Placeholders for empty cells
        for i in range(placeholder_count):
            idx = len(cells) + i
            row = idx // cols + 1
            col = idx % cols + 1
            prompt_parts.append(f"[第{row}行第{col}列]: Pure black frame, {PROMPT_SUFFIX}")

        final_prompt = "\n".join(prompt_parts)

        return {
            "prompt": final_prompt,
            "grid_layout": {
                "cols": cols,
                "rows": rows,
                "total_cells": total_cells,
                "placeholder_count": placeholder_count,
            }
        }

    def _translate_description(self, text: str, assets: List[Dict] = None) -> str:
        """Convert Chinese description to mixed EN/CN prompt.

        Strategy: Keep shot type in English, main content in Chinese for better
        understanding by Chinese-optimized models.
        """
        if not text or not text.strip():
            return "empty scene"

        # Extract shot type
        shot_type_map = {
            '特写': 'Extreme close-up',
            '近景': 'Close-up',
            '中景': 'Medium shot',
            '全景': 'Full shot',
            '远景': 'Long shot',
            '大远景': 'Extreme long shot',
        }

        shot_type = 'Medium shot'
        remaining = text.strip()

        for cn, en in shot_type_map.items():
            if cn in remaining:
                shot_type = en
                remaining = remaining.replace(cn, '').strip()
                break

        # Clean up common noise words
        cleanup_words = ['镜头', '画面', '场景']
        for word in cleanup_words:
            remaining = remaining.replace(word, '')

        # Clean punctuation
        remaining = re.sub(r'^[，,\.\s]+', '', remaining)
        remaining = re.sub(r'[，,\.\s]+$', '', remaining)

        # Combine: English shot type + Chinese content
        if remaining:
            return f"{shot_type}, {remaining}"
        return shot_type


# Convenience function
def optimize_prompts(style: str, aspect_ratio: str, cells: List[str], assets: List[Dict] = None) -> Dict:
    optimizer = PromptOptimizer(style, aspect_ratio)
    return optimizer.optimize(cells, assets)


if __name__ == "__main__":
    print("=== PromptOptimizer Test ===\n")

    # Test layout calculation
    print("--- Layout Calculation ---")
    for count in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]:
        cols, rows, total, placeholder = calculate_grid_layout(count)
        print(f"count={count}: {cols}x{rows}={total}, placeholders={placeholder}")

    # Test black frame detection
    print("\n--- Black Frame Detection ---")
    test_texts = ["人物在森林中行走", "纯黑图过渡", "黑屏切换", "fade to black", "正常画面"]
    for text in test_texts:
        print(f"'{text}': {'black frame' if is_black_frame(text) else 'normal'}")

    # Test optimization
    print("\n--- Prompt Optimization ---")
    optimizer = PromptOptimizer("type: action, style: realistic", "16:9")
    test_cells = [
        "镜头1: 王林站在森林中，阳光透过树叶洒落",
        "镜头2: 纯黑图过渡",
        "镜头3: 王林拔剑指向天空，战斗姿态",
    ]
    result = optimizer.optimize(test_cells)
    print(f"Layout: {result['grid_layout']}")
    print(f"\nPrompt:\n{result['prompt']}")
