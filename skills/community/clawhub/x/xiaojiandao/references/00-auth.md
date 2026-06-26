# 认证与加密协议

**Base URL**：`https://biyi.cxtfun.com`

## Token 获取

1. 访问小剪刀官网：https://xjd.funshion.com/
2. 点击右上角的openclaw
3. 登录后，可以获取Token

## 请求头构造

| 请求头 | 值 |
|--------|-----|
| `Content-Type` | `application/x-aes-ms-txt` |
| `pkgname` | `com.biyi.mscissors` |
| `device` | AES加密后的设备信息（Base64） |
| `appsecret` | Token（从抓包获取） |
| `x-ms-at` | 当前毫秒时间戳（字符串） |

## 设备信息 JSON

```json
{
  "app_os": "macos macOS 15.6",
  "app_vn": "1.0.9",
  "appid": 1,
  "arch": "aarch64",
  "cpu_model": "Apple M2",
  "mac": "5E:DF:20:60:17:13",
  "pkg_name": "com.funshion.biyi",
  "api_vn": 1
}
```

> ⚠️ 注意：`pkg_name` 为 `com.funshion.biyi`（服务端包名），但 CLI `--pkgname` 参数仍为 `com.biyi.mscissors`（用于 AES Key 映射查表）。两者不同！

## AES 加密参数

| 参数 | 值 |
|------|-----|
| 算法 | AES-128-CBC |
| Padding | PKCS7 |
| Key | `bz.srv.yz.2025!@`（`com.biyi.mscissors`） |
| IV | `md5(pkgname + x-ms-at)[8:24]`（16字符） |

**Key 映射表**（CLI `--pkgname` 参数值，对应 AES Key）：
```python
{
    "com.biyi.wscissors": "wd.srv.yz.2025!@",
    "com.biyi.mscissors": "bz.srv.yz.2025!@",
}
# 默认: "biyi#def!918.dyj"
```

> ⚠️ 注意：`com.funshion.biyi` 是设备信息 JSON 中的 `pkg_name`，用于服务端包名识别；CLI `--pkgname` 仍用 `com.biyi.mscissors` 查 AES Key 映射表。两者不同！

## Python 加解密完整实现

```python
import hashlib, base64, json, time, uuid, platform
from Crypto.Cipher import AES

def pkcs7_pad(data, block_size=16):
    return data + bytes([block_size - len(data) % block_size]) * (block_size - len(data) % block_size)

def pkcs7_unpad(data, block_size=16):
    pad_len = data[-1]
    return data[:-pad_len]

def get_aes_key(pkgname):
    return {"com.biyi.mscissors": "bz.srv.yz.2025!@"}.get(pkgname, "biyi#def!918.dyj")

def get_aes_iv(pkgname, unix_ms):
    return hashlib.md5(f"{pkgname}{unix_ms}".encode()).hexdigest()[8:24]

def encrypt_string(text, pkgname, unix_ms):
    key = get_aes_key(pkgname).encode()
    iv = get_aes_iv(pkgname, unix_ms).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(pkcs7_pad(text.encode()))).decode()

def decrypt_string(b64_text, pkgname, unix_ms):
    key = get_aes_key(pkgname).encode()
    iv = get_aes_iv(pkgname, unix_ms).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return pkcs7_unpad(cipher.decrypt(base64.b64decode(b64_text))).decode()

def default_device_info(pkgname, appid=1, api_vn=1):
    sys = platform.system().lower()
    os_name = "macos" if sys == "darwin" else ("windows" if sys.startswith("win") else sys)
    return {
        "app_os": f"{os_name} {platform.version()}",
        "app_vn": "0.0.0-dev",
        "appid": appid,
        "pkg_name": pkgname,
        "mac": "00:00:00:00:00:00",
        "arch": platform.machine() or "unknown",
        "cpu_model": platform.processor() or "",
        "api_vn": api_vn,
    }
    # 注意：新版 app (如 1.0.9) 设备信息中无 cl 和 device_id 字段

class HookHttpClient:
    def __init__(self, base_url, pkgname, appsecret, appid=1, api_vn=1, timeout_s=30):
        self.base_url = base_url
        self.pkgname = pkgname
        self.appsecret = appsecret
        self.appid = appid
        self.api_vn = api_vn
        self.timeout_s = timeout_s

    def _build_headers(self, unix_ms):
        device_info = default_device_info(self.pkgname, self.appid, self.api_vn)
        device_json = json.dumps(device_info, ensure_ascii=False, separators=(",", ":"))
        encrypted_device = encrypt_string(device_json, self.pkgname, unix_ms)
        return {
            "Content-Type": "application/x-aes-ms-txt",
            "pkgname": self.pkgname,
            "device": encrypted_device,
            "appsecret": self.appsecret,
            "x-ms-at": str(unix_ms),
        }

    def post(self, endpoint, payload):
        import requests
        unix_ms = int(time.time() * 1000)
        headers = self._build_headers(unix_ms)
        body_plain = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) if payload else "null"
        body_enc = encrypt_string(body_plain, self.pkgname, unix_ms)
        url = self.base_url.rstrip("/") + endpoint
        # self.base_url 应为 "https://biyi.cxtfun.com"
        resp = requests.post(url, data=body_enc.encode(), headers=headers, timeout=self.timeout_s)
        if resp.status_code != 200:
            return {"err_code": resp.status_code, "data": None}, {}
        resp_unix_ms = unix_ms
        if "x-ms-at" in resp.headers:
            resp_unix_ms = int(resp.headers["x-ms-at"])
        decrypted = decrypt_string(resp.text, self.pkgname, resp_unix_ms)
        return json.loads(decrypted), dict(resp.headers)
```

## 响应解密注意事项

服务端响应有时在 JSON 前夹杂调试字符，解密后需截取：

```python
decrypted = decrypt_string(resp.text, pkgname, resp_unix_ms)
# 找第一个 '{' 到最后一个 '}'
start = decrypted.find('{')
end = decrypted.rfind('}')
if start != -1 and end != -1 and end > start:
    result = json.loads(decrypted[start:end+1])
else:
    result = json.loads(decrypted)
```
