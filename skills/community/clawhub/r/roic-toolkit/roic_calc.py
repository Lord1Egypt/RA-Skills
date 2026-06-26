"""
ROIC 核心 V2.0 穿透模式 自动化计算工具

用法:
    python roic_calc.py 600426.SH 2021-2024
    python roic_calc.py 600426.SH 2021 2022 2023 2024
    python roic_calc.py 03690.HK 2021-2024

原理:
    从 finance-data API 获取利润表和资产负债表年报数据，
    按照 ROIC V2.0 框架自动计算核心 NOPAT 和投入资本，
    输出 Markdown 格式的穿透分析报告。

自动处理:
    - 应付票据 → 有息负债
    - 交易性金融资产、其他权益工具投资、其他非流动金融资产 → 剔除
    - 衍生金融资产、定期存款、应收款项融资 → 剔除
    - 一年内到期非流动资产 → 全额剔除（已退出经营循环）
    - 商誉、投资性房地产 → 非经营资产，全额剔除
    - 交易性金融负债、衍生金融负债 → 有息负债
    - 发放贷款及垫款 → 金融资产（从分母剔除）
    - 权益法投资收益（ass_invest_income）→ 加入分子

需人工复核（标注 ⚠️）:
    - 其他流动资产中的金融产品（结构性存款、理财、收益凭证）
    - 其他非流动资产中的金融产品（定期存款、结构性存款）
    - 长期股权投资中的基金/财务投资部分
    - 收购无形资产摊销
    - 复核方式：下载完整版年报PDF（pdfplumber提取）或东方财富HTML年报
"""

import sys
import json
import urllib.request
from datetime import datetime

API_URL = "https://www.codebuddy.cn/v2/tool/financedata"

# 利润表所需字段
INCOME_FIELDS = [
    "revenue",            # 营业收入
    "oper_cost",          # 营业成本
    "biz_tax_surchg",     # 税金及附加
    "sell_exp",           # 销售费用
    "admin_exp",          # 管理费用
    "rd_exp",             # 研发费用
    "total_profit",       # 利润总额
    "income_tax",         # 所得税费用
    "invest_income",      # 投资收益（合计）
    "ass_invest_income",  # 按权益法核算的长期股权投资收益（从脚注拆分）
    "fin_exp",            # 财务费用（仅供参考，不参与计算）
    "operate_profit",     # 营业利润
    "n_income",           # 净利润
]

# 资产负债表所需字段
BS_FIELDS = [
    "total_hldr_eqy_inc_min_int",  # 所有者权益合计（含少数股东权益）
    "total_hldr_eqy_exc_min_int",  # 归属母公司股东权益
    "st_borr",                     # 短期借款
    "lt_borr",                     # 长期借款
    "bond_payable",                # 应付债券
    "notes_payable",               # 应付票据
    "lease_liab",                  # 租赁负债
    "trading_fl",                  # 交易性金融负债
    "deriv_liab",                  # 衍生金融负债
    "money_cap",                   # 货币资金
    "trad_asset",                  # 交易性金融资产
    "oth_eq_invest",               # 其他权益工具投资（API字段名，非 oth_eqt_tools）
    "oth_illiq_fin_assets",        # 其他非流动金融资产（API字段名，非 oth_fncble_assets）
    "deriv_assets",                # 衍生金融资产
    "time_deposits",               # 定期存款
    "loanto_oth_bank_fi",          # 发放贷款及垫款
    "debt_invest",                 # 债券投资
    "goodwill",                    # 商誉
    "lt_eqt_invest",               # 长期股权投资
    "intang_assets",               # 无形资产
    "fix_assets",                  # 固定资产
    "cipo",                        # 在建工程
    "right_use_asset",             # 使用权资产
    "invest_real_estate",          # 投资性房地产（非经营资产，需剔除）
    "nca_within_1y",               # 一年内到期的非流动资产（退出经营循环，全额剔除）
    "oth_cur_assets",              # 其他流动资产（可能含金融产品）
    "oth_nca",                     # 其他非流动资产（可能含金融产品）
    "non_cur_liab_due_1y",         # 一年内到期的非流动负债
    "receiv_financing",            # 应收款项融资（银行承兑汇票/保理等，类金融资产，需剔除）
]


