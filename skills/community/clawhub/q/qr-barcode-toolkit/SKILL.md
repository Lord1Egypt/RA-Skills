---
name: qr-code-toolkit
description: "二维码/条形码全能工具集 - 支持生成、识别、美化、批量处理。Use when: (1) 需要生成二维码（URL/文本/WiFi/名片/支付）, (2) 需要识别/解码二维码或条形码, (3) 需要美化二维码（添加logo/改变颜色/样式）, (4) 需要批量生成或识别二维码, (5) 需要生成条形码（EAN/UPC/Code128）"
---

# QR Code Toolkit

二维码与条形码全能工具集，基于 Python + qrcode + opencv + zxing 实现。

## 核心能力

### 1. 二维码生成
- 基础二维码（文本/URL）
- WiFi 连接二维码
- vCard 名片二维码
- 邮箱/短信/电话二维码
- 支付二维码模板

### 2. 二维码美化
- 添加中心 Logo
- 自定义颜色（前景/背景）
- 圆角/点状/液态样式
- 嵌入背景图片

### 3. 二维码识别
- 图片解码（PNG/JPG/BMP）
- 摄像头实时识别
- 批量识别目录内图片
- 支持损坏/模糊二维码修复

### 4. 条形码生成
- Code128（通用）
- EAN-13（商品条码）
- UPC-A（北美商品码）
- Code39 / ITF / Codabar

### 5. 批量处理
- 批量生成二维码（CSV/Excel 数据源）
- 批量识别并导出结果
- 批量美化处理

## 快速开始

```bash
# 生成基础二维码
python3 scripts/generate_qr.py "https://example.com" --output qr.png

# 生成 WiFi 二维码
python3 scripts/generate_wifi.py --ssid MyWiFi --password secret123 --output wifi_qr.png

# 识别二维码
python3 scripts/decode_qr.py qr.png

# 美化二维码（加logo）
python3 scripts/style_qr.py qr.png --logo logo.png --output styled_qr.png

# 生成条形码
python3 scripts/generate_barcode.py "123456789012" --type ean13 --output barcode.png

# 批量生成
python3 scripts/batch_generate.py data.csv --output-dir ./qrs/
```

## 依赖安装

```bash
pip install -r requirements.txt
```

核心依赖：qrcode, pillow, opencv-python, pyzbar, python-barcode

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `generate_qr.py` | 生成基础二维码 |
| `generate_wifi.py` | 生成 WiFi 连接二维码 |
| `generate_vcard.py` | 生成名片二维码 |
| `decode_qr.py` | 识别/解码二维码 |
| `style_qr.py` | 美化二维码 |
| `generate_barcode.py` | 生成条形码 |
| `batch_generate.py` | 批量生成 |
| `batch_decode.py` | 批量识别 |
| `verify_qr.py` | 二维码验证与质量检测 |

## 详细用法

参见 `references/` 目录：
- `qr-standards.md` - 二维码标准与容量说明
- `barcode-types.md` - 条形码类型参考
- `api-reference.md` - 脚本 API 参考
