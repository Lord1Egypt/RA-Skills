# -*- coding: utf-8 -*-
"""
喜乐姐真蚕丝喜被 - MCP 后端服务
启动后在 http://127.0.0.1:8000 运行
打开 http://127.0.0.1:8000/docs 可以看到所有接口的说明和测试页面
"""
import sys
import json
import uuid
import sqlite3
import os
from datetime import datetime
from typing import Optional

sys.stdout.reconfigure(encoding="utf-8")

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data import (
    BRAND_INFO, PRODUCTS, SILK_AUTH_GUIDE, CARE_GUIDE,
    POLICIES, LATEST_NEWS, get_recommendation
)

# ============================================================
# 初始化 FastAPI 应用
# ============================================================
app = FastAPI(
    title="喜乐姐真蚕丝喜被 MCP 服务",
    description="AI Skill 后端接口，提供产品查询、下单、订单查询等功能",
    version="0.1.0"
)

# 允许跨域访问（MCP 客户端需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 数据库初始化（SQLite，自动创建）
# ============================================================
DB_PATH = os.path.join(os.path.dirname(__file__), "orders.db")


def init_db():
    """创建订单表（如果不存在）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            unit_price INTEGER NOT NULL,
            total_price INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            note TEXT DEFAULT '',
            status TEXT DEFAULT '待联系',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ============================================================
# 请求/响应模型
# ============================================================
class OrderRequest(BaseModel):
    """下单请求"""
    product_id: str
    quantity: int = 1
    customer_name: str
    phone: str
    address: str
    note: str = ""


class OrderQuery(BaseModel):
    """查询订单"""
    order_id: Optional[str] = None
    phone: Optional[str] = None


class RecommendRequest(BaseModel):
    """选购推荐请求"""
    bed_width: Optional[str] = None
    season: Optional[str] = None
    purpose: Optional[str] = None
    budget: Optional[str] = None


# ============================================================
# MCP 协议端点（核心！AI 助手通过这个接口调用工具）
# ============================================================
@app.post("/")
async def mcp_endpoint(request: Request):
    """
    MCP 协议入口（JSON-RPC 2.0）
    AI 助手会向这个地址发送 JSON-RPC 请求来调用各种工具
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(content={
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32700, "message": "请求格式不对，需要 JSON"}
        }, status_code=400)

    rpc_id = body.get("id")
    method = body.get("method", "")
    params = body.get("params", {})

    # tools/list - 列出所有可用工具
    if method == "tools/list":
        return JSONResponse(content={
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {"tools": get_tools_list()}
        })

    # tools/call - 调用具体工具
    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        result = call_tool(tool_name, arguments)
        return JSONResponse(content={
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": result
        })

    # 未知方法
    return JSONResponse(content={
        "jsonrpc": "2.0",
        "id": rpc_id,
        "error": {"code": -32601, "message": f"不支持的方法: {method}"}
    })


# ============================================================
# 工具列表（给 AI 看的"菜单"）
# ============================================================
def get_tools_list():
    """返回所有可用工具的定义"""
    skill_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skill.json")
    skill_json_path = os.path.normpath(skill_json_path)
    with open(skill_json_path, "r", encoding="utf-8") as f:
        skill = json.load(f)
    return skill.get("tools", [])


# ============================================================
# 工具调用路由（根据工具名执行对应功能）
# ============================================================
def call_tool(name: str, arguments: dict):
    """根据工具名调用对应的处理函数"""
    handlers = {
        "get_brand_info": handle_brand_info,
        "get_products": handle_products,
        "get_recommendation": handle_recommendation,
        "get_silk_auth_guide": handle_silk_auth,
        "get_care_guide": handle_care_guide,
        "get_policies": handle_policies,
        "place_order": handle_place_order,
        "get_order_status": handle_order_status,
        "get_latest_news": handle_latest_news,
        "get_purchase_links": handle_purchase_links,
    }

    handler = handlers.get(name)
    if not handler:
        return {
            "content": [{"type": "text", "text": f"没有这个工具: {name}"}],
            "isError": True
        }

    try:
        result = handler(arguments)
        return {
            "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
            "isError": False
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"工具执行出错: {str(e)}"}],
            "isError": True
        }


# ============================================================
# 各工具的处理函数
# ============================================================

def handle_brand_info(args):
    """品牌介绍"""
    return BRAND_INFO


def handle_products(args):
    """产品列表（可按类别筛选）"""
    category = args.get("category")
    if category:
        filtered = [p for p in PRODUCTS if category in p["category"]]
        if not filtered:
            return {"message": f"没有找到类别为'{category}'的产品", "available_categories": ["夏凉被", "春秋被", "冬被", "子母被", "喜被"]}
        return {"products": filtered, "count": len(filtered)}
    return {"products": PRODUCTS, "count": len(PRODUCTS)}


def handle_recommendation(args):
    """选购推荐"""
    results = get_recommendation(
        bed_width=args.get("bed_width"),
        season=args.get("season"),
        purpose=args.get("purpose"),
        budget=args.get("budget")
    )
    tips = []
    if args.get("bed_width"):
        tips.append(f"根据您的床宽({args['bed_width']})推荐了合适的尺寸")
    if args.get("purpose") and "结婚" in args.get("purpose", ""):
        tips.append("婚庆用被推荐喜被系列，含龙凤绣花被套，可定制绣字")
    if not tips:
        tips.append("如果告诉我床宽、季节、用途，可以推荐更精准")

    return {"recommended": results, "tips": tips}


