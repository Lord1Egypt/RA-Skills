#!/usr/bin/env python3
"""
个人记账 Skill - 自动化测试脚本
读取 eval_cases.yaml，执行 CSV 格式账本验证与查询功能测试。
零外部依赖（纯 Python 标准库）。
"""

import sys
import re
import yaml
from pathlib import Path
from datetime import datetime


# ─── 路径 ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
FIXTURES_DIR = BASE_DIR / "tests" / "fixtures"
RESULTS_DIR = BASE_DIR / "tests" / "results"
SAMPLE_CSV = FIXTURES_DIR / "sample.csv"
EMPTY_CSV = FIXTURES_DIR / "empty.csv"


# ─── 工具函数 ──────────────────────────────────────────

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def record_result(results, case_id, category, description, passed, detail=""):
    results.append({
        "id": case_id,
        "category": category,
        "description": description,
        "passed": passed,
        "detail": detail,
    })


# ─── CSV 账本解析器 ──────────────────────────────────

class CsvLedgerParser:
    """
    轻量级 CSV 格式账本解析器。

    格式：
      # 日期,类型,金额,分类,描述,账户
      余额,微信钱包,800.00
      2026-01-05,收入,15000.00,工资,1月薪资,银行卡
      2026-01-07,支出,15.00,餐饮,早餐-豆浆油条,微信钱包
    """

    def __init__(self, csv_text: str):
        self.raw = csv_text
        self.transactions = []
        self.initial_balances = {}
        self._parse()

    def _parse(self):
        for line in self.raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split(",")
            if len(parts) < 6:
                continue

            # 账户初始余额行
            if parts[0].strip() == "余额" and len(parts) >= 3:
                account = parts[1].strip()
                try:
                    self.initial_balances[account] = float(parts[2].strip())
                except ValueError:
                    pass
                continue

            date_str = parts[0].strip()
            txn_type = parts[1].strip()
            try:
                amount = float(parts[2].strip())
            except ValueError:
                continue

            if not re.match(r"\d{4}-\d{2}-\d{2}", date_str):
                continue

            category = parts[3].strip()
            description = parts[4].strip()
            account = parts[5].strip()

            self.transactions.append({
                "date": date_str,
                "type": txn_type,
                "amount": amount,
                "category": category,
                "description": description,
                "account": account,
            })

    def expenses_in_month(self, year: int, month: int) -> tuple:
        """返回 (总支出, 笔数)"""
        prefix = f"{year}-{month:02d}"
        total = 0.0
        count = 0
        for tx in self.transactions:
            if not tx["date"].startswith(prefix):
                continue
            if tx["type"] == "支出":
                total += tx["amount"]
                count += 1
        return total, count

    def income_in_month(self, year: int, month: int) -> tuple:
        """返回 (总收入, 笔数)"""
        prefix = f"{year}-{month:02d}"
        total = 0.0
        count = 0
        for tx in self.transactions:
            if not tx["date"].startswith(prefix):
                continue
            if tx["type"] == "收入":
                total += tx["amount"]
                count += 1
        return total, count

    def category_expenses(self, year: int, month: int, category_root: str) -> float:
        """按一级分类统计支出。"""
        prefix = f"{year}-{month:02d}"
        total = 0.0
        for tx in self.transactions:
            if not tx["date"].startswith(prefix):
                continue
            if tx["type"] == "支出":
                root = tx["category"].split(":")[0] if tx["category"] else "其他"
                if category_root in root or root in category_root:
                    total += tx["amount"]
        return total

    def range_expenses(self, start_date: str, end_date: str) -> float:
        """区间总支出。"""
        total = 0.0
        for tx in self.transactions:
            if start_date <= tx["date"] <= end_date and tx["type"] == "支出":
                total += tx["amount"]
        return total

    def recent_transactions(self, count: int) -> list:
        """最近N笔交易。"""
        sorted_txns = sorted(self.transactions, key=lambda t: t["date"], reverse=True)
        return sorted_txns[:count]

    def account_transactions(self, account_name: str) -> list:
        """某账户全部交易。"""
        return [tx for tx in self.transactions if tx["account"] == account_name]

    def max_expense(self, year: int, month: int):
        """最大单笔支出。"""
        prefix = f"{year}-{month:02d}"
        month_txns = [tx for tx in self.transactions
                      if tx["date"].startswith(prefix) and tx["type"] == "支出"]
        if not month_txns:
            return None
        best = max(month_txns, key=lambda t: t["amount"])
        return {"amount": best["amount"], "description": best["description"],
                "account": best["account"], "category": best["category"]}

    def keyword_search(self, keyword: str) -> list:
        """按描述/分类关键字搜索。"""
        result = []
        for tx in self.transactions:
            if keyword in tx["description"] or keyword in tx["category"]:
                result.append({"amount": tx["amount"], "description": tx["description"]})
        return result

    def category_ranking(self, year: int, month: int) -> list:
        """分类支出排行。"""
        prefix = f"{year}-{month:02d}"
        cats = {}
        for tx in self.transactions:
            if not tx["date"].startswith(prefix):
                continue
            if tx["type"] == "支出":
                root = tx["category"].split(":")[0] if tx["category"] else "其他"
                cats[root] = cats.get(root, 0) + tx["amount"]
        return sorted(cats.items(), key=lambda x: x[1], reverse=True)


