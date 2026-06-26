#!/usr/bin/env python3
"""
check_sites.py - 站点可用性和响应时间检查
"""
import sys
import time
import configparser
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("ERROR: requests 库未安装。请运行: pip3 install requests")
    sys.exit(1)


def check_site(url, timeout=3):
    """检查单个站点的可用性和响应时间"""
    result = {
        "url": url,
        "status": None,
        "response_time": None,
        "error": None,
        "ok": False
    }
    start = time.time()
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        result["status"] = response.status_code
        result["response_time"] = round(time.time() - start, 2)
        result["ok"] = response.status_code == 200
        if response.status_code != 200:
            result["error"] = f"状态码 {response.status_code}"
    except requests.exceptions.Timeout:
        result["error"] = "超时"
        result["response_time"] = round(time.time() - start, 2)
    except requests.exceptions.ConnectionError as e:
        result["error"] = f"连接失败: {str(e)[:50]}"
    except Exception as e:
        result["error"] = str(e)[:80]
    return result


def load_config(config_path):
    """加载配置文件"""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def check_shop(config, shop_name, timeout=None, webhook=None):
    """检查指定店铺的站点可用性"""
    default_timeout = float(config.get(shop_name, "response_timeout", fallback=3))
    timeout = timeout or default_timeout

    base_url = config.get(shop_name, "base_url")
    check_paths_str = config.get(shop_name, "check_paths", fallback="/")
    check_paths = [p.strip() for p in check_paths_str.split(",") if p.strip()]

    results = []
    for path in check_paths:
        url = base_url.rstrip("/") + "/" + path.lstrip("/")
        r = check_site(url, timeout=timeout)
        r["path"] = path
        results.append(r)
    return results


def main():
    config_path = __file__.replace("scripts/check_sites.py", "config/shops.conf")
    config = load_config(config_path)

    # 检查所有店铺
    all_results = {}
    for shop in config.sections():
        if shop == "DEFAULT":
            continue
        results = check_shop(config, shop)
        all_results[shop] = results

    # 输出汇总
    for shop, results in all_results.items():
        shop_name = config.get(shop, "name", fallback=shop)
        print(f"\n📦 {shop_name}")
        ok_count = sum(1 for r in results if r["ok"])
        print(f"   ✅ 正常: {ok_count}/{len(results)}")
        for r in results:
            if r["ok"]:
                print(f"   - {r['path']}: {r['status']} ({r['response_time']}s)")
            else:
                err = r.get("error", f"状态码 {r.get('status')}")
                print(f"   ❌ {r['path']}: {err} ({r['response_time']}s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())