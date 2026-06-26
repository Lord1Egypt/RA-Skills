"""
加载 SKILL.md 和 references/ 作为 AI 上下文。
每次查询时重新读取文件，确保数据始终是最新的。
"""

import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_DIR = os.path.join(SKILL_DIR, "references")


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def build_system_prompt() -> str:
    """构建完整的系统提示词 = SKILL.md + 所有参考数据"""

    sk = _read(os.path.join(SKILL_DIR, "SKILL.md"))

    # 收集所有 reference 文件
    refs = []
    for fname in sorted(os.listdir(REF_DIR)):
        if fname.endswith(".md"):
            content = _read(os.path.join(REF_DIR, fname))
            refs.append(f"### {fname}\n\n{content}")

    refs_text = "\n\n---\n\n".join(refs)

    return f"""{sk}

---

# 以下是当前门店最新业务数据（每次查询实时读取）

{refs_text}

---

重要提示：以上 references/ 中的价格、地址、营业时间、优惠活动等业务数据为当前最新值，对话中必须以此为准。SKILL.md 中不包含具体业务数据，仅包含对话流程和安全规则。
"""


def get_skill_version() -> str:
    """获取当前数据版本"""
    import json
    ver_path = os.path.join(SKILL_DIR, "version.json")
    try:
        with open(ver_path, encoding="utf-8") as f:
            v = json.load(f)
        return v.get("data_version", "unknown")
    except Exception:
        return "unknown"
