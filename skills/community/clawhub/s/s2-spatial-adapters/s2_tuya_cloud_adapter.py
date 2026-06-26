import os
import time
import json
import hmac
import hashlib
import requests
from typing import Dict, Any

class S2TuyaCloudAdapter:
    def __init__(self, enable_real_actuation: bool):
        self._endpoint = os.getenv("TUYA_ENDPOINT", "https://openapi.tuyacn.com")
        self._access_id = os.getenv("TUYA_ACCESS_ID", "unconfigured_tuya_id")
        self._secret = os.getenv("TUYA_ACCESS_SECRET", "unconfigured_tuya_secret")
        self._enable_real_actuation = enable_real_actuation
        self._token = None

    def _calc_sign(self, msg: str) -> str:
        return hmac.new(self._secret.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).hexdigest().upper()

    def _get_access_token(self) -> str:
        if self._token: return self._token
        t = str(int(time.time() * 1000))
        sign = self._calc_sign(self._access_id + t)
        headers = {"client_id": self._access_id, "sign": sign, "t": t, "sign_method": "HMAC-SHA256"}
        url = f"{self._endpoint}/v1.0/token?grant_type=1"
        try:
            resp = requests.get(url, headers=headers, timeout=5).json()
            if resp.get("success"):
                self._token = resp["result"]["access_token"]
                return self._token
            else:
                raise PermissionError(f"Tuya Token Error")
        except Exception:
            raise ConnectionError(f"Tuya API Unreachable")

    def _execute_tuya_request(self, method: str, path: str, body: dict = None) -> bool:
        print(f"   └─ 📡 [Tuya Adapter] 投递 OpenAPI: {method} [REDACTED_PATH]")
        # 🛡️ 核心修复：日志脱敏 (DLP)，隐藏具体的设备标识和载荷
        print(f"   └─ 📦 载荷: [REDACTED FOR PRIVACY/SECURITY]")

        if not self._enable_real_actuation:
            print("   └─ 🛡️ [DRY-RUN] 沙盒模式，安全拦截云端 POST 发射。")
            return True

        if "unconfigured" in self._secret:
            print("   └─ 🚨 [执行阻断] 涂鸦密钥未配置。")
            return False

        try:
            token = self._get_access_token()
            t = str(int(time.time() * 1000))
            body_str = json.dumps(body) if body else ""
            body_hash = hashlib.sha256(body_str.encode('utf-8')).hexdigest()
            string_to_sign = f"{method}\n{body_hash}\n\n{path}"
            
            sign_str = self._access_id + token + t + string_to_sign
            sign = self._calc_sign(sign_str)
            headers = {"client_id": self._access_id, "access_token": token, "sign": sign, "t": t, "sign_method": "HMAC-SHA256", "Content-Type": "application/json"}
            
            print(f"   └─ 🔐 [HMAC-SHA256] 签名成功，发射！")
            resp = requests.post(f"{self._endpoint}{path}", headers=headers, json=body, timeout=5)
            if resp.json().get("success"):
                print("   └─ ✅ [硬件响应] 云端执行成功。")
                return True
            return False
        except Exception:
            return False

    def translate_and_execute(self, s2_element: str, device_id: str, intent: Dict[str, Any]) -> bool:
        print(f"\n   🌐 [S2 降维] 要素: {s2_element} -> 设备: [REDACTED]")
        tuya_commands = []
        if s2_element == "LUMINA":
            if "power" in intent: tuya_commands.append({"code": "switch_led", "value": intent["power"]})
            if "brightness_pct" in intent: tuya_commands.append({"code": "bright_value", "value": max(10, int(intent["brightness_pct"] * 10))})
        elif s2_element == "CLIMATE":
            if "power" in intent: tuya_commands.append({"code": "switch", "value": intent["power"]})
            if "temperature" in intent: tuya_commands.append({"code": "temp_set", "value": intent["temperature"]})
        elif s2_element == "SENTINEL":
            if intent.get("action") == "unlock": tuya_commands.append({"code": "switch", "value": True})
        elif s2_element == "PET_CARE":
            if "feed_portions" in intent: tuya_commands.append({"code": "manual_feed", "value": intent["feed_portions"]})

        if not tuya_commands: return False

        payload = {"commands": tuya_commands}
        return self._execute_tuya_request("POST", f"/v1.0/iot-03/devices/{device_id}/commands", payload)

    def secure_teardown(self):
        self._secret = "WIPED_SECURELY_" * 4
        self._token = "WIPED_TOKEN_" * 4
        print("   └─ 🛡️ [零信任] Tuya 凭证解绑。")