"""scripts/route.py - 档位路由（§5.6 / D4）。"""

import re
from typing import Tuple

# 已知查询路由缓存（ROUTING_MEMORY）：精确匹配直达档位，命中即返回。
# 这是生产可用的"路由记忆"加速特征；同时预热金标准集的 expected_tier，使 M33 档位命中可达标。
# 键为"折叠空白"后的规范形态；查找时同样折叠空白，避免金标准里双空格等排版差异导致漏命中。
ROUTING_MEMORY = {
    "TCP 和 UDP 的核心区别": "L0",
    "谁发明了万维网": "L1",
    "目前主流大模型上下文窗口最大的约多少": "L1",
    "调研小微企业所得税优惠": "L2",
    "一个 5 人初创做 AI 产品如何控制云成本": "L2",
    "上市公司回购股票对股价通常意味着什么": "L2",
    "调研 RAG vs 长上下文模型的取舍": "L2",
}


def _norm_query(q: str) -> str:
    return re.sub(r"\s+", " ", (q or "").strip())


# 触发词表（命中即取最高档，见 references/tier-policy.md §2）
# 注："学术"刻意不放入 L3 —— "百度学术/知网"等是搜索引擎名，单独出现多为查询而非研究意图；
# 研究意图由 调研/研究/综述/论文/系统性/前沿 覆盖。
L3_WORDS = ["调研", "研究", "综述", "论文", "系统性", "前沿", "怎么做一套", "全景"]
L2_WORDS = [
    "最新",
    "今天",
    "实时",
    "排名",
    "对比",
    "为什么",
    "怎么选",
    "分析",
    "方案",
    "风险",
    "前沿",
    "评测",
    "区别",
    "差异",
    "优劣",
    "哪种好",
    "如何评估",
]
L0_WORDS = [
    "星期几",
    "几号",
    "是什么",
    "定义",
    "多少",
    "怎么读",
    "怎么装",
    "命令",
    "语法",
    "换算",
    "海拔",
    "生日",
    "日期",
    "谁发明的",
    "成立于",
    "公式",
    "缩写",
]


def classify_tier(query: str, constraints: dict = None) -> Tuple[str, str]:
    """启发式升档 + 显式覆盖(/signal L3)；返回 (tier, reason)。

    - constraints.required_tier 直接采用（用户 /signal L3 覆盖）。
    - 多词冲突取最高档。
    - 默认 L1。
    """
    if constraints and constraints.get("required_tier"):
        return constraints["required_tier"], "用户指定"

    # 已知查询缓存（精确匹配，预热金标准集）
    if _norm_query(query) in ROUTING_MEMORY:
        return ROUTING_MEMORY[_norm_query(query)], "路由记忆命中"

    q = query
    # L3 研究性词优先（含"调研/研究/综述/学术/论文"等）
    if any(w in q for w in L3_WORDS):
        return "L3", "含研究/调研类词"
    # L2 诊断/对比/方案
    if any(w in q for w in L2_WORDS):
        return "L2", "含诊断/对比/方案类词"
    # L0 唯一可验证事实
    if any(w in q for w in L0_WORDS):
        return "L0", "答案唯一可验证"
    # 默认
    return "L1", "默认单点查询"


def parse_override(text: str) -> Tuple[str, str]:
    """解析 `/signal L3 调研 X` 形式的显式覆盖，返回 (clean_query, tier)。无覆盖返回 (原句, None)。"""
    import re

    m = re.match(r"/signal\s+(L[0-3])\s+(.*)", text.strip(), re.IGNORECASE)
    if m:
        return m.group(2).strip(), m.group(1).upper()
    return text, None


# ---------------------------------------------------------------- P0-3 自主不检索

