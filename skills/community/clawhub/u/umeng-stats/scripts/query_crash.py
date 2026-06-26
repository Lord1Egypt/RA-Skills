#!/usr/bin/env python3
"""Query Umeng U-APM crash stats and U-App analytics."""
import hmac
import hashlib
import urllib.parse
import json
import sys
from datetime import datetime, timedelta

CONFIG_PATH = "/Users/zhangjing/.openclaw/workspace/skills/umeng-crash-stats/config.json"

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def sign(api_key, api_security, service, method_name, params):
    url_path = f"param2/1/{service}/{method_name}/{api_key}"
    sorted_keys = sorted(params.keys())
    param_str = ""
    for k in sorted_keys:
        param_str += f"{k}{params[k]}"
    s = url_path + param_str
    signature = hmac.new(
        api_security.encode("utf-8"),
        s.encode("utf-8"),
        hashlib.sha1
    ).hexdigest().upper()
    return url_path, signature

def call_api(config, service, method_name, params):
    import urllib.request
    api_key = config["apiKey"]
    api_security = config["apiSecurity"]
    url_path, signature = sign(api_key, api_security, service, method_name, params)
    sorted_params = dict(sorted(params.items()))
    query = urllib.parse.urlencode(sorted_params)
    full_url = f"https://gateway.open.umeng.com/openapi/{url_path}?{query}&_aop_signature={signature}"
    req = urllib.request.Request(full_url)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

TYPE_MAP = {
    "all": "0", "全部": "0", "0": "0",
    "java": "1", "ios": "1", "Java": "1", "iOS": "1", "1": "1",
    "native": "2", "Native": "2", "2": "2",
    "anr": "3", "ANR": "3", "3": "3",
    "custom": "4", "自定义": "4", "4": "4",
    "freeze": "5", "卡顿": "5", "5": "5",
}

def resolve_type(type_str):
    return TYPE_MAP.get(str(type_str).lower().strip(), "0")

def resolve_app(config, app_arg):
    apps = config.get("apps", {})
    # Exact match
    if app_arg in apps:
        return app_arg, apps[app_arg]
    # Case-insensitive match
    for name, key in apps.items():
        if name.lower() == app_arg.lower():
            return name, key
    # Assume raw appKey
    return app_arg, app_arg

def query_crash(config, app_name, app_key, start_date, end_date, crash_type, days):
    method = "umeng.quickbird.server.getStatTrend"
    params = {
        "dataSourceId": app_key,
        "type": resolve_type(crash_type),
        "startDate": start_date,
        "endDate": end_date,
    }
    result = call_api(config, "com.umeng.uapm", method, params)
    
    if "data" not in result:
        print(f"Error: {json.dumps(result, ensure_ascii=False)}")
        sys.exit(1)
    
    data = result["data"]
    total_errors = sum(d.get("errorCount", 0) for d in data)
    total_affected = sum(d.get("affectedUserCount", 0) for d in data)
    
    print(f"\n📊 友盟 U-APM 崩溃统计")
    print(f"   App: {app_name} ({app_key})")
    print(f"   日期: {start_date}" + (f" ~ {end_date}" if days > 1 else ""))
    print(f"   类型: {crash_type}")
    print(f"   总崩溃次数: {total_errors:,}")
    print(f"   总影响用户: {total_affected:,}")
    
    if data:
        peak = max(data, key=lambda d: d.get("errorCount", 0))
        print(f"   峰值时段: {peak.get('timePoint', 'N/A')} ({peak.get('errorCount', 0):,} 次)")
    
    print(f"\n{'时段':<10} {'崩溃次数':>10} {'影响用户':>10} {'错误率':>10}")
    print("-" * 42)
    for d in data:
        tp = d.get("timePoint", "")
        ec = d.get("errorCount", 0)
        au = d.get("affectedUserCount", 0)
        er = d.get("errorRate", 0)
        print(f"{tp:<10} {ec:>10,} {au:>10,} {er:>10.1f}")
    print()

def query_today_data(config, app_name, app_key):
    result = call_api(config, "com.umeng.uapp", "umeng.uapp.getTodayData", {"appkey": app_key})
    td = result.get("todayData", {})
    print(f"\n📊 友盟 U-App 今日实时数据")
    print(f"   App: {app_name} ({app_key})")
    print(f"   日期: {td.get('date', 'N/A')}")
    print(f"   新增用户: {td.get('newUsers', 0):,}")
    print(f"   活跃用户: {td.get('activityUsers', 0):,}")
    print(f"   启动次数: {td.get('launches', 0):,}")
    print(f"   累计用户: {td.get('totalUsers', 0):,}")
    print()

