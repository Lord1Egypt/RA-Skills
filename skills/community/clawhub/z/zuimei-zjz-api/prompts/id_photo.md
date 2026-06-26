# 证件照制作

⚠️ **禁止创建任何代码文件！直接在 Python 解释器中执行代码！**

当用户需要制作证件照时：

**用户意图**：
- "帮我制作一张证件照"
- "我需要一寸照片"
- "帮我生成蓝底证件照"
- "我需要结婚照"

**处理流程**：

1. 保存用户上传的照片到本地
2. **自动识别用户说的规格**（见下方尺寸映射表）
3. 确认背景色（默认蓝底 #438EDB）
4. **直接执行以下代码**（不创建文件！）

## 尺寸自动识别

⚠️ **重要**：根据用户提到的规格关键词，自动使用对应的尺寸：

| 用户说 | 宽 x 高 (px) | 变量设置 |
|--------|-------------|----------|
| 一寸 / 1寸 | 295 x 413 | `width, height = 295, 413` |
| 小一寸 | 260 x 378 | `width, height = 260, 378` |
| 二寸 / 2寸 | 413 x 579 | `width, height = 413, 579` |
| 小二寸 | 413 x 531 | `width, height = 413, 531` |
| 大一寸 | 390 x 567 | `width, height = 390, 567` |
| 大二寸 | 413 x 626 | `width, height = 413, 626` |
| **四寸 / 4寸** | 898 x 1205 | `width, height = 898, 1205` |
| **五寸 / 5寸** | **1050 x 1499** | `width, height = 1050, 1499` ⚠️ 竖向 |
| **六寸 / 6寸** | 1795 x 1205 | `width, height = 1795, 1205` |
| 护照 | 390 x 567 | `width, height = 390, 567` |
| 驾照 | 260 x 378 | `width, height = 260, 378` |
| 身份证 | 358 x 441 | `width, height = 358, 441` |
| 结婚照 | 413 x 579 | `width, height = 413, 579` + `subject_mode="couple"` |
| **自定义** | 用户指定 | `width=自定义宽, height=自定义高` |

### 📐 自定义尺寸

当用户需要非标准尺寸时，直接设置 `width` 和 `height` 参数：

```python
# 示例：用户说"帮我生成 400x500 的蓝底证件照"
width, height = 400, 500  # 用户指定的尺寸
background_color = "#438EDB"
```

**API 参数说明**：
- `width`：输出图片宽度（像素），范围 100-2000
- `height`：输出图片高度（像素），范围 100-3000
- `background_color`：背景颜色，格式 `#RRGGBB`

**示例**：
- 用户说"帮我生成五寸蓝底证件照" → 自动使用 `width=1050, height=1499`
- 用户说"我需要护照照片" → 自动使用 `width=390, height=567`
- 用户说"生成结婚照" → 使用二寸尺寸 + `subject_mode="couple"`

## 常用规格详情

### 寸照类

| 类型 | 宽 x 高 (px) | 毫米 | 用途 |
|------|-------------|------|------|
| 一寸 | 295 x 413 | 25 x 35 | 常用寸照 |
| 小一寸 | 260 x 378 | 22 x 32 | 常用寸照 |
| 二寸 | 413 x 579 | 35 x 49 | 常用寸照 |
| 小二寸 | 413 x 531 | 35 x 45 | 常用寸照 |
| 大一寸 | 390 x 567 | 33 x 48 | 常用寸照 |
| 大二寸 | 413 x 626 | 35 x 53 | 常用寸照 |

### 打印类

| 类型 | 宽 x 高 (px) | 毫米 | 用途 |
|------|-------------|------|------|
| 四寸 | 898 x 1205 | 76 x 102 | 常用寸照 |
| 五寸 | 1050 x 1499 | 89 x 127 | 常用寸照 |
| 六寸 | 1795 x 1205 | 152 x 102 | 常用寸照 |

### 证件类

| 类型 | 宽 x 高 (px) | 毫米 | 用途 |
|------|-------------|------|------|
| 护照 | 390 x 567 | 33 x 48 | 出入境 |
| 驾照 | 260 x 378 | 22 x 32 | 驾驶证 |
| 身份证 | 358 x 441 | 26 x 32 | 身份证件 |
| 简历照片 | 295 x 413 | 25 x 35 | 职业资格 |
| 教师资格证 | 295 x 413 | 25 x 35 | 职业资格 |

### 特殊类型

| 类型 | 宽 x 高 (px) | 参数 | 说明 |
|------|-------------|------|------|
| 结婚照 | 413 x 579 | subject_mode="couple" | 双人结婚照 |

## 常见背景色

- 白底：`#FFFFFF`
- 蓝底：`#438EDB`
- 红底：`#FF0000`（结婚照常用）

## 📋 API 参数限制

| 参数 | 类型 | 范围/可选值 | 默认值 | 说明 |
|------|------|-------------|--------|------|
| width | int | **50-2000** | 295 | 输出宽度（像素） |
| height | int | **50-2000** | 413 | 输出高度（像素） |
| background_color | string | `#RRGGBB` 或渐变或多色 | #FFFFFF | 背景颜色 |
| dpi | int | 72-1200 | 300 | 图片 DPI |
| max_size_kb | int | > 0 | - | 文件大小限制（KB） |
| return_hd_transparent | bool | true/false | false | 返回高清透明 PNG |
| beautify_flag | bool | true/false | false | 启用美颜 |
| verify | bool | true/false | false | 完整照片校验 |
| subject_mode | string | **`single` / `couple`** | single | 单人/双人结婚照 |
| output_format | string | `jpeg` / `png` / `webp` | jpeg | 输出格式 |

