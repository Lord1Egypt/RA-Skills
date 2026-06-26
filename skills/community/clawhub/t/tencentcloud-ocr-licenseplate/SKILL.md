---
name: tencentcloud-ocr-licenseplate
description: 腾讯云车牌识别(LicensePlateOCR)接口调用技能。当用户需要对中国大陆机动车车牌进行自动定位和识别时，应使用此技能。支持返回车牌号码、车牌颜色、置信度和像素坐标信息，支持多车牌场景识别，支持图片Base64和URL两种输入方式。
---

# 腾讯云车牌识别 (LicensePlateOCR)

## 用途

调用腾讯云OCR车牌识别接口，支持对中国大陆机动车车牌的自动定位和识别，返回地域编号和车牌号码与车牌颜色信息。

核心能力：
- **车牌号码识别**：自动定位并识别车牌号码（如：京AF0236）
- **车牌颜色识别**：支持白、黑、蓝、绿、黄、黄绿、临牌、喷漆、其它
- **车牌类别判断**：区分实体车牌与非实体车牌
- **多车牌识别**：支持图片中存在多个车牌的场景，通过 LicensePlateInfos 返回全部车牌信息
- **坐标定位**：返回车牌在原图中的像素坐标框（X, Y, Width, Height）

官方文档：https://cloud.tencent.com/document/api/866/36211

默认接口请求频率限制：10次/秒。

## 使用时机

当用户提出以下需求时触发此技能：
- 需要从图片中识别机动车车牌号码
- 需要获取车牌颜色信息
- 需要判断车牌类别（实体/非实体）
- 图片中包含多个车牌需要全部识别
- 涉及车牌OCR识别的任何场景

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成车牌识别。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ImageBase64 | str | 否(二选一) | 图片Base64值，编码后不超过10M，支持PNG/JPG/JPEG，不支持GIF |
| ImageUrl | str | 否(二选一) | 图片URL地址，下载时间不超过3秒。都提供时仅使用ImageUrl |
| **UserAgent** | **str** | **否** | **请求来源标识(可选)，用于追踪调用来源，统一固定为`Skills`** |

### 输出格式

识别成功后返回 JSON 格式结果：

```json
{
  "Number": "京AF0236",
  "Confidence": 99,
  "Color": "蓝",
  "LicensePlateCategory": "实体车牌",
  "Rect": {
    "X": 426,
    "Y": 423,
    "Width": 135,
    "Height": 66
  },
  "LicensePlateInfos": [
    {
      "Number": "京AF0236",
      "Confidence": 99,
      "Color": "蓝",
      "Rect": {
        "X": 426,
        "Y": 423,
        "Width": 135,
        "Height": 66
      },
      "LicensePlateCategory": "实体车牌"
    }
  ],
  "PlateCount": 1,
  "RequestId": "5141467c-0a67-4f7c-b1c5-8147d84681a1"
}
```

**响应字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Number | str | 识别出的车牌号码 |
| Confidence | int | 置信度，0-100 |
| Color | str | 车牌颜色：白/黑/蓝/绿/黄/黄绿/临牌/喷漆/其它 |
| LicensePlateCategory | str | 车牌类别：实体车牌/非实体车牌 |
| Rect | object | 车牌在原图中的像素坐标框（X, Y, Width, Height） |
| LicensePlateInfos | list | 全部车牌信息列表（多车牌场景） |
| LicensePlateInfos[].Number | str | 车牌号码 |
| LicensePlateInfos[].Confidence | int | 置信度 0-100 |
| LicensePlateInfos[].Color | str | 车牌颜色 |
| LicensePlateInfos[].Rect | object | 像素坐标框 |
| LicensePlateInfos[].LicensePlateCategory | str | 车牌类别 |
| PlateCount | int | 检测到的车牌数量 |
| RequestId | str | 唯一请求ID |

### 错误码说明

| 错误码 | 含义 |
|--------|------|
| FailedOperation.DownLoadError | 文件下载失败 |
| FailedOperation.ImageDecodeFailed | 图片解码失败 |
| FailedOperation.OcrFailed | OCR识别失败 |
| FailedOperation.UnKnowError | 未知错误 |
| FailedOperation.UnOpenError | 服务未开通 |
| InvalidParameterValue.InvalidParameterValueLimit | 参数值错误 |
| LimitExceeded.TooLargeFileError | 文件内容太大 |
| ResourceUnavailable.InArrears | 账号已欠费 |
| ResourceUnavailable.ResourcePackageRunOut | 账号资源包耗尽 |
| ResourcesSoldOut.ChargeStatusException | 计费状态异常 |

### 业务逻辑说明

1. ImageBase64和ImageUrl必须提供其一，都提供时只使用ImageUrl
2. 图片支持PNG、JPG、JPEG格式，不支持GIF
3. 图片经Base64编码后不超过10M，下载时间不超过3秒
4. 使用通用CommonOCR控制器，无特殊业务逻辑
5. 支持多车牌识别，通过LicensePlateInfos返回全部车牌

### 调用示例

```bash
# 通过URL识别车牌
python scripts/main.py --image-url "https://example.com/car.jpg"

# 通过文件路径(自动Base64编码)识别
python scripts/main.py --image-base64 ./car.jpg

# 通过Base64文本文件识别
python scripts/main.py --image-base64 ./base64.txt

# 指定地域
python scripts/main.py --image-url "https://example.com/car.jpg" --region ap-beijing```
