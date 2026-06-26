#!/usr/bin/env python3
"""
Cross-border Trade Email Generator
Generates professional business emails for foreign trade scenarios
with multi-language support (CN/EN/AR/ES/RU).

Usage:
    python email-generator.py --type inquiry_reply --lang en \
        --product "Stainless Steel Bolts M8" --qty 2000 --price "$0.15/pc FOB Ningbo" \
        --moq 1000 --lead-time "25 days" --payment "T/T 30% deposit" \
        --buyer-name "Ahmed" --company "Al-Rashid Trading"

    python email-generator.py --input '{"type":"inquiry_reply","lang":"ar","product":"不锈钢六角螺栓M8","qty":"2000套","price":"$0.15/pc FOB宁波","moq":"1000","lead_time":"25天","payment":"T/T 30%预付","buyer_name":"Ahmed","company":"Al-Rashid Trading"}'
"""

import argparse
import json
import sys
from datetime import datetime, timedelta


# ── Email Type Definitions ───────────────────────────────────────

EMAIL_TYPES = {
    "inquiry_reply": {
        "cn": "询盘回复",
        "en": "Inquiry Reply",
        "need_price": True,
    },
    "quotation": {
        "cn": "报价邮件",
        "en": "Quotation Email",
        "need_price": True,
    },
    "follow_up": {
        "cn": "跟进邮件",
        "en": "Follow-up Email",
        "need_price": False,
    },
    "sample_request": {
        "cn": "样品请求",
        "en": "Sample Request",
        "need_price": False,
    },
    "order_confirmation": {
        "cn": "订单确认",
        "en": "Order Confirmation",
        "need_price": True,
    },
    "shipment_notice": {
        "cn": "出货通知",
        "en": "Shipment Notice",
        "need_price": False,
    },
    "payment_reminder": {
        "cn": "付款提醒",
        "en": "Payment Reminder",
        "need_price": False,
    },
    "after_sales": {
        "cn": "售后跟进",
        "en": "After-sales Follow-up",
        "need_price": False,
    },
}

SUPPORTED_LANGS = ["cn", "en", "ar", "es", "ru"]

LANG_GREETINGS = {
    "cn": {"formal": "尊敬的", "informal": "你好"},
    "en": {"formal": "Dear", "informal": "Hi"},
    "ar": {"formal": "السيد", "informal": "مرحبا"},
    "es": {"formal": "Estimado", "informal": "Hola"},
    "ru": {"formal": "Уважаемый", "informal": "Здравствуйте"},
}

LANG_CLOSINGS = {
    "cn": "此致敬礼",
    "en": "Best regards",
    "ar": "مع خالص التحيات",
    "es": "Atentamente",
    "ru": "С уважением",
}

CURRENCY_MAP = {
    "cn": "CNY",
    "en": "USD",
    "ar": "USD",
    "es": "EUR",
    "ru": "USD",
}


# ── Template Functions ───────────────────────────────────────────

def _greeting(lang: str, buyer_name: str) -> str:
    g = LANG_GREETINGS.get(lang, LANG_GREETINGS["en"])
    return f"{g['formal']} {buyer_name},"


def _closing(lang: str, sender_name: str, company: str) -> str:
    cl = LANG_CLOSINGS.get(lang, LANG_CLOSINGS["en"])
    return f"{cl},\n{sender_name}\n{company}"


