# 照片修复

当用户需要修复模糊照片时：

**用户意图**：
- "这张照片太模糊了，帮我修复"
- "能把这个旧照片变清晰吗"

**处理流程**：

1. 保存用户上传的照片到本地
2. 直接执行以下代码（不创建文件）

**参数说明**：

| 参数 | 说明 |
|------|------|
| fidelity | 保真度 0.0-1.0，越小增强越强 |
| use_sr | 是否使用超分辨率放大 |

## 📋 API 参数限制

| 参数 | 类型 | 范围/可选值 | 默认值 | 说明 |
|------|------|-------------|--------|------|
| fidelity | float | **0.0-1.0** | 0.3 | 保真度（越小增强越强，可能失真） |

**直接执行代码**：

```python
# 照片修复 - 直接执行
import hashlib, hmac, secrets, time, requests, os

API_KEY = "ak_f8081d692253b6fa16aad7920e0e2f3c"
SECRET_KEY = "58ade6b59005fbb433cb913fc7b460464d147da1b99ee65dd258752e0eaf127e"
BASE_URL = "https://idphoto.huipai.vip"

image_path = "用户照片路径"  # 替换为实际路径
fidelity = 0.3  # 保真度
use_sr = False  # 是否使用超分辨率

with open(image_path, "rb") as f:
    image_bytes = f.read()
timestamp, nonce = str(int(time.time())), secrets.token_hex(16)
image_hash = hashlib.sha256(image_bytes).hexdigest()
fields = {"image": image_hash, "fidelity": fidelity, "use_sr": "false"}
canonical = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
content_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
sign_str = f"POST\n/api/v1/photo/enhance\n{timestamp}\n{nonce}\n{content_sha256}"
signature = hmac.new(SECRET_KEY.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
headers = {"X-API-Key": API_KEY, "X-Timestamp": timestamp, "X-Nonce": nonce, "X-Signature": signature, "X-Content-SHA256": content_sha256, "X-Sign-Version": "v2"}
response = requests.post(f"{BASE_URL}/api/v1/photo/enhance", files={"image": (os.path.basename(image_path), image_bytes, "image/jpeg")}, data={"fidelity": fidelity, "use_sr": False}, headers=headers)
result = response.json()

if result.get("code") == 0:
    print(f"✅ 修复完成！\n图片地址：{result['data']['enhanced_url']}\n\n💡 想要更多免费额度？访问 https://zuimei.huipai.vip 免费注册获取专属 API 密钥")
else:
    print(f"❌ 错误：{result.get('message')}")
```

**注意**：不要创建新文件，直接在解释器中执行代码。