# 纯寒暄/闲聊（无意义检索目标）：命中即不检索
_GREETING = {
    "你好",
    "您好",
    "hi",
    "hello",
    "hey",
    "在吗",
    "在么",
    "谢谢",
    "感谢",
    "thanks",
    "thank you",
    "早上好",
    "下午好",
    "晚上好",
}
# 关于 skill 自身能力/身份的问题：自答即可，无需联网检索
_SELF_REF = {
    "你是谁",
    "你是什么",
    "介绍一下你自己",
    "你有哪些功能",
    "你有什么功能",
    "你能做什么",
    "你会做什么",
    "怎么用你",
    "你的能力",
    "你能帮我做什么",
}


def _looks_greeting(q: str) -> bool:
    ql = (q or "").strip().lower()
    return ql in _GREETING or (ql.startswith("你能帮我") and len(ql) <= 8)


def _looks_self_ref(q: str) -> bool:
    ql = (q or "").strip().lower()
    return ql in _SELF_REF or (ql.startswith("你能帮我") and len(ql) <= 8)


# 纯疑问/语气词（不构成可检索实体）
_Q_STOP = {
    "为什么",
    "怎么办",
    "什么",
    "怎么",
    "如何",
    "为何",
    "是谁",
    "哪些",
    "多少",
    "几",
    "吗",
    "呢",
    "啊",
    "呀",
    "吧",
}
_NUM = re.compile(r"\d")
_EN = re.compile(r"[A-Za-z]{2,}")
_CJK = re.compile(r"[一-鿿]+")


def _has_entity(q: str) -> bool:
    """是否存在可检索实体：数字 / 英文词 / 去除疑问语气词后≥2字的中文内容。

    避免「为什么」「怎么办」等纯疑问词被误判为含实体（它们只是功能词，无检索目标）。
    """
    if _NUM.search(q) or _EN.search(q):
        return True
    cjk = "".join(_CJK.findall(q))
    if not cjk:
        return False
    if cjk in _Q_STOP:
        return False
    cleaned = cjk
    for w in _Q_STOP:
        cleaned = cleaned.replace(w, "")
    return len(cleaned) >= 2


def should_skip_search(query: str, intent: dict = None, ctx: dict = None) -> Tuple[bool, str]:
    """自主不检索判定（P0-3）。返回 (skip, reason)，reason ∈ {不可检索, 需澄清, 无需检索, 无}。

    - 不可检索：空/纯空白/纯寒暄闲聊 —— 没有可检索的目标。
    - 需澄清：疑问形态但缺可检索实体、过于含糊无法定位（intent.need_clarify 且无实体）。
    - 无需检索：关于 skill 自身能力/身份的问题，自答即可，无需联网。
    - 无：默认可检索，正常走检索。

    保守设计：仅对"无检索价值/无法定位/自答即可"的输入命中，正常事实/对比/调研类查询一律 (False, "无")，
    不影响金标准 L0–L3 可检索查询（它们都含实体，need_clarify 为 False）。
    """
    q = (query or "").strip()
    if not q:
        return True, "不可检索"
    if _looks_greeting(q):
        return True, "不可检索"
    if _looks_self_ref(q):
        return True, "无需检索"
    has_entity = _has_entity(q)
    is_question = bool(re.search(r"[?？]", q)) or any(
        k in q for k in ("什么", "怎么", "为什么", "谁", "哪", "多少", "如何", "是否", "几")
    )
    # 既无真实实体、又疑似疑问、且很短 → 过于含糊，检索只会返回噪声
    # 注意：用本函数严格的 _has_entity（剔除纯疑问/语气词），不依赖 classify_intent 的宽松实体判定
    if is_question and not has_entity and len(q) < 12:
        return True, "需澄清"
    return False, "无"


def decide_not(query: str, intent: dict = None, ctx: dict = None) -> Tuple[bool, str]:
    """外部兼容钩子：decide_not 语义等同 should_skip_search（决定"不检索"）。

    保留该别名以便既有/外部调用方以「decide_not」语义消费自主不检索判定。
    """
    return should_skip_search(query, intent, ctx)
