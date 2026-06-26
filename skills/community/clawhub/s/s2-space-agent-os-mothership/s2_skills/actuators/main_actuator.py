#!/usr/bin/env python3
import sys
import json
import logging
import os
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def validate_intent_payload(intent_data: dict) -> dict:
    if not isinstance(intent_data, dict): raise ValueError("Intent 必须是 JSON 对象。")
    allowed_keys = {"power", "brightness_pct", "color_temp", "temperature", "hvac_mode", "action", "feed_portions"}
    sanitized = {k: v for k, v in intent_data.items() if k in allowed_keys}
    if not sanitized: raise ValueError("过滤后有效意图为空。")
    return sanitized

def validate_endpoint_and_credentials(protocol: str, is_real_actuation: bool):
    """🛡️ 终极安全审计：纯净端点与条件凭证"""
    
    # 彻底移除有第三方钓鱼嫌疑的 iotbing.com，仅保留绝对官方域名
    allowed_tuya_domains = {
        "openapi.tuyacn.com", 
        "openapi.tuyaus.com", 
        "openapi.tuyaeu.com",
        "openapi.tuyain.com",
        "openapi-ueaz.tuyaus.com",
        "openapi-weaz.tuyaeu.com"
    }

    if protocol == "tuya":
        ep = os.getenv("TUYA_ENDPOINT", "https://openapi.tuyacn.com")
        hostname = urlparse(ep).hostname
        if hostname not in allowed_tuya_domains:
            logging.error(f"[端点拦截] {hostname} 为异常域名，已阻断潜在的 DNS 劫持！")
            sys.exit(1)
        if is_real_actuation and (not os.getenv("TUYA_ACCESS_ID") or not os.getenv("TUYA_ACCESS_SECRET")):
            logging.error("[执行阻断] 物理执行模式下，缺失 TUYA_ACCESS_ID/SECRET 凭证！")
            sys.exit(1)

    elif protocol == "ha":
        ha_ep = os.getenv("HA_BASE_URL", "")
        if ha_ep and urlparse(ha_ep).scheme not in ("http", "https"):
            logging.error("[端点拦截] HA_BASE_URL 协议必须为 http/https。")
            sys.exit(1)
        if is_real_actuation and not os.getenv("HA_BEARER_TOKEN"):
            logging.error("[执行阻断] 物理执行模式下，缺失 HA_BEARER_TOKEN 凭证！")
            sys.exit(1)

    elif protocol == "mijia":
        if is_real_actuation and (not os.getenv("MIJIA_DEVICE_IP") or not os.getenv("MIJIA_DEVICE_TOKEN")):
            logging.error("[执行阻断] 物理执行模式下，缺失 MIJIA_DEVICE_IP 或 TOKEN 凭证！")
            sys.exit(1)

def main():
    if len(sys.argv) < 5:
        logging.error("Usage: python main.py <protocol> <s2_element> <device_id> <intent_json>")
        sys.exit(1)

    protocol = sys.argv[1].lower()
    s2_element = sys.argv[2].upper()
    device_id = str(sys.argv[3])
    
    try:
        raw_intent = json.loads(sys.argv[4])
        action_intent = validate_intent_payload(raw_intent)
    except Exception as e:
        logging.error(f"Security Alert: {e}")
        sys.exit(1)

    actuation_env = os.getenv("S2_ENABLE_REAL_ACTUATION")
    if actuation_env is None:
        logging.warning("🚨 缺失系统级安全阀 S2_ENABLE_REAL_ACTUATION，默认进入沙盒模式 (Dry-Run)！")
        is_real_actuation = False
    else:
        is_real_actuation = str(actuation_env).lower() in ("true", "1", "t", "yes")

    logging.info(f"[S2 SecOps] Real Actuation Mode: {is_real_actuation}")
    validate_endpoint_and_credentials(protocol, is_real_actuation)

    from s2_ha_local_adapter import S2HomeAssistantAdapter
    from s2_mijia_local_adapter import S2MijiaLocalAdapter
    from s2_tuya_cloud_adapter import S2TuyaCloudAdapter

    adapter = None
    try:
        if protocol == "ha": adapter = S2HomeAssistantAdapter(is_real_actuation)
        elif protocol == "mijia": adapter = S2MijiaLocalAdapter(is_real_actuation)
        elif protocol == "tuya": adapter = S2TuyaCloudAdapter(is_real_actuation)
        else: raise ValueError(f"Unsupported protocol: {protocol}")

        adapter.translate_and_execute(s2_element, device_id, action_intent)
    except Exception as e:
        logging.error(f"Runtime Exception: {e}")
        sys.exit(1)
    finally:
        if adapter: adapter.secure_teardown()

if __name__ == "__main__":
    main()