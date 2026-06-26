---
name: tencentcloud-ocr-bizlicense
description: 腾讯云营业执照识别(BizLicenseOCR)接口调用技能。当用户需要识别营业执照图片上的字段信息（统一社会信用代码、公司名称、主体类型、法定代表人、注册资本、组成形式、成立日期、营业期限、经营范围等）时，应使用此技能。支持图片Base64和URL两种输入方式，支持复印件/翻拍件告警检测、有效期自动拼接、电子营业执照图片识别及非营业执照的营业类证件图片识别。
---

# 腾讯云营业执照识别 (BizLicenseOCR)

## 用途

调用腾讯云OCR营业执照识别接口，支持快速精准识别营业执照上的字段，包括统一社会信用代码、公司名称、主体类型、法定代表人、注册资本、组成形式、成立日期、营业期限和经营范围等字段。

核心能力：
- **基础识别**：识别统一社会信用代码（注册号）、公司名称、注册资本、法定代表人、地址、经营范围、主体类型、营业期限、组成形式、成立日期
- **扩展识别**：登记日期、登记机关、标题、编号、重要提示
- **辅助信息**：是否为副本、图片旋转角度、是否有国徽/二维码/印章、是否电子营业执照
- **告警检测**：黑白复印件告警(-9102)、翻拍件告警(-9104)
- **营业类证件**：开启后支持非营业执照的其他营业类证件识别

官方文档：https://cloud.tencent.com/document/api/866/36215

## 使用时机

当用户提出以下需求时触发此技能：
- 需要从营业执照图片中提取文字信息
- 需要获取公司的统一社会信用代码、名称、法定代表人等信息
- 需要检测营业执照是否为复印件或翻拍件
- 需要识别电子营业执照
- 需要识别非营业执照的其他营业类证件（如企业许可证等）
- 涉及营业执照OCR识别的任何场景

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成营业执照识别。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ImageBase64 | str | 否(二选一) | 图片Base64值，编码后不超过7M，支持PNG/JPG/JPEG，不支持GIF |
| ImageUrl | str | 否(二选一) | 图片URL地址，下载时间不超过3秒。都提供时仅使用ImageUrl |
| EnableCopyWarn | bool | 否 | 是否返回告警码（复印件/翻拍件告警），默认false |
| EnablePeriodComplete | bool | 否 | 是否返回自动拼接的有效期，默认true |
| EnableBusinessCertificate | bool | 否 | 是否支持营业类证件识别（含非营业执照证件），默认false |
| **UserAgent** | **str** | **否** | **请求来源标识(可选)，用于追踪调用来源，统一固定为`Skills`** |

### 输出格式

识别成功后返回 JSON 格式结果：

**标准营业执照识别结果**：
```json
{
  "RegNum": "91110000MA0XXXXXXX",
  "Name": "XX科技有限公司",
  "Capital": "1000万元人民币",
  "Person": "张三",
  "Address": "北京市海淀区XX路XX号",
  "Business": "技术开发、技术咨询、技术服务...",
  "Type": "有限责任公司(自然人投资或控股)",
  "Period": "2020年01月01日至2040年01月01日",
  "ComposingForm": "",
  "SetDate": "2020年01月01日",
  "IsDuplication": 1,
  "RegistrationDate": "2020年01月01日",
  "Angle": 0.0,
  "NationalEmblem": true,
  "QRCode": true,
  "Seal": true,
  "Title": "营业执照",
  "SerialNumber": "000000000",
  "RegistrationAuthority": "北京市海淀区市场监督管理局",
  "Electronic": false,
  "RequestId": "xxx"
}
```

**含告警信息的结果**（需开启 EnableCopyWarn）：
```json
{
  "RegNum": "91110000MA0XXXXXXX",
  "Name": "XX科技有限公司",
  "Warnings": [
    {
      "code": -9102,
      "message_id": "WARN_COPY_CARD",
      "description": "黑白复印件告警"
    }
  ],
  "RequestId": "xxx"
}
```

### 告警码说明

| 告警码 | 消息标识 | 含义 |
|--------|----------|------|
| -9102 | WARN_COPY_CARD | 黑白复印件告警 |
| -9104 | WARN_RESHOOT_CARD | 翻拍件告警 |

### 错误码说明

| 错误码 | 描述 |
|--------|------|
| FailedOperation.DownLoadError | 文件下载失败 |
| FailedOperation.ImageDecodeFailed | 图片解码失败 |
| FailedOperation.NoBizLicense | 非营业执照 |
| FailedOperation.OcrFailed | OCR识别失败 |
| FailedOperation.UnKnowError | 未知错误 |
| FailedOperation.UnOpenError | 服务未开通 |
| InvalidParameterValue.InvalidParameterValueLimit | 参数值错误 |
| LimitExceeded.TooLargeFileError | 文件内容太大 |
| ResourceUnavailable.InArrears | 账号已欠费 |
| ResourceUnavailable.ResourcePackageRunOut | 账号资源包耗尽 |
| ResourcesSoldOut.ChargeStatusException | 计费状态异常 |

### 重要业务逻辑

1. **ImageUrl 优先**：ImageBase64 和 ImageUrl 都提供时，仅使用 ImageUrl
2. **有效期拼接**：EnablePeriodComplete 未传入时默认设为 true，自动拼接营业期限
3. **EnableBusinessCertificate 分流逻辑**：
   - false → 直接走营业执照识别引擎
   - true → 先调用卡证分类模型：
     - 分类为 "BizLicense" → 走原营业执照引擎
     - 分类为 "EnterpriseLicense" → 走文档抽取基础版引擎(BizLicenseNew)
     - 其他类型 → 返回 FailedOperation.NoBizLicense 错误
4. **电子营业执照**：支持识别电子营业执照，通过 Electronic 字段标识
5. **图片限制**：Base64 编码后不超过 7M，支持 PNG/JPG/JPEG，不支持 GIF
6. **默认请求频率限制**：10次/秒

### 调用示例

```bash
# 通过URL识别营业执照
python scripts/main.py --image-url "https://example.com/biz_license.jpg"

# 通过文件路径(自动Base64编码)识别
python scripts/main.py --image-base64 ./biz_license.jpg

# 开启复印件/翻拍件告警检测
python scripts/main.py --image-url "https://example.com/biz_license.jpg" --enable-copy-warn

# 开启营业类证件识别（含非营业执照证件）
python scripts/main.py --image-url "https://example.com/biz_license.jpg" --enable-business-certificate

# 关闭有效期自动拼接
python scripts/main.py --image-url "https://example.com/biz_license.jpg" --enable-period-complete false

# 指定地域
python scripts/main.py --image-url "https://example.com/biz_license.jpg" --region ap-beijing```