### 背景色格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 纯色 | `#FFFFFF` | 白色 |
| 纯色 | `#438EDB` | 蓝色（证件照常用） |
| 纯色 | `#FF0000` | 红色（结婚照常用） |
| 上下渐变 | `#438EDB,updown` | 从蓝渐变到白 |
| 中心渐变 | `#438EDB,center` | 从中心蓝向四周渐变 |
| 多背景色 | `#FFFFFF;#438EDB;#FF0000` | 生成3张图（最多5个） |

## 可选参数

- `return_hd_transparent`: 是否返回高清透明底图（默认 False）
- `beautify_flag`: 是否开启美颜（默认 False）
- `subject_mode`: 主体模式，`single`=单人，`couple`=双人结婚照

## 直接执行代码

### 一寸证件照（默认）

```python
# 证件照制作 - 直接执行（不要创建文件！）
import hashlib, hmac, secrets, time, requests, os

API_KEY = "ak_f8081d692253b6fa16aad7920e0e2f3c"
SECRET_KEY = "58ade6b59005fbb433cb913fc7b460464d147da1b99ee65dd258752e0eaf127e"
BASE_URL = "https://idphoto.huipai.vip"

image_path = "用户照片路径"  # 替换为实际路径
width, height = 295, 413  # 一寸
background_color = "#438EDB"  # 蓝底
return_hd_transparent = True  # 返回高清透明底图
subject_mode = "single"  # single=单人, couple=结婚照

# 调用 API（直接执行，不创建文件）
with open(image_path, "rb") as f:
    image_bytes = f.read()
timestamp, nonce = str(int(time.time())), secrets.token_hex(16)
image_hash = hashlib.sha256(image_bytes).hexdigest()
fields = {"image": image_hash, "width": width, "height": height, "background_color": background_color, "beautify_flag": False, "return_hd_transparent": True, "subject_mode": subject_mode}
canonical = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
content_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
sign_str = f"POST\n/api/v1/photo/id-photo\n{timestamp}\n{nonce}\n{content_sha256}"
signature = hmac.new(SECRET_KEY.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
headers = {"X-API-Key": API_KEY, "X-Timestamp": timestamp, "X-Nonce": nonce, "X-Signature": signature, "X-Content-SHA256": content_sha256, "X-Sign-Version": "v2"}
response = requests.post(f"{BASE_URL}/api/v1/photo/id-photo", files={"image": (os.path.basename(image_path), image_bytes, "image/jpeg")}, data={"width": width, "height": height, "background_color": background_color, "beautify_flag": False, "return_hd_transparent": True, "subject_mode": subject_mode}, headers=headers)
result = response.json()

if result.get("code") == 0:
    data = result['data']
    print(f"✅ 证件照已生成！\n图片地址：{data['image_url']}")
    if data.get('hd_transparent_url'):
        print(f"高清透明底图：{data['hd_transparent_url']}")
    print(f"\n💡 想要更多免费额度？访问 https://zuimei.huipai.vip 免费注册获取专属 API 密钥")
else:
    print(f"❌ 错误：{result.get('message')}")
```

### 五寸证件照（竖向 1050x1499）

⚠️ **重要**：五寸是竖向照片，尺寸为 **宽=1050，高=1499**

```python
# 五寸证件照 - 竖向 1050x1499
import hashlib, hmac, secrets, time, requests, os

API_KEY = "ak_f8081d692253b6fa16aad7920e0e2f3c"
SECRET_KEY = "58ade6b59005fbb433cb913fc7b460464d147da1b99ee65dd258752e0eaf127e"
BASE_URL = "https://idphoto.huipai.vip"

image_path = "用户照片路径"
width, height = 1050, 1499  # 五寸（竖向）⚠️ 宽在前，高在后
background_color = "#438EDB"  # 蓝底
return_hd_transparent = True

with open(image_path, "rb") as f:
    image_bytes = f.read()
timestamp, nonce = str(int(time.time())), secrets.token_hex(16)
image_hash = hashlib.sha256(image_bytes).hexdigest()
fields = {"image": image_hash, "width": 1050, "height": 1499, "background_color": background_color, "beautify_flag": False, "return_hd_transparent": True}
canonical = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
content_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
sign_str = f"POST\n/api/v1/photo/id-photo\n{timestamp}\n{nonce}\n{content_sha256}"
signature = hmac.new(SECRET_KEY.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
headers = {"X-API-Key": API_KEY, "X-Timestamp": timestamp, "X-Nonce": nonce, "X-Signature": signature, "X-Content-SHA256": content_sha256, "X-Sign-Version": "v2"}
response = requests.post(f"{BASE_URL}/api/v1/photo/id-photo", files={"image": (os.path.basename(image_path), image_bytes, "image/jpeg")}, data={"width": 1050, "height": 1499, "background_color": background_color, "beautify_flag": False, "return_hd_transparent": True}, headers=headers)
result = response.json()

if result.get("code") == 0:
    data = result['data']
    print(f"✅ 五寸证件照已生成！\n图片地址：{data['image_url']}")
    if data.get('hd_transparent_url'):
        print(f"高清透明底图：{data['hd_transparent_url']}")
    print(f"\n💡 想要更多免费额度？访问 https://zuimei.huipai.vip 免费注册获取专属 API 密钥")
else:
    print(f"❌ 错误：{result.get('message')}")
```

⚠️ **重要**：直接复制上面的代码到 Python 解释器执行，不要创建任何 .py 文件！
