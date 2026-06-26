---
name: smartocr
description: >
  识别车辆证件（行驶证正页/副页）和收据/发票图片，返回结构化 JSON 数据。
  支持图片 URL 和本地文件两种方式，需要 API Key。
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - python3
---

# SmartOCR — 车辆证件与票据识别

从图片中提取结构化信息，支持**行驶证正页、行驶证副页、收据/发票**三种类型，自动判断图片类型并返回对应字段。

## Configuration

Set the following environment variables:
- `SMARTOCR_API_KEY` — API Key（sk- 前缀，必填）
- `SMARTOCR_API_URL` — API 地址（可选，默认 https://smartocr.yunlizhi.cn）

### Option 1: CLI configuration (recommended)

```bash
# Configure API Key
openclaw config set env.vars.SMARTOCR_API_KEY "sk-your-api-key"

# Configure API URL (optional)
openclaw config set env.vars.SMARTOCR_API_URL "http://localhost:5001"
```

### Option 2: Manual configuration

Edit `~/.openclaw/openclaw.json`，在 `env.vars` 中添加：

```json5
{
  "env": {
    "vars": {
      "SMARTOCR_API_KEY": "sk-your-api-key",
      "SMARTOCR_API_URL": "http://localhost:5001"
    }
  }
}
```


## Usage

```bash
# 识别图片 URL
uv run python {baseDir}/scripts/smartocr.py "https://example.com/receipt.jpg"

# 识别本地文件
uv run python {baseDir}/scripts/smartocr.py /path/to/receipt.jpg

# 指定超时时间
uv run python {baseDir}/scripts/smartocr.py -t 30 "https://example.com/vehicle.jpg"

# 输出原始 JSON（不格式化）
uv run python {baseDir}/scripts/smartocr.py --raw /path/to/invoice.jpg
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `image` | 图片 URL 或本地文件路径（必填） | — |
| `-t, --timeout` | 请求超时秒数 | 60 |
| `--raw` | 输出原始 JSON（不格式化） | false |

## 处理对话中上传的图片

当用户在对话中（飞书、WebChat、WeCom 等）直接发送图片时，agent 无法直接获取图片的原始数据。
请改用 `smartocr_from_session.py`，它会直接读取当前会话的 session 文件提取图片：

```bash
# 识别当前会话中最近上传的 1 张图片
uv run python {baseDir}/scripts/smartocr_from_session.py

# 识别最近 N 张图片
uv run python {baseDir}/scripts/smartocr_from_session.py -n 3

# 指定 agent ID（默认 main）
uv run python {baseDir}/scripts/smartocr_from_session.py --agent main

# 指定 session 文件路径（手动覆盖自动查找）
uv run python {baseDir}/scripts/smartocr_from_session.py --session /path/to/session.jsonl
```

脚本自动查找 `~/.openclaw/agents/{agent}/sessions/` 下最新的 session jsonl 文件，
从末尾向前扫描提取最近的图片 base64，直接调用 SmartOCR API 识别。

## 识别类型

| ocr_type | 说明 | 返回字段 |
|----------|------|----------|
| `vehicle_front` | 行驶证正页 | 号牌号码、车辆类型、所有人、品牌型号、车辆识别代号、发动机号码、注册日期、发证日期 |
| `vehicle_rear` | 行驶证副页 | 号牌号码、检验有效期、核定载人数、总质量、整备质量、准牵引总质量 |
| `receipt` | 收据/票据/发票 | 发票号码、开票日期、金额、税额、购买方、销售方、商品名称 |

## 响应格式

```json
{
  "ocr_type": "receipt",
  "content": {
    "发票号码": "12345678",
    "开票日期": "2025-06-01",
    "金额": "128.00",
    "税额": "7.68",
    "购买方": "某某公司",
    "销售方": "某某商店",
    "商品名称": "办公用品"
  }
}
```

> 无法识别的字段值返回 `"无法识别"`。

## 错误码

| 状态码 | 原因 | 处理 |
|--------|------|------|
| 401 | 缺少 X-API-Key | 检查 SMARTOCR_API_KEY 环境变量 |
| 403 | Key 无效或已禁用 | 重新配置 Key |
| 429 | 月度额度已用完（50 次/月） | 等待下月重置或联系管理员 |
| 502 | 识别服务异常 | 稍后重试，建议间隔 2-5 秒最多重试 2 次 |

## 注意事项

- 图片清晰、光线充足时识别效果最佳
- 本地文件会自动转为 Base64 上传，URL 方式更轻量
- 超时建议设置 60 秒
