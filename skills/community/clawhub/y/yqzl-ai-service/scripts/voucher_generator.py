#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云启智联AI服务 — 智能记账凭证生成器

将 OCR 解析结果（银行回单/对账单/发票）自动转换为记账凭证，
包含科目匹配置信度评分和人工复核建议。

适用于小微企业（小规模纳税人），依据《小企业会计准则》精简版科目体系。
"""

import argparse
import json
import os
import sys
from datetime import datetime, date as date_type
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from enum import Enum
from typing import List, Optional, Dict, Tuple
from collections import Counter

# Windows 终端编码修正（避免 GBK 无法输出 ¥ 等字符）
if sys.platform == 'win32':
    import io
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'encoding') and stream.encoding and stream.encoding.lower() not in ('utf-8', 'utf8'):
            try:
                stream.reconfigure(encoding='utf-8', errors='replace')
            except (AttributeError, Exception):
                pass


# ============================================================
# 1. 科目体系（小企业会计准则 · 精简版）
# ============================================================

class AccountCategory(str, Enum):
    """一级科目分类"""
    ASSET = "资产"
    LIABILITY = "负债"
    EQUITY = "所有者权益"
    REVENUE = "收入"
    EXPENSE = "费用"
    COST = "成本"


# 常用科目代码表
ACCOUNT_MAP = {
    # ---- 资产类 ----
    "1002":   ("银行存款",              AccountCategory.ASSET),
    "1122":   ("应收账款",              AccountCategory.ASSET),
    "1405":   ("库存商品",              AccountCategory.ASSET),
    "1601":   ("固定资产",              AccountCategory.ASSET),
    "1602":   ("累计折旧",              AccountCategory.ASSET),
    # ---- 负债类 ----
    "2202":   ("应付账款",              AccountCategory.LIABILITY),
    "2221":   ("应交税费",              AccountCategory.LIABILITY),
    "2221.01":("应交税费-应交增值税",    AccountCategory.LIABILITY),
    "2241":   ("其他应付款",            AccountCategory.LIABILITY),
    "2241.01":("其他应付款-股东垫款",    AccountCategory.LIABILITY),
    # ---- 所有者权益 ----
    "4001":   ("实收资本",              AccountCategory.EQUITY),
    "4103":   ("本年利润",              AccountCategory.EQUITY),
    # ---- 收入类 ----
    "5001":   ("主营业务收入",          AccountCategory.REVENUE),
    "5051":   ("其他业务收入",          AccountCategory.REVENUE),
    # ---- 成本类 ----
    "5401":   ("主营业务成本",          AccountCategory.COST),
    # ---- 费用类 ----
    "5602.01":("管理费用-办公费",       AccountCategory.EXPENSE),
    "5602.02":("管理费用-房租",         AccountCategory.EXPENSE),
    "5602.03":("管理费用-工资",         AccountCategory.EXPENSE),
    "5602.04":("管理费用-差旅费",       AccountCategory.EXPENSE),
    "5602.05":("管理费用-业务招待费",    AccountCategory.EXPENSE),
    "5602.06":("管理费用-职工教育经费",  AccountCategory.EXPENSE),
    "5602.07":("管理费用-社保费",       AccountCategory.EXPENSE),
    "5602.08":("管理费用-折旧费",       AccountCategory.EXPENSE),
    "5602.09":("管理费用-水电费",       AccountCategory.EXPENSE),
    "5602.10":("管理费用-通讯费",       AccountCategory.EXPENSE),
    "5602.11":("管理费用-车辆费",       AccountCategory.EXPENSE),
    "5603.01":("财务费用-手续费",       AccountCategory.EXPENSE),
    "5603.02":("财务费用-利息收入",     AccountCategory.EXPENSE),
    "5601.01":("销售费用-广告宣传费",    AccountCategory.EXPENSE),
    "5601.02":("销售费用-运费",         AccountCategory.EXPENSE),
    # ---- 税金及附加 ----
    "5403":   ("税金及附加",            AccountCategory.COST),
}


# ============================================================
# 2. 科目匹配规则
# ============================================================

# 交易摘要 → 默认科目编码（按优先级排序）
TRANSACTION_TYPE_RULES = [
    (["工资", "薪资", "奖金", "绩效", "津贴", "补贴", "劳务"],
     "5602.03", "工资/劳务支出"),
    (["社保", "公积金", "五险一金", "养老", "医疗", "失业"],
     "5602.07", "社保/公积金支出"),
    (["房租", "租金", "物业", "办公场所"],
     "5602.02", "房租/物业支出"),
    (["水电", "电费", "水费"],
     "5602.09", "水电费支出"),
    (["话费", "通讯", "电话费", "宽带"],
     "5602.10", "通讯费支出"),
    (["差旅", "出差", "机票", "火车票", "酒店", "住宿", "打车",
      "高铁", "网约车", "出租车"],
     "5602.04", "差旅费支出"),
    (["招待", "餐饮", "聚餐", "宴请", "礼品", "茶叶", "酒"],
     "5602.05", "业务招待费支出"),
    (["培训", "教育", "书籍", "课程", "学习"],
     "5602.06", "职工教育经费支出"),
    (["广告", "推广", "营销", "宣传", "投流", "竞价", "SEO"],
     "5601.01", "广告宣传费支出"),
    (["运费", "快递", "物流", "配送", "邮费"],
     "5601.02", "运费支出"),
    (["手续费", "银行手续费", "转账费", "汇款费", "工本费",
      "年费", "网银", "账户管理"],
     "5603.01", "银行手续费支出"),
    (["利息", "存款利息"],
     "5603.02", "利息收支"),
    (["销售", "商品款", "产品款"],
     "5001", "销售/货款收入"),
    (["税", "税款", "增值税", "所得税", "附加税", "印花税",
      "城建税", "教育费附加"],
     "5403", "税费缴纳"),
    (["投资", "入股", "增资", "注册资本"],
     "4001", "投资/入股"),
    (["借款", "贷款", "还款"],
     "2241", "借款/还款"),

    (["结息", "批量结息", "利息收入"],
     "5603.02", "利息收入"),

    (["批量扣费", "扣费", "银行扣费", "服务费"],
     "5603.01", "银行手续费/扣费"),

    (["保险", "财产保险", "车险"],
     "5602.11", "保险费用"),
]

# 关键词 → 科目 模糊匹配规则 (关键词列表, 科目编码, 规则权重)
ACCOUNT_KEYWORD_RULES = [
    (["电脑", "笔记本", "手机", "配件", "硬件", "设备", "打印机",
      "显示器", "键盘", "鼠标", "服务器", "路由器", "交换机",
      "商品", "货物", "产品", "进货", "采购"],
     "1405", 1.0),

    (["办公", "文具", "纸张", "打印", "耗材", "软件", "云服务",
      "域名", "SaaS", "会员", "订阅"],
     "5602.01", 0.9),

    (["房租", "租金", "物业", "办公场所"],
     "5602.02", 1.0),

    (["工资", "薪资", "奖金", "绩效", "津贴", "补贴",
      "社保", "公积金", "五险一金"],
     "5602.03", 1.0),

    (["差旅", "出差", "机票", "火车票", "酒店", "住宿",
      "打车", "出租车", "网约车", "高铁"],
     "5602.04", 1.0),

    (["招待", "餐饮", "聚餐", "宴请", "礼品", "礼物",
      "茶叶", "酒"],
     "5602.05", 0.95),

    (["培训", "教育", "书籍", "图书", "课程", "学习"],
     "5602.06", 0.9),

    (["手续费", "银行手续费", "转账费", "汇款费", "工本费",
      "年费", "账户管理"],
     "5603.01", 1.0),

    (["利息", "存款利息"],
     "5603.02", 1.0),

    (["广告", "推广", "营销", "宣传", "抖音", "淘宝",
      "拼多多", "小红书", "直播", "投流", "竞价", "SEO"],
     "5601.01", 1.0),

    (["运费", "快递", "物流", "配送", "货运", "快递费", "邮费"],
     "5601.02", 1.0),

    (["固定资产", "车辆", "汽车", "厂房", "机器", "设备采购"],
     "1601", 0.95),

    (["油费", "加油", "车险", "车保险", "车辆保险", "过路费",
      "停车费", "加油费", "ETC"],
     "5602.11", 1.0),

    (["税", "税款", "增值税", "所得税", "附加税", "扣税",
      "税费扣缴", "公共缴费"],
     "2221", 0.8),

    (["城建税", "教育费附加", "地方教育附加", "印花税",
      "房产税", "城镇土地使用税"],
     "5403", 0.95),
]


class AccountMatchResult:
    """单个科目匹配结果"""

    def __init__(self, code, name, confidence, matched_keywords=None, reason=""):
        self.code = code
        self.name = name
        self.confidence = round(confidence, 2)
        self.matched_keywords = matched_keywords or []
        self.reason = reason

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "confidence": self.confidence,
            "matched_keywords": self.matched_keywords,
            "reason": self.reason,
        }


class AccountMatchingEngine:
    """
    科目模糊匹配引擎
    策略：关键词命中 + 金额启发式 + 交易类型规则
    """

    def __init__(self, business_type="商贸"):
        self.business_type = business_type
        self._rules = ACCOUNT_KEYWORD_RULES
        self._tx_rules = TRANSACTION_TYPE_RULES

    def match(self, description, amount=0, direction="debit", context=""):
        """
        匹配最佳会计科目

        :param description: 交易描述（摘要/品名/用途）
        :param amount: 交易金额
        :param direction: "debit"(借方/支出) 或 "credit"(贷方/收入)
        :param context: 额外上下文（对方户名、备注等）
        :return: List[AccountMatchResult] 按置信度降序
        """
        desc = str(description).strip()
        desc_lower = desc.lower()
        full_text = " ".join([desc, str(context)]).lower()
        candidates = []

        # --- 1. 交易类型规则（仅匹配描述文本，不含对方户名，避免误匹配） ---
        for keywords, code, tx_type in self._tx_rules:
            matched = self._match_keywords(desc_lower, keywords)
            if matched:
                info = ACCOUNT_MAP.get(code)
                if info:
                    name, _ = info
                    base = min(len(matched) * 0.25 + 0.55, 0.92)
                    candidates.append(AccountMatchResult(
                        code, name, base, matched,
                        f"交易类型规则匹配：{tx_type}"
                    ))

        # --- 2. 关键词模糊匹配（使用完整文本含对方户名） ---
        for keywords, code, weight in self._rules:
            matched = self._match_keywords(full_text, keywords)
            if matched:
                info = ACCOUNT_MAP.get(code)
                if info:
                    name, _ = info
                    base = min(len(matched) * 0.3, 0.7)
                    score = min(base * weight + 0.1, 0.95)
                    # 避免与规则1重复
                    if not any(c.code == code for c in candidates):
                        candidates.append(AccountMatchResult(
                            code, name, score, matched,
                            f"关键词匹配（权重 {weight}）"
                        ))

        # --- 3. 金额启发式调整 ---
        amount_f = float(amount) if amount else 0
        if amount_f >= 5000 and direction == "debit":
            for c in candidates:
                if c.code == "1601":
                    c.confidence = min(c.confidence + 0.1, 0.98)
                    c.reason += "；大额交易启发式：可能为固定资产"
                elif c.code == "1405":
                    c.confidence = max(c.confidence - 0.05, 0.3)

        if amount_f < 200 and direction == "debit":
            for c in candidates:
                if c.code in ("5602.01", "5602.04"):
                    c.confidence = min(c.confidence + 0.05, 0.95)

        # --- 4. 餐饮特殊规则 ---
        food_kw = ["餐", "饮", "吃", "饭", "火锅", "烧烤", "咖啡", "奶茶"]
        if self._match_keywords(full_text, food_kw):
            has_travel = context and any(
                k in str(context) for k in ["出差", "酒店", "住宿"]
            )
            for c in candidates:
                if c.code == "5602.05" and not has_travel:
                    c.confidence = min(c.confidence + 0.15, 0.98)
                elif c.code == "5602.04" and has_travel:
                    c.confidence = min(c.confidence + 0.1, 0.95)

        # --- 5. 去重 + 排序 ---
        seen = set()
        unique = []
        for c in sorted(candidates, key=lambda x: -x.confidence):
            if c.code not in seen:
                seen.add(c.code)
                unique.append(c)

        return unique

    def _match_keywords(self, text, keywords):
        """返回 text 中命中的关键词列表"""
        text_lower = text.lower()
        return [kw for kw in keywords if kw.lower() in text_lower]


# ============================================================
# 3. 凭证数据模型
# ============================================================

class VoucherStatus(str, Enum):
    DRAFT = "草稿"
    PENDING = "待审核"
    APPROVED = "已审核"
    POSTED = "已入账"
    REJECTED = "已驳回"


class JournalEntry:
    """单条借贷分录"""

    def __init__(self, account_code, account_name, debit=0, credit=0, remark=""):
        self.account_code = account_code
        self.account_name = account_name
        self.debit = Decimal(str(debit)).quantize(Decimal("0.01"), ROUND_HALF_UP) if debit else Decimal("0.00")
        self.credit = Decimal(str(credit)).quantize(Decimal("0.01"), ROUND_HALF_UP) if credit else Decimal("0.00")
        self.remark = remark or ""

    @property
    def direction(self):
        return "debit" if self.debit > 0 else "credit"

    @property
    def amount(self):
        return self.debit if self.debit > 0 else self.credit

    def to_dict(self):
        return {
            "account_code": self.account_code,
            "account_name": self.account_name,
            "direction": self.direction,
            "amount": float(self.amount),
            "debit": float(self.debit),
            "credit": float(self.credit),
            "remark": self.remark,
        }


class Voucher:
    """
    记账凭证

    包含多条借贷分录，自动校验借贷平衡。
    """

    def __init__(self, date_str, description, entries, source_type="other",
                 source_no=None, confidence=None, status=VoucherStatus.DRAFT):
        self.date = date_str
        self.description = description
        self.entries = entries
        self.source_type = source_type
        self.source_no = source_no
        self.confidence = confidence
        self.status = status
        self.review_suggestion = None  # 由 VoucherGenerator 设置

    @property
    def total_debit(self):
        return sum((e.debit for e in self.entries), Decimal("0"))

    @property
    def total_credit(self):
        return sum((e.credit for e in self.entries), Decimal("0"))

    @property
    def is_balanced(self):
        return self.total_debit == self.total_credit

    def to_display_lines(self):
        """生成人类可读的凭证文本"""
        lines = [
            f"凭证日期：{self.date}  摘要：{self.description}",
            f"{'科目':<30} {'借方':>12} {'贷方':>12}",
            "-" * 56,
        ]
        for e in self.entries:
            d = f"{float(e.debit):>12,.2f}" if e.debit > 0 else ""
            c = f"{float(e.credit):>12,.2f}" if e.credit > 0 else ""
            lines.append(f"{e.account_name:<30} {d:<12} {c:<12}")
        lines.append("-" * 56)
        lines.append(
            f"{'合计':<30} {float(self.total_debit):>12,.2f} {float(self.total_credit):>12,.2f}"
        )
        if self.confidence is not None:
            lines.append(f"科目匹配置信度：{self.confidence * 100:.0f}%")
        lines.append(f"凭证状态：{self.status.value}")
        return lines

    def to_dict(self):
        """导出为结构化字典"""
        result = {
            "date": self.date,
            "description": self.description,
            "source_type": self.source_type,
            "source_no": self.source_no,
            "status": self.status.value,
            "confidence": self.confidence,
            "entries": [e.to_dict() for e in self.entries],
            "total_debit": float(self.total_debit),
            "total_credit": float(self.total_credit),
            "is_balanced": self.is_balanced,
        }
        if self.review_suggestion:
            result["review_suggestion"] = self.review_suggestion
        return result

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class VoucherBundle:
    """凭证汇总（多张凭证时返回）"""

    def __init__(self, vouchers, source_type=""):
        self.vouchers = vouchers
        self.source_type = source_type

    @property
    def total_debit(self):
        return sum((v.total_debit for v in self.vouchers), Decimal("0"))

    @property
    def total_credit(self):
        return sum((v.total_credit for v in self.vouchers), Decimal("0"))

    def to_dict(self):
        return {
            "source_type": self.source_type,
            "voucher_count": len(self.vouchers),
            "total_debit": float(self.total_debit),
            "total_credit": float(self.total_credit),
            "vouchers": [v.to_dict() for v in self.vouchers],
        }

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 4. 复核建议
# ============================================================

# 复核级别
REVIEW_HIGH = "high"       # 必须人工复核
REVIEW_MEDIUM = "medium"   # 建议复核
REVIEW_LOW = "low"         # 可信度高

# 常见复核标记 → 人类可读建议
FLAG_SUGGESTIONS = {
    "high_value": "大额交易（金额 ≥ ¥10,000），请核实交易真实性和凭证附件完整性",
    "low_confidence": "科目匹配置信度较低，请确认科目选择是否正确",
    "category_ambiguous": "交易描述不够明确，可能存在多种科目归属，建议人工确认",
    "missing_info": "关键信息缺失（如摘要、金额、对方户名），需人工补充判断",
    "tax_related": "涉税交易，请确认税率和税额计算是否正确",
    "fixed_asset_check": "大额支出可能属于固定资产而非费用，请判断是否需要资本化处理",
    "intercompany": "关联交易，请确认交易性质和往来方向是否正确",
    "unusual_amount": "金额异常（为零或负数），请核实原始单据",
    "cross_period": "交易日期可能跨期，请确认归属会计期间",
}


# ============================================================
# 5. 凭证生成器（核心）
# ============================================================

class VoucherGenerator:
    """
    将 OCR 解析结果转换为记账凭证

    支持三种输入类型：
    - receipt:  银行回单解析结果
    - statement: 银行对账单解析结果
    - invoice:  发票解析结果
    """

    def __init__(self, business_type="商贸", vat_rate=0.01,
                 income_tax_rate=0.03):
        """
        :param business_type: "商贸" 或 "服务"
        :param vat_rate: 增值税税率（小规模纳税人通常 1% 或 3%）
        :param income_tax_rate: 所得税税率（用于参考）
        """
        self.business_type = business_type
        self.vat_rate = Decimal(str(vat_rate))
        self.income_tax_rate = Decimal(str(income_tax_rate))
        self.engine = AccountMatchingEngine(business_type)

    # ----------------------------------------------------------
    # 公共入口
    # ----------------------------------------------------------

    def process(self, data, source_type, **kwargs):
        """
        统一入口：处理解析结果，返回凭证

        :param data: OCR 解析返回的 data 字段（list 或 dict）
        :param source_type: "receipt" | "statement" | "invoice"
        :return: Voucher 或 VoucherBundle
        """
        if source_type == "receipt":
            return self._process_receipts(data, **kwargs)
        elif source_type == "statement":
            return self._process_statements(data, **kwargs)
        elif source_type == "invoice":
            return self._process_invoices(data, **kwargs)
        else:
            raise ValueError(f"不支持的来源类型: {source_type}")

    # ----------------------------------------------------------
    # 银行回单处理
    # ----------------------------------------------------------

    def _process_receipts(self, data, **kwargs):
        """处理银行回单解析结果"""
        records = []
        if isinstance(data, list):
            for page in data:
                if not isinstance(page, dict):
                    continue
                page_data = page.get("page_data", [])
                if not isinstance(page_data, list):
                    continue
                page_company = page.get("companyName", "")
                page_account = page.get("companyAccount", "")
                for item in page_data:
                    if isinstance(item, dict):
                        record = dict(item)
                        record["_companyName"] = (
                            record.get("companyName") or page_company
                        )
                        record["_companyAccount"] = (
                            record.get("companyAccount") or page_account
                        )
                        records.append(record)

        vouchers = []
        for r in records:
            v = self._receipt_to_voucher(r)
            if v:
                vouchers.append(v)

        return self._wrap_result(vouchers, "receipt")

    def _receipt_to_voucher(self, record):
        """单张银行回单 → 记账凭证"""
        date_str = record.get("createDate", "")
        abstract = record.get("abstract", "")
        amount_raw = record.get("amount", 0)
        direction = record.get("balanceDirection", "")
        expend_customer = record.get("expendCustomer", "")
        income_customer = record.get("incomeCustomer", "")
        expend_account = record.get("expendAccount", "")
        income_account = record.get("incomeAccount", "")
        trans_no = record.get("transNo", "")
        remark = record.get("remark", "")

        try:
            amount = Decimal(str(amount_raw)).quantize(
                Decimal("0.01"), ROUND_HALF_UP
            )
        except (InvalidOperation, TypeError):
            amount = Decimal("0.00")

        if amount <= 0:
            return None

        # 回单语义（基于实际银行回单数据分析）：
        # "借方" = 银行借记公司账户 → 公司账户余额增加 → 收入/转入
        # "贷方" = 银行贷记公司账户 → 公司账户余额减少 → 支出/转出
        # 注意：这与会计科目中"借=资产增加"是一致的（银行存款是资产科目）
        is_income = direction in ("借", "借方", "收入", "debit", "in")
        is_expense = direction in ("贷", "贷方", "支出", "credit", "out")

        if not is_income and not is_expense:
            if abstract:
                income_kw = ["收款", "转入", "到账", "收入", "汇入", "转存"]
                expense_kw = ["付款", "转出", "支出", "扣款", "汇款", "转取",
                              "公共缴费"]
                if any(k in abstract for k in income_kw):
                    is_income = True
                elif any(k in abstract for k in expense_kw):
                    is_expense = True

        if not is_income and not is_expense:
            # 最终兜底：根据收付方判断
            company_name = record.get("_companyName", "")
            if company_name:
                if company_name in (income_customer or ""):
                    is_income = True
                elif company_name in (expend_customer or ""):
                    is_expense = True
            if not is_income and not is_expense:
                is_expense = True

        entries = []
        review_flags = []
        confidence = 0.0
        matched_account = None
        alternatives = []

        counterparty = (
            income_customer if is_expense else expend_customer
        ) or expend_customer or income_customer or ""
        # 组合摘要和备注用于科目匹配（两者都包含有用信息）
        search_parts = [p for p in [abstract, remark] if p]
        search_desc = " ".join(search_parts)

        if is_income:
            # 借：银行存款
            entries.append(JournalEntry(
                "1002", "银行存款", debit=amount,
                remark=f"收 {counterparty}",
            ))

            # 贷：匹配收入科目
            matches = self.engine.match(
                search_desc, amount, "credit", counterparty
            )
            if matches:
                best = matches[0]
                confidence = best.confidence
                matched_account = best
                alternatives = matches[1:3]
                entries.append(JournalEntry(
                    best.code, best.name, credit=amount,
                    remark=f"收 {counterparty} {search_desc}",
                ))
            else:
                confidence = 0.3
                review_flags.append("missing_info")
                entries.append(JournalEntry(
                    "5001", "主营业务收入", credit=amount,
                    remark=f"收 {counterparty}（科目待确认）",
                ))

            description = (
                f"收款：{counterparty}（{abstract or trans_no or '银行回单'}）"
            )

        else:
            # 借：匹配支出科目
            matches = self.engine.match(
                search_desc, amount, "debit", counterparty
            )
            if matches:
                best = matches[0]
                confidence = best.confidence
                matched_account = best
                alternatives = matches[1:3]
                entries.append(JournalEntry(
                    best.code, best.name, debit=amount,
                    remark=f"付 {counterparty} {search_desc}",
                ))
            else:
                confidence = 0.3
                review_flags.append("missing_info")
                # 根据摘要/备注智能选择默认科目
                if any(kw in search_desc for kw in ["货款", "购销", "进货"]):
                    default_code, default_name = "1405", "库存商品"
                elif any(kw in search_desc for kw in ["油费", "加油", "保险"]):
                    default_code, default_name = "5602.11", "管理费用-车辆费"
                else:
                    default_code, default_name = "5602.01", "管理费用-办公费"
                entries.append(JournalEntry(
                    default_code, default_name, debit=amount,
                    remark=f"付 {counterparty}（科目待确认）",
                ))

            # 贷：银行存款
            entries.append(JournalEntry(
                "1002", "银行存款", credit=amount,
                remark=f"付 {counterparty}",
            ))

            description = (
                f"付款：{counterparty}（{abstract or trans_no or '银行回单'}）"
            )

        # 额外复核标记
        if float(amount) >= 10000:
            review_flags.append("high_value")
        if matched_account and confidence < 0.6:
            review_flags.append("low_confidence")
        elif matched_account and confidence < 0.8:
            review_flags.append("category_ambiguous")
        if float(amount) >= 5000 and matched_account and matched_account.code not in ("1601", "1405"):
            review_flags.append("fixed_asset_check")

        # 生成复核建议
        review_suggestion = self._build_review_suggestion(
            confidence, matched_account, alternatives, review_flags, amount
        )

        status = (
            VoucherStatus.PENDING
            if review_suggestion["level"] in ("high", "medium")
            else VoucherStatus.DRAFT
        )

        voucher = Voucher(
            date_str=date_str,
            description=description,
            entries=entries,
            source_type="receipt",
            source_no=trans_no or None,
            confidence=round(confidence, 2),
            status=status,
        )
        voucher.review_suggestion = review_suggestion
        return voucher

    # ----------------------------------------------------------
    # 银行对账单处理
    # ----------------------------------------------------------

    def _process_statements(self, data, **kwargs):
        """处理银行对账单解析结果"""
        records = []
        if isinstance(data, list):
            for page in data:
                if not isinstance(page, dict):
                    continue
                page_data = page.get("page_data")
                if not isinstance(page_data, dict):
                    continue
                detail_list = page_data.get("detail_fields_list", [])
                if isinstance(detail_list, list):
                    records.extend(detail_list)

        vouchers = []
        for r in records:
            v = self._statement_to_voucher(r)
            if v:
                vouchers.append(v)

        return self._wrap_result(vouchers, "statement")

    def _statement_to_voucher(self, record):
        """单条对账单交易 → 记账凭证"""
        date_str = record.get("tradeDate") or record.get("transDate", "")
        counterparty = (
            record.get("counterpartyName")
            or record.get("counterparty", "")
        )
        cp_account = record.get("counterpartyAccount", "")
        credit_raw = float(record.get("amountCredited") or record.get("creditAmount") or 0)
        debit_raw = float(record.get("amountDebited") or record.get("debitAmount") or 0)
        abstract = record.get("abstract") or record.get("purpose", "")
        trans_no = record.get("transNo", "") or record.get("voucherNo", "")

        amount = Decimal(str(credit_raw or debit_raw)).quantize(
            Decimal("0.01"), ROUND_HALF_UP
        )
        if amount <= 0:
            return None

        # 对账单：贷方(credit) = 转入收入，借方(debit) = 转出支出
        is_income = credit_raw > 0
        direction_label = "收入" if is_income else "支出"

        entries = []
        review_flags = []
        confidence = 0.0
        matched_account = None
        alternatives = []

        search_desc = abstract or ""

        if is_income:
            entries.append(JournalEntry(
                "1002", "银行存款", debit=amount,
                remark=f"{direction_label} {counterparty}",
            ))
            matches = self.engine.match(
                search_desc, amount, "credit", counterparty
            )
            if matches:
                best = matches[0]
                confidence = best.confidence
                matched_account = best
                alternatives = matches[1:3]
                entries.append(JournalEntry(
                    best.code, best.name, credit=amount,
                    remark=f"{counterparty} {search_desc}",
                ))
            else:
                confidence = 0.3
                review_flags.append("missing_info")
                entries.append(JournalEntry(
                    "5001", "主营业务收入", credit=amount,
                    remark=f"{counterparty}（科目待确认）",
                ))
        else:
            matches = self.engine.match(
                search_desc, amount, "debit", counterparty
            )
            if matches:
                best = matches[0]
                confidence = best.confidence
                matched_account = best
                alternatives = matches[1:3]
                entries.append(JournalEntry(
                    best.code, best.name, debit=amount,
                    remark=f"{counterparty} {search_desc}",
                ))
            else:
                confidence = 0.3
                review_flags.append("missing_info")
                entries.append(JournalEntry(
                    "5602.01", "管理费用-办公费", debit=amount,
                    remark=f"{counterparty}（科目待确认）",
                ))
            entries.append(JournalEntry(
                "1002", "银行存款", credit=amount,
                remark=f"{direction_label} {counterparty}",
            ))

        description = (
            f"{direction_label}：{counterparty or '未知'}"
            f"（{abstract or trans_no or '对账单交易'}）"
        )

        if float(amount) >= 10000:
            review_flags.append("high_value")
        if matched_account and confidence < 0.6:
            review_flags.append("low_confidence")
        elif matched_account and confidence < 0.8:
            review_flags.append("category_ambiguous")
        if float(amount) >= 5000 and matched_account and matched_account.code not in ("1601", "1405"):
            review_flags.append("fixed_asset_check")

        review_suggestion = self._build_review_suggestion(
            confidence, matched_account, alternatives, review_flags, amount
        )
        status = (
            VoucherStatus.PENDING
            if review_suggestion["level"] in ("high", "medium")
            else VoucherStatus.DRAFT
        )

        voucher = Voucher(
            date_str=date_str,
            description=description,
            entries=entries,
            source_type="statement",
            source_no=trans_no or None,
            confidence=round(confidence, 2),
            status=status,
        )
        voucher.review_suggestion = review_suggestion
        return voucher

    # ----------------------------------------------------------
    # 发票处理
    # ----------------------------------------------------------

    def _process_invoices(self, data, **kwargs):
        """处理发票解析结果"""
        records = []
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = [data]

        vouchers = []
        for r in records:
            v = self._invoice_to_voucher(r)
            if v:
                vouchers.append(v)

        return self._wrap_result(vouchers, "invoice")

    def _invoice_to_voucher(self, record):
        """单张发票 → 记账凭证"""
        invoice_no = record.get("invoiceNo") or record.get("invoice_no", "")
        invoice_type = record.get("invoiceType") or record.get("invoice_type", "")
        date_str = record.get("date") or record.get("createDate", "")
        seller = record.get("sellerName") or record.get("seller_name", "")
        buyer = record.get("buyerName") or record.get("buyer_name", "")
        item_name = record.get("itemName") or record.get("item_name", "")
        total_raw = (
            record.get("totalAmount") or record.get("total_amount") or 0
        )
        tax_rate_raw = record.get("taxRate") or record.get("tax_rate", 0)
        tax_amount_raw = record.get("taxAmount") or record.get("tax_amount", 0)
        direction = record.get("direction", "purchase")

        try:
            total = Decimal(str(total_raw)).quantize(
                Decimal("0.01"), ROUND_HALF_UP
            )
        except (InvalidOperation, TypeError):
            return None

        if total <= 0:
            return None

        try:
            tax_rate = Decimal(str(tax_rate_raw))
            if tax_rate > 1:
                tax_rate = tax_rate / Decimal("100")
        except (InvalidOperation, TypeError):
            tax_rate = Decimal("0")

        try:
            tax_amount = Decimal(str(tax_amount_raw)).quantize(
                Decimal("0.01"), ROUND_HALF_UP
            )
        except (InvalidOperation, TypeError):
            tax_amount = Decimal("0.00")

        amount_before_tax = (total - tax_amount).quantize(
            Decimal("0.01"), ROUND_HALF_UP
        )

        entries = []
        review_flags = []
        confidence = 0.0
        matched_account = None
        alternatives = []

        if direction == "purchase":
            counterparty = seller
            # 借方科目：匹配
            matches = self.engine.match(item_name, total, "debit", seller)
            if matches:
                best = matches[0]
                confidence = best.confidence
                matched_account = best
                alternatives = matches[1:3]
                entries.append(JournalEntry(
                    best.code, best.name, debit=total,
                    remark=f"采购：{item_name}",
                ))
            else:
                if self.business_type == "商贸":
                    entries.append(JournalEntry(
                        "1405", "库存商品", debit=total,
                        remark=f"采购：{item_name}（科目待确认）",
                    ))
                else:
                    entries.append(JournalEntry(
                        "5602.01", "管理费用-办公费", debit=total,
                        remark=f"采购：{item_name}（科目待确认）",
                    ))
                confidence = 0.3
                review_flags.append("missing_info")

            # 贷方：银行存款
            entries.append(JournalEntry(
                "1002", "银行存款", credit=total,
                remark=f"付 {seller}",
            ))

            description = (
                f"采购：{item_name}（发票 {invoice_no}）"
                if invoice_no
                else f"采购：{item_name}"
            )

        elif direction == "sale":
            counterparty = buyer
            # 借方：银行存款
            entries.append(JournalEntry(
                "1002", "银行存款", debit=total,
                remark=f"收 {buyer}",
            ))
            # 贷方：主营业务收入（不含税）
            entries.append(JournalEntry(
                "5001", "主营业务收入", credit=amount_before_tax,
                remark=f"销售：{item_name}",
            ))
            # 贷方：应交税费-应交增值税
            if tax_amount > 0:
                entries.append(JournalEntry(
                    "2221.01", "应交税费-应交增值税", credit=tax_amount,
                    remark=f"销项税额（{float(tax_rate) * 100:.0f}%）",
                ))

            confidence = 0.85  # 销售凭证规则明确，置信度较高
            review_flags.append("tax_related")
            description = (
                f"销售：{item_name}（发票 {invoice_no}）"
                if invoice_no
                else f"销售：{item_name}"
            )

        else:
            # 其他/未知方向 → 当费用处理
            counterparty = seller
            matches = self.engine.match(item_name, total, "debit", seller)
            if matches:
                best = matches[0]
                confidence = best.confidence
                matched_account = best
                entries.append(JournalEntry(
                    best.code, best.name, debit=total,
                    remark=item_name,
                ))
            else:
                confidence = 0.3
                entries.append(JournalEntry(
                    "5602.01", "管理费用-办公费", debit=total,
                    remark=f"{item_name}（科目待确认）",
                ))
                review_flags.append("missing_info")

            entries.append(JournalEntry(
                "1002", "银行存款", credit=total,
                remark=f"付 {seller}",
            ))
            description = f"费用：{item_name}"

        # 额外复核标记
        if float(total) >= 10000:
            review_flags.append("high_value")
        if matched_account and confidence < 0.6:
            review_flags.append("low_confidence")
        elif matched_account and confidence < 0.8:
            review_flags.append("category_ambiguous")
        if float(total) >= 5000 and matched_account and matched_account.code not in ("1601", "1405"):
            review_flags.append("fixed_asset_check")

        review_suggestion = self._build_review_suggestion(
            confidence, matched_account, alternatives, review_flags, total
        )
        status = (
            VoucherStatus.PENDING
            if review_suggestion["level"] in ("high", "medium")
            else VoucherStatus.DRAFT
        )

        voucher = Voucher(
            date_str=date_str,
            description=description,
            entries=entries,
            source_type=direction if direction in ("purchase", "sale") else "other",
            source_no=invoice_no or None,
            confidence=round(confidence, 2),
            status=status,
        )
        voucher.review_suggestion = review_suggestion
        return voucher

    # ----------------------------------------------------------
    # 辅助方法
    # ----------------------------------------------------------

    def _build_review_suggestion(self, confidence, matched_account,
                                 alternatives, flags, amount):
        """构建复核建议"""
        # 确定复核级别
        if confidence < 0.5:
            level = REVIEW_HIGH
        elif confidence < 0.8 or "high_value" in flags:
            level = REVIEW_MEDIUM
        else:
            level = REVIEW_LOW

        # 生成自然语言摘要
        if matched_account:
            summary = (
                f"系统建议记入「{matched_account.name}」"
                f"（置信度 {confidence * 100:.0f}%，{matched_account.reason}）"
            )
        else:
            summary = "系统无法自动匹配科目，需人工判断"

        # 构建建议对象
        suggestion = {
            "level": level,
            "level_label": {
                "high": "必须人工复核",
                "medium": "建议复核",
                "low": "可信度较高，可快速确认",
            }[level],
            "summary": summary,
            "top_match": matched_account.to_dict() if matched_account else None,
            "alternatives": [
                {"code": a.code, "name": a.name, "confidence": a.confidence}
                for a in (alternatives or [])[:2]
            ],
            "flags": [],
        }

        # 去重 flags 并生成可读建议
        seen_flags = set()
        for flag in flags:
            if flag in seen_flags:
                continue
            seen_flags.add(flag)
            suggestion["flags"].append({
                "code": flag,
                "level": "warning" if flag in (
                    "low_confidence", "high_value", "missing_info",
                    "unusual_amount"
                ) else "info",
                "suggestion": FLAG_SUGGESTIONS.get(
                    flag, f"请核实：{flag}"
                ),
            })

        # 如果有候选科目且置信度不高，添加"请确认科目"提示
        if matched_account and alternatives and confidence < 0.85:
            alt_names = "、".join(
                f"「{a.name}」" for a in alternatives[:2]
            )
            suggestion["flags"].append({
                "code": "verify_account",
                "level": "info",
                "suggestion": f"除「{matched_account.name}」外，也可考虑{alt_names}，请根据实际业务性质确认",
            })

        return suggestion

    def _wrap_result(self, vouchers, source_type):
        """包装返回结果"""
        if not vouchers:
            return None
        if len(vouchers) == 1:
            return vouchers[0]
        return VoucherBundle(vouchers, source_type)


# ============================================================
# 6. 凭证 HTML 预览生成
# ============================================================

def generate_voucher_html(voucher_or_bundle, output_path=None):
    """
    生成记账凭证 HTML 预览文件

    :param voucher_or_bundle: Voucher 或 VoucherBundle
    :param output_path: 输出路径（可选）
    :return: 输出文件路径
    """
    if isinstance(voucher_or_bundle, VoucherBundle):
        vouchers = voucher_or_bundle.vouchers
    elif isinstance(voucher_or_bundle, Voucher):
        vouchers = [voucher_or_bundle]
    else:
        return None

    if not vouchers:
        return None

    if output_path is None:
        # 确定输出目录
        candidates = []
        try:
            home = os.path.expanduser("~")
            if home and home != "~":
                candidates.append(os.path.join(home, "yqzl-ai-service"))
        except Exception:
            pass
        try:
            cwd = os.getcwd()
            if cwd:
                candidates.append(os.path.join(cwd, "yqzl-ai-service-output"))
        except Exception:
            pass
        try:
            import tempfile
            candidates.append(os.path.join(tempfile.gettempdir(), "yqzl-ai-service"))
        except Exception:
            pass

        output_dir = None
        for d in candidates:
            try:
                os.makedirs(d, exist_ok=True)
                test_file = os.path.join(d, ".write_test")
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write("test")
                os.remove(test_file)
                output_dir = d
                break
            except Exception:
                continue
        if not output_dir:
            output_dir = os.path.dirname(os.path.abspath(__file__))

        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        base_name = f"voucher_{ts}"
        output_path = os.path.join(output_dir, f"{base_name}.html")
        counter = 1
        while os.path.exists(output_path):
            output_path = os.path.join(output_dir, f"{base_name}_{counter}.html")
            counter += 1

    def _fmt_money(n):
        try:
            return "¥ {:,.2f}".format(float(n))
        except (TypeError, ValueError):
            return "¥ 0.00"

    def _review_badge_html(suggestion):
        if not suggestion:
            return ""
        level = suggestion.get("level", "low")
        label = suggestion.get("level_label", "")
        colors = {
            "high": ("#c0392b", "#ffebee"),
            "medium": ("#e65100", "#fff3e0"),
            "low": ("#2e7d32", "#e8f5e9"),
        }
        fg, bg = colors.get(level, ("#555", "#f5f5f5"))
        return '<span style="display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;background:{bg};color:{fg};font-weight:600;">{label}</span>'.format(
            bg=bg, fg=fg, label=label
        )

    def _voucher_card_html(v, index):
        entries_html = ""
        for e in v.entries:
            d_cls = "vc-debit" if e.debit > 0 else ""
            c_cls = "vc-credit" if e.credit > 0 else ""
            entries_html += """
            <tr>
                <td class="vc-acct">{code} {name}</td>
                <td class="vc-amt {d_cls}">{debit}</td>
                <td class="vc-amt {c_cls}">{credit}</td>
                <td class="vc-remark">{remark}</td>
            </tr>""".format(
                code=e.account_code,
                name=e.account_name,
                d_cls=d_cls,
                c_cls=c_cls,
                debit=_fmt_money(e.debit) if e.debit > 0 else "-",
                credit=_fmt_money(e.credit) if e.credit > 0 else "-",
                remark=e.remark or "",
            )

        conf_text = f"{v.confidence * 100:.0f}%" if v.confidence is not None else "N/A"
        badge = _review_badge_html(v.review_suggestion)

        # 复核建议区域
        review_html = ""
        if v.review_suggestion:
            s = v.review_suggestion
            flags_html = ""
            for flag in s.get("flags", []):
                flag_level = flag.get("level", "info")
                flag_icon = "&#9888;" if flag_level == "warning" else "&#9432;"
                flag_color = "#e65100" if flag_level == "warning" else "#1565c0"
                flags_html += '<div style="color:{color};font-size:12px;margin:3px 0;">{icon} {text}</div>'.format(
                    color=flag_color, icon=flag_icon, text=flag.get("suggestion", "")
                )

            alt_html = ""
            if s.get("alternatives"):
                alt_items = ", ".join(
                    f"{a['name']}（{a['confidence']*100:.0f}%）"
                    for a in s["alternatives"]
                )
                alt_html = f'<div style="font-size:12px;color:#666;margin-top:4px;">备选科目：{alt_items}</div>'

            review_html = """
            <div class="vc-review">
                <div style="font-size:12px;color:#555;margin-bottom:4px;">{summary}</div>
                {alt_html}
                {flags_html}
            </div>""".format(
                summary=s.get("summary", ""),
                alt_html=alt_html,
                flags_html=flags_html,
            )

        return """
        <div class="vc-card">
            <div class="vc-header">
                <div class="vc-title">凭证 {index} &nbsp; {badge}</div>
                <div class="vc-meta">
                    <span>日期：{date}</span>
                    <span>来源：{source}</span>
                    <span>置信度：{conf}</span>
                    <span>状态：{status}</span>
                </div>
            </div>
            <div class="vc-desc">摘要：{description}</div>
            <table class="vc-table">
                <thead><tr>
                    <th>会计科目</th>
                    <th>借方金额</th>
                    <th>贷方金额</th>
                    <th>备注</th>
                </tr></thead>
                <tbody>{entries_html}
                    <tr class="vc-total">
                        <td>合计</td>
                        <td class="vc-amt vc-debit">{total_debit}</td>
                        <td class="vc-amt vc-credit">{total_credit}</td>
                        <td>{balance_status}</td>
                    </tr>
                </tbody>
            </table>
            {review_html}
        </div>""".format(
            index=index + 1,
            badge=badge,
            date=v.date,
            source=v.source_type,
            conf=conf_text,
            status=v.status.value,
            description=v.description,
            entries_html=entries_html,
            total_debit=_fmt_money(v.total_debit),
            total_credit=_fmt_money(v.total_credit),
            balance_status="平衡" if v.is_balanced else "不平衡!",
            review_html=review_html,
        )

    cards_html = ""
    for i, v in enumerate(vouchers):
        cards_html += _voucher_card_html(v, i)

    # 汇总统计
    total_d = sum(float(v.total_debit) for v in vouchers)
    total_c = sum(float(v.total_credit) for v in vouchers)
    review_count = sum(
        1 for v in vouchers
        if v.review_suggestion and v.review_suggestion.get("level") in ("high", "medium")
    )

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>记账凭证 - 云启智联AI服务</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: #f0f2f5; min-height: 100vh; padding: 20px;
}}
.vc-container {{ max-width: 1000px; margin: 0 auto; }}
.vc-page-header {{
    text-align: center; margin-bottom: 20px;
}}
.vc-page-header h1 {{ font-size: 20px; color: #333; margin-bottom: 6px; }}
.vc-page-header .subtitle {{ color: #666; font-size: 13px; }}
.vc-summary {{
    display: flex; gap: 16px; justify-content: center;
    margin-bottom: 20px; flex-wrap: wrap;
}}
.vc-stat {{
    background: #1565c0; color: #fff;
    padding: 12px 20px; border-radius: 10px;
    text-align: center; min-width: 130px;
}}
.vc-stat .label {{ font-size: 12px; opacity: 0.85; margin-bottom: 4px; }}
.vc-stat .value {{ font-size: 20px; font-weight: bold; }}
.vc-stat.warn {{ background: #e65100; }}
.vc-card {{
    background: #fff; border-radius: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    padding: 20px; margin-bottom: 16px;
}}
.vc-header {{ margin-bottom: 12px; }}
.vc-title {{
    font-size: 15px; font-weight: 600; color: #333;
    margin-bottom: 6px; display: flex; align-items: center; gap: 8px;
}}
.vc-meta {{
    display: flex; gap: 16px; font-size: 12px; color: #888;
    flex-wrap: wrap;
}}
.vc-desc {{
    font-size: 13px; color: #555; margin-bottom: 12px;
    padding: 8px 12px; background: #f8f9fa; border-radius: 6px;
    border-left: 3px solid #1565c0;
}}
.vc-table {{
    width: 100%; border-collapse: collapse; font-size: 13px;
    margin-bottom: 12px;
}}
.vc-table th {{
    background: #1565c0; color: #fff;
    padding: 10px 8px; font-size: 12px; text-align: left;
}}
.vc-table td {{
    padding: 8px; border-bottom: 1px solid #eee; vertical-align: top;
}}
.vc-table tr:hover {{ background: #f0f7ff; }}
.vc-acct {{ font-weight: 500; }}
.vc-amt {{ text-align: right; font-weight: bold; white-space: nowrap; }}
.vc-debit {{ color: #c0392b; }}
.vc-credit {{ color: #1565c0; }}
.vc-remark {{ color: #888; font-size: 12px; }}
.vc-total {{ background: #f0f4fa; font-weight: bold; }}
.vc-total td {{ border-top: 2px solid #1565c0; }}
.vc-review {{
    background: #fffbf0; border: 1px solid #ffe082;
    border-radius: 8px; padding: 12px; margin-top: 8px;
}}
.vc-footer {{
    text-align: center; font-size: 11px; color: #aaa;
    margin-top: 20px; padding-top: 16px;
    border-top: 1px solid #eee;
}}
</style>
</head>
<body>
<div class="vc-container">
    <div class="vc-page-header">
        <h1>记账凭证</h1>
        <div class="subtitle">基于云启智联AI服务 OCR 解析结果自动生成 | 仅供参考，请人工复核后入账</div>
    </div>
    <div class="vc-summary">
        <div class="vc-stat"><div class="label">凭证数量</div><div class="value">{count}</div></div>
        <div class="vc-stat"><div class="label">借方合计</div><div class="value">{total_debit}</div></div>
        <div class="vc-stat"><div class="label">贷方合计</div><div class="value">{total_credit}</div></div>
        <div class="vc-stat{warn_cls}"><div class="label">需复核</div><div class="value">{review_count}</div></div>
    </div>
    {cards}
    <div class="vc-footer">云启智联 AI 服务 | 智能记账凭证生成 | 仅供参考，以实际业务为准</div>
</div>
</body>
</html>""".format(
        count=len(vouchers),
        total_debit=_fmt_money(total_d),
        total_credit=_fmt_money(total_c),
        warn_cls=" warn" if review_count > 0 else "",
        review_count=review_count,
        cards=cards_html,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


# ============================================================
# 7. CLI 入口
# ============================================================

def _load_json_file(path):
    """加载 JSON 文件"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _detect_source_type(data):
    """自动检测数据来源类型"""
    if not isinstance(data, list) or not data:
        return None

    first = data[0]
    if not isinstance(first, dict):
        return None

    page_data = first.get("page_data")

    # 回单格式：page_data 是 list
    if isinstance(page_data, list):
        return "receipt"

    # 对账单格式：page_data 是 dict，含 detail_fields_list
    if isinstance(page_data, dict):
        if "detail_fields_list" in page_data:
            return "statement"

    return None


def cli_main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="云启智联AI服务 — 智能记账凭证生成器"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="解析结果 JSON 文件路径",
    )
    parser.add_argument(
        "--type", "-t",
        choices=["receipt", "statement", "invoice", "auto"],
        default="auto",
        help="数据来源类型（默认自动检测）",
    )
    parser.add_argument(
        "--business-type", default="商贸",
        choices=["商贸", "服务"],
        help="企业类型（默认：商贸）",
    )
    parser.add_argument(
        "--vat-rate", type=float, default=0.01,
        help="增值税税率（默认 0.01 即 1%%）",
    )
    parser.add_argument(
        "--output", "-o",
        help="凭证 JSON 输出路径（可选，默认输出到 stdout）",
    )
    parser.add_argument(
        "--html", action="store_true",
        help="同时生成 HTML 预览文件",
    )
    parser.add_argument(
        "--json-only", action="store_true",
        help="仅输出 JSON，不输出摘要文本",
    )

    args = parser.parse_args()

    # 加载数据
    try:
        data = _load_json_file(args.input)
    except Exception as e:
        print(f"错误：无法加载 JSON 文件: {e}", file=sys.stderr)
        sys.exit(1)

    # 如果是完整 API 响应，提取 data 字段
    if isinstance(data, dict) and "code" in data and "data" in data:
        data = data["data"]

    # 自动检测类型
    source_type = args.type
    if source_type == "auto":
        source_type = _detect_source_type(data)
        if not source_type:
            # 尝试作为发票格式
            if isinstance(data, dict) and data.get("data"):
                source_type = "invoice"
                data = data["data"]
            elif isinstance(data, list) and data and isinstance(data[0], dict):
                if "invoiceNo" in data[0] or "invoice_no" in data[0]:
                    source_type = "invoice"
                else:
                    print("错误：无法自动检测数据来源类型，请用 --type 指定", file=sys.stderr)
                    sys.exit(1)
            else:
                print("错误：无法自动检测数据来源类型，请用 --type 指定", file=sys.stderr)
                sys.exit(1)

    # 生成凭证
    generator = VoucherGenerator(
        business_type=args.business_type,
        vat_rate=args.vat_rate,
    )

    try:
        result = generator.process(data, source_type)
    except Exception as e:
        print(f"错误：凭证生成失败: {e}", file=sys.stderr)
        sys.exit(1)

    if result is None:
        print("未生成任何凭证（数据为空或所有记录金额为0）", file=sys.stderr)
        sys.exit(0)

    # 输出 JSON
    result_json = result.to_json(indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result_json)
        if not args.json_only:
            print(f"凭证 JSON 已保存: {args.output}")
    elif not args.json_only:
        pass  # 不输出到 stdout，避免与 HTML 路径混在一起

    # 打印摘要
    if not args.json_only:
        if isinstance(result, VoucherBundle):
            print(f"\n共生成 {len(result.vouchers)} 张凭证")
            for i, v in enumerate(result.vouchers):
                print(f"\n--- 凭证 {i + 1} ---")
                for line in v.to_display_lines():
                    print(line)
                if v.review_suggestion:
                    s = v.review_suggestion
                    print(f"复核级别：{s['level_label']}")
                    print(f"复核摘要：{s['summary']}")
                    for flag in s.get("flags", []):
                        print(f"  - {flag['suggestion']}")
        elif isinstance(result, Voucher):
            for line in result.to_display_lines():
                print(line)
            if result.review_suggestion:
                s = result.review_suggestion
                print(f"\n复核级别：{s['level_label']}")
                print(f"复核摘要：{s['summary']}")
                for flag in s.get("flags", []):
                    print(f"  - {flag['suggestion']}")

    # 生成 HTML
    if args.html:
        try:
            html_path = generate_voucher_html(result)
            if html_path:
                print(f"\n已生成凭证预览页面: {html_path}")
        except Exception as e:
            print(f"\n[提示] HTML 预览生成失败（不影响 JSON 结果）: {e}")

    # stdout 输出 JSON（供管道使用）
    if not args.output:
        print(result_json)


if __name__ == "__main__":
    cli_main()
