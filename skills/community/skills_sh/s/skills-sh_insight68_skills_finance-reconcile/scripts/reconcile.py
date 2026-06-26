#!/usr/bin/env python3
"""
财务审计脚本
支持资产负债表、利润表审计，科目变动追踪，报表勾稽关系验证
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

import pandas as pd


class AccountType(Enum):
    """账户类型"""
    ASSET = "资产"
    LIABILITY = "负债"
    EQUITY = "所有者权益"
    REVENUE = "收入"
    EXPENSE = "费用"
    PROFIT_ITEM = "利润项目"


@dataclass
class AccountBalance:
    """账户余额"""
    account: str
    account_type: AccountType
    opening_balance: float = 0.0
    debit_change: float = 0.0
    credit_change: float = 0.0
    closing_balance: float = 0.0
    is_balanced: bool = True
    diff: float = 0.0


@dataclass
class ProfitItem:
    """利润项目"""
    item: str
    amount: float
    is_positive: bool = True  # 增加利润的项目（收入、其他收益等）


@dataclass
class AuditResult:
    """审计结果"""
    is_passed: bool = True
    balance_sheet_check: Dict[str, Any] = field(default_factory=dict)
    income_statement_check: Dict[str, Any] = field(default_factory=dict)
    cross_validation: Dict[str, Any] = field(default_factory=dict)
    account_analysis: List[Dict] = field(default_factory=list)
    transaction_trace: List[Dict] = field(default_factory=list)
    unbalanced_items: List[Dict] = field(default_factory=list)


# ============================================================================
# 文件读取工具
# ============================================================================

def read_excel_file(
    filepath: Union[str, Path],
    sheet_name: Optional[Union[str, int]] = None,
    header: int = 0
) -> pd.DataFrame:
    """读取 Excel 文件，自动处理编码和空值"""
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name, header=header)
        # 清理列名：去除前后空格
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        raise ValueError(f"读取 Excel 文件失败 {filepath}: {e}")


def validate_columns(df: pd.DataFrame, required_columns: List[str], df_name: str) -> None:
    """验证 DataFrame 是否包含必需的列"""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"{df_name} 缺少必需的列: {missing_columns}")


def to_float(value: Any) -> float:
    """转换为浮点数，处理空值和无效值"""
    try:
        return float(value) if pd.notna(value) else 0.0
    except (ValueError, TypeError):
        return 0.0


# ============================================================================
# 资产负债表审计
# ============================================================================

def parse_balance_sheet(
    df: pd.DataFrame,
    account_col: str = "科目",
    opening_col: str = "期初余额",
    closing_col: str = "期末余额"
) -> Dict[str, AccountBalance]:
    """
    解析资产负债表

    Args:
        df: 资产负债表 DataFrame
        account_col: 科目列名
        opening_col: 期初余额列名
        closing_col: 期末余额列名

    Returns:
        科目余额字典 {科目: AccountBalance}
    """
    validate_columns(df, [account_col, opening_col, closing_col], "资产负债表")

    accounts = {}
    for _, row in df.iterrows():
        account = str(row[account_col]).strip()
        if not account or account in ["合计", "总计", "小计"]:
            continue

        opening = to_float(row[opening_col])
        closing = to_float(row[closing_col])

        # 推断账户类型（简化版，实际应根据科目编码或分类）
        account_type = AccountType.ASSET  # 默认为资产

        accounts[account] = AccountBalance(
            account=account,
            account_type=account_type,
            opening_balance=opening,
            closing_balance=closing
        )

    return accounts


def parse_account_changes(
    df: pd.DataFrame,
    account_col: str = "科目",
    debit_col: str = "借方",
    credit_col: str = "贷方"
) -> Dict[str, Tuple[float, float]]:
    """
    解析科目变动明细表

    Args:
        df: 科目变动明细表 DataFrame
        account_col: 科目列名
        debit_col: 借方列名
        credit_col: 贷方列名

    Returns:
        科目变动字典 {科目: (借方, 贷方)}
    """
    validate_columns(df, [account_col, debit_col, credit_col], "科目变动明细表")

    changes = {}
    for _, row in df.iterrows():
        account = str(row[account_col]).strip()
        if not account:
            continue

        debit = to_float(row[debit_col])
        credit = to_float(row[credit_col])

        # 累计变动
        if account in changes:
            prev_debit, prev_credit = changes[account]
            changes[account] = (prev_debit + debit, prev_credit + credit)
        else:
            changes[account] = (debit, credit)

    return changes


def validate_balance_sheet(
    balance_sheet: Dict[str, AccountBalance],
    account_changes: Dict[str, Tuple[float, float]],
    tolerance: float = 0.01
) -> List[AccountBalance]:
    """
    验证资产负债表平衡

    验证公式：期初余额 + 借方变动 - 贷方变动 = 期末余额

    Args:
        balance_sheet: 资产负债表科目
        account_changes: 科目变动
        tolerance: 容忍误差

    Returns:
        更新后的科目列表（包含是否平衡标记）
    """
    results = []

    for account, balance in balance_sheet.items():
        debit, credit = account_changes.get(account, (0.0, 0.0))

        # 计算预期期末余额
        # 资产类：期初 + 借方 - 贷方 = 期末
        # 负债权益类：期初 + 贷方 - 借方 = 期末
        if balance.account_type in [AccountType.ASSET]:
            expected_closing = balance.opening_balance + debit - credit
        else:
            expected_closing = balance.opening_balance + credit - debit

        diff = abs(balance.closing_balance - expected_closing)
        is_balanced = diff <= tolerance

        balance.debit_change = debit
        balance.credit_change = credit
        balance.diff = diff
        balance.is_balanced = is_balanced

        results.append(balance)

    return results


def verify_balance_sheet_total(
    df: pd.DataFrame,
    type_col: str = "类型",
    amount_col: str = "金额"
) -> Dict[str, Any]:
    """
    验证资产负债表平衡（资产 = 负债 + 所有者权益）

    Args:
        df: 资产负债表 DataFrame
        type_col: 类型列名（资产/负债/权益）
        amount_col: 金额列名

    Returns:
        验证结果
    """
    if type_col not in df.columns or amount_col not in df.columns:
        return {"is_balanced": False, "error": "缺少必要的列"}

    totals = {"资产": 0.0, "负债": 0.0, "所有者权益": 0.0}

    for _, row in df.iterrows():
        acc_type = str(row[type_col]).strip()
        amount = to_float(row[amount_col])
        totals[acc_type] = totals.get(acc_type, 0.0) + amount

    assets = totals.get("资产", 0.0)
    liabilities_equity = totals.get("负债", 0.0) + totals.get("所有者权益", 0.0)

    diff = abs(assets - liabilities_equity)

    return {
        "is_balanced": diff <= 0.01,
        "assets": assets,
        "liabilities": totals.get("负债", 0.0),
        "equity": totals.get("所有者权益", 0.0),
        "liabilities_equity": liabilities_equity,
        "diff": diff
    }


# ============================================================================
# 利润表审计
# ============================================================================

def parse_income_statement(
    df: pd.DataFrame,
    item_col: str = "项目",
    amount_col: str = "金额"
) -> List[ProfitItem]:
    """
    解析利润表

    Args:
        df: 利润表 DataFrame
        item_col: 项目列名
        amount_col: 金额列名

    Returns:
        利润项目列表
    """
    validate_columns(df, [item_col, amount_col], "利润表")

    items = []
    for _, row in df.iterrows():
        item = str(row[item_col]).strip()
        if not item or item in ["合计", "总计"]:
            continue

        amount = to_float(row[amount_col])

        # 判断是否为增加利润的项目
        positive_keywords = ["收入", "收益", "利得", "其他收益", "营业外收入"]
        negative_keywords = ["成本", "费用", "损失", "减值", "营业外支出", "所得税"]

        is_positive = any(kw in item for kw in positive_keywords)
        if any(kw in item for kw in negative_keywords):
            is_positive = False

        items.append(ProfitItem(item=item, amount=amount, is_positive=is_positive))

    return items


def verify_income_statement_with_details(
    income_items: List[ProfitItem],
    details_df: pd.DataFrame,
    item_col: str = "项目",
    amount_col: str = "金额"
) -> List[Dict[str, Any]]:
    """
    用明细表验证利润表项目

    Args:
        income_items: 利润表项目
        details_df: 明细表 DataFrame
        item_col: 明细表项目列名
        amount_col: 明细表金额列名

    Returns:
        验证结果列表
    """
    # 汇总明细表
    details_summary = {}
    for _, row in details_df.iterrows():
        item = str(row[item_col]).strip()
        if not item:
            continue
        amount = to_float(row[amount_col])
        details_summary[item] = details_summary.get(item, 0.0) + amount

    results = []
    for income_item in income_items:
        detail_amount = details_summary.get(income_item.item, 0.0)
        diff = abs(income_item.amount - detail_amount)
        is_matched = diff <= 0.01

        results.append({
            "项目": income_item.item,
            "利润表金额": income_item.amount,
            "明细表金额": detail_amount,
            "差异": diff,
            "是否匹配": is_matched,
            "增加利润": income_item.is_positive
        })

    return results


# ============================================================================
# 报表勾稽关系验证
# ============================================================================

def verify_cross_validation(
    balance_sheet: Dict[str, AccountBalance],
    net_profit: float,
    tolerance: float = 0.01
) -> Dict[str, Any]:
    """
    验证报表勾稽关系

    主要勾稽关系：
    1. 期末未分配利润 = 期初未分配利润 + 本年净利润 - 本年利润分配

    Args:
        balance_sheet: 资产负债表科目
        net_profit: 净利润（来自利润表）
        tolerance: 容忍误差

    Returns:
        勾稽关系验证结果
    """
    # 查找未分配利润科目
    retained_earnings_keys = [
        "未分配利润", "盈余公积", "未分配收益"
    ]

    retained_earnings = None
    for key in retained_earnings_keys:
        for account, balance in balance_sheet.items():
            if key in account:
                retained_earnings = balance
                break
        if retained_earnings:
            break

    results = {
        "retained_earnings_verified": False,
        "net_profit": net_profit,
        "retained_earnings_change": 0.0
    }

    if retained_earnings:
        # 未分配利润变动
        change = retained_earnings.closing_balance - retained_earnings.opening_balance
        results["retained_earnings_change"] = change

        # 验证是否匹配（可能有利润分配，所以不完全等于净利润）
        results["retained_earnings_verified"] = abs(change - net_profit) <= tolerance * 100

    return results


# ============================================================================
# 交易影响追踪
# ============================================================================

def trace_transaction_impact(
    transactions_df: pd.DataFrame,
    account_col: str = "科目",
    debit_col: str = "借方",
    credit_col: str = "贷方",
    date_col: Optional[str] = None,
    voucher_col: Optional[str] = "凭证号"
) -> List[Dict[str, Any]]:
    """
    追踪交易对各科目的影响

    Args:
        transactions_df: 交易明细表 DataFrame
        account_col: 科目列名
        debit_col: 借方列名
        credit_col: 贷方列名
        date_col: 日期列名（可选）
        voucher_col: 凭证号列名（可选）

    Returns:
        交易影响追踪列表
    """
    trace_list = []

    for _, row in transactions_df.iterrows():
        account = str(row[account_col]).strip()
        if not account:
            continue

        debit = to_float(row[debit_col])
        credit = to_float(row[credit_col])

        trace_info = {
            "科目": account,
            "借方": debit,
            "贷方": credit,
            "净影响": debit - credit
        }

        if date_col and date_col in row:
            trace_info["日期"] = row[date_col]
        if voucher_col and voucher_col in row:
            trace_info["凭证号"] = str(row[voucher_col])

        trace_list.append(trace_info)

    return trace_list


# ============================================================================
# 报告生成
# ============================================================================

def generate_account_analysis(accounts: List[AccountBalance]) -> pd.DataFrame:
    """生成科目变动分析表"""
    data = []
    for acc in accounts:
        data.append({
            "科目": acc.account,
            "科目类型": acc.account_type.value,
            "期初余额": acc.opening_balance,
            "借方变动": acc.debit_change,
            "贷方变动": acc.credit_change,
            "净变动": acc.debit_change - acc.credit_change,
            "期末余额": acc.closing_balance,
            "是否平衡": "是" if acc.is_balanced else "否",
            "差异": acc.diff
        })

    return pd.DataFrame(data)


def generate_audit_report(
    result: AuditResult,
    period: str = "本期"
) -> str:
    """生成审计报告文本"""
    lines = [
        "=" * 80,
        f"财务审计报告 - {period}".center(80),
        "=" * 80,
        "",
        "一、审计概述",
        "-" * 80,
        f"审计结果: {'通过 ✓' if result.is_passed else '不通过 ✗'}",
        "",
        "二、资产负债表审计",
        "-" * 80,
        f"资产总计: ¥{result.balance_sheet_check.get('assets', 0):,.2f}",
        f"负债总计: ¥{result.balance_sheet_check.get('liabilities', 0):,.2f}",
        f"所有者权益总计: ¥{result.balance_sheet_check.get('equity', 0):,.2f}",
        f"资产负债平衡: {'是 ✓' if result.balance_sheet_check.get('is_balanced') else '否 ✗'}",
    ]

    if not result.balance_sheet_check.get('is_balanced'):
        lines.append(f"  差异金额: ¥{result.balance_sheet_check.get('diff', 0):,.2f}")

    lines.extend([
        "",
        "三、利润表审计",
        "-" * 80,
    ])

    income_check = result.income_statement_check
    matched_count = sum(1 for item in income_check.get('items', []) if item['是否匹配'])
    total_count = len(income_check.get('items', []))
    lines.append(f"利润项目匹配: {matched_count}/{total_count}")

    if matched_count < total_count:
        lines.append("不匹配项目:")
        for item in income_check.get('items', []):
            if not item['是否匹配']:
                lines.append(f"  - {item['项目']}: 差异 ¥{item['差异']:.2f}")

    lines.extend([
        "",
        "四、报表勾稽关系",
        "-" * 80,
    ])

    cross = result.cross_validation
    lines.append(f"净利润: ¥{cross.get('net_profit', 0):,.2f}")
    lines.append(f"未分配利润变动: ¥{cross.get('retained_earnings_change', 0):,.2f}")
    lines.append(f"勾稽关系验证: {'通过 ✓' if cross.get('retained_earnings_verified') else '不通过 ✗'}")

    lines.extend([
        "",
        "五、不平衡项目清单",
        "-" * 80,
    ])

    if result.unbalanced_items:
        for item in result.unbalanced_items:
            lines.append(f"  - {item.get('科目', item.get('项目', ''))}: 差异 ¥{item.get('差异', 0):,.2f}")
    else:
        lines.append("  无不平衡项目")

    lines.extend([
        "",
        "=" * 80,
        "审计完成",
        "=" * 80,
    ])

    return "\n".join(lines)


def export_audit_report(
    result: AuditResult,
    output_file: Union[str, Path],
    accounts: List[AccountBalance],
    period: str = "本期"
) -> None:
    """导出完整的 Excel 审计报告"""
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 审计报告文本
        report_text = generate_audit_report(result, period)
        report_df = pd.DataFrame({'审计报告': [report_text]})
        report_df.to_excel(writer, sheet_name='审计报告', index=False)

        # 科目变动分析表
        account_analysis = generate_account_analysis(accounts)
        account_analysis.to_excel(writer, sheet_name='科目变动分析', index=False)

        # 交易影响追踪
        if result.transaction_trace:
            trace_df = pd.DataFrame(result.transaction_trace)
            trace_df.to_excel(writer, sheet_name='交易影响追踪', index=False)

        # 利润表项目核对
        if result.income_statement_check.get('items'):
            income_df = pd.DataFrame(result.income_statement_check['items'])
            income_df.to_excel(writer, sheet_name='利润表核对', index=False)

        # 不平衡项清单
        if result.unbalanced_items:
            unbalanced_df = pd.DataFrame(result.unbalanced_items)
            unbalanced_df.to_excel(writer, sheet_name='不平衡项', index=False)


# ============================================================================
# 主审计函数
# ============================================================================

def audit_financial_statements(
    # 文件路径
    balance_sheet_file: Union[str, Path],
    account_changes_file: Union[str, Path],
    income_statement_file: Optional[Union[str, Path]] = None,
    income_details_file: Optional[Union[str, Path]] = None,
    transactions_file: Optional[Union[str, Path]] = None,

    # 列名配置
    balance_sheet_config: Optional[Dict[str, str]] = None,
    account_changes_config: Optional[Dict[str, str]] = None,
    income_statement_config: Optional[Dict[str, str]] = None,
    income_details_config: Optional[Dict[str, str]] = None,
    transactions_config: Optional[Dict[str, str]] = None,

    # 其他配置
    tolerance: float = 0.01,
    period: str = "本期"
) -> Tuple[AuditResult, List[AccountBalance]]:
    """
    执行完整的财务报表审计

    Args:
        balance_sheet_file: 资产负债表文件路径
        account_changes_file: 科目变动明细表文件路径
        income_statement_file: 利润表文件路径（可选）
        income_details_file: 利润明细表文件路径（可选）
        transactions_file: 交易明细表文件路径（可选）
        balance_sheet_config: 资产负债表列名配置
        account_changes_config: 科目变动表列名配置
        income_statement_config: 利润表列名配置
        income_details_config: 利润明细表列名配置
        transactions_config: 交易明细表列名配置
        tolerance: 容忍误差
        period: 审计期间

    Returns:
        (审计结果, 科目余额列表)
    """
    # 默认列名配置
    if balance_sheet_config is None:
        balance_sheet_config = {
            "account": "科目",
            "opening": "期初余额",
            "closing": "期末余额",
            "type": "类型",
            "amount": "金额"
        }
    if account_changes_config is None:
        account_changes_config = {
            "account": "科目",
            "debit": "借方",
            "credit": "贷方"
        }
    if income_statement_config is None:
        income_statement_config = {
            "item": "项目",
            "amount": "金额"
        }
    if income_details_config is None:
        income_details_config = {
            "item": "项目",
            "amount": "金额"
        }
    if transactions_config is None:
        transactions_config = {
            "account": "科目",
            "debit": "借方",
            "credit": "贷方",
            "date": "日期",
            "voucher": "凭证号"
        }

    result = AuditResult()

    # 1. 读取资产负债表
    bs_df = read_excel_file(balance_sheet_file)
    balance_sheet = parse_balance_sheet(
        bs_df,
        balance_sheet_config["account"],
        balance_sheet_config["opening"],
        balance_sheet_config["closing"]
    )

    # 验证资产负债表平衡
    bs_check = verify_balance_sheet_total(
        bs_df,
        balance_sheet_config.get("type", "类型"),
        balance_sheet_config.get("amount", "金额")
    )
    result.balance_sheet_check = bs_check

    # 2. 读取科目变动明细
    changes_df = read_excel_file(account_changes_file)
    account_changes = parse_account_changes(
        changes_df,
        account_changes_config["account"],
        account_changes_config["debit"],
        account_changes_config["credit"]
    )

    # 3. 验证每个科目余额
    accounts = validate_balance_sheet(balance_sheet, account_changes, tolerance)

    # 收集不平衡项目
    for acc in accounts:
        if not acc.is_balanced:
            result.unbalanced_items.append({
                "科目": acc.account,
                "类型": "资产负债表科目",
                "差异": acc.diff
            })

    # 4. 利润表审计（如果提供）
    net_profit = 0.0
    if income_statement_file:
        income_df = read_excel_file(income_statement_file)
        income_items = parse_income_statement(
            income_df,
            income_statement_config["item"],
            income_statement_config["amount"]
        )

        # 计算净利润
        net_profit = sum(
            item.amount if item.is_positive else -item.amount
            for item in income_items
        )

        # 如果有明细表，进行核对
        if income_details_file:
            details_df = read_excel_file(income_details_file)
            verification = verify_income_statement_with_details(
                income_items,
                details_df,
                income_details_config["item"],
                income_details_config["amount"]
            )

            for item in verification:
                if not item["是否匹配"]:
                    result.unbalanced_items.append({
                        "项目": item["项目"],
                        "类型": "利润表项目",
                        "差异": item["差异"]
                    })

            result.income_statement_check = {
                "items": verification,
                "net_profit": net_profit
            }
        else:
            result.income_statement_check = {
                "items": [],
                "net_profit": net_profit
            }

    # 5. 报表勾稽关系验证
    cross_validation = verify_cross_validation(balance_sheet, net_profit, tolerance)
    result.cross_validation = cross_validation

    # 6. 交易影响追踪（如果提供）
    if transactions_file:
        trans_df = read_excel_file(transactions_file)
        result.transaction_trace = trace_transaction_impact(
            trans_df,
            transactions_config["account"],
            transactions_config["debit"],
            transactions_config["credit"],
            transactions_config.get("date"),
            transactions_config.get("voucher")
        )

    # 7. 汇总结果
    result.is_passed = (
        bs_check.get("is_balanced", False) and
        not any(not acc.is_balanced for acc in accounts) and
        not result.unbalanced_items
    )

    # 8. 生成科目变动分析
    result.account_analysis = generate_account_analysis(accounts).to_dict('records')

    return result, accounts


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    """命令行入口"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='财务报表审计工具')
    parser.add_argument('--balance-sheet', '-b', required=True, help='资产负债表文件路径')
    parser.add_argument('--account-changes', '-a', required=True, help='科目变动明细表文件路径')
    parser.add_argument('--income-statement', '-i', help='利润表文件路径（可选）')
    parser.add_argument('--income-details', '-d', help='利润明细表文件路径（可选）')
    parser.add_argument('--transactions', '-t', help='交易明细表文件路径（可选）')
    parser.add_argument('--output', '-o', help='输出审计报告文件路径')
    parser.add_argument('--period', '-p', default='本期', help='审计期间')
    parser.add_argument('--tolerance', type=float, default=0.01, help='容忍误差')
    parser.add_argument('--config', '-c', help='列名配置 JSON 文件路径')
    parser.add_argument('--bs-sheet', help='资产负债表 sheet 名称或索引')
    parser.add_argument('--ac-sheet', help='科目变动表 sheet 名称或索引')
    parser.add_argument('--is-sheet', help='利润表 sheet 名称或索引')
    parser.add_argument('--id-sheet', help='利润明细表 sheet 名称或索引')
    parser.add_argument('--trans-sheet', help='交易明细表 sheet 名称或索引')

    args = parser.parse_args()

    # 读取配置
    config = {}
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)

    result, accounts = audit_financial_statements(
        balance_sheet_file=args.balance_sheet,
        account_changes_file=args.account_changes,
        income_statement_file=args.income_statement,
        income_details_file=args.income_details,
        transactions_file=args.transactions,
        balance_sheet_config=config.get('balance_sheet'),
        account_changes_config=config.get('account_changes'),
        income_statement_config=config.get('income_statement'),
        income_details_config=config.get('income_details'),
        transactions_config=config.get('transactions'),
        tolerance=args.tolerance,
        period=args.period
    )

    # 打印审计报告
    print(generate_audit_report(result, args.period))

    # 导出报告
    if args.output:
        export_audit_report(result, args.output, accounts, args.period)
        print(f"\n审计报告已导出至: {args.output}")

    sys.exit(0 if result.is_passed else 1)


if __name__ == '__main__':
    main()