def call_api(api_name: str, params: dict, fields: list = None) -> dict:
    """调用 finance-data API"""
    body = {"api_name": api_name, "params": params}
    if fields:
        body["fields"] = ",".join(fields)
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read().decode("utf-8"))
        if result.get("code") != 0:
            raise Exception(f"API error: {result.get('msg', 'unknown')}")
        return result["data"]
    except Exception as e:
        raise RuntimeError(f"API call failed ({api_name}): {e}")


def fetch_annual_data(ts_code: str, year: int, api_name: str, fields: list) -> dict:
    """获取某年12月31日的年报数据，返回字段名→值的字典"""
    period = f"{year}1231"
    data = call_api(api_name, {"ts_code": ts_code, "period": period, "report_type": "1"}, fields)
    if not data["items"]:
        return {}
    fields_list = data["fields"]
    values = data["items"][0]
    return {f: v for f, v in zip(fields_list, values)}


def get_val(d: dict, field: str, default=0.0) -> float:
    """安全取值，null/missing 返回 default"""
    v = d.get(field)
    if v is None:
        return default
    return float(v)


def parse_years(years_spec: str) -> list:
    """解析年份参数，支持 '2021-2024' 或 '2021 2022 2023 2024'"""
    if "-" in years_spec:
        parts = years_spec.split("-")
        start, end = int(parts[0]), int(parts[1])
        return list(range(start, end + 1))
    else:
        return [int(y) for y in years_spec.split()]


