#!/usr/bin/env python3
"""
跨境魔方认证管理
提供 API 密钥申请、充值等功能。
"""
import argparse
import os
import sys
from common import (
    print_json_output, make_request, API_KEY_ENV, UPKUAJING_ENV_FILE, UPKUAJING_DIR, SKILL_BASE_DIR,
    normalize_plan_windows, format_plan_time
)


ACCOUNT_CENTER_URL = "https://developer.upkuajing.com/account/"
RECHARGE_CENTER_URL = "https://developer.upkuajing.com/recharge.html"


def mask_api_key(api_key: str) -> str:
    """返回可安全展示的 API Key 脱敏值。"""
    if len(api_key) <= 8:
        return "*" * len(api_key)
    return f"{api_key[:4]}...{api_key[-4:]}"


def get_local_api_key():
    """检测本地 API Key，并返回 (key, source)。此函数不发起网络请求。"""
    env_key = os.environ.get(API_KEY_ENV, '').strip()
    if env_key:
        return env_key, 'environment'

    if UPKUAJING_ENV_FILE.exists():
        try:
            with open(UPKUAJING_ENV_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    if key.strip() == API_KEY_ENV and value.strip():
                        return value.strip(), str(UPKUAJING_ENV_FILE)
        except IOError:
            pass

    return None, None


def normalize_balance(value) -> int:
    """将服务端返回的分钱余额转换为整数，异常值按 0 处理。"""
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def format_account_status(data: dict) -> dict:
    """格式化绑定状态、双余额和扣款顺序，供 Agent 直接向用户说明。"""
    org_phone = data.get('orgPhone', '')
    user_id = data.get('userId') or data.get('user_id')
    api_balance = normalize_balance(data.get('apiBalance', 0))
    org_balance = normalize_balance(data.get('orgBalance', 0))
    is_bound = bool(user_id or org_phone)

    if is_bound:
        deduction_order = ['API余额', '跨境魔方账号余额']
        if api_balance > 0 and org_balance > 0:
            balance_message = (
                f"当前API余额为{api_balance}分钱，跨境魔方账号余额为{org_balance}分钱。"
                "查询费用会先从API余额扣除，API余额不足后再从跨境魔方账号余额扣除。"
            )
            needs_recharge = False
        elif api_balance <= 0 and org_balance > 0:
            balance_message = (
                f"当前API余额为0分钱，跨境魔方账号余额为{org_balance}分钱。"
                "无需仅因API余额为0而充值，后续查询费用会从跨境魔方账号余额扣除。"
            )
            needs_recharge = False
        elif api_balance > 0:
            balance_message = (
                f"当前API余额为{api_balance}分钱，跨境魔方账号余额为0分钱。"
                "查询费用会先从API余额扣除；API余额用尽后需要充值。"
            )
            needs_recharge = False
        else:
            balance_message = "当前API余额和跨境魔方账号余额均为0分钱，需要充值后才能执行收费查询。"
            needs_recharge = True
    else:
        deduction_order = ['API余额']
        if api_balance > 0:
            balance_message = f"当前独立API Key余额为{api_balance}分钱，查询费用只从API余额扣除。"
            needs_recharge = False
        else:
            balance_message = "当前独立API Key余额为0分钱，需要充值后才能执行收费查询。"
            needs_recharge = True

    plan = data.get('plan')
    if isinstance(plan, dict):
        plan_available = None if plan.get('available') is None else plan.get('available') in (1, True, '1')
        if plan_available is True:
            plan_message = '当前套餐可用'
        elif plan_available is False:
            plan_message = '当前无有效套餐'
        else:
            plan_message = '套餐状态未知（接口未返回 available）'
        plan_detail = plan
    else:
        plan_available = None
        plan_message = '接口未返回套餐信息，可用 auth.py --plan_quota 查询额度'
        plan_detail = {}

    return {
        'isBoundToUpKuaJingAccount': is_bound,
        'bindingStatus': '已绑定跨境魔方账号' if is_bound else '未绑定跨境魔方账号',
        'userId': user_id or '',
        'orgPhone': org_phone,
        'apiAccount': data.get('apiAccount', ''),
        'apiBalanceFen': api_balance,
        'orgBalanceFen': org_balance,
        'usableBalanceFen': api_balance + org_balance if is_bound else api_balance,
        'deductionOrder': deduction_order,
        'needsRecharge': needs_recharge,
        'balanceMessage': balance_message,
        'planAvailable': plan_available,
        'planMessage': plan_message,
        'plan': plan_detail,
        'bindingUrl': ACCOUNT_CENTER_URL,
        'rechargeUrl': RECHARGE_CENTER_URL,
    }


def key_status() -> dict:
    """检测本地 API Key，并在存在时查询有效性、绑定状态和双余额。"""
    api_key, source = get_local_api_key()
    if not api_key:
        return {
            'hasApiKey': False,
            'apiKeyValid': False,
            'message': '未检测到本地API Key。',
            'bindingUrl': ACCOUNT_CENTER_URL,
        }

    base_result = {
        'hasApiKey': True,
        'maskedApiKey': mask_api_key(api_key),
        'apiKeySource': source,
    }
    response = make_request('/agent/auth/info', {}, api_key=api_key)
    if response.get('code') != 0:
        base_result.update({
            'apiKeyValid': False,
            'message': f"检测到本地API Key，但验证失败：{response.get('msg', '未知错误')}。",
            'bindingUrl': ACCOUNT_CENTER_URL,
        })
        return base_result

    base_result.update({
        'apiKeyValid': True,
        'message': '已检测到有效的本地API Key。',
    })
    base_result.update(format_account_status(response.get('data', {})))
    return base_result


def new_key() -> dict:
    """
    申请新的 API 密钥。
    """
    env_file = UPKUAJING_ENV_FILE
    existing_key, source = get_local_api_key()
    if existing_key:
        return {
            "success": False,
            "hasApiKey": True,
            "maskedApiKey": mask_api_key(existing_key),
            "message": f"已检测到本地API密钥（{mask_api_key(existing_key)}），来源：{source}。请先使用 --key_status 检查现有密钥。",
            "envFilePath": str(env_file)
        }

    # 不需要认证申请新密钥
    response = make_request('/agent/auth/create', {}, require_auth=False)

    # 检查是否申请成功
    if response.get('code') != 0:
        error_msg = response.get('msg', '未知错误')
        return {
            "success": False,
            "message": f"API密钥申请失败：{error_msg}。请稍后重试或联系技术支持。"
        }

    # 提取 apiKey
    data = response.get('data', {})
    api_key = data.get('apiKey')

    if not api_key:
        return {
            "success": False,
            "message": "API密钥申请失败：服务器响应格式异常，未返回apiKey。"
        }

    # 确保 ~/.upkuajing 目录存在
    try:
        UPKUAJING_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return {
            "success": False,
            "message": f"API密钥申请成功，但创建目录失败：{str(e)}。\n请手动创建目录 {UPKUAJING_DIR} 并设置环境变量 {API_KEY_ENV}。",
            "envFilePath": str(env_file)
        }

    # 保存到 .env 文件
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(f"{API_KEY_ENV}={api_key}\n")
        os.chmod(env_file, 0o600)
    except IOError as e:
        return {
            "success": False,
            "message": f"API密钥申请成功，但保存到 .env 文件失败：{str(e)}。\n请手动设置环境变量 {API_KEY_ENV}。",
            "envFilePath": str(env_file)
        }

    # 返回成功结果
    return {
        "success": True,
        "hasApiKey": True,
        "maskedApiKey": mask_api_key(api_key),
        "message": f"API密钥申请成功，已保存到：{env_file}。请勿在对话中公开完整密钥。",
        "envFilePath": str(env_file),
        "bindingUrl": ACCOUNT_CENTER_URL,
        "nextStep": "如果用户已有跨境魔方账号，请打开 bindingUrl，在账户中心的 API Key 管理中完成绑定，然后运行 --key_status 复查。"
    }


def account_info() -> dict:
    """
    获取账户信息并格式化返回
    """
    return key_status()


def plan_quota() -> dict:
    """
    查询当前账号的套餐额度用量（POST /agent/plan/quota）。
    """
    response = make_request('/agent/plan/quota', {})

    if response.get('code') != 0:
        return response

    data = response.get('data')
    if not isinstance(data, dict):
        data = {}
    available = data.get('available')
    windows = []
    for window in normalize_plan_windows(data.get('windows')):
        windows.append({
            'window': window.get('window'),
            'capability': window.get('capability'),
            'quotaType': window.get('quotaType'),
            'limit': window.get('limit'),
            'used': window.get('used'),
            'remaining': window.get('remaining'),
            'resetsAt': window.get('resetsAt'),
            'resetsAtText': format_plan_time(window.get('resetsAt'))
        })

    return {
        'available': available,
        'availableText': (
            '套餐状态未知' if available is None
            else ('套餐可用' if available in (1, True, '1') else '无可用套餐')
        ),
        'windows': windows,
        'guidance': '目标窗口 remaining=0 时套餐调用会返回额度不足；'
                    '可改用余额（设置 UPKUAJING_PLAN_MODE=1）或查看 --plan_config 升级档位',
        'requestId': response.get('requestId')
    }


def plan_config() -> dict:
    """
    查询各套餐档位的额度上限（POST /agent/plan/config，免鉴权）。
    """
    return make_request('/agent/plan/config', {}, require_auth=False)


def new_rec_order() -> dict:
    """
    创建充值订单，返回支付地址
    """
    response = make_request('/agent/auth/pay/url', {})
    return response


def price_info() -> dict:
    """
    获取开放平台接口定价信息
    """
    skill_name = os.path.basename(SKILL_BASE_DIR)
    response = make_request('/agent/api/list', {"name": skill_name})
    return response


def main():
    parser = argparse.ArgumentParser(
        description='跨境魔方认证管理'
    )
    parser.add_argument(
        '--new_key',
        action='store_true',
        help='申请新的 API 密钥'
    )
    parser.add_argument(
        '--account_info',
        action='store_true',
        help='获取当前账户信息'
    )
    parser.add_argument(
        '--key_status',
        action='store_true',
        help='检测本地API Key、绑定状态、API余额和跨境魔方账号余额'
    )
    parser.add_argument(
        '--new_rec_order',
        action='store_true',
        help='创建充值订单'
    )
    parser.add_argument(
        '--price_info',
        action='store_true',
        help='获取开放平台接口定价信息'
    )

    parser.add_argument(
        '--plan_quota',
        action='store_true',
        help='查询当前账号的套餐额度用量'
    )
    parser.add_argument(
        '--plan_config',
        action='store_true',
        help='查询各套餐档位的额度上限（免鉴权）'
    )

    args = parser.parse_args()

    # 验证至少指定一个操作
    action_count = sum([
        args.new_key,
        args.account_info,
        args.key_status,
        args.new_rec_order,
        args.price_info,
        args.plan_quota,
        args.plan_config,
    ])

    if action_count == 0:
        print("错误：请指定要执行的操作", file=sys.stderr)
        print("可用操作：--new_key, --key_status, --account_info, --new_rec_order, --price_info, --plan_quota, --plan_config", file=sys.stderr)
        sys.exit(1)

    if action_count > 1:
        print("错误：一次只能执行一个操作", file=sys.stderr)
        sys.exit(1)

    # 执行相应的操作
    if args.new_key:
        result = new_key()
        print_json_output(result)

    elif args.account_info or args.key_status:
        result = account_info()
        print_json_output(result)

    elif args.new_rec_order:
        result = new_rec_order()
        print_json_output(result)

    elif args.price_info:
        result = price_info()
        print_json_output(result)

    elif args.plan_quota:
        result = plan_quota()
        print_json_output(result)

    elif args.plan_config:
        result = plan_config()
        print_json_output(result)


if __name__ == '__main__':
    main()