def gen_inquiry_reply(params: dict) -> str:
    lang = params.get("lang", "en")
    buyer = params.get("buyer_name", "Customer")
    product = params.get("product", "N/A")
    qty = params.get("qty", "N/A")
    price = params.get("price", "TBD")
    moq = params.get("moq", "N/A")
    lead_time = params.get("lead_time", "N/A")
    payment = params.get("payment", "T/T")
    sender = params.get("sender_name", "Sales Team")
    company = params.get("company", "Our Company")
    sample = params.get("sample_available", "Yes")

    if lang == "en":
        subject = f"Re: Inquiry for {product} - Quotation from {company}"
        lines = [
            subject,
            "",
            _greeting(lang, buyer),
            "",
            f"Thank you for your inquiry regarding {product}.",
            f"We are pleased to submit our quotation as follows:",
            "",
            "─" * 45,
            "QUOTATION SUMMARY",
            "─" * 45,
            f"  Product:        {product}",
            f"  Quantity:       {qty}",
            f"  Unit Price:     {price}",
            f"  MOQ:            {moq}",
            f"  Lead Time:      {lead_time}",
            f"  Payment Terms:  {payment}",
            f"  Sample:         {sample}",
            "─" * 45,
            "",
            "This quotation is valid for 30 days from the date above.",
            "Please feel free to contact us for any further questions.",
            "",
            _closing(lang, sender, company),
        ]
    elif lang == "cn":
        subject = f"回复：{product}询盘 - {company}报价"
        lines = [
            subject,
            "",
            _greeting(lang, buyer),
            "",
            f"感谢您对{product}的询价。",
            f"以下是我们为您准备的报价：",
            "",
            "─" * 45,
            "报价概要",
            "─" * 45,
            f"  产品：      {product}",
            f"  数量：      {qty}",
            f"  单价：      {price}",
            f"  最小起订量：{moq}",
            f"  交期：      {lead_time}",
            f"  付款方式：  {payment}",
            f"  样品：      {sample}",
            "─" * 45,
            "",
            "本报价自发出之日起30天内有效。",
            "如有任何问题，欢迎随时联系。",
            "",
            _closing(lang, sender, company),
        ]
    else:
        # Fallback to English for other languages with a note
        result = gen_inquiry_reply({**params, "lang": "en"})
        lines = result.split("\n")
        lines.insert(0, f"[Auto-generated in English — translate to {lang.upper()} when sending]")

    return "\n".join(lines)


def gen_follow_up(params: dict) -> str:
    lang = params.get("lang", "en")
    buyer = params.get("buyer_name", "Customer")
    product = params.get("product", "your requested products")
    sender = params.get("sender_name", "Sales Team")
    company = params.get("company", "Our Company")
    days_ago = params.get("days_since_contact", 7)

    if lang == "en":
        subject = f"Following up: Quotation for {product}"
        lines = [
            subject,
            "",
            _greeting(lang, buyer),
            "",
            f"I hope this email finds you well.",
            f"",
            f"I'm following up on the quotation for {product} sent {days_ago} days ago.",
            f"Please let us know if you have any questions or need further information.",
            f"",
            f"We would be happy to:",
            f"  • Adjust specifications to meet your requirements",
            f"  • Provide samples for quality evaluation",
            f"  • Discuss volume-based pricing for larger orders",
            f"",
            f"Looking forward to hearing from you.",
            "",
            _closing(lang, sender, company),
        ]
    elif lang == "cn":
        subject = f"跟进：{product}报价"
        lines = [
            subject,
            "",
            _greeting(lang, buyer),
            "",
            f"希望您一切顺利！",
            f"",
            f"关于{days_ago}天前发送的{product}报价，想确认您是否已查阅。",
            f"如有任何问题或需要更多信息，请随时告知。",
            f"",
            f"我们可以：",
            f"  • 根据您的需求调整规格",
            f"  • 提供样品供质量评估",
            f"  • 为大批量订单提供阶梯报价",
            "",
            _closing(lang, sender, company),
        ]
    else:
        result = gen_follow_up({**params, "lang": "en"})
        lines = result.split("\n")
        lines.insert(0, f"[Auto-generated in English — translate to {lang.upper()} when sending]")

    return "\n".join(lines)


def gen_quotation(params: dict) -> str:
    """Generate formal quotation email."""
    # Reuse inquiry_reply with more formal framing
    params.setdefault("is_formal_quotation", True)
    result = gen_inquiry_reply(params)

    if params.get("lang") == "en":
        lines = result.split("\n")
        lines[0] = f"Competitive Quotation for {params.get('product', 'N/A')} - Valid for 30 days"
        return "\n".join(lines)
    return result


