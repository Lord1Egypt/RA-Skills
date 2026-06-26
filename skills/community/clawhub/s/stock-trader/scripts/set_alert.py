#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置股价监控提醒
用法: python set_alert.py <股票代码> <买入价下限> <买入价上限>
示例: python set_alert.py 002475 46.50 47.50
"""

import sys
import subprocess
import json

def set_price_alert(stock_code, buy_low, buy_high, user_id):
    """设置价格监控提醒"""
    
    # 标准化代码
    if not stock_code.startswith(("sz", "sh")):
        if stock_code.startswith(("6", "5", "9")):
            stock_code = f"sh{stock_code}"
        else:
            stock_code = f"sz{stock_code}"
    
    job_name = f"股票监控_{stock_code}"
    
    # 构建消息
    message = f"""检查{stock_code}股价，解析数据后判断是否在{buy_low}-{buy_high}元买入区间。
如果在区间内或接近，输出：📊{stock_code}现价XX元 ✅已进入买入区间 💡建议分批建仓。
如不在区间，说明差距。要求：直接输出，用emoji点缀，3句话内。"""
    
    # 构建 cron 命令
    cmd = [
        "openclaw", "cron", "add",
        "--name", job_name,
        "--cron", "0 16 * * 1-5",  # 工作日16:00
        "--tz", "Asia/Shanghai",
        "--session", "isolated",
        "--wake", "now",
        "--message", message,
        "--channel", "qqbot",
        "--to", user_id,
        "--announce"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 已设置监控: {stock_code}")
            print(f"   买入区间: {buy_low} - {buy_high} 元")
            print(f"   检查时间: 每个交易日 16:00")
            print(f"   提醒目标: {user_id}")
            return True
        else:
            print(f"❌ 设置失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    if len(sys.argv) < 4:
        print("用法: python set_alert.py <股票代码> <买入价下限> <买入价上限>")
        print("示例: python set_alert.py 002475 46.50 47.50")
        print("\n注意: 需要在 OpenClaw 环境中运行")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    buy_low = sys.argv[2]
    buy_high = sys.argv[3]
    
    # 尝试从环境获取用户ID，或使用默认值
    user_id = "D3AA9A40183306D5A885AB9BE7581B06"
    
    set_price_alert(stock_code, buy_low, buy_high, user_id)

if __name__ == "__main__":
    main()
