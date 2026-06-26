---
name: tencentcloud-ocr-mlidpassport
description: 腾讯云护照识别（多国多地区）(MLIDPassportOCR)接口调用技能。当用户需要识别护照图片中中国大陆、港澳台地区或其他国家/地区的护照信息（护照ID、姓名、出生日期、性别、有效期、发行国、国籍、国家地区代码、MRZ码等）时,应使用此技能。支持图片Base64和URL两种输入方式,支持护照图片人像照片裁剪功能,支持80+国家/地区的可机读护照图片识别,同时支持复印件、翻拍、PS、反光、模糊、边框不完整等告警功能（仅国际站生效）。
---

# 腾讯云护照识别（多国多地区）(MLIDPassportOCR)

## 用途

调用腾讯云OCR护照识别接口，支持中国大陆地区及中国港澳台地区、其他国家以及地区的护照识别，覆盖80+国家/地区的可机读护照。

核心能力：
- **机读码区(MRZ)解析**：识别护照ID、姓名（姓/名）、出生日期、性别、有效期、发行国、国籍、国家地区代码、类型、MRZ Code序列
- **信息区(VRZ)解析**：识别证件类型、发行国家、护照号码、姓、名、姓名、国籍、出生日期、性别、发行日期、截止日期、持证人签名（仅中国大陆护照）、签发地点（仅中国大陆护照）、签发机关（仅中国大陆护照）
- **人像裁剪**：支持返回护照人像照片Base64（需设置RetImage=true）
- **告警功能**（仅国际站生效）：边框不完整、复印件、翻拍、PS、反光、模糊等6种告警检测

官方文档：https://cloud.tencent.com/document/api/866/37657

## 使用时机

当用户提出以下需求时触发此技能：
- 需要从护照图片中提取证件信息
- 需要识别护照上的姓名、护照号、国籍、出生日期等字段
- 需要解析护照的MRZ机读码信息
- 需要裁剪护照上的人像照片
- 需要检测护照是否为复印件、翻拍件、PS件（国际站）
- 涉及护照OCR识别的任何场景
- 涉及多国多地区护照识别的场景

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成护照识别。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ImageBase64 | str | 否(二选一) | 图片Base64值，编码后不超过10M，分辨率建议500*800以上，支持PNG/JPG/JPEG/BMP/PDF，建议卡片部分占图片2/3以上 |
| ImageUrl | str | 否(二选一) | 图片URL地址，下载时间不超过3秒，都提供时只使用ImageUrl |
| RetImage | bool | 否 | 是否返回人像照片Base64，默认false |
| **UserAgent** | **str** | **否** | **请求来源标识(可选)，用于追踪调用来源，统一固定为`Skills`** |

### 输出格式

识别成功后返回 JSON 格式结果：

```json
{
  "ID": "456712345",
  "Name": "CARTER ESTHER",
  "Surname": "CARTER",
  "GivenName": "ESTHER",
  "DateOfBirth": "19900411",
  "Sex": "F",
  "DateOfExpiration": "20210726",
  "IssuingCountry": "USA",
  "Nationality": "USA",
  "Type": "P",
  "CodeSet": "P<USACARTER<<ESTHER<<<<<<<<<<<<<<<<<<<<<<<<<",
  "CodeCrc": "4567123452USA9004117F2107268713843748<708026",
  "PassportRecognizeInfos": {
    "Type": "P",
    "IssuingCountry": "USA",
    "PassportID": "456712345",
    "Surname": "CARTER",
    "GivenName": "ESTHER",
    "Name": "",
    "Nationality": "UNITED STATES OF AMERICA",
    "DateOfBirth": "11 Apr 1990",
    "Sex": "F",
    "DateOfIssuance": "27 Jul 2011",
    "DateOfExpiration": "26 Jul 2021",
    "Signature": "",
    "IssuePlace": "",
    "IssuingAuthority": ""
  },
  "WarnCardInfos": [],
  "RequestId": "dad946b2-1288-4df9-a0b4-6abfaba1e170"
}
```

### 告警码说明（WarnCardInfos，仅国际站生效）

| 告警码 | 含义 |
|--------|------|
| -9101 | 证件边框不完整告警 |
| -9102 | 证件复印件告警 |
| -9103 | 证件翻拍告警 |
| -9104 | 证件PS告警 |
| -9107 | 证件反光告警 |
| -9108 | 证件模糊告警 |
| -9109 | 告警能力未开通 |

> 注：WarnCardInfos 仅在国际站请求时生效，国内站固定返回空数组。Warn 和 AdvancedInfo 字段已废弃，不建议使用。

### 错误码说明

| 错误码 | 描述 |
|--------|------|
| FailedOperation.DownLoadError | 文件下载失败 |
| FailedOperation.FieldException | 字段值不符合预期 |
| FailedOperation.ImageDecodeFailed | 图片解码失败 |
| FailedOperation.InconsistencyBetweenMRZAndVRZ | 视读区信息与机读区信息不一致 |
| FailedOperation.NoPassport | 非护照 |
| FailedOperation.OcrFailed | OCR识别失败 |
| FailedOperation.UnKnowError | 未知错误 |
| FailedOperation.UnOpenError | 服务未开通 |
| FailedOperation.WarningServiceFailed | 通用告警服务异常 |
| InvalidParameterValue.InvalidParameterValueLimit | 参数值错误 |
| LimitExceeded.TooLargeFileError | 文件内容太大 |
| ResourceUnavailable.InArrears | 账号已欠费 |
| ResourceUnavailable.ResourcePackageRunOut | 账号资源包耗尽 |
| ResourcesSoldOut.ChargeStatusException | 计费状态异常 |

### 业务逻辑说明

1. ImageBase64 和 ImageUrl 必须提供其一，都提供时只使用 ImageUrl
2. 支持自动将 PDF 第1页转为图片进行识别
3. 区分国内版和国际版（通过地域配置），解析逻辑不同
4. 泰国护照(IssuingCountry=="THA")会自动校验OCR区和MRZ区字段一致性（姓名、护照号、性别、日期等）
5. Warn 和 AdvancedInfo 字段已废弃，固定返回空数组和"1"，不建议使用
6. WarnCardInfos 仅国际站请求生效，国内站固定返回空数组
7. CardCount 字段仅在请求曼谷地域(ap-bangkok)时返回
8. PassportRecognizeInfos 中的 Signature、IssuePlace、IssuingAuthority 仅在中国大陆护照时返回有效值
9. 默认接口请求频率限制：5次/秒

### 调用示例

```bash
# 通过URL识别护照
python scripts/main.py --image-url "https://example.com/passport.jpg"

# 通过URL识别护照并返回人像照片
python scripts/main.py --image-url "https://example.com/passport.jpg" --ret-image

# 通过Base64识别护照
python scripts/main.py --image-base64 "/path/to/passport.jpg"

# 指定地域（如使用国际站获取告警信息）
python scripts/main.py --image-url "https://example.com/passport.jpg" --region ap-bangkok

# 输出原始API响应（不格式化）
python scripts/main.py --image-url "https://example.com/passport.jpg" --raw```
