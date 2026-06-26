#!/usr/bin/env python3
"""
云端 API 认证示例 - Flask 实现
展示如何在云端 API 中使用 Bearer Token 认证
"""

from flask import Flask, request, jsonify
from functools import wraps
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from token_manager import TokenManager, init_token_manager

# 创建 Flask 应用
app = Flask(__name__)

# 初始化 Token 管理器
token_manager = init_token_manager(secret_key="your-secret-key", use_redis=False)


# ========== 认证装饰器 ==========

def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 获取 Authorization 头
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'success': False,
                'error': 'Missing Authorization header',
                'code': 'MISSING_AUTH'
            }), 401
        
        # 检查 Bearer 格式
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Invalid Authorization format. Use: Bearer <token>',
                'code': 'INVALID_AUTH_FORMAT'
            }), 401
        
        # 提取 Token
        token = auth_header.split(' ')[1]
        
        # 验证 Token
        token_data = token_manager.verify_token(token)
        
        if not token_data:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token',
                'code': 'INVALID_TOKEN'
            }), 401
        
        # 将用户信息添加到请求
        request.user = token_data
        request.token = token
        
        return f(*args, **kwargs)
    
    return decorated_function


# ========== API 路由 ==========

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    用户登录 - 获取 Token
    
    请求：
    POST /api/auth/login
    Content-Type: application/json
    
    {
        "phoneNumber": "13829295599",
        "password": "password123"  # 或其他认证方式
    }
    
    响应：
    {
        "success": true,
        "data": {
            "token": "Bearer Token",
            "expires_in": 86400,
            "user": {
                "user_id": "13829295599",
                "phone": "13829295599"
            }
        }
    }
    """
    data = request.get_json()
    
    if not data or not data.get('phoneNumber'):
        return jsonify({
            'success': False,
            'error': 'Missing phoneNumber',
            'code': 'MISSING_PARAMETER'
        }), 400
    
    phone = data['phoneNumber']
    
    # TODO: 验证用户密码（这里简化处理）
    # 实际应该查询数据库验证密码
    
    # 生成 Token
    token = token_manager.generate_token(
        user_id=phone,
        extra_data={
            'phone': phone,
            'vip_level': 1  # 示例：VIP 等级
        },
        expire_seconds=86400  # 24 小时
    )
    
    return jsonify({
        'success': True,
        'data': {
            'token': token,
            'expires_in': 86400,
            'token_type': 'Bearer',
            'user': {
                'user_id': phone,
                'phone': phone
            }
        }
    }), 200


@app.route('/api/auth/refresh', methods=['POST'])
@require_auth
def refresh_token():
    """
    刷新 Token
    
    请求：
    POST /api/auth/refresh
    Authorization: Bearer <token>
    
    响应：
    {
        "success": true,
        "data": {
            "token": "New Bearer Token",
            "expires_in": 86400
        }
    }
    """
    old_token = request.token
    
    # 刷新 Token
    new_token = token_manager.refresh_token(old_token)
    
    if not new_token:
        return jsonify({
            'success': False,
            'error': 'Failed to refresh token',
            'code': 'REFRESH_FAILED'
        }), 500
    
    return jsonify({
        'success': True,
        'data': {
            'token': new_token,
            'expires_in': 86400,
            'token_type': 'Bearer'
        }
    }), 200


@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """
    注销 - 撤销 Token
    
    请求：
    POST /api/auth/logout
    Authorization: Bearer <token>
    
    响应：
    {
        "success": true,
        "message": "Logged out successfully"
    }
    """
    token = request.token
    
    # 撤销 Token
    token_manager.revoke_token(token)
    
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200


@app.route('/api/account/query', methods=['POST'])
@require_auth
def query_account():
    """
    查询账户信息
    
    请求：
    POST /api/account/query
    Authorization: Bearer <token>
    Content-Type: application/json
    
    {
        "phoneNumber": "13829295599"
    }
    
    响应：
    {
        "success": true,
        "data": {
            "phoneNumber": "13829295599",
            "totalRecharged": 500.00,
            "balance": 20.00,
            "remainingUses": 5,
            "usedCount": 45,
            "isInsufficient": true
        }
    }
    """
    data = request.get_json()
    
    if not data or not data.get('phoneNumber'):
        return jsonify({
            'success': False,
            'error': 'Missing phoneNumber',
            'code': 'MISSING_PARAMETER'
        }), 400
    
    phone = data['phoneNumber']
    
    # 验证 Token 用户和查询用户是否一致
    if request.user['user_id'] != phone:
        return jsonify({
            'success': False,
            'error': 'Unauthorized to query this account',
            'code': 'UNAUTHORIZED'
        }), 403
    
    # TODO: 查询数据库获取账户信息
    # 这里返回模拟数据
    account_info = {
        'phoneNumber': phone,
        'totalRecharged': 500.00,
        'balance': 20.00,
        'remainingUses': 5,
        'usedCount': 45,
        'isInsufficient': True
    }
    
    return jsonify({
        'success': True,
        'data': account_info
    }), 200


@app.route('/api/account/recharge', methods=['POST'])
@require_auth
def create_recharge_order():
    """
    创建充值订单
    
    请求：
    POST /api/account/recharge
    Authorization: Bearer <token>
    Content-Type: application/json
    
    {
        "phoneNumber": "13829295599",
        "amount": 30,
        "packageType": "标准套餐",
        "package": {
            "amount": 30,
            "uses": 1200,
            "name": "标准套餐"
        }
    }
    
    响应：
    {
        "success": true,
        "data": {
            "orderId": "CLOUD_13829295599_20260428210001",
            "amount": 30,
            "uses": 1200,
            "alipayParams": {...},
            "cashierUrl": "https://..."
        }
    }
    """
    data = request.get_json()
    
    if not data or not data.get('phoneNumber'):
        return jsonify({
            'success': False,
            'error': 'Missing phoneNumber',
            'code': 'MISSING_PARAMETER'
        }), 400
    
    phone = data['phoneNumber']
    
    # 验证 Token 用户和充值用户是否一致
    if request.user['user_id'] != phone:
        return jsonify({
            'success': False,
            'error': 'Unauthorized to recharge this account',
            'code': 'UNAUTHORIZED'
        }), 403
    
    # TODO: 创建充值订单
    # 这里返回模拟数据
    import time
    order_id = f"CLOUD_{phone}_{int(time.time())}"
    
    return jsonify({
        'success': True,
        'data': {
            'orderId': order_id,
            'amount': data.get('amount', 0),
            'uses': data.get('package', {}).get('uses', 0),
            'packageType': data.get('packageType', ''),
            'alipayParams': {},
            'cashierUrl': 'https://excashier.alipay.com/pc.htm?...'
        }
    }), 200


@app.route('/api/payment/notify', methods=['POST'])
def payment_notify():
    """
    支付宝支付回调通知
    
    请求：
    POST /api/payment/notify
    Content-Type: application/x-www-form-urlencoded
    
    支付宝返回的参数
    
    响应：
    success 或 fail
    """
    # 获取支付宝回调参数
    data = request.form.to_dict()
    
    # TODO: 验证支付宝签名
    # TODO: 更新订单状态
    # TODO: 更新账户余额
    
    # 返回成功
    return 'success', 200


@app.route('/api/auth/stats', methods=['GET'])
@require_auth
def get_token_stats():
    """
    获取 Token 统计信息
    
    请求：
    GET /api/auth/stats
    Authorization: Bearer <token>
    
    响应：
    {
        "success": true,
        "data": {
            "storage": "Memory",
            "active_tokens": 10,
            "blacklisted_tokens": 2
        }
    }
    """
    stats = token_manager.get_stats()
    
    return jsonify({
        'success': True,
        'data': stats
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'message': 'API is running'
    }), 200


# ========== 启动应用 ==========

if __name__ == '__main__':
    print("\n\n")
    print("=" * 80)
    print("云端 API 认证服务器")
    print("=" * 80)
    
    print("\n📋 API 路由：")
    print("  POST /api/auth/login      - 用户登录（获取 Token）")
    print("  POST /api/auth/refresh    - 刷新 Token")
    print("  POST /api/auth/logout     - 注销（撤销 Token）")
    print("  POST /api/account/query   - 查询账户（需要认证）")
    print("  POST /api/account/recharge - 创建充值订单（需要认证）")
    print("  POST /api/payment/notify  - 支付宝支付回调")
    print("  GET  /api/auth/stats      - Token 统计（需要认证）")
    print("  GET  /health              - 健康检查")
    
    print("\n🧪 测试命令：")
    print("\n# 1. 登录获取 Token")
    print('curl -X POST http://localhost:5000/api/auth/login \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"phoneNumber": "13829295599"}\'')
    
    print("\n# 2. 查询账户（使用 Token）")
    print('curl -X POST http://localhost:5000/api/account/query \\')
    print('  -H "Authorization: Bearer <token>" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"phoneNumber": "13829295599"}\'')
    
    print("\n# 3. 创建充值订单")
    print('curl -X POST http://localhost:5000/api/account/recharge \\')
    print('  -H "Authorization: Bearer <token>" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"phoneNumber": "13829295599", "amount": 30, "packageType": "标准套餐"}\'')
    
    print("\n" + "=" * 80)
    
    # 启动 Flask 应用
    app.run(host='0.0.0.0', port=5000, debug=True)
