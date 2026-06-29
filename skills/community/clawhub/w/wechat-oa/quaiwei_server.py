#!/usr/bin/env python3
"""
去AI味 HTTP API 服务
====================
提供 REST API 端点，供支付宝AI收验证服务可用性，
以及供 AI Agent（OpenClaw等）调用执行去AI味功能。

运行方式：
  python quaiwei_server.py                  # 默认端口 8000
  python quaiwei_server.py --port 9000      # 自定义端口

API 端点：
  GET  /                        服务信息（支付宝验证用）
  GET  /api/quaiwei/info        服务描述 + 价格
  POST /api/quaiwei/order       创建订单（生成支付宝支付链接）
  POST /api/quaiwei/execute     执行去AI味（支付成功后调用）
  POST /api/quaiwei/full        一步到位：下单+支付+执行（Mock模式）
"""

import argparse
import hashlib
import json
import os
import sys
import time
import uuid
from pathlib import Path

# ── FastAPI 依赖 ──
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print("[ERROR] 缺少依赖，请先安装：")
    print("  pip install fastapi uvicorn")
    sys.exit(1)

# ── requests（调用 Claude API）──
try:
    import requests as http_requests
except ImportError:
    http_requests = None

# ── 配置 ──
CONFIG_FILE = Path(__file__).parent / "config.json"
SERVICE_VERSION = "1.0.0"
SERVICE_NAME = "去AI味 - 文字改写服务"
SERVICE_PRICE = 1.00  # 每次1元


def load_config():
    """从 config.json 加载配置"""
    default_config = {
        "APP_ID": "",
        "APP_SECRET": "",
        "author": "",
        "CLAUDE_API_KEY": "",
        "ALIPAY_APP_ID": "",
        "ALIPAY_PRIVATE_KEY": "",
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_config = json.load(f)
            default_config.update(user_config)
        except Exception as e:
            print(f"[WARN] 读取 config.json 失败: {e}")
    return default_config


CONFIG = load_config()

# ── Pydantic 请求模型 ──
class OrderRequest(BaseModel):
    text: str = Field(..., description="待改写的文字内容")
    
class ExecuteRequest(BaseModel):
    text: str = Field(..., description="待改写的文字内容")
    order_id: str = Field("", description="订单号（支付验证用）")
    mock_pay: bool = Field(False, description="是否模拟支付")

class FullRequest(BaseModel):
    text: str = Field(..., description="待改写的文字内容")


# ── FastAPI App ──
app = FastAPI(
    title=SERVICE_NAME,
    version=SERVICE_VERSION,
    description="去除文字中的AI生成痕迹，让文字读起来像真实人类写作者。按次收费1元，通过支付宝AI收结算。",
)


# ═══════════════════════════════════════════════════════════════
# API 端点
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """服务根路径 — 返回服务信息，支付宝验证用"""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "status": "running",
        "price": f"¥{SERVICE_PRICE}/次",
        "description": "去除文字中的AI生成痕迹，让文字读起来像真实人类写作者",
        "endpoints": {
            "info": "/api/quaiwei/info",
            "order": "/api/quaiwei/order",
            "execute": "/api/quaiwei/execute",
            "full": "/api/quaiwei/full",
        },
        "payment": {
            "method": "支付宝AI收",
            "alipay_app_id": CONFIG.get("ALIPAY_APP_ID", "未配置"),
            "price_per_request": SERVICE_PRICE,
        },
        "author": CONFIG.get("author", ""),
    }


@app.get("/api/quaiwei/info")
async def service_info():
    """服务描述 + 价格 — 供支付宝AI收询价"""
    return {
        "service_name": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "description": "去除文字中的AI生成痕迹，改写为人类自然写作风格",
        "price": {
            "amount": SERVICE_PRICE,
            "currency": "CNY",
            "unit": "per_request",
            "description": f"每次请求 ¥{SERVICE_PRICE}",
        },
        "capabilities": [
            "打散AI规整句式",
            "注入口语化表达",
            "替换AI过渡词",
            "加入人类写作瑕疵",
            "保留原文核心信息",
        ],
        "input_format": {
            "text": "string, required, 待改写的文字内容",
        },
        "output_format": {
            "result": "string, 改写后的文字",
            "original_length": "int, 原文字数",
            "rewritten_length": "int, 改写后字数",
        },
        "payment_required": True,
        "alipay_app_id": CONFIG.get("ALIPAY_APP_ID", "未配置"),
    }


