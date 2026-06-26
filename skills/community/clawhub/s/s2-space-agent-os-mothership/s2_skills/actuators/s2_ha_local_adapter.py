import os
import json
import time
import socket
import ipaddress
import requests
from urllib.parse import urlparse
from typing import Dict, Any

class S2HomeAssistantAdapter:
    def __init__(self, enable_real_actuation: bool):
        self._base_url = os.getenv("HA_BASE_URL", "http://homeassistant.local:8123/api")
        self._token = os.getenv("HA_BEARER_TOKEN", "unconfigured_ha_token")
        self._enable_real_actuation = enable_real_actuation

    def _validate_ssrf_safety(self, url: str) -> bool:
        try:
            hostname = urlparse(url).hostname
            if not hostname: return False
            if hostname.endswith(".local") or hostname == "localhost": return True
                
            resolved_ip = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(resolved_ip)
            is_safe = ip_obj.is_private or ip_obj.is_loopback
            if not is_safe:
                print(f"   └─ 🚨 [SSRF 拦截] 目标 IP ({resolved_ip}) 非局域网地址！")
            return is_safe
        except Exception:
            return False

    def _call_ha_service(self, domain: str, service: str, entity_id: str, kwargs: dict = None) -> bool:
        if "WIPED" in self._token:
            print("   └─ 🚨 [安全拦截] Token 已清洗，拒绝请求！")
            return False

        url = f"{self._base_url}/services/{domain}/{service}"
        payload = {"entity_id": entity_id}
        if kwargs: payload.update(kwargs)

        print(f"   └─ 📡 [HA Adapter] 投递 REST: POST {domain}/{service}")
        # 🛡️ 核心修复：日志脱敏 (DLP)，绝文明文打印 Payload！
        print(f"   └─ 📦 载荷: [REDACTED FOR PRIVACY/SECURITY]")

        if not self._enable_real_actuation:
            print("   └─ 🛡️ [DRY-RUN] 沙盒模式，安全拦截 HTTP 请求。")
            return True

        if "unconfigured" in self._token or not self._validate_ssrf_safety(url):
            print("   └─ 🚨 [执行阻断] 凭证异常或 SSRF 校验失败。")
            return False

        headers = {"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=3.0)
            response.raise_for_status()
            print("   └─ ✅ [硬件响应] HA 网关确认执行。")
            return True
        except Exception as e:
            print(f"   └─ ❌ [网络异常] {e}")
            return False

    def translate_and_execute(self, s2_element: str, device_id: str, intent: Dict[str, Any]) -> bool:
        print(f"\n   🌐 [S2 降维] 要素: {s2_element} -> 实体: [REDACTED]")
        if s2_element == "LUMINA":
            if intent.get("power") is False: return self._call_ha_service("light", "turn_off", device_id)
            kwargs = {}
            if "brightness_pct" in intent: kwargs["brightness_pct"] = intent["brightness_pct"]
            if "color_temp" in intent: kwargs["color_temp"] = intent["color_temp"]
            return self._call_ha_service("light", "turn_on", device_id, kwargs)
        elif s2_element == "CLIMATE":
            if "temperature" in intent: return self._call_ha_service("climate", "set_temperature", device_id, {"temperature": intent["temperature"]})
            if "hvac_mode" in intent: return self._call_ha_service("climate", "set_hvac_mode", device_id, {"hvac_mode": intent["hvac_mode"]})
        elif s2_element == "SENTINEL":
            if intent.get("action") == "unlock": return self._call_ha_service("lock", "unlock", device_id)
            elif intent.get("action") == "lock": return self._call_ha_service("lock", "lock", device_id)
        return False

    def secure_teardown(self):
        self._token = "WIPED_SECURELY_" * 5
        print("   └─ 🛡️ [零信任] 凭证已解绑，等待 GC 回收。")