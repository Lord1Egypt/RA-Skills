---
name: tencentcloud-ocr-idcard
description: 腾讯云身份证识别(IDCardOCR)接口调用技能。当用户需要识别身份证图片中中国大陆居民二代身份证正反面信息（姓名、性别、民族、出生日期、住址、身份证号、签发机关、有效期限等）时,应使用此技能。支持图片Base64和URL两种输入方式,同时支持身份证图片照片裁剪和多种告警功能。
---

# 腾讯云身份证识别 (IDCardOCR)

## 用途

调用腾讯云OCR身份证识别接口，支持中国大陆居民二代身份证正反面所有字段的识别，识别准确度达99%以上。

核心能力：
- **人像面(FRONT)**：识别姓名、性别、民族、出生日期、住址、公民身份证号
- **国徽面(BACK)**：识别签发机关、证件有效期
- **附加功能**：身份证照片/人像照片裁剪、7种告警检测（复印件、翻拍、PS、临时身份证等）

官方文档：https://cloud.tencent.com/document/api/866/33524

## 使用时机

当用户提出以下需求时触发此技能：
- 需要从身份证图片中提取文字信息
- 需要验证身份证真伪（复印件/翻拍/PS检测）
- 需要裁剪身份证照片或人像照片
- 涉及身份证OCR识别的任何场景

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成身份证识别。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ImageBase64 | str | 否(二选一) | 图片Base64值，不超过10MB |
| ImageUrl | str | 否(二选一) | 图片URL地址，优先使用 |
| CardSide | str | 否 | `FRONT`(人像面) / `BACK`(国徽面)，不填则自动判断 |
| Config | str | 否 | JSON字符串，可选开关见下方说明 |
| EnableRecognitionRectify | bool | 否 | 默认true，开启身份证号/出生日期/性别的矫正补齐 |
| EnableReflectDetail | bool | 否 | 默认false，需配合ReflectWarn使用 |
| CardWarnType | str | 否 | `Basic`(默认) / `Advanced`(进阶PS告警) |
| **UserAgent** | **str** | **否** | **请求来源标识(可选)，用于追踪调用来源，统一固定为`Skills`** |

**Config JSON 可选开关**：`CropIdCard`、`CropPortrait`、`CopyWarn`、`BorderCheckWarn`、`ReshootWarn`、`DetectPsWarn`、`TempIdWarn`、`InvalidDateWarn`、`Quality`、`MultiCardDetect`、`ReflectWarn`

### ⚠️ UserAgent参数使用指南

**`--user-agent`参数是可选参数**,统一固定为`Skills`，无需手动传递。用于标识API调用来源,便于追踪和统计:

| 调用框架 | --user-agent 参数值 | 说明 |
|---------|--------------|------|
| 所有框架 | `Skills` | 统一固定值，不传递时也默认为此值 |

**实现说明**:
- 通过`--user-agent`命令行参数传递，SDK 会将其拼接为 `SDK_PYTHON_x.x.x; Skills` 注入到请求中
- 统一固定为`Skills`，未传递时也默认为此值
- 该标识会记录在ES日志的 `ReqBody.RequestClient` 字段中，可用于追踪来源

### 输出格式

识别成功后返回 JSON 格式结果：

**人像面(FRONT)**：
```json
{
  "Name": "张三",
  "Sex": "男",
  "Nation": "汉",
  "Birth": "1990/01/01",
  "Address": "XX省XX市XX区XX路XX号",
  "IdNum": "110101199001011234",
  "AdvancedInfo": "{\"WarnInfos\":[]}",
  "RequestId": "xxx"
}
```

**国徽面(BACK)**：
```json
{
  "Authority": "XX市公安局",
  "ValidDate": "2020.01.01-2040.01.01",
  "AdvancedInfo": "{\"WarnInfos\":[]}",
  "RequestId": "xxx"
}
```

### 告警码说明

| 告警码 | 含义 |
|--------|------|
| -9100 | 有效日期不合法 |
| -9101 | 边框不完整 |
| -9102 | 复印件 |
| -9103 | 翻拍 |
| -9104 | 临时身份证 |
| -9105 | 框内遮挡 |
| -9106 | PS痕迹 |
| -9107 | 反光 |
| -9108 | 复印件(仅黑白) |
| -9110 | 电子身份证 |

### 调用示例

```bash
# 基础调用示例（--user-agent 默认为 Skills，可不传）
python scripts/main.py --image-url "https://example.com/idcard.jpg" --card-side FRONT

# 使用 Base64 文件调用
python scripts/main.py --image-base64 "/path/to/base64.txt"

# 开启告警检测和照片裁剪
python scripts/main.py --image-url "https://example.com/idcard.jpg" \
  --config '{"CropIdCard":true,"CopyWarn":true,"ReshootWarn":true}'

# 使用进阶PS告警
python scripts/main.py --image-url "https://example.com/idcard.jpg" \
  --card-warn-type Advanced
```
