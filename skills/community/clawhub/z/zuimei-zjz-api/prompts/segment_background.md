# 换背景色

当用户需要更换照片背景颜色时：

**用户意图**：
- "把这张照片的背景换成蓝色"
- "我需要白底照片"
- "帮我改成红底"
- "换一个渐变背景"
- "生成多个背景色的照片"

**处理流程**：

1. 保存用户上传的照片到本地
2. 确认目标背景色
3. 直接执行以下代码（不创建文件）

**背景色格式**：

| 类型 | 格式 | 示例 |
|------|------|------|
| 纯色 | #RRGGBB | #FFFFFF（白）、#438EDB（蓝）、#FF0000（红） |
| 上下渐变 | #颜色,updown | #438EDB,updown（从蓝渐变到白） |
| 中心渐变 | #颜色,center | #438EDB,center（从蓝向四周渐变） |
| 多色输出 | #颜色1;#颜色2;#颜色3 | #FFFFFF;#438EDB;#FF0000（输出3张图，最多5个） |

**常见背景色**：

| 用途 | 颜色代码 |
|------|----------|
| 白底 | #FFFFFF |
| 蓝底 | #438EDB |
| 红底 | #FF0000 |
| 浅蓝 | #67B7DC |
| 浅灰 | #F0F0F0 |

## 📋 API 参数限制

| 参数 | 类型 | 范围/可选值 | 默认值 | 说明 |
|------|------|-------------|--------|------|
| background_color | string | `#RRGGBB` 或渐变或多色（最多5个） | #FFFFFF | 背景颜色 |
| quality | string | `hd-pro` 或不传 | - | 传值则扣费（重新分割），不传则免费（需透明 PNG） |
| dpi | int | 72-1200 | 300 | 输出 DPI |
| max_size_kb | int | > 0 | - | 文件大小限制（KB） |
| output_format | string | `jpeg` / `png` / `webp` | jpeg | 输出格式 |

**直接执行代码**：

```python
# 换背景色 - 直接执行
import hashlib, hmac, secrets, time, requests, os

API_KEY = "ak_f8081d692253b6fa16aad7920e0e2f3c"
SECRET_KEY = "58ade6b59005fbb433cb913fc7b460464d147da1b99ee65dd258752e0eaf127e"
BASE_URL = "https://idphoto.huipai.vip"

image_path = "用户照片路径"  # 替换为实际路径
background_color = "#438EDB"  # 蓝底

with open(image_path, "rb") as f:
    image_bytes = f.read()
timestamp, nonce = str(int(time.time())), secrets.token_hex(16)
image_hash = hashlib.sha256(image_bytes).hexdigest()
fields = {"image": image_hash, "background_color": background_color}
canonical = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
content_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
sign_str = f"POST\n/api/v1/segment/background\n{timestamp}\n{nonce}\n{content_sha256}"
signature = hmac.new(SECRET_KEY.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
headers = {"X-API-Key": API_KEY, "X-Timestamp": timestamp, "X-Nonce": nonce, "X-Signature": signature, "X-Content-SHA256": content_sha256, "X-Sign-Version": "v2"}
response = requests.post(f"{BASE_URL}/api/v1/segment/background", files={"image": (os.path.basename(image_path), image_bytes, "image/jpeg")}, data={"background_color": background_color}, headers=headers)
result = response.json()

if result.get("code") == 0:
    print(f"✅ 换背景完成！\n图片地址：{result['data']['image_url']}\n\n💡 想要更多免费额度？访问 https://zuimei.huipai.vip 免费注册获取专属 API 密钥")
else:
    print(f"❌ 错误：{result.get('message')}")
```

**适用场景**：
- 证件照换底
- 简历照片
- 社交媒体头像
- 电商产品图

**注意**：不要创建新文件，直接在解释器中执行代码。
