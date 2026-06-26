#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock email data for testing InvoiceAnalyzerWithLLM
"""

from typing import NamedTuple


class MockEmail(NamedTuple):
    subject: str
    text: str
    html: str
    has_attachments: bool
    expected_type: str       # expected invoice_type.value
    expected_confidence_min: float  # minimum expected confidence


MOCK_EMAILS = [
    # ── 1. 和运国际税务平台（已知平台，置信度应高）─────────────────────────
    MockEmail(
        subject="【和运国际】电子发票开具成功",
        text="""尊敬的纳税人，您好！
您开具的电子发票已成功生成，发票代码：144031900100，发票号码：44556677
开票日期：2026-03-10
发票金额：¥1,280.00
请登录电子税务局平台下载发票。
平台地址：https://dppt.shanghai.chinatax.gov.cn:8443""",
        html="""<html><body>
<p>尊敬的纳税人，您好！</p>
<p>您开具的电子发票已成功生成，发票代码：144031900100</p>
<p>请登录 <a href="https://dppt.shanghai.chinatax.gov.cn:8443">电子税务局</a> 下载。</p>
</body></html>""",
        has_attachments=False,
        expected_type="tax_platform",
        expected_confidence_min=0.7,
    ),

    # ── 2. 诺诺网（已知平台）──────────────────────────────────────────────
    MockEmail(
        subject="诺诺发票下载提醒 - 开票成功",
        text="""您好，您有一张发票可以下载。
开票主体：深圳市某某公司
发票金额：568.00元
请登录诺诺网平台下载：
https://nnfp.jss.com.cn/invoice/download?no=ABC123""",
        html="""<html><body>
<p>您好，您有一张发票可以下载。</p>
<p>请登录 <a href="https://nnfp.jss.com.cn/invoice/download?no=ABC123">诺诺网下载</a></p>
</body></html>""",
        has_attachments=False,
        expected_type="nuonuo",
        expected_confidence_min=0.7,
    ),

    # ── 3. 中海油批量邮件（已知平台）─────────────────────────────────────
    MockEmail(
        subject="【中海油】2026年3月电子发票批量下载通知",
        text="""中国海油集团电子发票通知
您本期共有 5 张电子发票可以下载，发票总金额 ¥8,920.00
支持批量zip下载，请点击下方按钮：
批量zip下载：https://zzslg.cnooc.com.cn/batch/invoices.zip
也可访问个人发票列表逐一下载。""",
        html="""<html><body>
<p>中国海油集团电子发票通知</p>
<p>本期共有 5 张发票，发票总金额 ¥8,920.00</p>
<p><a href="https://zzslg.cnooc.com.cn/batch/invoices.zip">批量zip下载</a></p>
</body></html>""",
        has_attachments=False,
        expected_type="cnooc",
        expected_confidence_min=0.7,
    ),

    # ── 4. 陌生新平台 → 触发 LLM ──────────────────────────────────────────
    MockEmail(
        subject="您的发票开具完成 - 顺捷云平台",
        text="""您好，您的增值税发票已开具完成。
公司名称：深圳市顺捷云科技有限公司
发票金额：¥3,450.00
请登录顺捷云平台下载：https://shunjeyun.com/invoice/abc123""",
        html="""<html><body>
<p>您的发票已开具完成</p>
<a href="https://shunjeyun.com/invoice/abc123">立即下载</a>
</body></html>""",
        has_attachments=False,
        expected_type="unknown",   # base analyzer 不认识，顺捷云不在 PLATFORM_PATTERNS
        expected_confidence_min=0.0,  # confidence < 0.7 → LLM triggered
    ),

    # ── 5. 非发票邮件 → 跳过 ─────────────────────────────────────────────
    MockEmail(
        subject="【重要】请确认您的订单信息",
        text="""您好，您的订单已于2026-03-10确认收货。
订单编号：DD20260310001
商品：办公用品套装
收货地址：上海市嘉定区南翔镇""",
        html="""<html><body>
<p>您的订单已确认收货</p>
<p>订单编号：DD20260310001</p>
</body></html>""",
        has_attachments=False,
        expected_type="unknown",
        expected_confidence_min=0.0,
    ),
]
