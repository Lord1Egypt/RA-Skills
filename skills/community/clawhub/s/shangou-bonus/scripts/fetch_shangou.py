#!/usr/bin/env python3
"""
淘宝闪购每日福利查询脚本

从聚满减API获取当日最新的淘宝闪购福利活动信息。
API地址: https://v.jumanjian.com/api/
"""

import json
import sys
from pathlib import Path

try:
    import urllib.request
    import urllib.error
except ImportError:
    print("错误: 无法导入 urllib 模块")
    sys.exit(1)


# API 配置
API_URL = "https://v.jumanjian.com/api/"
DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_FILE = DATA_DIR / "latest.json"


def fetch_shangou_data():
    """从API获取淘宝闪购福利数据"""
    try:
        req = urllib.request.Request(
            API_URL,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.URLError as e:
        print(f"网络请求失败: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None


def save_cache(data):
    """保存数据到缓存文件"""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"缓存保存失败: {e}")


def format_output(data):
    """格式化输出活动信息"""
    if not data:
        return "无法获取数据"
    
    update_date = data.get("updateDate", "未知")
    coupon_list = data.get("couponList", [])
    
    if not coupon_list:
        return f"更新日期：{update_date}\n\n暂无活动信息"
    
    # 从 tip 中提取搜索口令
    import re
    
    lines = [
        f"📅 更新日期：{update_date}",
        "",
        "=== 淘宝闪购今日福利 ===",
        ""
    ]
    
    for i, coupon in enumerate(coupon_list, 1):
        title = coupon.get("title", "未知活动")
        desc = coupon.get("desc", "")
        tip = coupon.get("tip", "")
        copy_code = coupon.get("copyCode", "")
        
        # 从 tip 中提取搜索口令（通常是4位数字）
        search_code = ""
        match = re.search(r'搜索[码口]?\s*(\d{4,})', tip)
        if match:
            search_code = match.group(1)
        
        lines.append(f"【{title}】")
        if search_code:
            lines.append(f"🔍 搜索口令：{search_code}")
        if desc:
            lines.append(f"📝 简介：{desc}")
        if tip:
            lines.append(f"📖 详细说明：{tip}")
        if copy_code:
            lines.append(f"🎫 优惠码：{copy_code}")
        lines.append("")
    
    # 添加使用说明
    lines.extend([
        "",
        "═══════════════════════════════════════",
        "🎯 使用方式：",
        "1. 打开手机淘宝 APP",
        '2. 点击顶部「闪购」入口',
        '3. 在搜索框输入指定的口令/数字',
        "4. 点击搜索即可领取福利",
        "═══════════════════════════════════════"
    ])
    
    return "\n".join(lines)


def main():
    print("正在获取淘宝闪购每日福利...")
    print()
    
    data = fetch_shangou_data()
    
    if data:
        # 保存缓存
        save_cache(data)
        # 格式化输出
        output = format_output(data)
        print(output)
    else:
        # 尝试读取缓存
        if CACHE_FILE.exists():
            print("API请求失败，读取缓存数据：")
            print()
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                print(format_output(cached_data))
            except Exception as e:
                print(f"读取缓存失败: {e}")
        else:
            print("获取数据失败，且无缓存可用")


if __name__ == "__main__":
    main()