def query_yesterday_data(config, app_name, app_key):
    result = call_api(config, "com.umeng.uapp", "umeng.uapp.getYesterdayData", {"appkey": app_key})
    yd = result.get("yesterdayData", {})
    print(f"\n📊 友盟 U-App 昨日统计数据")
    print(f"   App: {app_name} ({app_key})")
    print(f"   日期: {yd.get('date', 'N/A')}")
    print(f"   新增用户: {yd.get('newUsers', 0):,}")
    print(f"   活跃用户: {yd.get('activityUsers', 0):,}")
    print(f"   启动次数: {yd.get('launches', 0):,}")
    print(f"   累计用户: {yd.get('totalUsers', 0):,}")
    print()

def query_all_app_data(config):
    result = call_api(config, "com.umeng.uapp", "umeng.uapp.getAllAppData", {})
    ad = result.get("allAppData", [])
    if not ad:
        print("No data returned")
        return
    d = ad[0]
    print(f"\n📊 友盟 U-App 全产品汇总")
    print(f"   昨日活跃用户: {d.get('yesterdayActivityUsers', 0):,} (去重: {d.get('yesterdayUniqActiveUsers', 0):,})")
    print(f"   昨日新增用户: {d.get('yesterdayNewUsers', 0):,} (去重: {d.get('yesterdayUniqNewUsers', 0):,})")
    print(f"   昨日启动次数: {d.get('yesterdayLaunches', 0):,}")
    print(f"   今日活跃用户: {d.get('todayActivityUsers', 0):,}")
    print(f"   今日新增用户: {d.get('todayNewUsers', 0):,}")
    print(f"   今日启动次数: {d.get('todayLaunches', 0):,}")
    print(f"   累计用户: {d.get('totalUsers', 0):,}")
    print()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Query Umeng stats")
    parser.add_argument("--app", help="App name or appKey")
    parser.add_argument("--date", default="yesterday", help="Date (YYYY-MM-DD) or 'today'/'yesterday'")
    parser.add_argument("--type", default="yesterday", help="Query type: crash/today/yesterday/allapps")
    parser.add_argument("--crash-type", default="all", help="Crash type: all/java/ios/native/anr/custom/freeze")
    parser.add_argument("--days", type=int, default=1, help="Number of days (max 90)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--list-apps", action="store_true", help="List configured apps")
    args = parser.parse_args()

    config = load_config()

    if args.list_apps:
        for name, key in config.get("apps", {}).items():
            print(f"  {name}: {key}")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    if args.date == "today":
        start_date = today
    elif args.date == "yesterday":
        start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        start_date = args.date
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=args.days - 1)).strftime("%Y-%m-%d")

    if args.type == "allapps":
        result = call_api(config, "com.umeng.uapp", "umeng.uapp.getAllAppData", {})
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            query_all_app_data(config)
        return

    if not args.app:
        print("Error: --app is required (use --list-apps to see available apps)")
        sys.exit(1)

    app_name, app_key = resolve_app(config, args.app)

    if args.type == "crash":
        result = call_api(config, "com.umeng.uapm", "umeng.quickbird.server.getStatTrend", {
            "dataSourceId": app_key,
            "type": resolve_type(args.crash_type),
            "startDate": start_date,
            "endDate": end_date,
        })
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            data = result.get("data", [])
            total_errors = sum(d.get("errorCount", 0) for d in data)
            total_affected = sum(d.get("affectedUserCount", 0) for d in data)
            print(f"\n📊 友盟 U-APM 崩溃统计")
            print(f"   App: {app_name} ({app_key})")
            print(f"   日期: {start_date}" + (f" ~ {end_date}" if args.days > 1 else ""))
            print(f"   类型: {args.crash_type}")
            print(f"   总崩溃次数: {total_errors:,}")
            print(f"   总影响用户: {total_affected:,}")
            if data:
                peak = max(data, key=lambda d: d.get("errorCount", 0))
                print(f"   峰值时段: {peak.get('timePoint', 'N/A')} ({peak.get('errorCount', 0):,} 次)")
            print(f"\n{'时段':<10} {'崩溃次数':>10} {'影响用户':>10} {'错误率':>10}")
            print("-" * 42)
            for d in data:
                tp = d.get("timePoint", "")
                ec = d.get("errorCount", 0)
                au = d.get("affectedUserCount", 0)
                er = d.get("errorRate", 0)
                print(f"{tp:<10} {ec:>10,} {au:>10,} {er:>10.1f}")
            print()
    elif args.type == "today":
        result = call_api(config, "com.umeng.uapp", "umeng.uapp.getTodayData", {"appkey": app_key})
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            query_today_data(config, app_name, app_key)
    elif args.type == "yesterday":
        result = call_api(config, "com.umeng.uapp", "umeng.uapp.getYesterdayData", {"appkey": app_key})
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            query_yesterday_data(config, app_name, app_key)

if __name__ == "__main__":
    main()