def handle_silk_auth(args):
    """蚕丝真伪鉴别"""
    return SILK_AUTH_GUIDE


def handle_care_guide(args):
    """洗涤保养"""
    return CARE_GUIDE


def handle_policies(args):
    """售后政策"""
    return POLICIES


def handle_place_order(args):
    """下单"""
    product_id = args.get("product_id", "")
    quantity = args.get("quantity", 1)
    customer_name = args.get("customer_name", "")
    phone = args.get("phone", "")
    address = args.get("address", "")
    note = args.get("note", "")

    # 校验必填项
    if not all([product_id, customer_name, phone, address]):
        return {"error": "缺少必填信息，需要：商品编号、收货人姓名、手机号、收货地址"}

    # 查找商品
    product = None
    for p in PRODUCTS:
        if p["id"] == product_id:
            product = p
            break

    if not product:
        return {
            "error": f"没有找到编号为'{product_id}'的商品",
            "available_products": [{"id": p["id"], "name": p["name"], "price": p["price"]} for p in PRODUCTS]
        }

    if not product["in_stock"]:
        return {"error": f"'{product['name']}'暂时缺货，请选择其他款式"}

    # 生成订单
    order_id = "XLJ" + datetime.now().strftime("%Y%m%d") + str(uuid.uuid4().hex[:6]).upper()
    total_price = product["price"] * quantity
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 存入数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (order_id, product_id, product_name, quantity, unit_price, total_price,
                           customer_name, phone, address, note, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (order_id, product_id, product["name"], quantity, product["price"], total_price,
          customer_name, phone, address, note, "待联系", created_at))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "order_id": order_id,
        "product": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "total_price": total_price,
        "payment": "货到付款（快递送到后验货再付钱）",
        "customer": customer_name,
        "phone": phone,
        "address": address,
        "note": note or "无",
        "status": "待联系",
        "message": f"下单成功！订单号 {order_id}，我们会尽快联系您确认订单，然后48小时内发货。货到付款，不用提前转账。"
    }


def handle_order_status(args):
    """查询订单"""
    order_id = args.get("order_id")
    phone = args.get("phone")

    if not order_id and not phone:
        return {"error": "请提供订单号或下单时的手机号来查询"}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if order_id:
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    else:
        cursor.execute("SELECT * FROM orders WHERE phone = ? ORDER BY created_at DESC", (phone,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"message": "没有找到相关订单。请确认订单号或手机号是否正确。"}

    orders = []
    for row in rows:
        orders.append({
            "order_id": row["order_id"],
            "product": row["product_name"],
            "quantity": row["quantity"],
            "total_price": row["total_price"],
            "status": row["status"],
            "created_at": row["created_at"],
            "address": row["address"]
        })

    return {"orders": orders, "count": len(orders)}


def handle_latest_news(args):
    """最新活动"""
    return {"news": LATEST_NEWS}


def handle_purchase_links(args):
    """购买方式与团购链接"""
    return {
        "douyin_group": "https://aweme.snssdk.com/falcon/poi_mwa/trade_detail?activity_id=1864313654090764",
        "wechat_customer": {
            "wechat_id": "18637535738",
            "qr_code": "微信扫码添加客服",
            "note": "有定制、绣字、特殊尺寸需求，请加微信客服"
        },
        "payment_methods": ["货到付款", "微信支付", "支付宝"],
        "note": "抖音团购有优惠，货到付款更安心"
    }


# ============================================================
# 便捷的 REST 接口（给浏览器/调试用，非 MCP 协议）
# ============================================================
@app.get("/products")
async def api_products(category: Optional[str] = None):
    """查看所有产品（浏览器打开就能看）"""
    return handle_products({"category": category} if category else {})


@app.get("/products/{product_id}")
async def api_product_detail(product_id: str):
    """查看单个商品详情"""
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return {"error": f"没有找到编号为'{product_id}'的商品"}


@app.post("/orders")
async def api_create_order(order: OrderRequest):
    """下单"""
    return handle_place_order(order.dict())


@app.get("/orders/{order_id}")
async def api_order_status(order_id: str):
    """查询订单"""
    return handle_order_status({"order_id": order_id})


@app.post("/recommend")
async def api_recommend(req: RecommendRequest):
    """选购推荐"""
    return handle_recommendation(req.dict())


@app.get("/brand")
async def api_brand():
    """品牌信息"""
    return BRAND_INFO


@app.get("/faq/silk-auth")
async def api_silk_auth():
    """蚕丝真伪鉴别"""
    return SILK_AUTH_GUIDE


@app.get("/faq/care")
async def api_care():
    """洗涤保养"""
    return CARE_GUIDE


@app.get("/policies")
async def api_policies():
    """售后政策"""
    return POLICIES


@app.get("/news")
async def api_news():
    """最新活动"""
    return {"news": LATEST_NEWS}


@app.get("/health")
async def health_check():
    """健康检查（服务器是否正常运行）"""
    return {"status": "ok", "service": "喜乐姐真蚕丝喜被 MCP 服务", "version": "0.1.0"}


# ============================================================
# 启动入口
# ============================================================
if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  喜乐姐真蚕丝喜被 MCP 服务 启动中...")
    print("  打开浏览器访问: http://127.0.0.1:8000/docs")
    print("  看到接口文档页面就说明启动成功了")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)
