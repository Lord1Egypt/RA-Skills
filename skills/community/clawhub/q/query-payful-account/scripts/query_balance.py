#!/usr/bin/env python3
"""
Payful Account Balance Query Script

Queries user account balance from Payful API.
Requires PAYFUL_TOKEN and PAYFUL_USER_ID environment variables.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any


def get_env_var(name: str) -> str:
    """Get required environment variable."""
    value = os.environ.get(name)
    if not value:
        print(f"Error: {name} environment variable is not set", file=sys.stderr)
        print(f"Please set {name} and try again", file=sys.stderr)
        sys.exit(1)
    return value


def is_success_code(code: Any) -> bool:
    """Check if API response code indicates success."""
    code_str = str(code) if code is not None else ""
    return code_str in ("0000", "000000", "0", "success", "SUCCESS")


def query_balance(api_url: Optional[str] = None) -> dict:
    """Query Payful account balance."""
    base_url = api_url or "https://global.payful.com"
    endpoint = f"{base_url}/api/user/account/queryUserAccBalByHomePage"
    
    user_id = get_env_var("PAYFUL_USER_ID")
    token = get_env_var("PAYFUL_TOKEN")
    cookie = f"AGL_USER_ID={user_id}; BF-INTERNATIONAL-MEMBER-TOKEN={token}"
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Referer': f"{base_url}/account/userAccount",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'request-system-name': 'member-exchange-client',
    }
    
    req = urllib.request.Request(endpoint, headers=headers, method='GET')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def get_result_data(data: dict) -> dict:
    """Extract result data from API response."""
    # Payful uses 'result' field
    if "result" in data and isinstance(data["result"], dict):
        return data["result"]
    # Fallback to 'data' field
    if "data" in data and isinstance(data["data"], dict):
        return data["data"]
    return {}


def parse_accounts(data: dict) -> List[Dict]:
    """Extract account balances from API response."""
    accounts = []
    result = get_result_data(data)
    
    # Exchange account (汇兑账户)
    ex_bal = result.get("exchangeBal", 0)
    ex_avail = result.get("exAvailableBal", 0)
    ex_frozen = result.get("exFrozenBal", 0)
    ex_ccy = result.get("exchangeCcy", "USD")
    
    if ex_bal > 0 or ex_avail > 0 or ex_frozen > 0:
        accounts.append({
            "type": "汇兑账户",
            "ccy": ex_ccy,
            "ccy_str": "美元" if ex_ccy == "USD" else ex_ccy,
            "balance": float(ex_bal),
            "available": float(ex_avail),
            "frozen": float(ex_frozen),
        })
    
    # Individual accounts
    for acc in result.get("accountBalVos", []):
        ccy = acc.get("ccy", "")
        if ccy == ex_ccy:
            continue
        
        bal = acc.get("currentBalance", 0) or 0
        avail = acc.get("payeeAvailableBal", 0) or 0
        frozen = acc.get("frozenBal", 0) or 0
        
        if bal > 0 or avail > 0 or frozen > 0:
            accounts.append({
                "type": "收款账户",
                "ccy": ccy,
                "ccy_str": acc.get("ccyStr", ccy),
                "balance": float(bal),
                "available": float(avail),
                "frozen": float(frozen),
            })
    
    return accounts


def format_balance(data: dict) -> str:
    """Format balance for display."""
    if not is_success_code(data.get("code", "")):
        msg = data.get("message") or data.get("msg", "Unknown error")
        return f"❌ 查询失败: {msg}"
    
    accounts = parse_accounts(data)
    if not accounts:
        return "✅ 查询成功\n\n暂无余额信息"
    
    lines = [
        "═══════════════════════════════════════",
        "         💰 宝付账户余额",
        "═══════════════════════════════════════",
        ""
    ]
    
    usd_available = 0.0
    for acc in accounts:
        lines.append(f"【{acc['type']}】{acc['ccy_str']} ({acc['ccy']})")
        lines.append(f"  可用余额: {acc['available']:,.2f}")
        lines.append(f"  冻结金额: {acc['frozen']:,.2f}")
        lines.append(f"  账户总额: {acc['balance']:,.2f}")
        lines.append("")
        if acc['ccy'] == 'USD':
            usd_available = acc['available']
    
    lines.extend([
        "═══════════════════════════════════════",
        f"💵 美元可用余额: {usd_available:,.2f} USD",
        "═══════════════════════════════════════"
    ])
    
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Query Payful account balance')
    parser.add_argument('--api-url', help='Custom API base URL')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    parser.add_argument('--raw', action='store_true', help='Output raw response')
    args = parser.parse_args()
    
    result = query_balance(args.api_url)
    
    if args.raw:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.json:
        print(json.dumps({
            "success": is_success_code(result.get("code", "")),
            "accounts": parse_accounts(result)
        }, indent=2, ensure_ascii=False))
    else:
        print(format_balance(result))


if __name__ == "__main__":
    main()
