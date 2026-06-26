import json, os, sys, hashlib, time
sys.path.insert(0, os.path.expanduser('~/v19_cognition/v101/alipay'))
sys.path.insert(0, os.path.expanduser('~/v19_cognition/v83/clawtip_skill/scripts'))

PRICING_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pricing.json')

def get_price(task_type):
    with open(PRICING_FILE, 'r') as f:
        pricing = json.load(f)
    return pricing.get(task_type, None)

def verify_payment(task_type, payment_credential):
    """验证支付凭证并确认金额正确"""
    price = get_price(task_type)
    if price is None:
        return {"status": "error", "message": "不支持的任务类型"}

    if not payment_credential or 'payStatus' not in payment_credential:
        return {"status": "error", "message": "缺少支付凭证"}

    if payment_credential.get('payStatus') != 'SUCCESS':
        return {"status": "error", "message": "支付未成功"}

    if abs(payment_credential.get('paidAmount', 0) - price) > 0.001:
        return {"status": "error", "message": "支付金额不匹配"}

    return {"status": "verified", "price": price, "transaction_id": payment_credential.get('transactionId', '')}
