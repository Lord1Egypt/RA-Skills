---
name: tencentcloud-ocr-vatinvoice
description: 腾讯云通用票据识别高级版(VatInvoiceOCR)接口调用技能。当用户需要识别发票图片中增值税专用发票、增值税普通发票、增值税电子专票、增值税电子普票、电子发票（普通/增值税专用）的全字段信息时,应使用此技能。支持识别发票图片中的发票代码、发票号码、开票日期、合计金额、校验码、税率、合计税额、价税合计、购买方/销售方信息、明细条目等全部字段,同时支持PDF格式发票图片识别。
---

# 腾讯云通用票据识别高级版 (VatInvoiceOCR)

## 用途

调用腾讯云OCR通用票据识别高级版接口，支持增值税专用发票、增值税普通发票、增值税电子专票、增值税电子普票、电子发票（普通发票）、电子发票（增值税专用发票）全字段的内容检测和识别。

核心能力：
- **发票头信息识别**：发票代码、发票号码、打印发票代码、打印发票号码、开票日期、机器编号、校验码、密码区等
- **买卖方信息识别**：购买方/销售方名称、识别号（税号）、地址/电话、开户行及账号
- **金额信息识别**：合计金额、合计税额、价税合计(大写)、小写金额、税率
- **明细条目识别**：货物/服务名称、规格型号、单位、数量、单价、不含税金额、税率、税额、税收分类编码等
- **人员信息识别**：开票人、收款人、复核
- **其他信息识别**：备注、联次名称、发票名称、发票类型、车牌号、通行费标志等
- **PDF发票支持**：支持PDF格式发票识别（需开启IsPdf参数）
- **全电发票支持**：自动分类识别全电发票，并统一输出格式

官方文档：https://cloud.tencent.com/document/api/866/36210

## 使用时机

当用户提出以下需求时触发此技能：
- 需要从发票图片中提取全部字段信息
- 需要从PDF格式发票中识别内容
- 需要提取发票中的明细条目（货物/服务列表）
- 需要识别增值税专用/普通发票、电子发票
- 涉及发票OCR识别的任何场景
- 需要批量处理发票并结构化提取信息

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成通用票据识别。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ImageBase64 | str | 否(二选一) | 图片/PDF的Base64值，编码后不超过10M，像素需介于20-10000px，支持PNG/JPG/JPEG/PDF |
| ImageUrl | str | 否(二选一) | 图片/PDF的URL地址，都提供时只使用ImageUrl |
| IsPdf | bool | 否 | 是否开启PDF识别，默认false，开启后可同时支持图片和PDF的识别 |
| PdfPageNumber | int | 否 | PDF页码，仅当IsPdf=true时有效，默认1，必须>=1 |
| **UserAgent** | **str** | **否** | **请求来源标识(可选)，用于追踪调用来源，统一固定为`Skills`** |

### 输出格式

识别成功后返回 JSON 格式结果：

**格式化输出模式（默认）**：
```json
{
  "发票基本信息": {
    "发票代码": "012002100311",
    "发票号码": "48026588",
    "开票日期": "2021年09月15日",
    "发票名称": "增值税电子普通发票",
    "发票类型": "10",
    "校验码": "12345678901234567890",
    "机器编号": "661234567890"
  },
  "购买方信息": {
    "购买方名称": "XX科技有限公司",
    "购买方识别号": "91440300MA5XXXXXX"
  },
  "销售方信息": {
    "销售方名称": "YY有限公司",
    "销售方识别号": "91110108MA0XXXXXX"
  },
  "金额信息": {
    "合计金额": "¥1000.00",
    "合计税额": "¥60.00",
    "价税合计(大写)": "壹仟零陆拾圆整",
    "小写金额": "¥1060.00"
  },
  "人员信息": {
    "开票人": "张三",
    "收款人": "李四",
    "复核": "王五"
  },
  "明细条目": [
    {
      "行号": "1",
      "名称": "*信息技术服务*软件开发服务",
      "规格型号": "",
      "单位": "次",
      "数量": "1",
      "单价": "1000.00",
      "不含税金额": "1000.00",
      "税率": "6%",
      "税额": "60.00"
    }
  ],
  "其他信息": {
    "备注": "",
    "旋转角度": 0.0
  },
  "RequestId": "xxx"
}
```

**原始输出模式（--raw）**：
```json
{
  "VatInvoiceInfos": [
    {
      "Name": "发票代码",
      "Value": "012002100311",
      "Polygon": {"LeftTop": {"X": 50, "Y": 100}, ...}
    },
    {
      "Name": "发票号码",
      "Value": "48026588",
      "Polygon": {...}
    }
  ],
  "Items": [
    {
      "LineNo": "1",
      "Name": "*信息技术服务*软件开发服务",
      "Spec": "",
      "Unit": "次",
      "Quantity": "1",
      "UnitPrice": "1000.00",
      "AmountWithoutTax": "1000.00",
      "TaxRate": "6%",
      "TaxAmount": "60.00",
      "TaxClassifyCode": "3040201"
    }
  ],
  "PdfPageSize": 0,
  "Angle": 0.0,
  "RequestId": "xxx"
}
```

