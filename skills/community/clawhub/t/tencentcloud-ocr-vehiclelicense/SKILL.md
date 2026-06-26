---
name: tencentcloud-ocr-vehiclelicense
description: 腾讯云行驶证识别(VehicleLicenseOCR)接口调用技能。当用户需要识别行驶证图片主页（车牌号码、车辆类型、所有人、住址、使用性质、品牌型号、识别代码、发动机号、注册日期、发证日期）或副页（号牌号码、档案编号、核定载人数、总质量、整备质量、核定载质量、外廓尺寸、准牵引总质量、备注、检验记录）信息时,应使用此技能。支持图片Base64和URL两种输入方式,支持复印件、翻拍、反光、模糊、边框不完整等告警功能,支持电子行驶证图片和拖拉机行驶证图片识别。
---

# 腾讯云行驶证识别 (VehicleLicenseOCR)

## 用途

调用腾讯云OCR行驶证识别接口，支持行驶证主页和副页所有字段的自动定位与识别，同时支持复印件、翻拍告警功能。

核心能力：
- **主页(FRONT)**：识别号牌号码、车辆类型、所有人、住址、使用性质、品牌型号、车辆识别代号、发动机号码、注册日期、发证日期、印章
- **副页(BACK)**：识别号牌号码、档案编号、核定人数、总质量、整备质量、核定载质量、外廓尺寸、准牵引总质量、备注、检验记录、副页编码、燃料种类
- **双面(DOUBLE)**：同时识别主页和副页
- **电子行驶证**：额外支持状态、检验有效期、生成时间（主页）及住址、发证机关、车身颜色（副页）
- **拖拉机行驶证**：支持拖拉机行驶证副页识别
- **告警功能**：复印件、翻拍件、反光、模糊、边框不完整等5种告警检测

官方文档：https://cloud.tencent.com/document/api/866/36209

## 使用时机

当用户提出以下需求时触发此技能：
- 需要从行驶证图片中提取车辆信息
- 需要识别行驶证主页或副页内容
- 需要获取车牌号码、车辆类型、所有人、VIN码等行驶证字段
- 需要检测行驶证是否为复印件、翻拍件
- 需要识别电子行驶证信息
- 需要识别拖拉机行驶证信息
- 涉及行驶证OCR识别的任何场景

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成行驶证识别。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ImageBase64 | str | 否(二选一) | 图片Base64值，编码后不超过7M，分辨率建议500*800以上，支持PNG/JPG/JPEG/BMP，建议卡片占图片2/3以上 |
| ImageUrl | str | 否(二选一) | 图片URL地址，下载时间不超过3秒，都提供时只使用ImageUrl |
| CardSide | str | 否 | `FRONT`(主页正面，有红色印章) / `BACK`(副页正面，有号码号牌) / `DOUBLE`(主副双面)，默认FRONT |
| TractorCardSide | str | 否 | `FRONT`(拖拉机行驶证主页) / `BACK`(拖拉机行驶证副页) |
| **UserAgent** | **str** | **否** | **请求来源标识(可选)，用于追踪调用来源，统一固定为`Skills`** |

### 输出格式

识别成功后返回 JSON 格式结果：

**主页(FRONT)**：
```json
{
  "FrontInfo": {
    "PlateNo": "京A12345",
    "VehicleType": "小型轿车",
    "Owner": "张三",
    "Address": "XX省XX市XX区XX路XX号",
    "UseCharacter": "非营运",
    "Model": "大众牌SVW71412SE",
    "Vin": "LSVAM4187C2XXXXXX",
    "EngineNo": "CDF0XXXXX",
    "RegisterDate": "2020-01-01",
    "IssueDate": "2020-01-01",
    "Seal": "XX市公安局交通管理局"
  },
  "VehicleLicenseType": "Normal",
  "RecognizeWarnCode": [],
  "RecognizeWarnMsg": [],
  "RequestId": "xxx"
}
```

**副页(BACK)**：
```json
{
  "BackInfo": {
    "PlateNo": "京A12345",
    "FileNo": "110100XXXXXXXX",
    "AllowNum": "5人",
    "TotalMass": "1750kg",
    "CurbWeight": "1390kg",
    "LoadQuality": "-",
    "ExternalSize": "4620×1800×1480mm",
    "TotalQuasiMass": "-",
    "Marks": "",
    "Record": "检验有效期至2026年01月",
    "SubPageCode": "110100XXXXXXXX",
    "FuelType": "汽油"
  },
  "VehicleLicenseType": "Normal",
  "RecognizeWarnCode": [],
  "RecognizeWarnMsg": [],
  "RequestId": "xxx"
}
```

### 告警码说明

| 告警码 | 含义 | 消息标识 |
|--------|------|----------|
| -9102 | 复印件告警 | WARN_DRIVER_LICENSE_COPY_CARD |
| -9103 | 翻拍件告警 | WARN_DRIVER_LICENSE_SCREENED_CARD |
| -9104 | 反光告警 | WARN_DRIVER_LICENSE_REFLECTION |
| -9105 | 模糊告警 | WARN_DRIVER_LICENSE_BLUR |
| -9106 | 边框不完整告警 | WARN_DRIVER_LICENSE_BORDER_INCOMPLETE |

> 注：告警码可以同时存在多个。

### 错误码说明

| 错误码 | 描述 |
|--------|------|
| FailedOperation.DownLoadError | 文件下载失败 |
| FailedOperation.EmptyImageError | 图片内容为空 |
| FailedOperation.ImageBlur | 图片模糊 |
| FailedOperation.ImageDecodeFailed | 图片解码失败 |
| FailedOperation.ImageNoText | 图片中未检测到文本 |
| FailedOperation.ImageSizeTooLarge | 图片尺寸过大 |
| FailedOperation.LicenseCardSideError | CardSide与实际卡证正副页类型不符 |
| FailedOperation.LicenseMultiCardError | 图片中存在两张及以上同面卡证 |
| FailedOperation.NoVehicleLicenseError | 上传的图片非行驶证 |
| FailedOperation.OcrFailed | OCR识别失败 |
| FailedOperation.UnKnowError | 未知错误 |
| FailedOperation.UnOpenError | 服务未开通 |
| InvalidParameter.EngineImageDecodeFailed | 图片解码失败 |
| InvalidParameterValue.InvalidParameterValueLimit | 参数值错误 |
| LimitExceeded.TooLargeFileError | 文件内容太大 |
| ResourceUnavailable.InArrears | 账号已欠费 |
| ResourceUnavailable.ResourcePackageRunOut | 账号资源包耗尽 |
| ResourcesSoldOut.ChargeStatusException | 计费状态异常 |

### 调用示例

```bash
# 通过URL识别行驶证主页
python scripts/main.py --image-url "https://example.com/vehicle_license.jpg" --card-side FRONT

# 通过URL识别行驶证副页
python scripts/main.py --image-url "https://example.com/vehicle_license_back.jpg" --card-side BACK

# 识别行驶证主页+副页（双面）
python scripts/main.py --image-url "https://example.com/vehicle_license.jpg" --card-side DOUBLE

# 通过Base64识别行驶证（默认主页）
python scripts/main.py --image-base64 "/path/to/vehicle_license.jpg"

# 识别拖拉机行驶证副页
python scripts/main.py --image-url "https://example.com/tractor_license.jpg" --tractor-card-side BACK

# 指定地域
python scripts/main.py --image-url "https://example.com/vehicle_license.jpg" --region ap-beijing```
