# 排版照

当用户需要将证件照排版打印时：

**用户意图**：
- "帮我把证件照排成6寸的"
- "我需要打印排版"
- "生成冲印排版"
- "排版成一版多张"

**处理流程**：

1. 保存用户上传的证件照到本地
2. 直接执行以下代码（不创建文件）

**排版规格**：

| 类型 | 尺寸 | 说明 |
|------|------|------|
| 6inch | 6寸（4x6英寸） | 最常用，适合一寸/二寸 |
| 5inch | 5寸（3.5x5英寸） | 小尺寸排版 |
| a4 | A4纸 | 大量排版 |

## 📋 API 参数限制

| 参数 | 类型 | 范围/可选值 | 默认值 | 说明 |
|------|------|-------------|--------|------|
| layout_type | string | **`6inch` / `5inch` / `A4` / `3R` / `4R`** | 6inch | 排版类型 |
| crop_line | bool | true/false | false | 添加裁剪线 |
| watermark | string | **最多6字符** | - | 自定义水印 |

**排版类型对应尺寸：**

| layout_type | 画布尺寸 (px) | 毫米 |
|-------------|--------------|------|
| 6inch / 4R | 1795 x 1205 | 152mm x 102mm |
| 5inch / 3R | 1500 x 1051 | 127mm x 89mm |
| A4 | 3508 x 2479 | 297mm x 210mm |

**直接执行代码**：

```python
# 排版照 - 直接执行
import hashlib, hmac, secrets, time, requests, os

API_KEY = "ak_f8081d692253b6fa16aad7920e0e2f3c"
SECRET_KEY = "58ade6b59005fbb433cb913fc7b460464d147da1b99ee65dd258752e0eaf127e"
BASE_URL = "https://idphoto.huipai.vip"

image_path = "证件照路径"  # 替换为实际路径
layout_type = "6inch"  # 排版类型：6inch/5inch/a4
crop_line = True  # 是否添加裁切线（默认添加）

with open(image_path, "rb") as f:
    image_bytes = f.read()
timestamp, nonce = str(int(time.time())), secrets.token_hex(16)
image_hash = hashlib.sha256(image_bytes).hexdigest()
fields = {"image": image_hash, "layout_type": layout_type, "crop_line": "true"}
canonical = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
content_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
sign_str = f"POST\n/api/v1/photo/layout\n{timestamp}\n{nonce}\n{content_sha256}"
signature = hmac.new(SECRET_KEY.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
headers = {"X-API-Key": API_KEY, "X-Timestamp": timestamp, "X-Nonce": nonce, "X-Signature": signature, "X-Content-SHA256": content_sha256, "X-Sign-Version": "v2"}
response = requests.post(f"{BASE_URL}/api/v1/photo/layout", files={"image": (os.path.basename(image_path), image_bytes, "image/jpeg")}, data={"layout_type": layout_type, "crop_line": True}, headers=headers)
result = response.json()

if result.get("code") == 0:
    print(f"✅ 排版完成！\n图片地址：{result['data']['image_url']}\n共 {result['data']['photo_count']} 张\n\n💡 想要更多免费额度？访问 https://zuimei.huipai.vip 免费注册获取专属 API 密钥")
else:
    print(f"❌ 错误：{result.get('message')}")
```

**适用场景**：
- 证件照打印
- 冲印店冲印
- 自助打印

**注意**：不要创建新文件，直接在解释器中执行代码。
