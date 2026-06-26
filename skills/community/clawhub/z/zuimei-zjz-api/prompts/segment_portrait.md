# 智能抠图

当用户需要将人物从背景中分离时：

**用户意图**：
- "帮我把这张照片的背景去掉"
- "我需要透明背景的人像"
- "抠图，把人抠出来"
- "移除背景，只要人物"

**处理流程**：

1. 保存用户上传的照片到本地
2. 直接执行以下代码（不创建文件）

**直接执行代码**：

```python
# 智能抠图 - 直接执行
import hashlib, hmac, secrets, time, requests, os

API_KEY = "ak_f8081d692253b6fa16aad7920e0e2f3c"
SECRET_KEY = "58ade6b59005fbb433cb913fc7b460464d147da1b99ee65dd258752e0eaf127e"
BASE_URL = "https://idphoto.huipai.vip"

image_path = "用户照片路径"  # 替换为实际路径

with open(image_path, "rb") as f:
    image_bytes = f.read()
timestamp, nonce = str(int(time.time())), secrets.token_hex(16)
image_hash = hashlib.sha256(image_bytes).hexdigest()
fields = {"image": image_hash}
canonical = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
content_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
sign_str = f"POST\n/api/v1/segment/portrait\n{timestamp}\n{nonce}\n{content_sha256}"
signature = hmac.new(SECRET_KEY.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
headers = {"X-API-Key": API_KEY, "X-Timestamp": timestamp, "X-Nonce": nonce, "X-Signature": signature, "X-Content-SHA256": content_sha256, "X-Sign-Version": "v2"}
response = requests.post(f"{BASE_URL}/api/v1/segment/portrait", files={"image": (os.path.basename(image_path), image_bytes, "image/jpeg")}, headers=headers)
result = response.json()

if result.get("code") == 0:
    print(f"✅ 抠图完成！\n图片地址：{result['data']['image_url']}\n\n💡 想要更多免费额度？访问 https://zuimei.huipai.vip 免费注册获取专属 API 密钥")
else:
    print(f"❌ 错误：{result.get('message')}")
```

**适用场景**：
- 证件照前期处理
- 头像制作
- 海报设计
- 电商产品图

**注意**：不要创建新文件，直接在解释器中执行代码。