def calc_roic(ts_code: str, year: int) -> dict:
    """计算某年的核心ROIC，返回所有中间数据"""
    # 获取利润表
    inc = fetch_annual_data(ts_code, year, "income", INCOME_FIELDS)
    if not inc:
        return None

    # 获取资产负债表
    bs = fetch_annual_data(ts_code, year, "balancesheet", BS_FIELDS)
    if not bs:
        return None

    # ===== 提取利润表数据 =====
    revenue = get_val(inc, "revenue")
    oper_cost = get_val(inc, "oper_cost")
    tax_surchg = get_val(inc, "biz_tax_surchg")
    sell_exp = get_val(inc, "sell_exp")
    admin_exp = get_val(inc, "admin_exp")
    rd_exp = get_val(inc, "rd_exp")
    total_profit = get_val(inc, "total_profit")
    income_tax = get_val(inc, "income_tax")
    invest_income = get_val(inc, "invest_income")
    ass_invest_income = get_val(inc, "ass_invest_income")  # 权益法投资收益
    fin_exp = get_val(inc, "fin_exp")

    # ===== 实际税率 =====
    if total_profit > 0:
        tax_rate = income_tax / total_profit
    else:
        tax_rate = 0.0  # 利润总额为负时不计算税率

    # ===== NOPAT =====
    core_op_profit_bt = revenue - oper_cost - tax_surchg - sell_exp - admin_exp - rd_exp
    core_op_profit_at = core_op_profit_bt * (1 - tax_rate)

    # 注意：权益法投资收益从API获取（ass_invest_income），如果API返回0则需⚠️提醒
    equity_method_income = ass_invest_income
    acquisition_amort = 0.0     # ⚠️ 需手动补充

    nopat = core_op_profit_at + equity_method_income * (1 - tax_rate) + acquisition_amort * (1 - tax_rate)

    # ===== 资产负债表数据 =====
    total_equity = get_val(bs, "total_hldr_eqy_inc_min_int")  # 所有者权益合计
    st_borr = get_val(bs, "st_borr")                         # 短期借款
    lt_loan = get_val(bs, "lt_borr")                                # 长期借款
    bonds_pay = get_val(bs, "bond_payable")                         # 应付债券
    notes_pay = get_val(bs, "notes_payable")                  # 应付票据
    lease_liab = get_val(bs, "lease_liab")                    # 租赁负债
    ncl_due_1y = get_val(bs, "non_cur_liab_due_1y")           # 一年内到期非流动负债
    trading_fl = get_val(bs, "trading_fl")                    # 交易性金融负债
    deriv_liab = get_val(bs, "deriv_liab")                    # 衍生金融负债

    money_cap = get_val(bs, "money_cap")                      # 货币资金
    trad_asset = get_val(bs, "trad_asset")                    # 交易性金融资产
    oth_eq_invest = get_val(bs, "oth_eq_invest")              # 其他权益工具投资
    oth_illiq_fin = get_val(bs, "oth_illiq_fin_assets")       # 其他非流动金融资产
    deriv_assets = get_val(bs, "deriv_assets")                # 衍生金融资产
    time_deposits = get_val(bs, "time_deposits")              # 定期存款（单独列示的）
    goodwill = get_val(bs, "goodwill")                        # 商誉
    lt_eqt_inv = get_val(bs, "lt_eqt_invest")                 # 长期股权投资
    oth_cur_assets = get_val(bs, "oth_cur_assets")            # 其他流动资产
    oth_nca = get_val(bs, "oth_nca")                          # 其他非流动资产
    receiv_financing = get_val(bs, "receiv_financing")        # 应收款项融资（类金融资产）
    invest_real_estate = get_val(bs, "invest_real_estate")    # 投资性房地产
    nca_within_1y = get_val(bs, "nca_within_1y")              # 一年内到期的非流动资产
    loan_adv = get_val(bs, "loanto_oth_bank_fi")              # 发放贷款及垫款
    debt_inv = get_val(bs, "debt_invest")                      # 债券投资

    # ===== 有息负债 =====
    interest_debt = st_borr + ncl_due_1y + lt_loan + bonds_pay + notes_pay + lease_liab + trading_fl + deriv_liab

    # ===== 金融资产（自动剔除） =====
    financial_assets = (money_cap + trad_asset + oth_eq_invest + oth_illiq_fin
                        + deriv_assets + time_deposits + receiv_financing
                        + nca_within_1y + loan_adv + debt_inv)  # 一年内到期非流动资产，退出经营循环，全额剔除；发放贷款及垫款，金融资产；债券投资，金融资产

    # ===== 非经营资产（自动剔除） =====
    non_op_assets = goodwill + invest_real_estate  # 商誉 + 投资性房地产自动剔除

    # 以下两项需要人工判断，脚本设为0并标记
    financial_lt_invest = 0.0       # ⚠️ 长投中基金/财务部分需手动补充
    acquisition_intang = 0.0        # ⚠️ 收购无形资产账面值需手动补充
    hidden_fin_assets = 0.0         # ⚠️ 其他资产中隐藏金融资产需手动补充

    non_op_assets += financial_lt_invest + acquisition_intang + hidden_fin_assets

    # ===== 投入资本 =====
    invested_capital = total_equity + interest_debt - financial_assets - non_op_assets

    # ===== ROIC =====
    roic = nopat / invested_capital if invested_capital > 0 else 0.0

    # 汇总返回
    return {
        "year": year,
        # 利润表原始数据
        "revenue": revenue,
        "oper_cost": oper_cost,
        "tax_surchg": tax_surchg,
        "sell_exp": sell_exp,
        "admin_exp": admin_exp,
        "rd_exp": rd_exp,
        "total_profit": total_profit,
        "income_tax": income_tax,
        "invest_income": invest_income,
        "ass_invest_income": ass_invest_income,
        "fin_exp": fin_exp,
        # 税率
        "tax_rate": tax_rate,
        # NOPAT
        "core_op_profit_bt": core_op_profit_bt,
        "core_op_profit_at": core_op_profit_at,
        "equity_method_income": equity_method_income,
        "acquisition_amort": acquisition_amort,
        "nopat": nopat,
        # 资产负债表
        "total_equity": total_equity,
        "st_borr": st_borr,
        "lt_loan": lt_loan,
        "bonds_pay": bonds_pay,
        "notes_pay": notes_pay,
        "lease_liab": lease_liab,
        "ncl_due_1y": ncl_due_1y,
        "trading_fl": trading_fl,
        "deriv_liab": deriv_liab,
        "interest_debt": interest_debt,
        "money_cap": money_cap,
        "trad_asset": trad_asset,
        "oth_eq_invest": oth_eq_invest,
        "oth_illiq_fin": oth_illiq_fin,
        "deriv_assets": deriv_assets,
        "time_deposits": time_deposits,
        "loan_adv": loan_adv,
        "debt_inv": debt_inv,
        "financial_assets": financial_assets,
        "goodwill": goodwill,
        "lt_eqt_inv": lt_eqt_inv,
        "oth_cur_assets": oth_cur_assets,
        "oth_nca": oth_nca,
        "receiv_financing": receiv_financing,
        "invest_real_estate": invest_real_estate,
        "nca_within_1y": nca_within_1y,
        "non_op_assets": non_op_assets,
        "invested_capital": invested_capital,
        "roic": roic,
        # 需人工检查标记
        "warnings": [],
    }


def fmt(val: float, unit: str = "亿元") -> str:
    """格式化金额，亿元"""
    v = val / 1e8
    if v == 0:
        return f"0.00"
    return f"{v:,.2f}"


