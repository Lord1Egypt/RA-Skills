"""Small deterministic helpers shared by inventory and report code."""

import hashlib
import json


def run_id(report) -> str:
    """报告内容的短哈希 —— 用来证明这份报告背后真的跑过一次扫描。

    防的不是「算错数字」（那一类已经被结构性消灭：token 数、预算、冲突分类
    只以扫描输出的形式存在），而是**根本没跑就凭上次的印象写报告**。Agent
    编不出这 8 位，因为它由本次扫描的全部内容决定。

    **不进 scan JSON**，只在渲染时算。放进 schema 会让 11 份 golden 全部失效，
    而 CLAUDE.md 明确警告过反射性 `--update` 会让 golden 退化成「当前行为的
    记录」，测试就此失去意义。

    同一份机器状态在同一天重复跑得到同一个值；`days_since` 按天变，所以跨天
    会变 —— 那本来就是另一次扫描。

    `default=str` 是保险：标记算不出来也绝不能让 doctor 崩掉。
    """
    canonical = json.dumps(report, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:8]


def safe_str(value: str) -> str:
    """Replace surrogateescaped filename bytes with the Unicode replacement char."""
    return value.encode("utf-8", "surrogateescape").decode("utf-8", "replace")


def norm(path) -> str:
    """Return a lossy, forward-slash path representation on every platform."""
    return safe_str(str(path).replace("\\", "/"))


def est_tokens(text: str) -> int:
    """Estimate tokens using the CLI's stable CJK and non-CJK ratios."""
    if not text:
        return 0
    cjk = sum(1 for char in text if "一" <= char <= "鿿")
    other = len(text) - cjk
    return int(cjk / 1.5 + other / 4)