@app.post("/api/quaiwei/order")
async def create_order(req: OrderRequest):
    """创建订单 — 生成支付宝支付链接
    
    支付宝AI收流程：
    1. 商家下单Skill 调用此接口生成订单
    2. 调支付宝收单接口获取支付链接
    3. 将支付链接压缩成短链
    4. 引导加载支付宝支付处理技能
    """
    text = req.text

    if not text:
        raise HTTPException(status_code=400, detail="缺少必填参数: text")

    # 生成订单号
    order_id = f"QUAIWEI_{int(time.time())}_{uuid.uuid4().hex[:8]}"

    alipay_app_id = CONFIG.get("ALIPAY_APP_ID", "")

    if not alipay_app_id or not CONFIG.get("ALIPAY_PRIVATE_KEY"):
        # Mock 模式：没有配置支付宝密钥时返回模拟订单
        return {
            "order_id": order_id,
            "status": "mock_order_created",
            "amount": SERVICE_PRICE,
            "currency": "CNY",
            "description": f"去AI味 - 文字改写 ({len(text)}字)",
            "payment_link": None,
            "payment_method": "mock",
            "message": "支付宝AI收未配置，使用模拟支付。配置 ALIPAY_APP_ID + ALIPAY_PRIVATE_KEY 后可切换真实支付。",
            "next_step": "直接调用 /api/quaiwei/execute 执行服务（Mock模式免支付）",
        }

    # 真实模式：调用支付宝收单接口
    # TODO: 安装 alipay-sdk-python 后实现真实下单
    # 1. 调用 alipay.trade.create 生成交易
    # 2. 获取支付链接
    # 3. 调用支付宝命令压缩成短链
    return {
        "order_id": order_id,
        "status": "order_created",
        "amount": SERVICE_PRICE,
        "currency": "CNY",
        "description": f"去AI味 - 文字改写 ({len(text)}字)",
        "payment_link": "alipay_*_xxxxxx",  # 真实短链（需实现）
        "payment_method": "alipay_aipay",
        "message": "请引导用户使用支付宝支付处理技能完成支付",
        "next_step": "支付成功后调用 /api/quaiwei/execute?order_id={order_id}",
    }


@app.post("/api/quaiwei/execute")
async def execute_quaiwei(req: ExecuteRequest):
    """执行去AI味 — 支付成功后调用
    
    请求参数：
    - text: 待改写的文字内容（必填）
    - order_id: 订单号（可选，支付验证用）
    - mock_pay: 是否模拟支付（可选，默认false）
    """
    text = req.text
    order_id = req.order_id
    mock_pay = req.mock_pay

    if not text:
        raise HTTPException(status_code=400, detail="缺少必填参数: text")

    # 支付验证（Mock模式跳过）
    if not mock_pay and order_id:
        # TODO: 真实模式 — 查询支付宝订单状态，确认已支付
        pass

    # ── 调用 Claude API 或 Mock ──
    api_key = CONFIG.get("CLAUDE_API_KEY", "")
    use_mock = not api_key or api_key == "mock" or not api_key.startswith("sk-ant-")

    if use_mock:
        result_text = _mock_quaiwei(text)
        mode = "mock"
    else:
        result_text = _claude_quaiwei(text, api_key)
        mode = "claude_api"

    return {
        "status": "success",
        "mode": mode,
        "order_id": order_id,
        "original_text": text,
        "result": result_text,
        "original_length": len(text),
        "rewritten_length": len(result_text),
        "price_charged": SERVICE_PRICE if not mock_pay else 0,
        "currency": "CNY",
    }


@app.post("/api/quaiwei/full")
async def full_workflow(req: FullRequest):
    """一步到位：下单 + 支付 + 执行
    
    Mock模式下免支付直接执行；
    真实模式下生成支付链接，需用户完成支付后再执行。
    """
    text = req.text

    if not text:
        raise HTTPException(status_code=400, detail="缺少必填参数: text")

    alipay_configured = CONFIG.get("ALIPAY_APP_ID") and CONFIG.get("ALIPAY_PRIVATE_KEY")

    if not alipay_configured:
        # Mock 模式：直接执行
        api_key = CONFIG.get("CLAUDE_API_KEY", "")
        use_mock = not api_key or api_key == "mock" or not api_key.startswith("sk-ant-")

        if use_mock:
            result_text = _mock_quaiwei(text)
            mode = "mock_full"
        else:
            result_text = _claude_quaiwei(text, api_key)
            mode = "claude_api_full"

        return {
            "status": "success",
            "mode": mode,
            "order_id": f"MOCK_{int(time.time())}",
            "payment_status": "mock_paid",
            "original_text": text,
            "result": result_text,
            "original_length": len(text),
            "rewritten_length": len(result_text),
            "price_charged": SERVICE_PRICE,
            "currency": "CNY",
            "message": "Mock模式：模拟支付成功，直接返回结果",
        }

    # 真实模式：生成订单 + 支付链接
    order_id = f"QUAIWEI_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    return {
        "status": "order_created",
        "mode": "real_payment",
        "order_id": order_id,
        "payment_status": "pending",
        "amount": SERVICE_PRICE,
        "currency": "CNY",
        "payment_link": "alipay_*_xxxxxx",  # 真实短链（需实现）
        "message": "请完成支付后再调用 /api/quaiwei/execute 获取结果",
        "next_step": f"POST /api/quaiwei/execute with order_id={order_id}&text=...",
    }


