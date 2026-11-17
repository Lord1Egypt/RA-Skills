"""统一证据链 — 四权分离的数据契约与 Vault 知识加载。

设计约束（最高原则）：
- 仅本地只读访问 Obsidian Vault，绝无任何网络调用（见 validator 离线扫描）。
- 每个 Pipeline Step 的输出必须能追溯到 rule_id -> input -> 中间计算 -> output。
"""
from __future__ import annotations

import os
import re
import yaml
from dataclasses import dataclass, asdict
from typing import Any

RULE_VERSION = "tianxing-mipai-jilaoshi@v0.3.1"
VAULT_DEFAULT = "/Volumes/珑/我的AI大脑/08_命理"


@dataclass
class EvidenceRecord:
    """统一证据链单步记录。AI 解释权只能翻译/组织这些字段，不得改写 output。"""

    step: str
    input: dict
    rules_used: list  # [rule_id, ...]
    intermediate_reasoning: str
    opposing_evidence: str
    output: Any
    confidence: float  # 0.0 - 1.0
    rule_version: str = RULE_VERSION
    vault_source: str = ""  # 实际加载到的 vault 文件路径（或 VAULT_UNREADABLE）
    needs_formalization: bool = False  # 该步命理规则在 vault 中仅为自然语言，未形式化
    conflict: bool = False  # 该步存在规则冲突，见 conflict_detector

    def to_dict(self) -> dict:
        return asdict(self)


def load_vault_text(rel_path: str, vault_base: str | None = None):
    """按 loading_matrix 指定的 vault 相对路径读取规则文本（仅本地文件）。

    返回 (绝对路径, 文本或 None)。文本为 None 表示 vault 不可读（如珑盘未挂载），
    调用方须据此降低 confidence 并标记，绝不可凭记忆臆造规则。
    """
    base = vault_base or os.environ.get("VAULT_BASE", VAULT_DEFAULT)
    p = os.path.join(base, rel_path)
    try:
        with open(p, "r", encoding="utf-8") as f:
            return p, f.read()
    except OSError:
        return p, None


# ---- 知识加载矩阵：引擎只能用 canonical 名读取，由矩阵决定真实源文件 ----
_MATRIX_CACHE: dict | None = None


def load_matrix(path: str | None = None) -> dict:
    """读取 rules/loading_matrix.yaml（统一口径为「天星密派」）。"""
    global _MATRIX_CACHE
    if _MATRIX_CACHE is not None:
        return _MATRIX_CACHE
    p = path or os.path.join(os.path.dirname(__file__), "..", "rules", "loading_matrix.yaml")
    try:
        with open(p, "r", encoding="utf-8") as f:
            _MATRIX_CACHE = yaml.safe_load(f) or {"knowledge": [], "pipeline": []}
    except OSError:
        _MATRIX_CACHE = {"knowledge": [], "pipeline": []}
    return _MATRIX_CACHE


def resolve_source_file(canonical: str, matrix: dict | None = None) -> str | None:
    """canonical（天星密派口径）-> vault 真实源文件名。找不到返回 None。"""
    matrix = matrix or load_matrix()
    for k in matrix.get("knowledge", []):
        if k.get("canonical") == canonical:
            return k.get("source_file")
    return None


def load_by_canonical(canonical: str, vault_base: str | None = None,
                      matrix: dict | None = None):
    """按 canonical 名经矩阵解析真实源文件后加载。返回 (路径, 文本或 None)。"""
    src = resolve_source_file(canonical, matrix)
    if src is None:
        return None, None
    return load_vault_text(src, vault_base)


# ---- 原子库速查层：08_命理/原子库 下「原子 — *.md」为极简规则速查 ----
ATOM_DIR_NAME = "原子库"

# 问事主题关键词 -> 命理原子 domain 的检索映射（用于断事前速查）
# 2026-09-22 增补：岁运应期 / 十神运动（原书下册 02/05 精微规律，此前未进检索域）
THEME_DOMAIN = {
    "事业": ["发散律", "大运流年作用", "应事律", "能量流", "岁运应期", "十神运动"],
    "财运": ["六亲应事", "应事律", "发散律", "大运流年作用", "岁运应期", "十神运动"],
    "婚姻": ["六亲应事", "空亡应用", "应事律", "十神运动"],
    "健康": ["六亲应事", "作用律"],
    "学业": ["发散律", "应事律"],
    "子女": ["空亡应用", "六亲应事"],
    "官非": ["六亲应事", "应事律", "岁运应期"],
    "排盘": ["排盘校验"],
    "格局": ["格局", "旺衰", "取用"],
    "空亡": ["空亡", "空亡应用"],
    "取象": ["能量流", "应事律", "发散律", "取象"],
}


def atom_dir(vault_base: str | None = None) -> str:
    base = vault_base or VAULT_DEFAULT
    return os.path.join(base, ATOM_DIR_NAME)


def _parse_atom_front(text: str) -> dict | None:
    """解析原子 frontmatter：title / domain / source / page / boundary / counter + body。"""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        return None
    fm, body = m.group(1), m.group(2).strip()
    d: dict = {}
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip().strip('"')
    title = d.get("title", "")
    if title.startswith("原子 — "):
        title = title[len("原子 — "):]
    return {
        "title": title,
        "domain": d.get("domain", ""),
        "source": d.get("source", ""),
        "page": d.get("page", ""),
        "boundary": d.get("boundary", ""),
        "counter": d.get("counter", ""),
        "body": body,
    }


def load_all_atoms(vault_base: str | None = None) -> list:
    """扫描原子库目录，返回所有原子 dict 列表（仅本地只读）。"""
    d = atom_dir(vault_base)
    out = []
    try:
        for fn in os.listdir(d):
            # 原子库下两类速查文件均载入：紧凑「原子 — 」规则 + 「取象字典 — 」象意素材表
            if fn.endswith(".md") and (
                fn.startswith("原子 — ") or fn.startswith("取象字典 — ")
            ):
                p = os.path.join(d, fn)
                try:
                    t = open(p, "r", encoding="utf-8").read()
                except OSError:
                    continue
                parsed = _parse_atom_front(t)
                if parsed:
                    parsed["file"] = fn
                    parsed["path"] = p
                    out.append(parsed)
    except OSError:
        pass
    return out


def search_atoms(query: str = "", vault_base: str | None = None, top: int = 12):
    """按问事主题检索相关原子规则，作为速查层。返回 (原子列表, 路径或 'ATOM_LIB_UNREADABLE')。

    命中优先级：主题映射 domain（+3）> 标题含主题词（+2）> 正文含主题词（+1）。
    原子库不可读时返回 ([], 'ATOM_LIB_UNREADABLE')，调用方须降低 confidence 并标记。
    """
    atoms = load_all_atoms(vault_base)
    if not atoms:
        return [], "ATOM_LIB_UNREADABLE"
    q = query or ""
    domains = []
    for kw, ds in THEME_DOMAIN.items():
        if kw in q:
            domains.extend(ds)
    scored = []
    for a in atoms:
        score = 0
        if a["domain"] in domains:
            score += 3
        for kw in THEME_DOMAIN:
            if kw in q:
                if kw in a["title"]:
                    score += 2
                if kw in a["body"]:
                    score += 1
        if q and (q in a["body"] or q in a["title"]):
            score += 1
        if score > 0:
            scored.append((score, a))
    scored.sort(key=lambda x: -x[0])
    if not scored:
        scored = [(0, a) for a in atoms]
    return [a for _, a in scored[:top]], atom_dir(vault_base)
