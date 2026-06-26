import os
import time
import json
import socket
import hashlib
import ipaddress
from typing import Dict, Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class S2MijiaLocalAdapter:
    def __init__(self, enable_real_actuation: bool):
        self._ip = os.getenv("MIJIA_DEVICE_IP", "192.168.1.100")
        self._token_hex = os.getenv("MIJIA_DEVICE_TOKEN", "ffffffffffffffffffffffffffffffff")
        self._enable_real_actuation = enable_real_actuation
        self._port = 54321
        self._key = None
        self._iv = None
        self._validate_local_ip(self._ip)
        self._derive_keys()

    def _validate_local_ip(self, ip_str: str):
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            if not (ip_obj.is_private or ip_obj.is_loopback):
                print(f"   └─ 🚨 [SSRF 拦截] IP 非局域网地址！")
                self._ip = None 
        except Exception:
            self._ip = None 

    def _derive_keys(self):
        if not self._token_hex or len(self._token_hex) != 32: return
        try:
            token_bytes = bytes.fromhex(self._token_hex)
            self._key = hashlib.md5(token_bytes).digest()
            self._iv = hashlib.md5(self._key + token_bytes).digest()
        except Exception:
            self._key = None

    def _encrypt_payload(self, payload_dict: dict) -> bytes:
        cipher = AES.new(self._key, AES.MODE_CBC, self._iv)
        plaintext = json.dumps(payload_dict).encode('utf-8')
        return cipher.encrypt(pad(plaintext, AES.block_size))

    def _send_udp_miio(self, payload_dict: dict) -> bool:
        # 🛡️ 核心修复：日志脱敏 (DLP)，不打印带真实值的 Miot Spec
        print(f"   └─ 📡 [Mijia Adapter] Miot Spec 降维构建完成: [REDACTED FOR PRIVACY]")
        
        if not self._enable_real_actuation:
            print("   └─ 🛡️ [DRY-RUN] 沙盒模式，安全拦截 UDP 发射。")
            return True
            
        if not self._key or not self._ip or "ffffffffffffffff" in self._token_hex:
            print("   └─ 🚨 [执行阻断] 凭证配置无效或 IP 异常。")
            return False

        try:
            print(f"   └─ 🔐 [AES 加密] 封装密文，射向局域网...")
            req_data = {"id": int(time.time() % 100000), "method": "set_properties", "params": payload_dict["params"]}
            encrypted_data = self._encrypt_payload(req_data)
            
            packet_len = 32 + len(encrypted_data)
            header = bytes.fromhex("2131") + packet_len.to_bytes(2, byteorder='big') + bytes.fromhex("00000000ffffffffffffffffffffffff")
            final_packet = header + encrypted_data
            
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2.0)
                sock.sendto(final_packet, (self._ip, self._port))
            
            print("   └─ ✅ [硬件响应] UDP 成功发射。")
            return True
        except Exception as e:
            print(f"   └─ ❌ [UDP 异常] {e}")
            return False

    def translate_and_execute(self, s2_element: str, device_id: str, intent: Dict[str, Any]) -> bool:
        print(f"\n   🌐 [S2 降维] 要素: {s2_element} -> 设备: [REDACTED]")
        miot_params = []
        if s2_element == "LUMINA":
            if "power" in intent: miot_params.append({"did": device_id, "siid": 2, "piid": 1, "value": intent["power"]})
            if "brightness_pct" in intent: miot_params.append({"did": device_id, "siid": 2, "piid": 2, "value": intent["brightness_pct"]})
        elif s2_element == "CLIMATE":
            if "power" in intent: miot_params.append({"did": device_id, "siid": 2, "piid": 1, "value": intent["power"]})
            if "temperature" in intent: miot_params.append({"did": device_id, "siid": 2, "piid": 3, "value": intent["temperature"]})

        if miot_params: return self._send_udp_miio({"params": miot_params})
        return False

    def secure_teardown(self):
        if self._key: self._key = b'\x00' * 16
        if self._iv: self._iv = b'\x00' * 16
        self._token_hex = "WIPED_SECURELY"
        print("   └─ 🛡️ [零信任] AES 密钥解绑。")