def gen_report(ts_code: str, results: list) -> str:
    """生成 Markdown 分析报告"""
    lines = []
    company = ts_code.split(".")[0]
    lines.append(f"# {company} 核心 ROIC 穿透分析\n")
    lines.append(f"**股票代码：** {ts_code}  ")
    lines.append(f"**分析年度：** {results[0]['year']}-{results[-1]['year']}  ")
    lines.append(f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # ===== 多年 ROIC 汇总 =====
    lines.append("## 核心结果汇总\n")
    lines.append("| 年度 | NOPAT（亿元）| 投入资本（亿元）| 核心 ROIC |")
    lines.append("|------|------------|----------------|-----------|")
    for r in results:
        lines.append(f"| {r['year']} | {fmt(r['nopat'])} | {fmt(r['invested_capital'])} | **{r['roic']*100:.2f}%** |")
    lines.append("")

    # ===== ⚠️ 人工检查提醒 =====
    has_warnings = False
    for r in results:
        if r["lt_eqt_inv"] > 0:
            r["warnings"].append(f"存在长期股权投资 {fmt(r['lt_eqt_inv'])} 亿元，需拆分战略/财务部分")
            has_warnings = True
        if r["oth_cur_assets"] > 2e9:  # >2亿才提醒
            r["warnings"].append(f"其他流动资产 {fmt(r['oth_cur_assets'])} 亿元（>2亿），需检查是否含金融产品（结构性存款、理财、收益凭证等）")
            has_warnings = True
        if r["oth_nca"] > 2e9:  # >2亿才提醒
            r["warnings"].append(f"其他非流动资产 {fmt(r['oth_nca'])} 亿元（>2亿），需检查是否含金融产品（定期存款等）")
            has_warnings = True
        if r["invest_income"] > 0:
            r["warnings"].append(f"存在投资收益 {fmt(r['invest_income'])} 亿元，权益法部分已从API获取（{fmt(r.get('ass_invest_income',0))}亿），需确认是否准确")
            has_warnings = True
        if r["goodwill"] > 0:
            r["warnings"].append(f"存在商誉 {fmt(r['goodwill'])} 亿元（已自动剔除）")
            has_warnings = True
        if r.get("ass_invest_income", 0) > 0:
            r["warnings"].append(f"权益法投资收益 {fmt(r.get('ass_invest_income',0))} 亿元（已从API获取并加入分子）")
            has_warnings = True

    if has_warnings:
        lines.append("## ⚠️ 需人工补充/确认的项目\n")
        lines.append("以下项目 API 无法自动获取，需要查阅年报脚注后手动补充：\n")
        for r in results:
            if r["warnings"]:
                lines.append(f"### {r['year']} 年")
                for w in r["warnings"]:
                    lines.append(f"- {w}")
                lines.append("")

    # ===== 逐年明细 =====
    for r in results:
        y = r["year"]
        lines.append("---\n")
        lines.append(f"## {y} 年度明细\n")

        # 税率
        lines.append("### 实际税率")
        lines.append(f"- 所得税费用：{fmt(r['income_tax'])} 亿元")
        lines.append(f"- 利润总额：{fmt(r['total_profit'])} 亿元")
        if r["total_profit"] > 0:
            lines.append(f"- **实际税率：{r['tax_rate']*100:.2f}%**\n")
        else:
            lines.append("- **实际税率：不适用（利润总额为负）**\n")

        # NOPAT
        lines.append("### NOPAT 计算（分子）")
        lines.append("| 项目 | 金额（亿元）|")
        lines.append("|------|------------|")
        lines.append(f"| 营业收入 | {fmt(r['revenue'])} |")
        lines.append(f"| (-) 营业成本 | {fmt(r['oper_cost'])} |")
        lines.append(f"| (-) 税金及附加 | {fmt(r['tax_surchg'])} |")
        lines.append(f"| (-) 销售费用 | {fmt(r['sell_exp'])} |")
        lines.append(f"| (-) 管理费用 | {fmt(r['admin_exp'])} |")
        lines.append(f"| (-) 研发费用 | {fmt(r['rd_exp'])} |")
        lines.append(f"| = 核心经营利润（税前）| {fmt(r['core_op_profit_bt'])} |")
        lines.append(f"| × (1 - {r['tax_rate']*100:.2f}%) |")
        lines.append(f"| = 核心经营利润（税后）| {fmt(r['core_op_profit_at'])} |")
        if r["equity_method_income"] != 0:
            lines.append(f"| (+) 权益法投资收益（税后）| {fmt(r['equity_method_income']*(1-r['tax_rate']))} | API自动获取 |")
        else:
            lines.append(f"| (+) 权益法投资收益（税后）| 0.00 | API返回0，需⚠️确认 |")
        if r["acquisition_amort"] != 0:
            lines.append(f"| (+) 收购无形资产摊销（税后）| {fmt(r['acquisition_amort']*(1-r['tax_rate']))} |")
        else:
            lines.append(f"| (+) 收购无形资产摊销（税后）| 0.00 ⚠️ 需确认 |")
        lines.append(f"| **= NOPAT** | **{fmt(r['nopat'])}** |\n")

        # 投入资本
        lines.append("### 投入资本计算（分母）")
        lines.append("| 项目 | 金额（亿元）| 说明 |")
        lines.append("|------|------------|------|")
        lines.append(f"| 所有者权益合计 | {fmt(r['total_equity'])} | 含少数股东权益 |")
        lines.append(f"| (+) 有息负债合计 | {fmt(r['interest_debt'])} | 见下表 |")
        lines.append(f"| (-) 金融资产合计 | ({fmt(r['financial_assets'])}) | 见下表 |")
        lines.append(f"| (-) 非经营资产合计 | ({fmt(r['non_op_assets'])}) | 见下表 |")
        lines.append(f"| **= 投入资本** | **{fmt(r['invested_capital'])}** |\n")

        # 有息负债明细
        lines.append("**有息负债明细：**\n")
        lines.append("| 项目 | 金额（亿元）|")
        lines.append("|------|------------|")
        lines.append(f"| 短期借款 | {fmt(r['st_borr'])} |")
        lines.append(f"| 一年内到期非流动负债 | {fmt(r['ncl_due_1y'])} |")
        lines.append(f"| 长期借款 | {fmt(r['lt_loan'])} |")
        lines.append(f"| 应付债券 | {fmt(r['bonds_pay'])} |")
        lines.append(f"| 应付票据 | {fmt(r['notes_pay'])} |")
        lines.append(f"| 租赁负债 | {fmt(r['lease_liab'])} |")
        lines.append(f"| 交易性金融负债 | {fmt(r['trading_fl'])} |")
        lines.append(f"| 衍生金融负债 | {fmt(r['deriv_liab'])} |")
        lines.append(f"| **有息负债合计** | **{fmt(r['interest_debt'])}** |\n")

        # 金融资产明细
        lines.append("**金融资产明细（已剔除）：**\n")
        lines.append("| 项目 | 金额（亿元）|")
        lines.append("|------|------------|")
        lines.append(f"| 货币资金 | {fmt(r['money_cap'])} |")
        lines.append(f"| 交易性金融资产 | {fmt(r['trad_asset'])} |")
        lines.append(f"| 其他权益工具投资 | {fmt(r['oth_eq_invest'])} |")
        lines.append(f"| 其他非流动金融资产 | {fmt(r['oth_illiq_fin'])} |")
        lines.append(f"| 衍生金融资产 | {fmt(r['deriv_assets'])} |")
        lines.append(f"| 定期存款（单独列示）| {fmt(r['time_deposits'])} |")
        lines.append(f"| 应收款项融资 | {fmt(r['receiv_financing'])} | 银行承兑汇票/保理，类金融资产 |")
        lines.append(f"| 一年内到期非流动资产 | {fmt(r['nca_within_1y'])} | 退出经营循环，自动剔除 |")
        lines.append(f"| 发放贷款及垫款 | {fmt(r['loan_adv'])} | 金融资产，自动剔除 |")
        if r.get("debt_inv", 0) > 0:
            lines.append(f"| 债券投资 | {fmt(r['debt_inv'])} | 金融资产，自动剔除 |")
        if r.get("hidden_fin_assets", 0) > 0:
            lines.append(f"| 其他隐藏金融资产 | {fmt(r['hidden_fin_assets'])} | ⚠️ 需补充 |")
        lines.append(f"| **金融资产合计** | **{fmt(r['financial_assets'])}** |\n")

        # 非经营资产明细
        lines.append("**非经营资产明细（已剔除）：**\n")
        lines.append("| 项目 | 金额（亿元）|")
        lines.append("|------|------------|")
        lines.append(f"| 商誉 | {fmt(r['goodwill'])} | {'自动剔除' if r['goodwill']>0 else '无'} |")
        lines.append(f"| 投资性房地产 | {fmt(r['invest_real_estate'])} | 非核心经营资产，自动剔除 |")
        if r["lt_eqt_inv"] > 0:
            lines.append(f"| 长期股权投资（财务部分）| 0.00 | ⚠️ 总额{fmt(r['lt_eqt_inv'])}亿，需拆分 |")
        lines.append(f"| **非经营资产合计** | **{fmt(r['non_op_assets'])}** |\n")

        # ROIC 结果
        lines.append(f"### ROIC 结果\n")
        lines.append(f"**核心 ROIC = {fmt(r['nopat'])} ÷ {fmt(r['invested_capital'])} = {r['roic']*100:.2f}%**\n")

    # ===== 趋势分析 =====
    if len(results) > 1:
        lines.append("---\n")
        lines.append("## 趋势分析\n")

        first, last = results[0], results[-1]
        nopat_chg = (last["nopat"] - first["nopat"]) / abs(first["nopat"]) * 100 if first["nopat"] != 0 else 0
        cap_chg = (last["invested_capital"] - first["invested_capital"]) / abs(first["invested_capital"]) * 100 if first["invested_capital"] != 0 else 0

        lines.append(f"| 指标 | {first['year']}年 | {last['year']}年 | 变化幅度 |")
        lines.append("|------|--------|--------|----------|")
        lines.append(f"| NOPAT | {fmt(first['nopat'])} | {fmt(last['nopat'])} | {nopat_chg:+.1f}% |")
        lines.append(f"| 投入资本 | {fmt(first['invested_capital'])} | {fmt(last['invested_capital'])} | {cap_chg:+.1f}% |")
        lines.append(f"| ROIC | {first['roic']*100:.2f}% | {last['roic']*100:.2f}% | {(last['roic']-first['roic'])*100:+.2f}pp |")
        lines.append("")

        if last["roic"] > first["roic"]:
            lines.append(f"ROIC 从 {first['roic']*100:.2f}% 提升至 {last['roic']*100:.2f}%，盈利能力改善。")
        else:
            lines.append(f"ROIC 从 {first['roic']*100:.2f}% 下降至 {last['roic']*100:.2f}%，盈利能力承压。")

        if abs(nopat_chg) > abs(cap_chg):
            lines.append(f"主要驱动：NOPAT 变化（{nopat_chg:+.1f}%）幅度大于投入资本变化（{cap_chg:+.1f}%）。")
        else:
            lines.append(f"主要驱动：投入资本变化（{cap_chg:+.1f}%）幅度大于 NOPAT 变化（{nopat_chg:+.1f}%）。")

    lines.append("\n---\n*报告由 ROIC V2.0 穿透模式工具自动生成，⚠️ 标记项目需人工查阅年报脚注补充。*")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("用法: python roic_calc.py <股票代码> <年份范围>")
        print("示例: python roic_calc.py 600426.SH 2021-2024")
        print("      python roic_calc.py 03690.HK 2021 2022 2023 2024")
        sys.exit(1)

    ts_code = sys.argv[1]
    years_spec = " ".join(sys.argv[2:])
    years = parse_years(years_spec)

    print(f"[ROIC] 计算 {ts_code} {years[0]}-{years[-1]} 年核心 ROIC...")
    print()

    results = []
    for y in years:
        print(f"  获取 {y} 年年报数据...", end=" ", flush=True)
        try:
            r = calc_roic(ts_code, y)
            if r is None:
                print(f"  [!] {y} 年年报尚未发布，跳过")
                continue
            results.append(r)
            print(f"  [OK] ROIC = {r['roic']*100:.2f}%")
        except Exception as e:
            print(f"  [FAIL] {e}")

    if not results:
        print(f"\n[FAIL] 未获取到任何年份数据。请检查股票代码和年份范围。")
        sys.exit(1)

    # 生成报告
    report = gen_report(ts_code, results)

    # 保存
    import os
    company = ts_code.split(".")[0]
    filename = f"{company}_ROIC穿透分析_{results[0]['year']}-{results[-1]['year']}.md"
    workspace = os.environ.get('OPENCLAW_WORKSPACE', os.path.expanduser('~/.openclaw/workspace'))
    output_dir = os.path.join(workspace, 'output', 'roic')
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n[DONE] 报告已保存: {filepath}")
    print(f"   共 {len(results)} 个年度数据")


if __name__ == "__main__":
    main()