### 响应数据结构说明

**TextVatInvoice 结构（KV形式）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| Name | str | 字段名称，支持识别的完整字段列表见下方 |
| Value | str | 字段对应的值 |
| Polygon | Polygon | 字段在原图中的四点坐标（可能为null） |

**Name 字段可识别的完整列表**：发票代码、发票号码、打印发票代码、打印发票号码、开票日期、购买方识别号、小写金额、价税合计(大写)、销售方识别号、校验码、购买方名称、销售方名称、税额、复核、联次名称、备注、联次、密码区、开票人、收款人、货物或应税劳务/服务名称、省、市、服务类型、通行费标志、是否代开、是否收购、合计金额、是否有公司印章、发票消费类型、车船税、机器编号、成品油标志、税率、合计税额、购买方地址/电话、销售方地址/电话、单价、金额、销售方开户行及账号、购买方开户行及账号、规格型号、发票名称、单位、数量、校验码备选、校验码后六位备选、发票号码备选、车牌号、类型、通行日期起、通行日期止、发票类型

**VatInvoiceItem 结构（明细条目）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| LineNo | str | 行号 |
| Name | str | 项目名称 |
| Spec | str | 规格型号 |
| Unit | str | 单位 |
| Quantity | str | 数量 |
| UnitPrice | str | 单价 |
| AmountWithoutTax | str | 不含税金额 |
| TaxRate | str | 税率 |
| TaxAmount | str | 税额 |
| TaxClassifyCode | str | 税收分类编码 |
| VehicleType | str | 运输工具类型 |
| VehicleBrand | str | 运输工具牌号 |
| DeparturePlace | str | 起始地 |
| ArrivalPlace | str | 到达地 |
| TransportItemsName | str | 运输货物名称 |
| ConstructionPlace | str | 建筑服务发生地 |
| ConstructionName | str | 建筑项目名称 |

### 错误码说明

| 错误码 | 含义 |
|--------|------|
| FailedOperation.DownLoadError | 文件下载失败 |
| FailedOperation.EmptyImageError | 图片内容为空 |
| FailedOperation.ImageBlur | 图片模糊 |
| FailedOperation.ImageDecodeFailed | 图片解码失败 |
| FailedOperation.ImageNoText | 图片中未检测到文本 |
| FailedOperation.ImageSizeTooLarge | 图片尺寸过大，请确保编码后不超过10M，像素介于20-10000px |
| FailedOperation.OcrFailed | OCR识别失败 |
| FailedOperation.UnKnowError | 未知错误 |
| FailedOperation.UnOpenError | 服务未开通，请先在腾讯云控制台开通增值税发票识别服务 |
| InvalidParameter.EngineImageDecodeFailed | 引擎图片解码失败 |
| InvalidParameterValue.InvalidParameterValueLimit | 参数值错误 |
| LimitExceeded.TooLargeFileError | 文件内容太大 |
| ResourceUnavailable.InArrears | 账号已欠费 |
| ResourceUnavailable.ResourcePackageRunOut | 账号资源包耗尽 |
| ResourcesSoldOut.ChargeStatusException | 计费状态异常 |

### 重要业务逻辑

1. **ImageBase64和ImageUrl必须提供其一**，都提供时只使用ImageUrl
2. 图片/PDF编码后不超过10M，像素需介于20-10000px
3. 支持格式：PNG、JPG、JPEG、PDF（不支持GIF）
4. **IsPdf默认为false**，识别PDF格式发票需显式设置为true
5. **PdfPageNumber仅当IsPdf=true时有效**，默认值为1，必须>=1
6. **默认接口请求频率限制：10次/秒**
7. **复杂的内部分流逻辑**：接口会先调用InvoiceMixedClassify对票据分类
   - 分类Type==16（全电发票）→ 走全电发票识别引擎
   - 其他类型 → 走传统增值税发票识别引擎
8. 全电发票会进行字段映射转换，将ElectricInvoiceItem统一转换为TextVatInvoice+VatInvoiceItem格式输出
9. 建议图片存储于腾讯云COS以获得更高的下载速度和稳定性

### 调用示例

```bash
# 通过URL识别发票
python scripts/main.py --image-url "https://example.com/invoice.jpg"

# 通过文件路径(自动Base64编码)识别
python scripts/main.py --image-base64 ./invoice.jpg

# 识别PDF格式发票
python scripts/main.py --image-base64 ./invoice.pdf --is-pdf

# 识别PDF发票的指定页码
python scripts/main.py --image-base64 ./invoice.pdf --is-pdf --pdf-page-number 2

# 输出原始JSON响应
python scripts/main.py --image-url "https://example.com/invoice.jpg" --raw

# 指定地域
python scripts/main.py --image-url "https://example.com/invoice.jpg" --region ap-beijing```