def gen_sample_request(params: dict) -> str:
    lang = params.get("lang", "en")
    buyer = params.get("buyer_name", "Customer")
    product = params.get("product", "N/A")
    sender = params.get("sender_name", "Sales Team")
    company = params.get("company", "Our Company")

    if lang == "en":
        subject = f"Sample Arrangement for {product}"
        lines = [
            subject,
            "",
            _greeting(lang, buyer),
            "",
            f"Following your interest in {product}, we are arranging sample shipment.",
            "",
            "Sample Details:",
            f"  Product: {product}",
            f"  Sample Cost: Free of charge",
            f"  Shipping: Via DHL/FedEx (freight collect or prepaid)",
            f"  Estimated Delivery: 5-7 business days",
            "",
            "Please confirm your shipping address and preferred courier.",
            "",
            _closing(lang, sender, company),
        ]
    elif lang == "cn":
        subject = f"{product}样品安排"
        lines = [
            subject,
            "",
            _greeting(lang, buyer),
            "",
            f"感谢您对{product}的关注，我们正在安排样品发货。",
            "",
            "样品详情：",
            f"  产品：{product}",
            f"  样品费：免收",
            f"  运输：DHL/FedEx（运费到付或预付）",
            f"  预计送达：5-7个工作日",
            "",
            "请确认您的收货地址和偏好的快递方式。",
            "",
            _closing(lang, sender, company),
        ]
    else:
        result = gen_sample_request({**params, "lang": "en"})
        lines = result.split("\n")
        lines.insert(0, f"[Auto-generated in English — translate to {lang.upper()} when sending]")
        return "\n".join(lines)

    return "\n".join(lines)


def gen_shipment_notice(params: dict) -> str:
    lang = params.get("lang", "en")
    buyer = params.get("buyer_name", "Customer")
    product = params.get("product", "N/A")
    sender = params.get("sender_name", "Sales Team")
    company = params.get("company", "Our Company")
    vessel = params.get("vessel", "TBD")
    etd = params.get("etd", "TBD")
    eta = params.get("eta", "TBD")
    bl = params.get("bl_number", "Pending")

    if lang == "en":
        subject = f"Shipment Notice: {product}"
        lines = [
            subject,
            "",
            _greeting(lang, buyer),
            "",
            f"We are pleased to inform you that your order has been shipped.",
            "",
            "Shipment Details:",
            f"  Product: {product}",
            f"  Vessel/Flight: {vessel}",
            f"  ETD: {etd}",
            f"  ETA: {eta}",
            f"  B/L Number: {bl}",
            "",
            "Shipping documents will be sent upon request.",
            "",
            _closing(lang, sender, company),
        ]
    else:
        result = gen_shipment_notice({**params, "lang": "en"})
        lines = result.split("\n")
        lines.insert(0, f"[Auto-generated in English — translate to {lang.upper()} when sending]")
        return "\n".join(lines)

    return "\n".join(lines)


def gen_payment_reminder(params: dict) -> str:
    lang = params.get("lang", "en")
    buyer = params.get("buyer_name", "Customer")
    product = params.get("product", "N/A")
    sender = params.get("sender_name", "Sales Team")
    company = params.get("company", "Our Company")
    amount = params.get("amount", "N/A")
    due_date = params.get("due_date", "N/A")

    if lang == "en":
        subject = f"Payment Reminder: Order for {product}"
        lines = [
            subject,
            "",
            _greeting(lang, buyer),
            "",
            f"This is a friendly reminder regarding the pending payment for your order.",
            "",
            "Payment Details:",
            f"  Product: {product}",
            f"  Outstanding Amount: {amount}",
            f"  Due Date: {due_date}",
            "",
            "Please arrange payment at your earliest convenience.",
            "If payment has already been made, please share the remittance advice.",
            "",
            _closing(lang, sender, company),
        ]
    else:
        result = gen_payment_reminder({**params, "lang": "en"})
        lines = result.split("\n")
        lines.insert(0, f"[Auto-generated in English — translate to {lang.upper()} when sending]")
        return "\n".join(lines)

    return "\n".join(lines)


