# -*- coding: utf-8 -*-
"""客服引擎 - 自动回复买家咨询"""
import json, os, sys, time
from pathlib import Path

DATA_DIR  = Path.home() / ".qclaw" / "solo-ecommerce-data"
CONFIG_FILE = DATA_DIR / "config.json"
CUST_FILE   = DATA_DIR / "customers.json"
LOG_FILE    = DATA_DIR / "logs" / f"{time.strftime('%Y-%m-%d')}.log"

REPLIES = {
    "咨询": "感谢您的咨询！小店商品均为正品，支持7天无理由退换，有任何问题随时联系客服~",
    "尺码": "您好！尺码对照表已更新在商品详情页，建议您根据平时尺码结合详情页推荐选择~",
    "库存": "您好，该商品有现货，付款后24小时内发货，请放心下单！",
    "催发货": "您好，非常抱歉给您带来不便！您的订单已在打包中，预计今天发出，请耐心等待~",
    "物流": "您好，您的包裹已发出，请点击订单详情查看实时物流，如有异常请联系我们~",
    "售后": "您好，小店支持7天无理由退换货，请在订单中申请退款退货，我们会第一时间处理~",
}

def log(msg):
    ts = time.strftime('%H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\r\n")

def classify(text):
    text = text or ""
    if any(k in text for k in ["什么时候发","发货","发货时间"]): return "催发货"
    if any(k in text for k in ["物流","到哪了","查物流"]): return "物流"
    if any(k in text for k in ["尺码","大小","选哪个"]): return "尺码"
    if any(k in text for k in ["有没有货","库存","还有吗"]): return "库存"
    if any(k in text for k in ["退货","退款","售后","不满意"]): return "售后"
    return "咨询"

def get_reply(msg_type):
    return REPLIES.get(msg_type, REPLIES["咨询"])

def main():
    cfg = load_config()
    if not cfg or not cfg.get("enabled"):
        log("[SKIP] 智能体未启用，跳过客服处理")
        return
    auto = cfg.get("automation", {}).get("customer_service", {})
    if not auto.get("enabled"):
        log("[SKIP] 客服功能未启用")
        return

    log(f"[START] 客服引擎启动")
    # TODO: 接入平台消息API或浏览器自动化
    log("[DONE] 客服功能待配置平台接入")

if __name__ == "__main__":
    main()