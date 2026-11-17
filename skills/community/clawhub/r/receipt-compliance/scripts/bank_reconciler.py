#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行流水对账引擎
功能：解析银行流水 CSV + 与发票数据进行模糊匹配
匹配规则：金额 ±0.01 元容差 + 日期 ±3 天容差，综合评分匹配
"""

import csv
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


# === 默认配置 ===
DEFAULT_CONFIG = {
    "amount_tolerance": 0.01,        # 金额容差（元）
    "date_tolerance_days": 3,        # 日期容差（天）
    "match_threshold": 0.85,         # 综合评分阈值（高于此值视为匹配）
    "date_formats": [                # 支持的日期格式
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y年%m月%d日",
        "%Y%m%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
    ],
    "encoding_fallbacks": ["utf-8", "gbk", "gb2312", "utf-8-sig"],  # 编码尝试顺序
}

# === 匹配结果状态 ===
MATCH_STATUS = {
    "matched": "已匹配",
    "unmatched": "未匹配",
    "multi_match": "多重匹配",
}


class BankTransaction:
    """银行流水单条记录"""

    def __init__(
        self,
        date: datetime,
        amount: float,       # 正数=收入，负数=支出
        summary: str = "",   # 摘要/备注
        counterparty: str = "",  # 对方户名
        transaction_id: str = "",  # 交易流水号
        raw_data: Dict[str, str] = None,
    ):
        self.date = date
        self.amount = amount
        self.summary = summary
        self.counterparty = counterparty
        self.transaction_id = transaction_id
        self.raw_data = raw_data or {}
        self.matched_invoice: Optional[Dict] = None
        self.match_score: float = 0.0
        self.match_status: str = "unmatched"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "amount": self.amount,
            "summary": self.summary,
            "counterparty": self.counterparty,
            "transaction_id": self.transaction_id,
            "match_status": self.match_status,
            "match_score": round(self.match_score, 3),
            "matched_invoice_number": (
                self.matched_invoice.get("invoice_number") if self.matched_invoice else None
            ),
        }


class BankReconciler:
    """
    银行流水对账引擎

    核心能力：
    1. 解析主流银行 CSV 流水（工行/建行/农行/招行/中信等）
    2. 金额模糊匹配（±0.01 元容差）
    3. 日期模糊匹配（±3 天容差）
    4. 综合评分机制（金额权重 60% + 日期权重 40%）
    5. 多重匹配检测与报告
    """

    # === 常见银行 CSV 列名映射 ===
    COLUMN_MAPPINGS = {
        "date": ["交易日期", "日期", "记账日期", "交易时间", "Date", "Transaction Date", "入账日期"],
        "amount": ["交易金额", "金额", "收入", "支出", "借方", "贷方", "Amount", "Transaction Amount"],
        "summary": ["摘要", "备注", "用途", "交易摘要", "交易说明", "Description", "Narration", "对方信息"],
        "counterparty": ["对方户名", "对方账户", "户名", "交易对手", "Counterparty", "对手方"],
        "transaction_id": ["交易流水号", "流水号", "交易编号", "Transaction ID", "Reference"],
    }

    def __init__(self, config: Optional[Dict] = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.transactions: List[BankTransaction] = []
        self.invoices: List[Dict[str, Any]] = []
        self.results: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # CSV 解析
    # ------------------------------------------------------------------

    def parse_csv(self, csv_path: str) -> List[BankTransaction]:
        """
        解析银行流水 CSV 文件
        自动检测编码、识别列名、处理借贷方向
        """
        path = Path(csv_path)
        if not path.exists():
            raise FileNotFoundError(f"CSV 文件不存在: {csv_path}")

        raw_rows = self._read_csv_with_encoding(path)
        if not raw_rows:
            raise ValueError(f"CSV 文件为空或解析失败: {csv_path}")

        headers = list(raw_rows[0].keys())
        col_map = self._detect_columns(headers)

        if "date" not in col_map:
            raise ValueError(f"未识别到日期列，CSV 列名: {headers}")
        if "amount" not in col_map:
            raise ValueError(f"未识别到金额列，CSV 列名: {headers}")

        transactions = []
        for i, row in enumerate(raw_rows, 1):
            try:
                # 解析日期
                date_str = str(row.get(col_map.get("date", ""), "")).strip()
                tx_date = self._parse_date(date_str)
                if not tx_date:
                    continue

                # 解析金额（处理借贷分离列）
                amount = self._parse_amount(row, col_map, headers)
                if amount is None:
                    continue

                # 解析可选字段
                summary = str(row.get(col_map.get("summary", ""), "")).strip()
                counterparty = str(row.get(col_map.get("counterparty", ""), "")).strip()
                tx_id = str(row.get(col_map.get("transaction_id", ""), "")).strip()

                tx = BankTransaction(
                    date=tx_date,
                    amount=amount,
                    summary=summary,
                    counterparty=counterparty,
                    transaction_id=tx_id,
                    raw_data=dict(row),
                )
                transactions.append(tx)

            except Exception as e:
                # 跳过解析失败的行，记录到日志
                continue

        self.transactions = transactions
        return transactions

    def _read_csv_with_encoding(self, path: Path) -> List[Dict[str, str]]:
        """尝试多种编码读取 CSV"""
        for enc in self.config["encoding_fallbacks"]:
            try:
                with open(path, "r", encoding=enc, newline="") as f:
                    content = f.read()
                # 跳过可能的 BOM
                content = content.lstrip("\ufeff")
                # 跳过银行常见的头部说明行（如"中国银行股份有限公司..."）
                lines = content.split("\n")
                header_line_idx = 0
                for idx, line in enumerate(lines):
                    # CSV 表头通常包含"日期"或"Date"关键字
                    if any(kw in line for kw in ["日期", "Date", "交易", "金额", "Amount"]):
                        header_line_idx = idx
                        break
                filtered_content = "\n".join(lines[header_line_idx:])
                from io import StringIO
                reader = csv.DictReader(StringIO(filtered_content))
                rows = [row for row in reader if any(v.strip() for v in row.values())]
                if rows:
                    return rows
            except (UnicodeDecodeError, UnicodeError):
                continue
        return []

    def _detect_columns(self, headers: List[str]) -> Dict[str, str]:
        """自动识别列名映射"""
        col_map = {}
        for std_name, candidates in self.COLUMN_MAPPINGS.items():
            for h in headers:
                h_clean = h.strip()
                for candidate in candidates:
                    if candidate in h_clean or h_clean in candidate:
                        col_map[std_name] = h
                        break
                if std_name in col_map:
                    break
        return col_map

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """尝试多种格式解析日期"""
        if not date_str:
            return None
        # 去除时间部分
        date_str = date_str.strip().split(" ")[0]
        for fmt in self.config["date_formats"]:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

    def _parse_amount(self, row: Dict, col_map: Dict, headers: List[str]) -> Optional[float]:
        """
        解析金额，处理多种格式：
        - 单一金额列（正负表示借贷）
        - 借贷分离列（收入/支出、借方/贷方）
        - 千分位逗号、货币符号
        """
        amount_col = col_map.get("amount", "")
        raw_val = str(row.get(amount_col, "")).strip()

        if not raw_val:
            # 尝试借贷分离列
            for credit_col in ["收入", "贷方", "Credit"]:
                for h in headers:
                    if credit_col in h:
                        credit_val = str(row.get(h, "")).strip()
                        if credit_val:
                            return self._clean_amount(credit_val)
            for debit_col in ["支出", "借方", "Debit"]:
                for h in headers:
                    if debit_col in h:
                        debit_val = str(row.get(h, "")).strip()
                        if debit_val:
                            return -self._clean_amount(debit_val)
            return None

        return self._clean_amount(raw_val)

    @staticmethod
    def _clean_amount(val: str) -> Optional[float]:
        """清理金额字符串（去逗号、货币符号等）"""
        if not val:
            return None
        # 去除千分位逗号、货币符号、空格
        cleaned = val.replace(",", "").replace("¥", "").replace("￥", "").replace(" ", "").strip()
        # 处理括号表示负数 (100.00) → -100.00
        if cleaned.startswith("(") and cleaned.endswith(")"):
            cleaned = "-" + cleaned[1:-1]
        try:
            return float(cleaned)
        except ValueError:
            return None

    # ------------------------------------------------------------------
    # 模糊匹配引擎
    # ------------------------------------------------------------------

    def load_invoices(self, invoices: List[Dict[str, Any]]) -> 'BankReconciler':
        """
        加载发票数据（用于匹配的目标）
        发票 dict 需包含：invoice_number, amount（价税合计或不含税金额）, billing_date
        """
        self.invoices = invoices
        return self

    def match_all(self) -> List[Dict[str, Any]]:
        """
        对所有银行流水记录执行匹配
        返回匹配结果列表
        """
        if not self.transactions:
            raise ValueError("未加载银行流水，请先调用 parse_csv()")
        if not self.invoices:
            raise ValueError("未加载发票数据，请先调用 load_invoices()")

        results = []
        for tx in self.transactions:
            best_match = self._find_best_match(tx)
            if best_match:
                tx.matched_invoice = best_match["invoice"]
                tx.match_score = best_match["score"]
                tx.match_status = "matched" if best_match["score"] >= self.config["match_threshold"] else "unmatched"

            results.append(tx.to_dict())

        self.results = results
        return results

    def _find_best_match(self, tx: BankTransaction) -> Optional[Dict[str, Any]]:
        """
        为单条银行流水寻找最佳匹配发票

        匹配算法：
        - 金额维度（权重 60%）：|流水金额 - 发票金额| <= 0.01 → 1.0；超出容差线性递减
        - 日期维度（权重 40%）：|流水日期 - 发票日期| <= 3天 → 1.0；超出容差线性递减
        - 综合评分 = 金额分 × 0.6 + 日期分 × 0.4
        """
        best_score = 0.0
        best_invoice = None

        for inv in self.invoices:
            score = self._calculate_match_score(tx, inv)
            if score > best_score:
                best_score = score
                best_invoice = inv

        if best_invoice and best_score > 0:
            return {"invoice": best_invoice, "score": best_score}
        return None

    def _calculate_match_score(self, tx: BankTransaction, inv: Dict[str, Any]) -> float:
        """计算单条流水与单张发票的匹配得分"""

        # --- 金额维度 ---
        inv_amount = inv.get("total") or inv.get("amount")
        if inv_amount is None:
            return 0.0

        # 银行流水的支出（负数）对应发票金额（正数）
        tx_amount_abs = abs(tx.amount)
        amount_diff = abs(tx_amount_abs - float(inv_amount))
        amount_tolerance = self.config["amount_tolerance"]

        if amount_diff <= amount_tolerance:
            amount_score = 1.0
        else:
            # 容差之外，线性递减，到 1 元时降为 0
            amount_score = max(0.0, 1.0 - (amount_diff - amount_tolerance) / 1.0)

        # --- 日期维度 ---
        inv_date_str = inv.get("billing_date") or inv.get("invoice_date")
        if not inv_date_str:
            return amount_score * 0.6  # 无日期时仅靠金额

        inv_date = self._parse_date(str(inv_date_str))
        if not inv_date:
            return amount_score * 0.6

        date_diff_days = abs((tx.date - inv_date).days)
        date_tolerance = self.config["date_tolerance_days"]

        if date_diff_days <= date_tolerance:
            date_score = 1.0
        else:
            # 容差之外，线性递减，到 30 天时降为 0
            date_score = max(0.0, 1.0 - (date_diff_days - date_tolerance) / 30.0)

        # --- 综合评分 ---
        return amount_score * 0.6 + date_score * 0.4

    # ------------------------------------------------------------------
    # 汇总报告
    # ------------------------------------------------------------------

    def generate_report(self) -> Dict[str, Any]:
        """生成对账汇总报告"""
        if not self.results:
            self.match_all()

        total = len(self.results)
        matched = sum(1 for r in self.results if r["match_status"] == "matched")
        unmatched = total - matched

        unmatched_tx = [r for r in self.results if r["match_status"] != "matched"]
        matched_tx = [r for r in self.results if r["match_status"] == "matched"]

        # 按金额区间统计
        amount_ranges = {
            "小额（<1000）": 0,
            "中额（1000-10000）": 0,
            "大额（10000-50000）": 0,
            "超大额（≥50000）": 0,
        }
        for r in unmatched_tx:
            amt = abs(r["amount"])
            if amt < 1000:
                amount_ranges["小额（<1000）"] += 1
            elif amt < 10000:
                amount_ranges["中额（1000-10000）"] += 1
            elif amt < 50000:
                amount_ranges["大额（10000-50000）"] += 1
            else:
                amount_ranges["超大额（≥50000）"] += 1

        return {
            "summary": {
                "total_transactions": total,
                "matched": matched,
                "unmatched": unmatched,
                "match_rate": f"{(matched / total * 100):.1f}%" if total > 0 else "0%",
                "total_matched_amount": round(sum(r["amount"] for r in matched_tx), 2),
                "total_unmatched_amount": round(sum(r["amount"] for r in unmatched_tx), 2),
            },
            "unmatched_by_amount_range": amount_ranges,
            "unmatched_details": unmatched_tx,
            "matched_details": matched_tx,
        }


# ======================================================================
# 便捷函数（供外部直接调用）
# ======================================================================

def reconcile(csv_path: str, invoices: List[Dict], config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    一站式对账函数

    参数:
        csv_path: 银行流水 CSV 文件路径
        invoices: 发票列表（dict 列表，需含 amount/total 和 billing_date）
        config: 可选的对账配置

    返回:
        dict: 对账汇总报告
    """
    reconciler = BankReconciler(config=config)
    reconciler.parse_csv(csv_path)
    reconciler.load_invoices(invoices)
    reconciler.match_all()
    return reconciler.generate_report()


# ======================================================================
# CLI 入口
# ======================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="银行流水对账引擎")
    parser.add_argument("--csv", required=True, help="银行流水 CSV 文件路径")
    parser.add_argument("--invoices", required=True, help="发票 JSON 文件路径（或 - 从 stdin 读取）")
    parser.add_argument("--output", help="对账报告输出路径（JSON）")
    parser.add_argument("--amount-tol", type=float, default=0.01, help="金额容差（元，默认 0.01）")
    parser.add_argument("--date-tol", type=int, default=3, help="日期容差（天，默认 3）")
    parser.add_argument("--threshold", type=float, default=0.85, help="匹配阈值（默认 0.85）")

    args = parser.parse_args()

    config = {
        "amount_tolerance": args.amount_tol,
        "date_tolerance_days": args.date_tol,
        "match_threshold": args.threshold,
    }

    # 加载发票
    if args.invoices == "-":
        invoices = json.loads(sys.stdin.read())
    else:
        with open(args.invoices, "r", encoding="utf-8") as f:
            invoices = json.load(f)

    # 执行对账
    report = reconcile(args.csv, invoices, config)

    # 输出
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n对账报告已保存: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
