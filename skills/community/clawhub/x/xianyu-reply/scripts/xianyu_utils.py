"""闲鱼工具函数：Cookie 解析、消息加解密、签名生成等"""

import json
import time
import hashlib
import base64
import struct
import random
from typing import Any, Dict, List


def trans_cookies(cookies_str: str) -> Dict[str, str]:
    """解析 cookie 字符串为字典"""
    cookies = {}
    for cookie in cookies_str.split("; "):
        try:
            parts = cookie.split('=', 1)
            if len(parts) == 2:
                cookies[parts[0]] = parts[1]
        except:
            continue
    return cookies


def generate_mid() -> str:
    """生成消息 ID"""
    random_part = int(1000 * random.random())
    timestamp = int(time.time() * 1000)
    return f"{random_part}{timestamp} 0"


def generate_uuid() -> str:
    """生成 UUID"""
    timestamp = int(time.time() * 1000)
    return f"-{timestamp}1"


def generate_device_id(user_id: str) -> str:
    """生成设备 ID"""
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    result = []
    for i in range(36):
        if i in [8, 13, 18, 23]:
            result.append("-")
        elif i == 14:
            result.append("4")
        else:
            if i == 19:
                rand_val = int(16 * random.random())
                result.append(chars[(rand_val & 0x3) | 0x8])
            else:
                rand_val = int(16 * random.random())
                result.append(chars[rand_val])
    return ''.join(result) + "-" + user_id


def generate_sign(t: str, token: str, data: str) -> str:
    """生成 API 请求签名"""
    app_key = "34839810"
    msg = f"{token}&{t}&{app_key}&{data}"
    md5_hash = hashlib.md5()
    md5_hash.update(msg.encode('utf-8'))
    return md5_hash.hexdigest()


class MessagePackDecoder:
    """MessagePack 解码器（纯 Python 实现）"""

    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0
        self.length = len(data)

    def read_byte(self) -> int:
        if self.pos >= self.length:
            raise ValueError("Unexpected end of data")
        byte = self.data[self.pos]
        self.pos += 1
        return byte

    def read_bytes(self, count: int) -> bytes:
        if self.pos + count > self.length:
            raise ValueError("Unexpected end of data")
        result = self.data[self.pos:self.pos + count]
        self.pos += count
        return result

    def read_uint8(self) -> int:
        return self.read_byte()

    def read_uint16(self) -> int:
        return struct.unpack('>H', self.read_bytes(2))[0]

    def read_uint32(self) -> int:
        return struct.unpack('>I', self.read_bytes(4))[0]

    def read_uint64(self) -> int:
        return struct.unpack('>Q', self.read_bytes(8))[0]

    def read_int8(self) -> int:
        return struct.unpack('>b', self.read_bytes(1))[0]

    def read_int16(self) -> int:
        return struct.unpack('>h', self.read_bytes(2))[0]

    def read_int32(self) -> int:
        return struct.unpack('>i', self.read_bytes(4))[0]

    def read_int64(self) -> int:
        return struct.unpack('>q', self.read_bytes(8))[0]

    def read_float32(self) -> float:
        return struct.unpack('>f', self.read_bytes(4))[0]

    def read_float64(self) -> float:
        return struct.unpack('>d', self.read_bytes(8))[0]

    def read_string(self, length: int) -> str:
        return self.read_bytes(length).decode('utf-8')

    def decode_value(self) -> Any:
        if self.pos >= self.length:
            raise ValueError("Unexpected end of data")
        format_byte = self.read_byte()

        if format_byte <= 0x7f:
            return format_byte
        elif 0x80 <= format_byte <= 0x8f:
            return self.decode_map(format_byte & 0x0f)
        elif 0x90 <= format_byte <= 0x9f:
            return self.decode_array(format_byte & 0x0f)
        elif 0xa0 <= format_byte <= 0xbf:
            return self.read_string(format_byte & 0x1f)
        elif format_byte == 0xc0:
            return None
        elif format_byte == 0xc2:
            return False
        elif format_byte == 0xc3:
            return True
        elif format_byte == 0xc4:
            return self.read_bytes(self.read_uint8())
        elif format_byte == 0xc5:
            return self.read_bytes(self.read_uint16())
        elif format_byte == 0xc6:
            return self.read_bytes(self.read_uint32())
        elif format_byte == 0xca:
            return self.read_float32()
        elif format_byte == 0xcb:
            return self.read_float64()
        elif format_byte == 0xcc:
            return self.read_uint8()
        elif format_byte == 0xcd:
            return self.read_uint16()
        elif format_byte == 0xce:
            return self.read_uint32()
        elif format_byte == 0xcf:
            return self.read_uint64()
        elif format_byte == 0xd0:
            return self.read_int8()
        elif format_byte == 0xd1:
            return self.read_int16()
        elif format_byte == 0xd2:
            return self.read_int32()
        elif format_byte == 0xd3:
            return self.read_int64()
        elif format_byte == 0xd9:
            return self.read_string(self.read_uint8())
        elif format_byte == 0xda:
            return self.read_string(self.read_uint16())
        elif format_byte == 0xdb:
            return self.read_string(self.read_uint32())
        elif format_byte == 0xdc:
            return self.decode_array(self.read_uint16())
        elif format_byte == 0xdd:
            return self.decode_array(self.read_uint32())
        elif format_byte == 0xde:
            return self.decode_map(self.read_uint16())
        elif format_byte == 0xdf:
            return self.decode_map(self.read_uint32())
        elif format_byte >= 0xe0:
            return format_byte - 256
        else:
            raise ValueError(f"Unknown format byte: 0x{format_byte:02x}")

    def decode_array(self, size: int) -> List[Any]:
        return [self.decode_value() for _ in range(size)]

    def decode_map(self, size: int) -> Dict[Any, Any]:
        result = {}
        for _ in range(size):
            key = self.decode_value()
            value = self.decode_value()
            result[key] = value
        return result

    def decode(self) -> Any:
        try:
            return self.decode_value()
        except Exception:
            return base64.b64encode(self.data).decode('utf-8')


def decrypt(data: str) -> str:
    """解密闲鱼 WebSocket 消息"""
    try:
        cleaned_data = ''.join(
            c for c in data
            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        )
        while len(cleaned_data) % 4 != 0:
            cleaned_data += '='

        try:
            decoded_bytes = base64.b64decode(cleaned_data)
        except Exception as e:
            return json.dumps({"error": f"Base64 decode failed: {str(e)}", "raw_data": data})

        try:
            decoder = MessagePackDecoder(decoded_bytes)
            result = decoder.decode()

            def json_serializer(obj):
                if isinstance(obj, bytes):
                    try:
                        return obj.decode('utf-8')
                    except:
                        return base64.b64encode(obj).decode('utf-8')
                elif hasattr(obj, '__dict__'):
                    return obj.__dict__
                else:
                    return str(obj)

            return json.dumps(result, ensure_ascii=False, default=json_serializer)
        except Exception as e:
            try:
                text_result = decoded_bytes.decode('utf-8')
                return json.dumps({"text": text_result})
            except:
                hex_result = decoded_bytes.hex()
                return json.dumps({"hex": hex_result, "error": f"Decode failed: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"Decrypt failed: {str(e)}", "raw_data": data})
