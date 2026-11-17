"""事实台账 + 论点台账公共模块。

供以下消费者共享同一份 ledger.json / claims.json 加载/校验逻辑：
- report_assembler 的 HTML 组装（--ledger-mode scan|placeholder，--claims 校验）
- docx_export 的 Word 组装
- pptx_export 的幻灯片组装
- HTML 报告附录中的"关键数据溯源"表与"论点与论据"表

设计要点：
- 单一格式化函数：值 → 字符串，供占位符替换与附录表格共用，避免报告内
  外数字口径分叉。
- 占位符语法 {{id}} / {{id:fmt}>>，fmt 是合法 Python format spec（',.0f' / '.1f' / ',.1f' 等）。
- 替换器报错统一抛 LedgerError，由调用方按 5004 / 5005 / 5008 错误码输出。
- claims（论点台账）只做形式校验（论点挂了论据、论据真实可定位）；
  「论据是否真支撑论点」的实质校验是 LLM 的职责，代码不做（见 改进方案.md 边界）。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


_PLACEHOLDER_RE = re.compile(
    r"\{\{\s*(?P<id>[A-Za-z_][A-Za-z0-9_]*)\s*(?::\s*(?P<fmt>[^{}]*?)\s*)?\}\}"
)

# 数字识别（Level 1 修订版）：
#   必须溯源 —— 任何小数、>=100 的整数、紧跟%/个百分点/倍 的数字
#   豁免    —— 日期（图 1）、图号（图 2）、章节引用（§1）、纯小整数（"59 名学生"）
_DATE_PATTERNS = [
    re.compile(r"\d{4}-\d{2}(-\d{2})?"),                             # 2025-01 / 2025-06-30
    re.compile(r"(?:从|至|截至|于|在|自|到|至)\s*(?:19|20)\d{2}"),       # 从 2025 / 至 2026
    re.compile(r"(?:19|20)\d{2}\s*(?:年|年度|全年|上半年|下半年|期间|以来|至今|Q[1-4])"),  # 2025 年 / 2025 全年
    re.compile(r"\d{1,2}\s*月(?![度内例])"),                             # 6 月
    re.compile(r"Q[1-4]|第?[1-4一二三四]季度"),
    re.compile(r"图\s*\d+"),
    re.compile(r"§\w+"),
]
# %/个百分点/倍 必须溯源（无论整数小数，堵漏 37%）
# 关键：分窗口检查，避免把"远处有 倍/%"误判为 %-like
#   单字符形态（%/％/倍）看紧邻 ≤ 2 字符；
#   多字符"个百分点"需 ≤ 6 字符。
_PERCENT_LIKE_TIGHT_RE = re.compile(r"[%％]|倍")          # 紧邻 2 字符
_PERCENT_LIKE_LOOSE_RE = re.compile(r"个百分点")          # 紧邻 6 字符
_NUM_RE = re.compile(r"-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+\.\d+|-?\d+")


class LedgerError(Exception):
    _CODE_NAMES = {
        5004: "LEDGER_MISMATCH",
        5005: "RAW_NUMBER_IN_PLACEHOLDER_MODE",
        5008: "CLAIM_EVIDENCE_INVALID",
    }

    def __init__(self, message: str, code: int = 5004, details: dict | None = None,
                 code_name: str | None = None):
        super().__init__(message)
        self.code = code
        self.code_name = code_name or self._CODE_NAMES.get(code, "LEDGER_MISMATCH")
        self.message = message
        self.details = details or {}


@dataclass
class LedgerEntry:
    id: str
    metric: str
    value: float
    unit: str = ""
    source: str = ""
    sections: list[str] = field(default_factory=list)


@dataclass
class LedgerResolver:
    ledger_path: Path
    entries: list[LedgerEntry]
    by_id: dict[str, LedgerEntry]
    citations: dict[str, list[str]] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path) -> "LedgerResolver":
        p = Path(path).expanduser()
        if not p.is_file():
            raise LedgerError(
                f"ledger 文件不存在: {path}",
                code=5004,
                details={"given": str(path), "suggestion": "Step 4 应把台账落盘为 ledger.json"},
            )
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise LedgerError(
                f"ledger 不是合法 JSON: {e}",
                code=5004,
                details={"given": str(p), "suggestion": "用 json.dumps(..., ensure_ascii=False) 生成"},
            )
        if not isinstance(raw, list) or not raw:
            raise LedgerError(
                "ledger 须为非空数组",
                code=5004,
                details={"given": str(p), "suggestion": "参考 REPORT.md 台账 schema：每项含 metric/value/source"},
            )
        entries: list[LedgerEntry] = []
        by_id: dict[str, LedgerEntry] = {}
        for i, item in enumerate(raw):
            if not isinstance(item, dict) or "value" not in item or "id" not in item:
                raise LedgerError(
                    f"ledger 第 {i} 项缺少 id/value 或不是对象",
                    code=5004,
                    details={"given": str(p)},
                )
            try:
                value = float(item["value"])
            except (TypeError, ValueError):
                raise LedgerError(
                    f"ledger 第 {i} 项 value 无法转为数字: {item['value']!r}",
                    code=5004,
                    details={"given": str(p)},
                )
            if not str(item["id"]).strip():
                raise LedgerError(f"ledger 第 {i} 项 id 为空", code=5004, details={"given": str(p)})
            eid = str(item["id"])
            if eid in by_id:
                raise LedgerError(f"ledger 存在重复 id: {eid!r}", code=5004, details={"given": str(p)})
            entry = LedgerEntry(
                id=eid,
                metric=str(item.get("metric", eid)),
                value=value,
                unit=str(item.get("unit", "")),
                source=str(item.get("source", "")),
                sections=list(item.get("sections") or []),
            )
            entries.append(entry)
            by_id[eid] = entry
        return cls(ledger_path=p, entries=entries, by_id=by_id)

    def _decimals(self, value: float) -> int:
        """源 value 的有效小数位数（基于 str 解析；整数视为 0）。"""
        s = repr(value) if isinstance(value, float) else str(value)
        if "." in s:
            return len(s.split(".")[1].rstrip("0"))
        return 0

    def _format_value(self, entry: LedgerEntry, fmt: str | None) -> str:
        val = entry.value
        if fmt is None or fmt.strip() == "":
            if isinstance(val, float) and val.is_integer():
                return str(int(val))
            return str(val)
        try:
            return format(val, fmt)
        except (ValueError, TypeError) as e:
            raise LedgerError(
                f"占位符格式说明非法: id={entry.id!r} fmt={fmt!r} → {e}",
                code=5004,
                details={"id": entry.id, "fmt": fmt, "suggestion": "fmt 是 Python format spec，如 ',.0f' / '.1f' / ',.1f'"},
            )

    def _verify_format_precision(self, entry: LedgerEntry, rendered: str, where: str) -> None:
        """format spec 不能把 value 粗化到精度以下（98.56 → .0f → 99 视为失真）。"""
        src_decimals = self._decimals(entry.value)
        cleaned = rendered.replace(",", "").replace("%", "").strip()
        try: numeric = float(cleaned)
        except ValueError:
            return  # 非纯数字占位符（如 "约 100"）放过
        rendered_decimals = 0 if "." not in cleaned else len(cleaned.split(".")[1].rstrip("0"))
        if rendered_decimals < src_decimals:
            raise LedgerError(
                f"占位符 fmt 把 {entry.id}={entry.value} 粗化为 {rendered!r}（精度下降）",
                code=5004,
                details={
                    "id": entry.id,
                    "source_decimals": src_decimals,
                    "rendered": rendered,
                    "where": where,
                    "suggestion": f"fmt 至少保留 {src_decimals} 位小数（value={entry.value}）；或更新 ledger 让 value 更粗",
                },
            )

    def resolve_text(self, text: str, where: str) -> str:
        """解析文本中的 {{id}} / {{id:fmt}} 占位符并替换；citation 入账。"""
        if not text:
            return text

        def _rep(m: re.Match) -> str:
            eid = m.group("id")
            fmt = m.group("fmt")
            if eid not in self.by_id:
                raise LedgerError(
                    f"未注册占位符: {eid!r}",
                    code=5004,
                    details={
                        "where": where,
                        "id": eid,
                        "available_ids": sorted(self.by_id),
                        "suggestion": f"把 {eid} 写入 ledger.json 或在文本中改用已注册 id",
                    },
                )
            entry = self.by_id[eid]
            try:
                rendered = self._format_value(entry, fmt)
            except LedgerError:
                raise
            self._verify_format_precision(entry, rendered, where)
            self.citations.setdefault(eid, []).append(where)
            return rendered

        return _PLACEHOLDER_RE.sub(_rep, text)

    # ---------- 占位符模式专用：发现占位符 id 与裸数字 ----------

    def placeholder_ids_in(self, text: str) -> set[str]:
        return set(m.group("id") for m in _PLACEHOLDER_RE.finditer(text or ""))

    def unresolved_placeholders(self, text: str) -> list[tuple[str, int]]:
        """返回未匹配到 ledger 的占位符列表 [(id, span_start)]，空表示全部注册。"""
        return [(m.group("id"), m.start()) for m in _PLACEHOLDER_RE.finditer(text or "")
                if m.group("id") not in self.by_id]

    # ---------- 数字扫描共用（Level 1 修订：%/个百分点/倍强制） ----------

    @staticmethod
    def strip_placeholders(text: str) -> str:
        """把 {{...}} 替换为空白占位符，便于对残留文本扫描数字。"""
        return _PLACEHOLDER_RE.sub(" ", text or "")

    @staticmethod
    def required_numbers(text: str) -> list[tuple[str, float, str]]:
        """找出必须溯源台账的数字：(display, value, context)。

        context 为前后各 ~20 字符（日期豁免后；占位符已剥离）。
        规则：任何小数 / >=100 整数 / 紧跟 %/个百分点/倍 的数字（无论大小）。
        """
        cleaned = LedgerResolver.strip_placeholders(text)
        for pat in _DATE_PATTERNS:
            cleaned = pat.sub(" ", cleaned)
        out = []
        for m in _NUM_RE.finditer(cleaned):
            display = m.group(0)
            try:
                value = float(display.replace(",", ""))
            except ValueError:
                continue
            has_decimal = "." in display
            # 紧邻窗口：单字符形态 ≤2 字符，"个百分点" ≤6 字符；避免远处命中误带
            tight_window = cleaned[m.end():m.end() + 2]
            loose_window = cleaned[m.end():m.end() + 6]
            is_percent_like = bool(_PERCENT_LIKE_TIGHT_RE.search(tight_window)) or \
                              bool(_PERCENT_LIKE_LOOSE_RE.search(loose_window))
            if not has_decimal and value < 100 and not is_percent_like:
                continue  # 裸小整数（"3 个类别" / "Top 5"）：计数语境，放行
            ctx = cleaned[max(0, m.start() - 20):m.end() + 25].replace("\n", " ").strip()
            out.append((display, value, ctx))
        return out

    # ---------- 兼容旧 API：供 scan 模式沿用 ----------

    def values_for_matching(self) -> list[float]:
        """所有 entry 的可匹配数值（兼容字符串 value "98.6%"）。"""
        vals: list[float] = []
        for e in self.entries:
            s = str(e.value)
            try:
                vals.append(float(s.replace(",", "").replace("%", "").strip()))
            except ValueError:
                pass
        return vals


def matches_any(value: float, ledger_vals: list[float]) -> bool:
    """容差匹配：用于 scan 模式兜底。"""
    decimals = len(str(value).split(".")[1]) if "." in str(value) else 0
    tol = 0.5 * (10 ** -decimals) + 1e-9
    for v in ledger_vals:
        if abs(v - value) <= tol:
            return True
        if round(v, decimals) == round(value, decimals):
            return True
    return False


# ═══════════════ 论点台账（claims.json）═══════════════
#
# 设计依据（改进方案.md 改进 3）：ledger 从「数字台账」升级为「论据台账」，
# claim（论点）成为一等公民。claims.json 引用 facts（ledger 条目）与图表，
# 由 assembler 做形式校验；实质校验（论据是否真支撑论点）是 LLM 职责。
#
# 形式校验（机械可判定）：
#   1. 每个 claim 必须声明至少一个 evidence（缺 → 报错）
#   2. evidence id 必须可解析：ledger 事实 id / 含图章节 id / 图表文件 stem
#   3. claim 文本中的必溯源数字必须能命中台账值（沿用数字溯源容差）
#   4. coverage 模式：每个含图章节必须被至少一个 claim 引用（每张图可追溯到论点）

_CLAIM_EVIDENCE_CODE = 5008


@dataclass
class Claim:
    id: str
    claim: str
    evidence: list[str] = field(default_factory=list)
    section: str = ""
    type: str = ""


@dataclass
class ClaimsResolver:
    claims_path: Path
    claims: list[Claim]
    by_id: dict[str, Claim]

    @classmethod
    def load(cls, path: str | Path) -> "ClaimsResolver":
        p = Path(path).expanduser()
        if not p.is_file():
            raise LedgerError(
                f"claims 文件不存在: {path}",
                code=_CLAIM_EVIDENCE_CODE,
                details={"given": str(path), "suggestion": "Step 4 应把论点台账落盘为 claims.json"},
            )
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise LedgerError(
                f"claims 不是合法 JSON: {e}",
                code=_CLAIM_EVIDENCE_CODE,
                details={"given": str(p), "suggestion": "用 json.dumps(..., ensure_ascii=False) 生成"},
            )
        if not isinstance(raw, list) or not raw:
            raise LedgerError(
                "claims 须为非空数组",
                code=_CLAIM_EVIDENCE_CODE,
                details={"given": str(p),
                         "suggestion": "参考 REPORT.md 论点台账 schema：每项含 id/claim/evidence"},
            )
        claims: list[Claim] = []
        by_id: dict[str, Claim] = {}
        for i, item in enumerate(raw):
            if not isinstance(item, dict):
                raise LedgerError(
                    f"claims 第 {i} 项不是对象",
                    code=_CLAIM_EVIDENCE_CODE,
                    details={"given": str(p)},
                )
            cid = str(item.get("id") or "").strip()
            text = str(item.get("claim") or "").strip()
            if not cid:
                raise LedgerError(f"claims 第 {i} 项 id 为空", code=_CLAIM_EVIDENCE_CODE,
                                  details={"given": str(p)})
            if not text:
                raise LedgerError(f"claims 第 {i} 项 claim 为空（论点必须有主张文本）",
                                  code=_CLAIM_EVIDENCE_CODE, details={"given": str(p), "id": cid})
            if cid in by_id:
                raise LedgerError(f"claims 存在重复 id: {cid!r}", code=_CLAIM_EVIDENCE_CODE,
                                  details={"given": str(p)})
            evidence = item.get("evidence")
            if evidence is None:
                evidence = []
            if not isinstance(evidence, list) or not all(str(e) for e in evidence):
                raise LedgerError(
                    f"claims 第 {i} 项 evidence 须为非空字符串数组",
                    code=_CLAIM_EVIDENCE_CODE,
                    details={"given": str(p), "id": cid,
                             "suggestion": "evidence 引用 ledger 事实 id 或含图章节 id，如 [\"rev_h1\", \"s3\"]"},
                )
            claim = Claim(
                id=cid,
                claim=text,
                evidence=[str(e) for e in evidence],
                section=str(item.get("section") or ""),
                type=str(item.get("type") or ""),
            )
            claims.append(claim)
            by_id[cid] = claim
        return cls(claims_path=p, claims=claims, by_id=by_id)


def validate_claims(claims_resolver: ClaimsResolver | None,
                    ledger_resolver: "LedgerResolver | None",
                    section_ids: set[str],
                    charted_section_ids: set[str],
                    chart_stems: set[str],
                    mode: str = "basic",
                    narrative_section_ids: set[str] | None = None) -> dict | None:
    """论点台账形式校验（改进方案.md：代码只做形式校验，不做实质校验）。

    参数：
    - claims_resolver：claims.json 加载器（None = 未启用，直接返回 None）
    - ledger_resolver：事实台账（数字溯源用；None 时跳过 claim 文本数字校验）
    - section_ids：report_spec 全部章节 id（含 summary，供 claim.section 引用）
    - charted_section_ids：report_spec 中含 chart_path 的章节 id 集合
    - chart_stems：spec 引用的图表文件 stem 集合（chart_path 去扩展名）
    - mode：basic = 规则 1~4；coverage = basic + 每个含图章节被论点引用
             + 每个含叙事章节被 claim.section 指向
    - narrative_section_ids：report_spec 中 narrative 非空的章节 id 集合
             （coverage 模式「叙事 → 论点」反向覆盖用；None 则跳过该检查）

    返回统计 dict；违规抛 LedgerError（code 5008）。
    """
    if claims_resolver is None:
        return None

    fact_ids = set(ledger_resolver.by_id) if ledger_resolver else set()
    resolvable = fact_ids | charted_section_ids | chart_stems
    evidence_refs = 0
    violations: list[dict] = []

    for c in claims_resolver.claims:
        # 规则 1：每个 claim 必须声明至少一个 evidence
        if not c.evidence:
            violations.append({
                "claim": c.id, "problem": "missing_evidence",
                "detail": f"论点 {c.id!r} 未声明任何论据（evidence 为空）",
            })
            continue
        # 规则 2：evidence id 必须可解析
        for eid in c.evidence:
            evidence_refs += 1
            if eid not in resolvable:
                violations.append({
                    "claim": c.id, "problem": "unknown_evidence", "evidence": eid,
                    "detail": f"论点 {c.id!r} 的论据 {eid!r} 无法解析"
                              f"（不在 ledger 事实 id / 含图章节 id / 图表文件 stem 中）",
                })
        # claim 的 section 字段若填写，必须指向真实章节
        if c.section and c.section not in section_ids:
            violations.append({
                "claim": c.id, "problem": "unknown_section", "evidence": c.section,
                "detail": f"论点 {c.id!r} 的 section {c.section!r} 不在 report_spec 章节中",
            })
        # 规则 3：claim 文本中的必溯源数字须命中台账（沿用数字溯源）
        if ledger_resolver is not None:
            ledger_vals = ledger_resolver.values_for_matching()
            for display, value, ctx in LedgerResolver.required_numbers(c.claim):
                if not matches_any(value, ledger_vals):
                    violations.append({
                        "claim": c.id, "problem": "untraced_number", "evidence": display,
                        "detail": f"论点 {c.id!r} 文本数字 {display} 未命中事实台账（上下文: {ctx[:40]}）",
                    })

    # 规则 4（coverage）：每个含图章节被论点引用（图 → 论点）
    uncovered: list[str] = []
    uncovered_narratives: list[str] = []
    if mode == "coverage":
        cited = set()
        section_anchored = set()
        for c in claims_resolver.claims:
            cited |= {e for e in c.evidence}
            if c.section:
                cited.add(c.section)
                section_anchored.add(c.section)
        uncovered = sorted(sid for sid in charted_section_ids if sid not in cited)
        for sid in uncovered:
            violations.append({
                "claim": None, "problem": "uncovered_chart", "evidence": sid,
                "detail": f"章节 {sid!r} 的图表未被任何论点引用（coverage 模式要求每张图可追溯到论点）",
            })
        # 规则 5（coverage）：每个含叙事章节被 claim.section 指向（叙事 → 论点）
        if narrative_section_ids is not None:
            uncovered_narratives = sorted(
                sid for sid in narrative_section_ids if sid not in section_anchored)
            for sid in uncovered_narratives:
                violations.append({
                    "claim": None, "problem": "uncovered_narrative", "evidence": sid,
                    "detail": f"章节 {sid!r} 的叙事未被任何论点的 section 指向"
                              f"（coverage 模式要求每段叙事可锚定到一个论点）",
                })

    if violations:
        raise LedgerError(
            f"论点台账校验失败：{len(violations)} 处违规（形式校验：论点须挂论据、论据须可定位）",
            code=_CLAIM_EVIDENCE_CODE,
            details={
                "violations": violations[:20],
                "violations_total": len(violations),
                "suggestion": "补齐 evidence 引用（ledger 事实 id / 含图章节 id），"
                               "claim 文本数字先入台账；coverage 模式下为每个含图章节挂论点、"
                               "为每段叙事补 claim.section 指向",
            },
        )
    return {
        "checked": True,
        "mode": mode,
        "claims": len(claims_resolver.claims),
        "evidence_refs": evidence_refs,
        "uncovered_charts": len(uncovered),
        "uncovered_narratives": len(uncovered_narratives),
    }