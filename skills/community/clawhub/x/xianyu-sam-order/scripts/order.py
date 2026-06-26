#!/usr/bin/env python3
"""
闲鱼山姆代下单 - 辅助工具
"""

import os

def check_env():
    """检查环境配置"""
    cookie = os.environ.get("XIANYU_COOKIE", "")
    sam_phone = os.environ.get("SAM_PHONE", "")
    
    print("🔧 环境检查:")
    print(f"  闲鱼Cookie: {'✅ 已配置' if cookie else '❌ 未配置'}")
    print(f"  山姆手机号: {'✅ 已配置' if sam_phone else '❌ 未配置'}")
    
    if not cookie:
        print("\n📝 配置方法：")
        print("1. 打开闲鱼APP")
        print("2. 我的 → 设置 → 账号与安全")
        print("3. 复制Cookie（或直接手动下单）")

def order_help():
    """下单帮助"""
    print("""
🛒 山姆下单帮助

方法1：手动下单（推荐）
------------------------------
1. 打开山姆APP/小程序
2. 选商品，加入购物车
3. 选配送地址，付款
4. 把订单发给我帮你跟踪

方法2：让我帮你查价格
------------------------------
告诉我商品名称，我帮你查山姆价格

方法3：自动下单（需要Cookie）
------------------------------
配置XIANYU_COOKIE环境变量
⚠️ 注意：不建议自动下单，风险较高
""")

if __name__ == "__main__":
    check_env()
    print()
    order_help()
