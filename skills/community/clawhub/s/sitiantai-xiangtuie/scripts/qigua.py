"""
qigua.py — 起卦引擎（司天监象推演系统 v0.3.0）

支持两种起卦方式：
  B1: 梅花易数日期起卦（需 calendar/meihua 模块）
  B2: 掷铜钱起卦（传统三硬币法）

输出统一为 hexagram_encoding，可直接传入 liuyao.py 排盘。
"""

import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any


# ============================================================
# 编码映射
# ============================================================
# 六爻编码
#   1 = 少阴 (-- -- 阴爻静)
#   2 = 少阳 (----- 阳爻静)
#   3 = 老阳 (----- ○ 阳爻动)
#   4 = 老阴 (-- -- × 阴爻动)

# 铜钱背数 → 爻象
COIN_TO_LINE = {
    3: ("老阳", "----- ○", 3),   # 3背 → 老阳 动（阳爻动）
    2: ("少阴", "-- --",   1),   # 2背1字 → 少阴 静（阴爻静）
    1: ("少阳", "-----",   2),   # 1背2字 → 少阳 静（阳爻静）
    0: ("老阴", "-- -- ×", 4),   # 0背(3字) → 老阴 动（阴爻动）
}

# 八卦 → 三爻二进制
TRIGRAM_BINARY = {
    "乾": [1,1,1], "兑": [1,1,0], "离": [1,0,1], "震": [1,0,0],
    "巽": [0,1,1], "坎": [0,1,0], "艮": [0,0,1], "坤": [0,0,0],
}

# 三爻二进制 → 八卦
BINARY_TO_TRIGRAM = {tuple(v):k for k,v in TRIGRAM_BINARY.items()}


# ============================================================
# B1: 梅花易数日期起卦
# ============================================================

def meihua_date_qigua(year: int, month: int, day: int, hour: int) -> Dict:
    """
    梅花易数日期起卦。
    调用 meihua.py::compute_meihua 获取卦象，补充 hexagram_encoding。

    Returns:
        {
            "method": "meihua_date",
            "卦名": "...",
            "上卦": "...", "下卦": "...",
            "体卦": "...", "用卦": "...",
            "变爻": int,
            "变卦": {...}, "互卦": {...}, "错卦": {...}, "综卦": {...},
            "hexagram_encoding": [int]*6,
            "变卦_encoding": [int]*6,
        }
    """
    from scripts.meihua import compute_meihua

    # 调用 compute_meihua 获得完整卦象信息
    mh = compute_meihua(year, month, day, hour)

    # 从卦名反推上下卦二进制 → 六爻编码
    hexagram_encoding = _gua_name_to_encoding(mh["上卦"], mh["下卦"])
    bian_encoding = _gua_name_to_encoding(
        mh["变卦"]["上卦"], mh["变卦"]["下卦"]
    )

    # 动爻处理：将动爻位置上的编码改为 3(老阳动) 或 4(老阴动)
    change_line = mh["变爻"]
    if change_line and 1 <= change_line <= 6:
        idx = change_line - 1  # 编码索引：1→0(初爻), 6→5(上爻)
        if hexagram_encoding[idx] == 2:  # 少阳→老阳
            hexagram_encoding[idx] = 3
        elif hexagram_encoding[idx] == 1:  # 少阴→老阴
            hexagram_encoding[idx] = 4

    return {
        "method": "meihua_date",
        "卦名": mh["卦名"],
        "上卦": mh["上卦"],
        "下卦": mh["下卦"],
        "体卦": mh["体卦"],
        "用卦": mh["用卦"],
        "变爻": mh["变爻"],
        "变卦": mh["变卦"],
        "互卦": mh["互卦"],
        "错卦": mh["错卦"],
        "综卦": mh["综卦"],
        "hexagram_encoding": hexagram_encoding,
        "变卦_encoding": bian_encoding,
    }


def meihua_to_hexagram_encoding(meihua_result: Dict) -> List[int]:
    """
    梅花易数结果 → 六爻编码桥接。
    从 compute_meihua 或 meihua_date_qigua 的输出提取六爻编码。
    """
    if "hexagram_encoding" in meihua_result:
        return meihua_result["hexagram_encoding"]

    # 无编码时从卦名推导
    up = meihua_result.get("上卦", "")
    down = meihua_result.get("下卦", "")
    encoding = _gua_name_to_encoding(up, down)

    change_line = meihua_result.get("变爻", 0)
    if change_line and 1 <= change_line <= 6:
        idx = change_line - 1  # 1→0(初爻), 6→5(上爻)
        if encoding[idx] == 2:
            encoding[idx] = 3
        elif encoding[idx] == 1:
            encoding[idx] = 4

    return encoding


# ============================================================
# B2: 掷铜钱起卦
# ============================================================

def coin_toss_qigua(tosses: List[int]) -> Dict:
    """
    掷铜钱起卦（手动输入）。
    参数 tosses: [6个int]，每个为背数（0-3）
    返回: 完整起卦结果字典
    """
    if len(tosses) != 6:
        raise ValueError(f"需要6次掷铜钱结果，收到{len(tosses)}次")

    summary = []
    hexagram_encoding = []
    positions = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

    for i, backs in enumerate(tosses):
        backs = max(0, min(3, int(backs)))
        line_type, symbol, enc = COIN_TO_LINE[backs]
        summary.append({
            "爻位": positions[i],
            "背数": backs,
            "结果": line_type,
            "爻象": symbol,
        })
        hexagram_encoding.append(enc)

    # 获取卦名
    gua_name = _encoding_to_gua_name(hexagram_encoding)
    moving_indices = [i for i, v in enumerate(hexagram_encoding) if v in (3, 4)]

    return {
        "method": "coin_toss",
        "toss_summary": summary,
        "hexagram_encoding": hexagram_encoding,
        "卦名": gua_name,
        "动爻": moving_indices,
    }


