#!/usr/bin/env python3
"""实战 59 支付系统 (2026-06-16)
- 订单管理: 创建/查询/取消
- 支付宝: 沙箱/真接 (待犀牛提供 APPID 后切换)
- 端点: /v1/pay/{create,query,cancel,callback,orders}
- 状态机: pending -> paid -> active / cancelled / refunded
"""
import os
import json
import time
import secrets
from pathlib import Path
from typing import Optional, Dict, List

ORDERS_FILE = Path('/home/ubuntu/star-search/orders.json')

# 支付宝配置 (实战 59 阶段: 沙箱模式, 实际付款二维码 mock)
ALIPAY_CONFIG = {
    'app_id': os.environ.get('ALIPAY_APP_ID', 'SANDBOX_PENDING'),
    'private_key': os.environ.get('ALIPAY_PRIVATE_KEY', ''),
    'public_key': os.environ.get('ALIPAY_PUBLIC_KEY', ''),
    'sign_type': 'RSA2',
    'gateway': 'https://openapi.alipaydev.com/gateway.do',  # 沙箱
    'notify_url': 'https://search.token-star.cn/v1/pay/callback',
    'return_url': 'https://search.token-star.cn/pricing.html?status=success',
}

# 套餐定义
TIERS = {
    'basic': {
        'name': '基础会员',
        'price': 29,
        'period_days': 30,
        'quota_per_period': 1000,
        'period_type': 'month',
    },
    'pro': {
        'name': 'Pro 会员',
        'price': 299,
        'period_days': 365,
        'quota_per_period': 10000,
        'period_type': 'year',
    },
}


def _load_orders() -> Dict:
    if not ORDERS_FILE.exists():
        return {'orders': {}}
    try:
        with open(ORDERS_FILE) as f:
            return json.load(f)
    except Exception:
        return {'orders': {}}


def _save_orders(data: Dict):
    ORDERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ORDERS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_order(user_id: str, tier: str, amount: int) -> Dict:
    """实战 59: 创建订单
    - 验证 tier
    - 生成 order_id
    - 返回支付 URL (沙箱模式返 mock URL)
    """
    if tier not in TIERS:
        return {'error': f'unknown tier: {tier}'}
    tier_info = TIERS[tier]
    if amount != tier_info['price']:
        return {'error': f'amount mismatch: expected {tier_info["price"]}, got {amount}'}

    order_id = f'SS{int(time.time())}{secrets.token_hex(4).upper()}'
    order = {
        'order_id': order_id,
        'user_id': user_id,
        'tier': tier,
        'amount': amount,
        'status': 'pending',  # pending / paid / active / cancelled / refunded / expired
        'created_at': int(time.time()),
        'paid_at': None,
        'activated_at': None,
        'expire_at': None,
        'tier_info': tier_info,
    }
    data = _load_orders()
    data['orders'][order_id] = order
    _save_orders(data)

    # 实战 59: 沙箱模式 - 返 mock pay_url (待接真支付宝后改)
    if ALIPAY_CONFIG['app_id'] == 'SANDBOX_PENDING':
        # 沙箱模式: 返本地 callback URL (让用户直接点 "我已支付" 模拟)
        pay_url = f'https://search.token-star.cn/pricing.html?order_id={order_id}&status=mock'
    else:
        # 真接支付宝 (待实现)
        pay_url = f'{ALIPAY_CONFIG["gateway"]}?out_trade_no={order_id}&total={amount}'

    return {
        'order_id': order_id,
        'amount': amount,
        'tier': tier,
        'status': 'pending',
        'pay_url': pay_url,
        'sandbox_mode': ALIPAY_CONFIG['app_id'] == 'SANDBOX_PENDING',
        'created_at': order['created_at'],
    }


def query_order(order_id: str, user_id: str = None) -> Optional[Dict]:
    data = _load_orders()
    order = data['orders'].get(order_id)
    if not order:
        return None
    if user_id and order['user_id'] != user_id:
        return None
    return order


def cancel_order(order_id: str, user_id: str) -> Dict:
    data = _load_orders()
    order = data['orders'].get(order_id)
    if not order:
        return {'error': 'order not found'}
    if order['user_id'] != user_id:
        return {'error': 'not your order'}
    if order['status'] not in ['pending']:
        return {'error': f'cannot cancel: status={order["status"]}'}
    order['status'] = 'cancelled'
    order['cancelled_at'] = int(time.time())
    _save_orders(data)
    return {'order_id': order_id, 'status': 'cancelled'}


def list_orders(user_id: str, limit: int = 20) -> List[Dict]:
    data = _load_orders()
    orders = [o for o in data['orders'].values() if o['user_id'] == user_id]
    orders.sort(key=lambda x: x['created_at'], reverse=True)
    return orders[:limit]


def mark_paid(order_id: str, trade_no: str = '') -> Dict:
    """实战 59: 标记订单已支付 (沙箱模式: 用户手动触发)
    真接后: 由支付宝回调触发
    """
    data = _load_orders()
    order = data['orders'].get(order_id)
    if not order:
        return {'error': 'order not found'}
    if order['status'] != 'pending':
        return {'error': f'order status: {order["status"]}'}

    now = int(time.time())
    order['status'] = 'active'
    order['paid_at'] = now
    order['activated_at'] = now
    order['expire_at'] = now + order['tier_info']['period_days'] * 86400
    order['trade_no'] = trade_no or f'MOCK_TRADE_{order_id}'

    # 更新用户 tier (调用 user_auth)
    try:
        import user_auth as _ua
        users_file = Path('/home/ubuntu/star-search/users.json')
        if users_file.exists():
            with open(users_file) as f:
                ud = json.load(f)
            for u in ud.get('users', {}).values():
                if u['user_id'] == order['user_id']:
                    u['tier'] = order['tier']
                    u['tier_expire_at'] = order['expire_at']
                    u['tier_started_at'] = now
                    with open(users_file, 'w') as f:
                        json.dump(ud, f, indent=2, ensure_ascii=False)
                    break
    except Exception as e:
        order['upgrade_error'] = str(e)

    _save_orders(data)
    return {
        'order_id': order_id,
        'status': 'active',
        'tier': order['tier'],
        'expire_at': order['expire_at'],
    }


def alipay_callback(params: Dict) -> Dict:
    """实战 59: 支付宝异步回调
    沙箱模式: 直接 trust params
    真接: 验证 sign + verify via alipay SDK
    """
    order_id = params.get('out_trade_no', '')
    trade_status = params.get('trade_status', '')
    trade_no = params.get('trade_no', '')

    if trade_status in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
        result = mark_paid(order_id, trade_no)
        return {'code': 'success', 'message': 'paid', 'result': result}
    return {'code': 'fail', 'message': f'trade_status={trade_status}'}