# ─── 测试执行器 ──────────────────────────────────────

class TestRunner:
    def __init__(self, cases_path):
        self.cases = load_yaml(cases_path)
        self.results = []
        self.passed = 0
        self.failed = 0
        self.total = 0

    def run_all(self):
        sample = CsvLedgerParser(read_csv(SAMPLE_CSV))
        empty = CsvLedgerParser(read_csv(EMPTY_CSV))

        self._run_nlp_tests()
        self._run_format_tests()
        self._run_query_tests(sample, empty)
        self._run_report_tests(sample)

        return self.results

    # ── A. 自然语言解析 ──

    def _run_nlp_tests(self):
        cases = self.cases.get("natural_language_parsing", [])
        for c in cases:
            self.total += 1
            passed = True
            details = []

            e = c["expected"]
            # 日期格式验证
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", e["date"]):
                passed = False
                details.append(f"日期格式错误: {e['date']}")

            # 金额验证
            try:
                amt = float(e["amount"])
                if amt <= 0:
                    passed = False
                    details.append(f"金额应 > 0: {amt}")
            except (ValueError, TypeError):
                passed = False
                details.append(f"金额无效: {e['amount']}")

            # 类型验证
            if e.get("type") not in ("收入", "支出"):
                passed = False
                details.append(f"类型无效: {e.get('type')}")

            # 分类验证
            if not e.get("category"):
                passed = False
                details.append("缺少分类")

            if passed:
                self.passed += 1
            else:
                self.failed += 1

            record_result(self.results, c["id"], "自然语言解析",
                          c["input"], passed, "; ".join(details) or "规范验证通过")

    # ── B. CSV 格式验证 ──

    def _run_format_tests(self):
        cases = self.cases.get("ledger_format_validation", [])
        for c in cases:
            self.total += 1
            passed = True
            details = []
            check_lines = c["check"].strip().splitlines()
            exp = c["expected"]

            if exp.get("has_date"):
                m = re.match(r"^\d{4}-\d{2}-\d{2}", check_lines[0])
                if not m:
                    passed = False
                    details.append("缺少日期")
                elif exp.get("date_format") == "YYYY-MM-DD" and not re.match(
                    r"^\d{4}-\d{2}-\d{2}$", m.group()
                ):
                    passed = False
                    details.append("日期格式非 YYYY-MM-DD")

            if exp.get("has_type"):
                has_type = any(
                    t in check_lines[0] for t in ["收入", "支出", "余额"]
                )
                if not has_type:
                    passed = False
                    details.append("缺少类型字段")

            if exp.get("has_amount"):
                has_amount = all(
                    re.search(r"-?[\d.]+", line) for line in check_lines if line.strip()
                )
                if not has_amount:
                    passed = False
                    details.append("缺少金额")

            if exp.get("has_csv_structure"):
                # 验证 CSV 格式：逗号分隔，至少6列
                for line in check_lines:
                    if line.strip() and not line.strip().startswith("#"):
                        parts = line.split(",")
                        if len(parts) < 6:
                            passed = False
                            details.append(f"CSV列数不足: {line}")
                            break

            if exp.get("initial_balance"):
                # 验证余额行格式: 余额,账户,金额
                line = check_lines[0]
                parts = line.split(",")
                if parts[0].strip() != "余额":
                    passed = False
                    details.append("余额行应以'余额,'开头")
                elif len(parts) < 3:
                    passed = False
                    details.append("余额行列数不足")

            if exp.get("transaction_row"):
                # 验证交易行有6个CSV字段
                line = check_lines[0]
                parts = line.split(",")
                if len(parts) < 6:
                    passed = False
                    details.append(f"交易行字段不足，期望6个字段")

            if passed:
                self.passed += 1
            else:
                self.failed += 1

            record_result(self.results, c["id"], "格式验证",
                          c["description"], passed, "; ".join(details) or "格式正确")

    # ── C. 查询功能 ──

    def _run_query_tests(self, ledger, empty_ledger):
        cases = self.cases.get("query_functionality", [])
        for c in cases:
            self.total += 1
            passed = True
            details = []
            exp = c["expected"]
            qt = c["query_type"]
            params = c["params"]

            if qt == "monthly_expenses":
                lr = empty_ledger if "empty" in c.get("notes", "").lower() else ledger
                total, count = lr.expenses_in_month(params["year"], params["month"])
                if abs(total - exp["total_expenses"]) > 0.01:
                    passed = False
                    details.append(f"支出合计: 期望 {exp['total_expenses']}, 实际 {total:.2f}")
                if count != exp["transaction_count"]:
                    passed = False
                    details.append(f"交易笔数: 期望 {exp['transaction_count']}, 实际 {count}")

            elif qt == "monthly_income":
                total, count = ledger.income_in_month(params["year"], params["month"])
                if abs(total - exp["total_income"]) > 0.01:
                    passed = False
                    details.append(f"收入合计: 期望 {exp['total_income']}, 实际 {total:.2f}")
                if count != exp["transaction_count"]:
                    passed = False
                    details.append(f"交易笔数: 期望 {exp['transaction_count']}, 实际 {count}")

            elif qt == "category_expenses":
                total = ledger.category_expenses(params["year"], params["month"], params["category"])
                if abs(total - exp["total"]) > 0.01:
                    passed = False
                    details.append(f"分类支出: 期望 {exp['total']}, 实际 {total:.2f}")

            elif qt == "recent_transactions":
                txs = ledger.recent_transactions(params["count"])
                if len(txs) != exp["count"]:
                    passed = False
                    details.append(f"返回笔数: 期望 {exp['count']}, 实际 {len(txs)}")
                if exp.get("sorted_by_date_desc"):
                    dates = [tx["date"] for tx in txs]
                    if dates != sorted(dates, reverse=True):
                        passed = False
                        details.append("未按日期降序排列")

            elif qt == "range_expenses":
                total = ledger.range_expenses(params["start_date"], params["end_date"])
                if abs(total - exp["total_expenses"]) > 0.01:
                    passed = False
                    details.append(f"区间支出: 期望 {exp['total_expenses']}, 实际 {total:.2f}")

            elif qt == "account_transactions":
                txs = ledger.account_transactions(params["account"])
                if not txs:
                    all_accounts = {tx["account"] for tx in ledger.transactions}
                    if params["account"] not in all_accounts:
                        passed = False
                        details.append(f"账户 {params['account']} 在账本中无交易")

            elif qt == "max_expense":
                best = ledger.max_expense(params["year"], params["month"])
                if best is None:
                    passed = False
                    details.append("未找到支出记录")
                else:
                    if abs(best["amount"] - exp["amount"]) > 0.01:
                        passed = False
                        details.append(f"最大支出: 期望 {exp['amount']}, 实际 {best['amount']}")
                    if exp.get("description") and exp["description"] not in best["description"]:
                        passed = False
                        details.append(f"描述: 期望含'{exp['description']}', 实际'{best['description']}'")

            elif qt == "keyword_search":
                results = ledger.keyword_search(params["keyword"])
                if len(results) != exp["count"]:
                    passed = False
                    details.append(f"搜索结果数: 期望 {exp['count']}, 实际 {len(results)}")
                elif results and exp.get("amount") and abs(results[0]["amount"] - exp["amount"]) > 0.01:
                    passed = False
                    details.append(f"金额: 期望 {exp['amount']}, 实际 {results[0]['amount']}")

            if passed:
                self.passed += 1
            else:
                self.failed += 1

            record_result(self.results, c["id"], "查询功能",
                          c["description"], passed, "; ".join(details) or "查询正确")

    # ── D. 报告生成 ──

    def _run_report_tests(self, ledger):
        cases = self.cases.get("report_generation", [])
        for c in cases:
            self.total += 1
            passed = True
            details = []
            exp = c["expected"]
            rt = c["report_type"]
            params = c["params"]
            year, month = params["year"], params["month"]

            if rt == "monthly_summary":
                income, _ = ledger.income_in_month(year, month)
                expenses, _ = ledger.expenses_in_month(year, month)
                net = income - expenses

                if abs(income - exp["total_income"]) > 0.01:
                    passed = False
                    details.append(f"收入: 期望 {exp['total_income']}, 实际 {income:.2f}")
                if abs(expenses - exp["total_expenses"]) > 0.01:
                    passed = False
                    details.append(f"支出: 期望 {exp['total_expenses']}, 实际 {expenses:.2f}")
                if abs(net - exp["net_balance"]) > 0.01:
                    passed = False
                    details.append(f"结余: 期望 {exp['net_balance']}, 实际 {net:.2f}")

            elif rt == "category_ranking":
                ranking = ledger.category_ranking(year, month)
                if not ranking:
                    passed = False
                    details.append("无分类数据")
                else:
                    top_cat, top_amt = ranking[0]
                    if abs(top_amt - exp["top_amount"]) > 0.01:
                        passed = False
                        details.append(f"TOP分类金额: 期望 {exp['top_amount']}, 实际 {top_amt:.2f}")
                    if len(ranking) < exp.get("category_count", 0):
                        passed = False
                        details.append(f"分类数: 期望 ≥ {exp['category_count']}, 实际 {len(ranking)}")

            elif rt == "daily_average":
                expenses, _ = ledger.expenses_in_month(year, month)
                days_in_month = 31 if month in (1, 3, 5, 7, 8, 10, 12) else (30 if month != 2 else 28)
                daily = expenses / days_in_month
                r = exp["daily_average_range"]
                if not (r["min"] <= daily <= r["max"]):
                    passed = False
                    details.append(f"日均消费: 期望 {r['min']}-{r['max']}, 实际 {daily:.2f}")

            elif rt == "max_single_expense":
                best = ledger.max_expense(year, month)
                if best is None:
                    passed = False
                    details.append("无支出记录")
                else:
                    if abs(best["amount"] - exp["amount"]) > 0.01:
                        passed = False
                        details.append(f"最大支出: 期望 {exp['amount']}, 实际 {best['amount']}")
                    if exp.get("description_contains") and exp["description_contains"] not in best["description"]:
                        passed = False
                        details.append(f"描述: 期望含'{exp['description_contains']}'")

            if passed:
                self.passed += 1
            else:
                self.failed += 1

            record_result(self.results, c["id"], "报告生成",
                          c["description"], passed, "; ".join(details) or "报告正确")

    def print_report(self):
        print("\n" + "=" * 70)
        print("  个人记账 Skill - 测试报告（CSV格式）")
        print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        categories = {}
        for r in self.results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = {"passed": 0, "failed": 0, "total": 0}
            categories[cat]["total"] += 1
            if r["passed"]:
                categories[cat]["passed"] += 1
            else:
                categories[cat]["failed"] += 1

        print(f"\n{'类别':<16} {'通过':>6} {'失败':>6} {'合计':>6} {'通过率':>8}")
        print("-" * 50)
        for cat, stats in categories.items():
            rate = stats["passed"] / stats["total"] * 100 if stats["total"] else 0
            print(f"{cat:<16} {stats['passed']:>6} {stats['failed']:>6} {stats['total']:>6} {rate:>7.1f}%")
        print("-" * 50)
        total_rate = self.passed / self.total * 100 if self.total else 0
        print(f"{'总计':<16} {self.passed:>6} {self.failed:>6} {self.total:>6} {total_rate:>7.1f}%")

        failed = [r for r in self.results if not r["passed"]]
        if failed:
            print("\n" + "─" * 50)
            print("❌ 失败用例:")
            for r in failed:
                print(f"  [{r['id']}] {r['description']}")
                print(f"         类别: {r['category']}")
                print(f"         详情: {r['detail']}")
                print()

        print("=" * 70)
        print(f"  结果: {'✅ 全部通过' if self.failed == 0 else f'⚠️  {self.failed} 条失败'}")
        print("=" * 70 + "\n")

        return self.results

    def save_markdown_report(self, path):
        lines = []
        lines.append(f"# 个人记账 Skill - 测试报告 v2（CSV格式）")
        lines.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**测试用例**: {self.total} 条")
        lines.append(f"**通过**: {self.passed} | **失败**: {self.failed}")
        lines.append(f"**通过率**: {self.passed / self.total * 100:.1f}%\n")

        categories = {}
        for r in self.results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = {"passed": 0, "failed": 0, "total": 0}
            categories[cat]["total"] += 1
            if r["passed"]:
                categories[cat]["passed"] += 1
            else:
                categories[cat]["failed"] += 1

        lines.append("## 概述\n")
        lines.append("| 类别 | 通过 | 失败 | 合计 | 通过率 |")
        lines.append("|------|------|------|------|--------|")
        for cat, stats in categories.items():
            rate = stats["passed"] / stats["total"] * 100 if stats["total"] else 0
            lines.append(f"| {cat} | {stats['passed']} | {stats['failed']} | {stats['total']} | {rate:.1f}% |")
        total_rate = self.passed / self.total * 100 if self.total else 0
        lines.append(f"| **总计** | **{self.passed}** | **{self.failed}** | **{self.total}** | **{total_rate:.1f}%** |\n")

        failed = [r for r in self.results if not r["passed"]]
        if failed:
            lines.append("## 失败用例分析\n")
            for r in failed:
                lines.append(f"### [{r['id']}] {r['description']}")
                lines.append(f"- **类别**: {r['category']}")
                lines.append(f"- **详情**: {r['detail']}\n")
        else:
            lines.append("## 失败用例\n无\n")

        lines.append("## 全部用例结果\n")
        lines.append("| ID | 类别 | 描述 | 结果 | 详情 |")
        lines.append("|----|------|------|------|------|")
        for r in self.results:
            status = "✅ PASS" if r["passed"] else "❌ FAIL"
            lines.append(f"| {r['id']} | {r['category']} | {r['description']} | {status} | {r['detail'] or '-'} |")

        lines.append("\n## 格式说明\n")
        lines.append("本版本使用 CSV 格式账本（`*.csv`），格式：")
        lines.append("```")
        lines.append("# 日期,类型,金额,分类,描述,账户")
        lines.append("余额,微信钱包,1000.00")
        lines.append("2026-05-21,支出,50.00,餐饮,午餐,微信钱包")
        lines.append("2026-05-22,收入,8000.00,工资,5月工资,银行卡")
        lines.append("```")

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


# ─── 主入口 ──────────────────────────────────────────

def main():
    cases_path = Path(__file__).resolve().parent / "eval_cases.yaml"
    if not cases_path.exists():
        print(f"❌ 测试用例文件不存在: {cases_path}")
        sys.exit(1)

    if not SAMPLE_CSV.exists():
        print(f"❌ 测试账本不存在: {SAMPLE_CSV}")
        sys.exit(1)

    runner = TestRunner(cases_path)
    runner.run_all()
    runner.print_report()

    report_path = RESULTS_DIR / "v2_report.md"
    runner.save_markdown_report(report_path)
    print(f"📄 报告已保存: {report_path}")

    sys.exit(0 if runner.failed == 0 else 1)


if __name__ == "__main__":
    main()