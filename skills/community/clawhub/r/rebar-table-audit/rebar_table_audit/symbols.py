"""钢筋牌号/直径符号解码。

同一图纸里，"规格"单元格常把牌号符号和直径数字连写，例如：
  %%13212      -> %%132(HRB400) + 直径12
  %%20110      -> %%201(HPB300 观察映射) + 直径10
  Ì12          -> Ì(HRB400 观察映射) + 直径12
  Φ12 / φ12    -> 牌号未指明，直径12

decode_spec() 对一段单元格文本做尽量多的符号识别，返回可能的多个 (diameter_mm, grade) 候选
（同一单元格理论上只应有一个规格，但表格偶尔会写多个直径用顿号/逗号分隔，如 "Φ12、Φ14"）。
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

DEFAULT_SYMBOLS_PATH = Path(__file__).parent / "data" / "symbols.default.json"

_NUM = r"(\d+(?:\.\d+)?)"


@dataclass
class SymbolMapping:
    """一条 code/raw_char -> grade 的映射规则，附带一个用于按 (diameter+grade) 抽取的编译正则。"""

    grade: str
    source: str
    note: str
    pattern: re.Pattern
    label: str  # 报告里展示用的标识（code 或 raw_char）


@dataclass
class SymbolTable:
    mappings: list[SymbolMapping]
    diameter_only_codes: list[str]
    diameter_only_pattern: re.Pattern
    usage: dict[str, int] = field(default_factory=dict)

    def record_usage(self, label: str) -> None:
        self.usage[label] = self.usage.get(label, 0) + 1

    def usage_report(self) -> list[dict]:
        """按 label 汇总本次运行实际用到的符号映射次数（供 evidence.symbol_mappings_used）。"""
        by_label = {m.label: m for m in self.mappings}
        out = []
        for label, count in sorted(self.usage.items()):
            m = by_label.get(label)
            if m is None:
                out.append({"code": label, "grade": None, "source": "diameter-only", "count": count})
            else:
                out.append({"code": label, "grade": m.grade, "source": m.source, "count": count})
        return out


def load_symbol_table(path: Optional[Path] = None, extra_path: Optional[Path] = None) -> SymbolTable:
    """加载符号映射表。path 为 None 时用内置默认表；extra_path（--symbols）在默认表之上覆盖/追加。"""
    data = json.loads((path or DEFAULT_SYMBOLS_PATH).read_text(encoding="utf-8"))
    if extra_path is not None:
        extra = json.loads(Path(extra_path).read_text(encoding="utf-8"))
        data = _merge_symbol_data(data, extra)
    return _build_symbol_table(data)


def _merge_symbol_data(base: dict, extra: dict) -> dict:
    merged = dict(base)
    merged["grade_mappings"] = list(base.get("grade_mappings", []))
    # extra 里同 code/raw_char 的条目覆盖 base 里的，其余追加
    def key_of(m):
        return (m.get("code"), m.get("raw_char"))
    base_keys = {key_of(m): i for i, m in enumerate(merged["grade_mappings"])}
    for m in extra.get("grade_mappings", []):
        k = key_of(m)
        if k in base_keys:
            merged["grade_mappings"][base_keys[k]] = m
        else:
            merged["grade_mappings"].append(m)
    merged["diameter_only_codes"] = list(
        dict.fromkeys(base.get("diameter_only_codes", []) + extra.get("diameter_only_codes", []))
    )
    return merged


def _build_symbol_table(data: dict) -> SymbolTable:
    mappings: list[SymbolMapping] = []
    for m in data.get("grade_mappings", []):
        code = m.get("code")
        raw_char = m.get("raw_char")
        grade = m["grade"]
        source = m.get("source", "unknown")
        note = m.get("note", "")
        # 一条映射条目可以同时带 code（"%%130" 这种控制码字面文本）和 raw_char（同一个符号在
        # 某条转换链下被解成的具体字符，如 "\x82"）——两种写法可能出现在不同转换链产出的同
        # 一份图纸里，都要能单独匹配上，不能因为 code 存在就把 raw_char 那条模式丢掉。
        if code:
            mappings.append(SymbolMapping(
                grade=grade, source=source, note=note,
                pattern=re.compile(re.escape(code) + _NUM), label=code,
            ))
        if raw_char:
            mappings.append(SymbolMapping(
                grade=grade, source=source, note=note,
                pattern=re.compile(re.escape(raw_char) + _NUM), label=raw_char,
            ))
    # 更长/更具体的 code 优先匹配（例如 %%201 要早于任何更短前缀）
    mappings.sort(key=lambda m: -len(m.label))

    diameter_codes = data.get("diameter_only_codes", [])
    if diameter_codes:
        alt = "|".join(re.escape(c) for c in diameter_codes)
        diameter_pattern = re.compile(f"(?:{alt})\\s*{_NUM}")
    else:
        diameter_pattern = re.compile(r"(?!)")  # 永不匹配
    return SymbolTable(mappings=mappings, diameter_only_codes=diameter_codes, diameter_only_pattern=diameter_pattern)


@dataclass
class SpecMatch:
    diameter_mm: Optional[float]
    grade: Optional[str]
    grade_source: str  # "known" | "observed-in-sample" | "unspecified" | "unresolved"
    matched_label: Optional[str]
    span: tuple[int, int]


def decode_spec(text: str, table: SymbolTable) -> list[SpecMatch]:
    """在一段单元格文本里找出所有 (直径, 牌号) 候选，按出现顺序返回。找不到任何符号时返回空列表。"""
    if not text:
        return []
    candidates: list[SpecMatch] = []
    consumed = [False] * (len(text) + 1)

    def mark_consumed(start, end):
        for i in range(start, end):
            consumed[i] = True

    for m in table.mappings:
        for match in m.pattern.finditer(text):
            start, end = match.span()
            if any(consumed[start:end]):
                continue
            diameter = float(match.group(1))
            candidates.append(
                SpecMatch(diameter_mm=diameter, grade=m.grade, grade_source=m.source, matched_label=m.label, span=(start, end))
            )
            mark_consumed(start, end)
            table.record_usage(m.label)

    for match in table.diameter_only_pattern.finditer(text):
        start, end = match.span()
        if any(consumed[start:end]):
            continue
        diameter = float(match.group(1))
        candidates.append(
            SpecMatch(diameter_mm=diameter, grade=None, grade_source="unspecified", matched_label=match.group(0), span=(start, end))
        )
        mark_consumed(start, end)
        table.record_usage(match.group(0).rstrip("0123456789. "))

    candidates.sort(key=lambda c: c.span[0])
    return candidates


# 表头/正文里常见的显式牌号名（不经符号解码、直接写出 HRB400 等）
EXPLICIT_GRADE_RE = re.compile(r"HPB300|HRB335|HRB400|HRB500|RRB400")


def find_explicit_grade(text: str) -> Optional[str]:
    m = EXPLICIT_GRADE_RE.search(text or "")
    return m.group(0) if m else None