# ── Generator Router ─────────────────────────────────────────────

GENERATORS = {
    "inquiry_reply": gen_inquiry_reply,
    "quotation": gen_quotation,
    "follow_up": gen_follow_up,
    "sample_request": gen_sample_request,
    "order_confirmation": gen_inquiry_reply,  # Reuse with different context
    "shipment_notice": gen_shipment_notice,
    "payment_reminder": gen_payment_reminder,
    "after_sales": gen_follow_up,  # Reuse with different context
}


def generate(params: dict) -> dict:
    """Generate email from parameters."""
    email_type = params.get("type", "inquiry_reply")
    lang = params.get("lang", "en")

    if email_type not in GENERATORS:
        return {"error": f"Unknown email type: {email_type}", "valid_types": list(GENERATORS.keys())}

    if lang not in SUPPORTED_LANGS:
        return {"error": f"Unsupported language: {lang}", "valid_langs": SUPPORTED_LANGS}

    email_content = GENERATORS[email_type](params)
    type_info = EMAIL_TYPES.get(email_type, {})

    return {
        "type": email_type,
        "type_name": type_info.get(lang, type_info.get("en", email_type)),
        "lang": lang,
        "content": email_content,
        "timestamp": datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Cross-border Trade Email Generator")
    parser.add_argument("--type", required=True, choices=list(EMAIL_TYPES.keys()), help="Email type")
    parser.add_argument("--lang", default="en", choices=SUPPORTED_LANGS, help="Output language")
    parser.add_argument("--product", default="N/A", help="Product name")
    parser.add_argument("--qty", default="N/A", help="Quantity")
    parser.add_argument("--price", default="TBD", help="Unit price")
    parser.add_argument("--moq", default="N/A", help="Minimum order quantity")
    parser.add_argument("--lead-time", default="N/A", help="Lead time")
    parser.add_argument("--payment", default="T/T 30% deposit", help="Payment terms")
    parser.add_argument("--buyer-name", default="Customer", help="Buyer name")
    parser.add_argument("--sender-name", default="Sales Team", help="Sender name")
    parser.add_argument("--company", default="Our Company", help="Company name")
    parser.add_argument("--sample-available", default="Yes", help="Sample availability")
    parser.add_argument("--days-since-contact", type=int, default=7, help="Days since last contact")
    parser.add_argument("--vessel", default="TBD", help="Vessel/flight name")
    parser.add_argument("--etd", default="TBD", help="Estimated departure")
    parser.add_argument("--eta", default="TBD", help="Estimated arrival")
    parser.add_argument("--bl-number", default="Pending", help="Bill of lading number")
    parser.add_argument("--amount", default="N/A", help="Payment amount")
    parser.add_argument("--due-date", default="N/A", help="Payment due date")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--input", type=str, help="JSON string with all parameters")

    args = parser.parse_args()

    if args.input:
        params = json.loads(args.input)
    else:
        params = {
            "type": args.type,
            "lang": args.lang,
            "product": args.product,
            "qty": args.qty,
            "price": args.price,
            "moq": args.moq,
            "lead_time": args.lead_time,
            "payment": args.payment,
            "buyer_name": args.buyer_name,
            "sender_name": args.sender_name,
            "company": args.company,
            "sample_available": args.sample_available,
            "days_since_contact": args.days_since_contact,
            "vessel": args.vessel,
            "etd": args.etd,
            "eta": args.eta,
            "bl_number": args.bl_number,
            "amount": args.amount,
            "due_date": args.due_date,
        }

    result = generate(params)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        print(result["content"])


if __name__ == "__main__":
    main()
