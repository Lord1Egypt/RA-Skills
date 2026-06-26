# ImageModeration API 参考文档

> 原始文档：[图片内容安全 - 图片内容检测](https://cloud.tencent.com/document/product/1125/53273)
>
> SDK 调用指引：[图片内容安全 - SDK 调用指引](https://cloud.tencent.com/document/product/1124/100983)

## 接口概述

- **接口名称**：ImageModeration
- **服务端点**：`ims.tencentcloudapi.com`
- **API 版本**：`2020-12-29`
- **SDK 模块**：`tencentcloud.ims.v20201229`
- **功能说明**：图片内容检测接口，支持对图片进行多维度安全检测，包括 AI 生成图片识别（`Type=IMAGE_AIGC`）。

---

## 核心输入参数

| 参数名称 | 必选 | 类型 | 描述 |
|---------|------|------|------|
| BizType | 否 | String | 自定义审核策略的编号。不填默认使用默认策略。在腾讯云内容安全控制台中可创建自定义策略。 |
| DataId | 否 | String | 业务数据标识，可用于将检测结果与业务数据进行关联，长度限制 128 字符。 |
| FileContent | 否 | String | 图片文件内容的 **Base64 编码**（与 FileUrl 二选一，同时存在时使用 FileContent）。 |
| FileUrl | 否 | String | 图片文件的访问 **URL**（与 FileContent 二选一）。 |
| Interval | 否 | Integer | GIF 图片截帧间隔（单位：帧数），默认为 0 表示只取第一帧。 |
| MaxFrames | 否 | Integer | GIF 图片最大截帧数量，默认为 1。 |
| Type | 否 | String | 检测类型。设置为 `IMAGE_AIGC` 时进行 AI 生成图片识别判定。不传或留空时为常规内容安全检测。 |

### 图片输入说明

- `FileContent` 和 `FileUrl` **二选一**，同时存在时优先使用 `FileContent`
- 支持格式：**PNG、JPG、JPEG、BMP、GIF、WEBP**
- 图片大小限制：**不超过 5MB**
- 图片分辨率建议：**不低于 256x256**

---

## 核心输出参数

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| Suggestion | String | 处置建议：`Block`（建议打击）、`Review`（建议人工复审）、`Pass`（建议通过） |
| Label | String | 恶意标签，当 `Suggestion=Pass` 时为 `Normal`。可能值包括：`Normal`（正常）、`Porn`（色情）、`Abuse`（谩骂）、`Ad`（广告）、`Custom`（自定义违规）、`GeneratedContentRisk`（AI 生成内容风险）等 |
| SubLabel | String | 二级标签分类 |
| Score | Integer | 风险置信度评分，范围 0-100。分数越高表示风险越大：<br>• 0-60：低风险<br>• 60-80：中风险<br>• 80-100：高风险 |
| LabelResults | Array of [LabelResult](#labelresult-对象) | 分类模型检测结果，包含各检测维度的具体信息 |
| ObjectResults | Array of [ObjectResult](#objectresult-对象) | 物体检测结果 |
| OcrResults | Array of [OcrResult](#ocrresult-对象) | OCR 检测结果 |
| Extra | String | 附加信息，JSON 字符串格式 |
| DataId | String | 请求时传入的 DataId |
| BizType | String | 使用的审核策略编号 |
| RequestId | String | 唯一请求 ID |

### LabelResult 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| Scene | String | 检测场景，如 `Porn`、`Terrorism` 等 |
| Label | String | 恶意标签 |
| Suggestion | String | 处置建议 |
| Score | Integer | 置信度评分 0-100 |
| SubLabel | String | 二级标签 |
| Details | Array of [LabelDetailItem](#labeldetailitem-对象) | 详细标签信息 |

### LabelDetailItem 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| Id | Integer | 序号 |
| Name | String | 标签名称 |
| Score | Integer | 置信度评分 |

### ObjectResult 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| Scene | String | 检测场景 |
| Label | String | 恶意标签 |
| Suggestion | String | 处置建议 |
| Score | Integer | 置信度评分 0-100 |
| SubLabel | String | 二级标签 |
| Names | Array of String | 物体名称列表 |
| Location | [Location](#location-对象) | 物体位置 |

### OcrResult 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| Scene | String | 检测场景 |
| Label | String | 恶意标签 |
| Suggestion | String | 处置建议 |
| Score | Integer | 置信度评分 0-100 |
| SubLabel | String | 二级标签 |
| Text | String | OCR 识别的文本内容 |
| Details | Array of [OcrTextDetail](#ocrtextdetail-对象) | OCR 详细信息 |

### OcrTextDetail 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| Text | String | 识别到的文本 |
| Label | String | 恶意标签 |
| Keywords | Array of String | 命中的关键词列表 |
| Score | Integer | 置信度评分 |
| Location | [Location](#location-对象) | 文本位置 |

### Location 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| X | Float | 左上角 X 坐标 |
| Y | Float | 左上角 Y 坐标 |
| Width | Float | 宽度 |
| Height | Float | 高度 |
| Rotate | Float | 旋转角度 |

---

## AIGC 检测说明

当设置 `Type=IMAGE_AIGC` 时，接口会对输入图片进行 AI 生成内容的判定：

- **Score**：AIGC 风险分值，分数越高表示图片越可能是 AI 生成
- **Label**：当判定为 AI 生成时，Label 会反映相应标签（如 `GeneratedContentRisk`）
- **Suggestion**：
  - `Pass`：图片大概率为真实图片
  - `Review`：存疑，建议人工复审
  - `Block`：图片大概率为 AI 生成

---

## 请求频率限制

| 检测类型 | 默认 QPS 上限 |
|---------|-------------|
| IMAGE_AIGC（AI 生成图片识别） | 以控制台配额为准 |
| 常规图片内容安全检测 | 以控制台配额为准 |

> 超过频率限制会返回 `RequestLimitExceeded` 错误。如需提升配额，请联系腾讯云商务或提工单申请。

---

## 常见错误码

| 错误码 | 描述 | 处理建议 |
|-------|------|---------|
| AuthFailure | 鉴权失败 | 检查 SecretId 和 SecretKey 是否正确 |
| AuthFailure.SignatureExpire | 签名过期 | 检查系统时间是否准确 |
| InternalError | 内部错误 | 稍后重试 |
| InvalidParameter | 参数错误 | 检查请求参数是否符合规范 |
| InvalidParameterValue | 参数取值错误 | 检查图片 URL 或 Base64 编码是否正确 |
| InvalidParameterValue.ImageSizeExceed | 图片大小超限 | 压缩图片至 5MB 以内 |
| MissingParameter | 缺少参数 | 检查必填参数是否传入 |
| RequestLimitExceeded | 请求频率超限 | 降低请求频率或申请提升配额 |
| ResourceNotFound | 资源不存在 | 检查 BizType 是否正确 |
| UnauthorizedOperation | 未授权操作 | 确认账号已开通图片内容安全服务 |
| UnsupportedOperation | 不支持的操作 | 检查 API 版本和接口名称 |

---

## 调用示例（Python SDK）

```python
import base64
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ims.v20201229 import ims_client, models

# Create credentials
cred = credential.Credential("your-secret-id", "your-secret-key")

# Configure HTTP and Client profiles
httpProfile = HttpProfile()
httpProfile.endpoint = "ims.tencentcloudapi.com"
clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile

# Create client
client = ims_client.ImsClient(cred, "ap-guangzhou", clientProfile)

# Build request - using URL
req = models.ImageModerationRequest()
req.FileUrl = "https://example.com/image.jpg"
req.Type = "IMAGE_AIGC"

# Send request
resp = client.ImageModeration(req)
print(json.loads(resp.to_json_string()))

# Alternative: using local file with Base64
with open("image.png", "rb") as f:
    content = base64.b64encode(f.read()).decode("utf-8")
req2 = models.ImageModerationRequest()
req2.FileContent = content
req2.Type = "IMAGE_AIGC"
resp2 = client.ImageModeration(req2)
print(json.loads(resp2.to_json_string()))
```
