---
name: qrcode-scan
version: 1.0.0
description: QR code scanning and generation. Invoke when user needs to scan/decode QR codes from images, generate QR codes (text, URL, WiFi), or mentions QR code related tasks.
author: Moxin
triggers:
    - "scan qr code"
    - "qrcode scan"
    - "generate qr code"
    - "create qr code"
    - "wifi qr code"
    - "decode qr code"
    - "二维码扫描"
    - "二维码生成"
    - "扫描二维码"
    - "生成二维码"
---

# QR Code Scan & Generate

基于 [qrcode](https://github.com/lincolnloop/python-qrcode) 和 [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) 的二维码扫描和生成工具。

## When to Use This Skill

当用户有以下请求时，应该激活此技能：

- **扫描/解码二维码**：
  - "扫描这个二维码图片"
  - "解码二维码"
  - "读取二维码内容"
  - "这个二维码是什么"

- **生成二维码**：
  - "生成一个二维码"
  - "创建二维码"
  - "把这段文字转成二维码"
  - "生成网址二维码"

- **WiFi 二维码**：
  - "生成 WiFi 二维码"
  - "创建 WiFi 分享码"
  - "解析 WiFi 二维码"

## 依赖安装

```bash
pip install qrcode pillow pyzbar
```

**注意**：Windows 用户可能需要安装 Visual C++ Redistributable，详见 [pyzbar 文档](https://pypi.org/project/pyzbar/)。

## 支持的输入格式

### 扫描二维码输入
- **文件路径**：本地图片文件路径
- **URL**：网络图片地址
- **Base64**：Base64 编码的图片数据

### 生成二维码输出
- **PNG 图片文件**：保存到指定路径
- **Base64 字符串**：返回 Base64 编码的图片

## 命令行使用

（注意：如果想要更快速和节省Token，你应该优先使用命令行的方式！）

### 扫描二维码

```bash
python scripts/main.py scan <input> [--format json]
```

参数：
- `input`：图片路径、URL 或 base64 数据
- `--format json`：以 JSON 格式输出结果

### 生成二维码

```bash
python scripts/main.py generate <content> --output <path> [--type text|url|wifi]
```

参数：
- `content`：要编码的内容
- `--output`：输出文件路径（可选，不指定则输出 base64）
- `--type`：二维码类型（text/url/wifi，默认 text）

### 生成 WiFi 二维码

```bash
python scripts/main.py wifi --ssid <SSID> --password <PASSWORD> --security WPA --output <path>
```

参数：
- `--ssid`：WiFi 名称
- `--password`：WiFi 密码
- `--security`：加密类型（WPA/WEP/NONE，默认 WPA）
- `--output`：输出文件路径（可选）

## Python API 使用

### 快速开始

```python
from scripts.main import scan_qrcode, generate_qrcode, generate_wifi_qrcode

# 扫描二维码
result = scan_qrcode("qrcode.png")
print(result)  # 解码内容

# 生成文字二维码
generate_qrcode("Hello World", output_path="output.png")

# 生成 URL 二维码
generate_qrcode("https://example.com", qr_type="url", output_path="url_qr.png")

# 生成 WiFi 二维码
generate_wifi_qrcode("MyWiFi", "password123", security="WPA", output_path="wifi_qr.png")
```

### 从 Base64 扫描

```python
from scripts.main import scan_qrcode

# base64 字符串（支持带或不带 data:image 前缀）
result = scan_qrcode("data:image/png;base64,iVBORw0KGgo...")
# 或纯 base64
result = scan_qrcode("iVBORw0KGgo...", input_type="base64")
```

### 从 URL 扫描

```python
from scripts.main import scan_qrcode

result = scan_qrcode("https://example.com/qrcode.png")
```

### 解析 WiFi 二维码

```python
from scripts.main import scan_qrcode, parse_wifi_qrcode

result = scan_qrcode("wifi_qr.png")
wifi_info = parse_wifi_qrcode(result)
print(wifi_info)
# {'ssid': 'MyWiFi', 'password': 'password123', 'security': 'WPA'}
```

## API Reference

### `scan_qrcode(input_data, input_type=None, format_json=False)`

扫描并解码二维码图片。

**参数：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `input_data` | `str` | 是 | 图片路径、URL 或 base64 数据 |
| `input_type` | `str` | 否 | 输入类型：`file`/`url`/`base64`，自动检测 |
| `format_json` | `bool` | 否 | 是否返回 JSON 格式结果 |

**返回值：**

- `str` 或 `dict`：解码内容，多个二维码时返回列表

**异常：**

- `FileNotFoundError`：文件不存在
- `ValueError`：无法解码二维码
- `ImportError`：缺少依赖库

---

### `generate_qrcode(content, output_path=None, qr_type='text', size=10, border=4)`

生成二维码图片。

**参数：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `content` | `str` | 是 | 要编码的内容 |
| `output_path` | `str` | 否 | 输出文件路径，不指定则返回 base64 |
| `qr_type` | `str` | 否 | 二维码类型：`text`/`url`/`wifi` |
| `size` | `int` | 否 | 二维码尺寸（每个模块的像素数） |
| `border` | `int` | 否 | 边框宽度（模块数） |

**返回值：**

- `str`：base64 编码的图片（未指定 output_path 时）
- `None`：保存到文件（指定 output_path 时）

---

### `generate_wifi_qrcode(ssid, password, security='WPA', output_path=None, hidden=False)`

生成 WiFi 配置二维码。

**参数：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `ssid` | `str` | 是 | WiFi 名称 |
| `password` | `str` | 是 | WiFi 密码 |
| `security` | `str` | 否 | 加密类型：`WPA`/`WEP`/`NONE` |
| `output_path` | `str` | 否 | 输出文件路径 |
| `hidden` | `bool` | 否 | 是否隐藏网络 |

**返回值：**

- `str`：base64 编码的图片或 None

---

### `parse_wifi_qrcode(content)`

解析 WiFi 二维码内容。

**参数：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `content` | `str` | 是 | 二维码解码内容 |

**返回值：**

- `dict`：包含 `ssid`、`password`、`security` 的字典
- `None`：如果不是有效的 WiFi 二维码

## 最佳实践

1. **扫描二维码**：
   - 确保图片清晰，分辨率足够
   - 支持常见格式：PNG、JPEG、BMP、GIF
   - 图片中可以有多个二维码，会全部返回

2. **生成二维码**：
   - 内容越长，二维码越复杂
   - 建议使用 `size=10` 以上保证可扫描性
   - URL 类型会自动验证格式

3. **WiFi 二维码**：
   - 使用 WPA 加密最常见
   - 密码可能包含特殊字符，会自动处理
   - 扫描后手机可直接连接 WiFi

## 完整示例

```python
from scripts.main import scan_qrcode, generate_qrcode, generate_wifi_qrcode, parse_wifi_qrcode

# 生成并扫描 URL 二维码
generate_qrcode("https://github.com", output_path="github_qr.png")
result = scan_qrcode("github_qr.png")
print(f"扫描结果: {result}")

# 生成 WiFi 二维码
generate_wifi_qrcode(
    ssid="MyHomeWiFi",
    password="MySecurePassword123",
    security="WPA",
    output_path="wifi_qr.png"
)

# 解析 WiFi 二维码
wifi_content = scan_qrcode("wifi_qr.png")
wifi_info = parse_wifi_qrcode(wifi_content)
print(f"WiFi 信息: SSID={wifi_info['ssid']}, 密码={wifi_info['password']}")

# 从 base64 生成并获取 base64 输出
base64_qr = generate_qrcode("Hello World")
print(f"Base64 QR: {base64_qr[:50]}...")

# 扫描网络图片
result = scan_qrcode("https://example.com/qrcode.png")
```
