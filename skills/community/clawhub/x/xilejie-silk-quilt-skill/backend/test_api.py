# -*- coding: utf-8 -*-
"""
喜乐姐真蚕丝喜被 - 接口测试脚本
先启动 start.bat，然后另开一个命令窗口运行这个脚本：
    python test_api.py
它会自动测试所有接口，全绿就说明没问题。
"""
import sys
import json
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8000"


def test_get(path, description):
    """测试 GET 接口"""
    try:
        req = urllib.request.Request(f"{BASE_URL}{path}")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"  ✅ {description} — 成功")
            return data
    except Exception as e:
        print(f"  ❌ {description} — 失败: {e}")
        return None


def test_post(path, body, description):
    """测试 POST 接口"""
    try:
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            f"{BASE_URL}{path}",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            print(f"  ✅ {description} — 成功")
            return result
    except Exception as e:
        print(f"  ❌ {description} — 失败: {e}")
        return None


def test_mcp_call(tool_name, arguments, description):
    """测试 MCP 协议调用"""
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    result = test_post("/", body, f"[MCP] {description}")
    return result


def main():
    print("=" * 50)
    print("  喜乐姐蚕丝被 Skill — 接口测试")
    print("  请确保已先运行 start.bat 启动服务")
    print("=" * 50)
    print()

    # 先测试服务是否在线
    print("【0】健康检查")
    health = test_get("/health", "服务是否在线")
    if not health:
        print("\n  ⚠️  服务没启动！请先双击 start.bat 启动服务。")
        return
    print()

    # --- REST 接口测试 ---
    print("【1】REST 接口测试（浏览器也能用的接口）")
    test_get("/brand", "品牌信息")
    test_get("/products", "所有产品")
    test_get("/products?category=" + urllib.parse.quote("夏凉被"), "夏凉被产品")
    test_get("/products/CQ-S-200", "单个商品详情")
    test_get("/faq/silk-auth", "蚕丝真伪鉴别")
    test_get("/faq/care", "洗涤保养")
    test_get("/policies", "售后政策")
    test_get("/news", "最新活动")
    print()

    # --- 选购推荐测试 ---
    print("【2】选购推荐测试")
    test_post("/recommend", {"bed_width": "1.8米", "season": "冬天"}, "1.8米床+冬天推荐")
    test_post("/recommend", {"purpose": "结婚"}, "婚庆推荐")
    test_post("/recommend", {"budget": "1000以内"}, "预算1000以内")
    print()

    # --- 下单测试 ---
    print("【3】下单测试")
    order_result = test_post("/orders", {
        "product_id": "CQ-S-220",
        "quantity": 1,
        "customer_name": "测试用户",
        "phone": "13800138000",
        "address": "北京市朝阳区测试路1号",
        "note": "测试订单，请忽略"
    }, "下单（春秋被220×240）")

    if order_result and "order_id" in order_result:
        order_id = order_result["order_id"]
        print()
        print("【4】查询订单测试")
        test_get(f"/orders/{order_id}", f"按订单号查询: {order_id}")
    print()

    # --- MCP 协议测试 ---
    print("【5】MCP 协议测试（AI 助手实际使用的方式）")

    # tools/list
    test_post("/", {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }, "[MCP] 获取工具列表")

    test_mcp_call("get_brand_info", {}, "品牌信息")
    test_mcp_call("get_products", {}, "所有产品")
    test_mcp_call("get_products", {"category": "喜被"}, "喜被产品")
    test_mcp_call("get_recommendation", {"bed_width": "1.5米", "purpose": "送礼"}, "1.5米+送礼推荐")
    test_mcp_call("get_silk_auth_guide", {}, "蚕丝真伪鉴别")
    test_mcp_call("get_care_guide", {}, "洗涤保养")
    test_mcp_call("get_policies", {}, "售后政策")
    test_mcp_call("get_latest_news", {}, "最新活动")

    # MCP 下单
    test_mcp_call("place_order", {
        "product_id": "XB-S-220",
        "quantity": 2,
        "customer_name": "张三",
        "phone": "13900139000",
        "address": "上海市浦东新区测试路2号",
        "note": "MCP测试订单"
    }, "下单（喜被220×240×2床）")

    test_mcp_call("get_order_status", {"phone": "13900139000"}, "按手机号查订单")
    print()

    print("=" * 50)
    print("  测试完成！全绿 ✅ 就说明一切正常")
    print("=" * 50)


if __name__ == "__main__":
    main()