def coin_toss_random() -> Dict:
    """随机模拟掷铜钱6次，返回完整起卦结果"""
    tosses = [random.randint(0, 3) for _ in range(6)]
    return coin_toss_qigua(tosses)


def coin_toss_interactive_input(input_str: str) -> Dict:
    """
    简化格式铜钱输入。
    支持格式：
      - "3 2 1 0 2 1"（空格分隔背数）
      - "3背 2背1字 1背2字 3字 2背1字 1背2字"（中文描述）
    """
    # 尝试解析为数字
    tokens = input_str.strip().split()
    if all(t.isdigit() for t in tokens):
        tosses = [int(t) for t in tokens]
        if len(tosses) == 6:
            return coin_toss_qigua(tosses)

    # 中文描述解析
    tosses = []
    for token in tokens:
        if "背" in token:
            # 提取背数
            num = ''.join(c for c in token if c.isdigit())
            tosses.append(int(num) if num else 3)
        elif "字" in token or token == "3字":
            tosses.append(0)
        else:
            raise ValueError(f"无法解析铜钱输入: {token}")

    if len(tosses) == 6:
        return coin_toss_qigua(tosses)
    raise ValueError(f"需要6次结果，当前{tosses}次")


def coin_toss_result_to_encoding(tosses: List[int]) -> List[int]:
    """铜钱背数列表 → 六爻编码列表"""
    return [COIN_TO_LINE[max(0, min(3, t))][2] for t in tosses]


# ============================================================
# 一站式：起卦 → 六爻排盘
# ============================================================

def qigua_full_pailian(encoding: List[int], time: Optional[datetime] = None,
                        reason: str = "") -> Dict:
    """
    起卦 → 六爻排盘一站式调用。
    参数:
        encoding: 六爻编码 [1,2,3,4]×6
        time: 时间（默认当前）
        reason: 原因描述
    返回: liuyao.py::arrange_hexagram 的完整输出
    """
    if time is None:
        time = datetime.now()

    from scripts.liuyao import arrange_hexagram
    return arrange_hexagram(encoding, time, reason)


# ============================================================
# 显示工具
# ============================================================

def encoding_to_display(encoding: List[int]) -> str:
    """六爻编码 → 爻象显示文本"""
    symbols = {1:"-- --", 2:"-----", 3:"----- ○", 4:"-- -- ×"}
    positions = ["上爻", "五爻", "四爻", "三爻", "二爻", "初爻"]
    lines = []
    for i in range(6):
        lines.append(f"{positions[i]}: {symbols.get(encoding[5-i], '?')}")
    return "\n".join(lines)


# ============================================================
# 内部工具
# ============================================================

def _gua_name_to_encoding(up_trigram: str, down_trigram: str) -> List[int]:
    """
    上下卦名 → 六爻编码列表（从初爻到上爻）。
    编码规则：1=少阴(阴爻静), 2=少阳(阳爻静)
    TRIGRAM_BINARY: 1=阳, 0=阴
    阳爻(b=1) → 少阳(2), 阴爻(b=0) → 少阴(1)
    """
    up_bin = TRIGRAM_BINARY.get(up_trigram, [0, 0, 0])
    down_bin = TRIGRAM_BINARY.get(down_trigram, [0, 0, 0])

    encoding = []
    for b in down_bin:    # 下卦：初二三爻
        encoding.append(2 if b == 1 else 1)  # 阳→2(少阳), 阴→1(少阴)
    for b in up_bin:      # 上卦：四五上爻
        encoding.append(2 if b == 1 else 1)

    return encoding


def _encoding_to_gua_name(encoding: List[int]) -> str:
    """
    六爻编码 → 卦名。
    编码: [1=少阴, 2=少阳, 3=老阳, 4=老阴]×6
    动爻(3,4)按静爻(2,1)处理。
    """
    # 动爻转为静爻: 老阳(3)→少阳(2), 老阴(4)→少阴(1)
    static = [2 if v == 3 else (1 if v == 4 else v) for v in encoding]

    # 拆为下卦（低3位）和上卦（高3位）
    lower = static[:3]   # 下卦: 初/二/三爻
    upper = static[3:]   # 上卦: 四/五/上爻

    # 编码→二进制: 少阳(2)→1(阳), 少阴(1)→0(阴)
    up_bin = tuple(1 if v == 2 else 0 for v in upper)
    down_bin = tuple(1 if v == 2 else 0 for v in lower)

    up_trigram = BINARY_TO_TRIGRAM.get(up_bin, "")
    down_trigram = BINARY_TO_TRIGRAM.get(down_bin, "")

    if not up_trigram or not down_trigram:
        return "未知卦"

    # 使用 meihua.py 的卦名查找
    try:
        from scripts.meihua import get_bian_gua_name
        return get_bian_gua_name(up_trigram, down_trigram)
    except ImportError:
        return f"{up_trigram}{down_trigram}"
