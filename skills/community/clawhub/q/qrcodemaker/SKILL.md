---
version: 1.0.4
name: QR Code Generator
description: 生成和解析二维码。支持 URL / vCard / WIFI / 纯文本四种模式，可自定义颜色、嵌入 Logo。解析需安装 opencv-python。
---

# QR Code Generator

生成和解析二维码，支持 URL / vCard / WIFI / 纯文本四种模式，可自定义颜色、嵌入 Logo。

## 触发场景

用户发了一张图片并说「生成二维码」「做个二维码」「QR 码」「扫一下这个二维码」「解析二维码」「decode QR」；或指定生成模式如「生成 WIFI 二维码」「生成 vCard 二维码」。

## 依赖

```bash
pip install qrcode pillow
# 解析功能（可选）：
pip install opencv-python
```

## 命令用法

```bash
# URL 模式
python3 scripts/qr_code.py url "https://example.com" -o qr.png

# WIFI 模式
python3 scripts/qr_code.py wifi -s WiFi名称 -p 密码 -o wifi.png

# vCard 模式
python3 scripts/qr_code.py vcard -n 姓名 -t 电话 -e 邮箱 -o card.png

# 解析二维码
python3 scripts/qr_code.py text "任意文本" -o text.png
```

#### 纯文本模式

```bash
# 纯文本（任意内容）
python3 scripts/qr_code.py text "Hello World" -o text.png

# 带颜色
python3 scripts/qr_code.py text "你好" -o text.png --fg black --bg white
```

### 解析二维码

```bash
python3 scripts/qr_code.py decode 图片路径
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--fg` | 前景色（默认 black） |
| `--bg` | 背景色（默认 white） |
| `--logo` | Logo 图片路径 |
| `--logo-size` | Logo 大小比例 0.1~0.3（默认 0.25） |
| `--hidden` | WIFI 隐藏网络 |