# ═══════════════════════════════════════════════════════════════
# 去AI味 核心函数
# ═══════════════════════════════════════════════════════════════

def _mock_quaiwei(text):
    """Mock 模式：简单模拟去AI味效果"""
    import random
    random.seed(abs(hash(text)) % (2**32))
    result = text

    # 1. 开头加口语化表达（50%概率）
    starters = ["说实话，", "我觉得，", "嗯，"]
    if random.random() > 0.5 and not any(result.startswith(s) for s in starters):
        result = random.choice(starters) + result

    # 2. 替换AI过渡词
    replacements = [
        ("值得注意的是", "其实呢"),
        ("综上所述", "总结一下"),
        ("此外", "还有"),
        ("然而", "不过呢"),
        ("因此", "所以"),
        ("带来了前所未有的", "带来了"),
        ("需要关注", "得留意"),
    ]
    for old, new in replacements:
        if old in result:
            result = result.replace(old, new, 1)
            break

    # 3. 拆长句
    if "，" in result:
        idx = result.find("，")
        if 10 < idx < len(result) - 10:
            result = result[:idx] + "。" + result[idx+1:]

    # 4. 结尾加点人类感觉
    if result and result[-1] not in "。！？~":
        result += "呢。"

    return result


SYSTEM_PROMPT = """你是一个专业的文字改写助手。你的任务是去除文字中的"AI味"，让文字读起来像真实人类写作者。

去AI味的要点：
1. 打散过于规整的句式结构 — 人类写作句式长短交替、不规则
2. 注入个人语气 — 加入口语化表达、个人感受、轻微情绪
3. 故意加入"人类瑕疵" — 适当重复用词、偶尔用不完整句、加入填充词
4. 破坏AI典型的过渡词模式 — 删掉"值得注意的是""综上所述""此外"等
5. 让逻辑有些"跳跃" — 人类写作不会每句话都完美衔接
6. 加入具体细节 — AI倾向于泛泛而谈，人类会举具体例子

输出要求：
- 直接输出改写后的文字，不要加任何解释或说明
- 保留原文的核心信息和意思
- 文字长度与原文相当"""


def _claude_quaiwei(text, api_key):
    """调用 Claude API 去AI味"""
    if http_requests is None:
        return _mock_quaiwei(text)  # fallback to mock

    claude_url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4096,
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": f"请改写以下文字，去除AI味：\n\n{text}"}
        ]
    }

    try:
        resp = http_requests.post(claude_url, headers=headers, json=payload, timeout=60)
        result = resp.json()
        if "content" in result:
            return result["content"][0]["text"]
        else:
            return f"[ERROR] Claude API 返回异常: {result}"
    except Exception as e:
        return f"[ERROR] Claude API 调用失败: {e}"


# ═══════════════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="去AI味 HTTP API 服务")
    parser.add_argument("--port", type=int, default=8000, help="服务端口（默认8000）")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="绑定地址（默认0.0.0.0）")
    args = parser.parse_args()

    print(f"╔══════════════════════════════════════════╗")
    print(f"║  {SERVICE_NAME}                    ║")
    print(f"║  版本: {SERVICE_VERSION}                      ║")
    print(f"║  价格: ¥{SERVICE_PRICE}/次                     ║")
    print(f"╚══════════════════════════════════════════╝")
    print()
    print(f"[INFO] 服务地址: http://{args.host}:{args.port}")
    print(f"[INFO] API文档:  http://{args.host}:{args.port}/docs")
    print()
    print("[INFO] 端点说明:")
    print("  GET  /                   → 服务信息")
    print("  GET  /api/quaiwei/info   → 服务描述+价格")
    print("  POST /api/quaiwei/order  → 创建订单")
    print("  POST /api/quaiwei/execute → 执行去AI味")
    print("  POST /api/quaiwei/full   → 一步到位")
    print()

    alipay_status = "✅ 已配置" if CONFIG.get("ALIPAY_APP_ID") else "❌ 未配置（Mock模式）"
    claude_status = "✅ 已配置" if CONFIG.get("CLAUDE_API_KEY", "").startswith("sk-ant-") else "❌ 未配置（Mock模式）"
    print(f"[CONFIG] 支付宝AI收: {alipay_status}")
    print(f"[CONFIG] Claude API: {claude_status}")
    print()

    uvicorn.run(app, host=args.host, port=args.port)
