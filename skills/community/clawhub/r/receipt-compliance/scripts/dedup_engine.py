#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查重三信号引擎 v4.5.0

针对报销场景中的重复报销（含 P 图改抬头重复）做两阶段检测：
  阶段一  精确分组：发票号码标准化哈希，同号即重复（覆盖原样重复）
  阶段二  组内近似比对：金额（±0.01）+ 日期（±3 天）+ 销售方/票号前缀相似，
           覆盖「改了抬头/票号但金额日期一致」的变造重复

输出查重组，每组含成员、信号类型、差异字段、置信度，供 ledger_db 生成复核工单。

设计约束（死规则 #9）：纯标准库实现，无外部依赖；豁免规则由调用方注入。
"""

import re
from collections import defaultdict
from datetime import datetime, date
from typing import Optional, Dict, Any, List


_AMOUNT_TOL = 0.01
_DATE_TOL_DAYS = 3


def _norm_number(v: Optional[str]) -> str:
    """标准化发票号码：去空格，统一小写"""
    if not v:
        return ""
    return re.sub(r"\s+", "", str(v)).strip().lower()


def _parse_date(v: Optional[str]) -> Optional[date]:
    if not v:
        return None
    s = str(v).strip().replace("/", "-")
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y年%m月%d日"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _money(v: Any) -> float:
    try:
        return round(float(v or 0), 2)
    except (TypeError, ValueError):
        return 0.0


def _norm_seller(v: Optional[str]) -> str:
    if not v:
        return ""
    # 去常见后缀与公司类型词，便于近似比对
    s = re.sub(r"[\s（）()]", "", str(v))
    s = re.sub(r"(有限公司|股份有限公司|有限责任公司|公司|厂|店|部|所|中心)$", "", s)
    return s.lower()


class DedupEngine:
    """查重引擎：输入票据列表，输出重复组"""

    def __init__(self, exempt_rules: Optional[List[Dict[str, Any]]] = None):
        """
        exempt_rules: 豁免规则列表，每条形如
            {"seller_contains": "某固定供应商", "amount": 100.0, "date_window": 3}
        命中规则的候选组合不计入重复（误报沉淀）。
        """
        self.exempt_rules = exempt_rules or []

    # ---------- 外部入口 ----------

    def find_duplicates(self, invoices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Args:
            invoices: 每项至少含 invoice_number / seller_name / amount 或 total /
                      billing_date / source_file / id（可选）
        Returns:
            重复组列表，每组：
            {
              "signal": "exact" | "fuzzy",
              "confidence": float,
              "diff_fields": [字段名...],
              "members": [ {id, invoice_number, seller_name, amount, total,
                            billing_date, source_file} ]
            }
        """
        norm = [self._normalize(x) for x in invoices if self._normalize(x)]

        # 阶段一：精确按票号分组
        by_num: Dict[str, List[dict]] = defaultdict(list)
        for it in norm:
            by_num[it["number_norm"]].append(it)
        exact_groups = [g for g in by_num.values() if len(g) >= 2]
        exact_members = {id(m) for g in exact_groups for m in g}

        groups: List[Dict[str, Any]] = []
        for g in exact_groups:
            groups.append(self._build_group(g, "exact"))

        # 阶段二：近似比对（排除已精确命中，避免重复提示）
        fuzzy_pool = [it for it in norm if id(it) not in exact_members]
        for g in self._fuzzy_cluster(fuzzy_pool):
            if self._match_exempt(g):
                continue
            grp = self._build_group(g, "fuzzy")
            if grp:
                groups.append(grp)

        return groups

    # ---------- 内部 ----------

    def _normalize(self, x: Dict[str, Any]) -> Optional[dict]:
        number = _norm_number(x.get("invoice_number"))
        if not number and not (x.get("amount") or x.get("total")):
            return None
        seller = x.get("seller_name") or ""
        amount = _money(x.get("amount") if x.get("amount") is not None else x.get("total"))
        return {
            "id": x.get("id"),
            "number_norm": number,
            "invoice_number": x.get("invoice_number"),
            "seller_name": seller,
            "seller_norm": _norm_seller(seller),
            "amount": amount,
            "total": _money(x.get("total")),
            "billing_date": x.get("billing_date") or x.get("travel_date"),
            "date": _parse_date(x.get("billing_date") or x.get("travel_date")),
            "source_file": x.get("source_file"),
        }

    def _fuzzy_cluster(self, items: List[dict]) -> List[List[dict]]:
        """按金额分桶 → 桶内按日期 ±3 天 + 销售方/票号前缀相似聚类"""
        by_amt: Dict[float, List[dict]] = defaultdict(list)
        for it in items:
            by_amt[it["amount"]].append(it)

        clusters: List[List[dict]] = []
        for amt, members in by_amt.items():
            if len(members) < 2:
                continue
            members_sorted = sorted(members, key=lambda m: (m["date"] or date.max))
            cluster: List[dict] = [members_sorted[0]]
            for m in members_sorted[1:]:
                last = cluster[-1]
                if self._linkable(last, m):
                    cluster.append(m)
                else:
                    if len(cluster) >= 2:
                        clusters.append(cluster)
                    cluster = [m]
            if len(cluster) >= 2:
                clusters.append(cluster)
        return clusters

    def _linkable(self, a: dict, b: dict) -> bool:
        """两票是否应归为同一近似重复簇"""
        if a["date"] and b["date"]:
            if abs((a["date"] - b["date"]).days) <= _DATE_TOL_DAYS:
                return True
        if a["seller_norm"] and b["seller_norm"] and a["seller_norm"] == b["seller_norm"]:
            return True
        # 票号前缀 8 位一致（疑似只改了后段）
        if a["number_norm"] and b["number_norm"] and a["number_norm"][:8] == b["number_norm"][:8]:
            return True
        return False

    def _build_group(self, members: List[dict], signal: str) -> Dict[str, Any]:
        if len(members) < 2:
            return {}
        diff_fields = self._diff_fields(members)
        confidence = self._confidence(members, signal, diff_fields)
        return {
            "signal": signal,
            "confidence": confidence,
            "diff_fields": diff_fields,
            "members": [
                {
                    "id": m["id"],
                    "invoice_number": m["invoice_number"],
                    "seller_name": m["seller_name"],
                    "amount": m["amount"],
                    "total": m["total"],
                    "billing_date": m["billing_date"],
                    "source_file": m["source_file"],
                }
                for m in members
            ],
        }

    @staticmethod
    def _diff_fields(members: List[dict]) -> List[str]:
        fields = ["invoice_number", "seller_name", "amount", "billing_date"]
        diff = []
        for f in fields:
            vals = {m[f] for m in members}
            if len(vals) > 1:
                diff.append(f)
        return diff

    @staticmethod
    def _confidence(members: List[dict], signal: str, diff_fields: List[str]) -> float:
        if signal == "exact":
            return 0.99
        # fuzzy：金额+日期完全一致，销售方不一致 → 高度疑似改抬头
        if "seller_name" in diff_fields and "invoice_number" in diff_fields:
            return 0.9
        if "seller_name" in diff_fields:
            return 0.85
        return 0.75

    def _match_exempt(self, members: List[dict]) -> bool:
        """命中豁免规则则不告警"""
        for rule in self.exempt_rules:
            seller_kw = (rule.get("seller_contains") or "").lower()
            for m in members:
                if seller_kw and seller_kw not in (m["seller_name"] or "").lower():
                    break
            else:
                # 全部成员销售方均含关键词
                amt = rule.get("amount")
                if amt is not None:
                    if any(abs(m["amount"] - float(amt)) > _AMOUNT_TOL for m in members):
                        continue
                return True
        return False


def deduplicate(invoices: List[Dict[str, Any]],
                exempt_rules: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """便捷函数"""
    return DedupEngine(exempt_rules).find_duplicates(invoices)


if __name__ == "__main__":
    import json
    sample = [
        {"id": 1, "invoice_number": "24312000000012345678", "seller_name": "甲公司",
         "amount": 1000.0, "billing_date": "2026-01-05", "source_file": "a.pdf"},
        {"id": 2, "invoice_number": "24312000000012345678", "seller_name": "甲公司",
         "amount": 1000.0, "billing_date": "2026-01-05", "source_file": "b.pdf"},
        {"id": 3, "invoice_number": "24312000000099999999", "seller_name": "乙公司",
         "amount": 1000.0, "billing_date": "2026-01-06", "source_file": "c.png"},
        {"id": 4, "invoice_number": "24312000000088888888", "seller_name": "乙公司",
         "amount": 1000.0, "billing_date": "2026-01-07", "source_file": "d.png"},
    ]
    print(json.dumps(deduplicate(sample), ensure_ascii=False, indent=2))
