# TextModeration API 参考文档

> 原始文档：[文本内容安全 - 文本内容检测](https://cloud.tencent.com/document/product/1124/51860)
>
> SDK 调用指引：[文本内容安全 - SDK 调用指引](https://cloud.tencent.com/document/product/1124/100983)

## 接口概述

- **接口名称**：TextModeration
- **服务端点**：`tms.tencentcloudapi.com`
- **API 版本**：`2020-12-29`
- **SDK 模块**：`tencentcloud.tms.v20201229`
- **功能说明**：文本内容检测接口，支持对文本进行多维度安全检测，包括 AI 生成文本识别（`Type=TEXT_AIGC`）。

---

## 核心输入参数

| 参数名称 | 必选 | 类型 | 描述 |
|---------|------|------|------|
| Content | 是 | String | 待检测文本内容，需进行 **UTF-8 编码后 Base64 编码**，文本长度限制为 **10000 个 Unicode 字符**。 |
| Type | 否 | String | 检测类型。设置为 `TEXT_AIGC` 时进行 AI 生成文本识别判定。不传或留空时为常规内容安全检测。 |
| BizType | 否 | String | 自定义审核策略的编号。不填默认使用默认策略。在腾讯云内容安全控制台中可创建自定义策略。 |
| DataId | 否 | String | 业务数据标识，可用于将检测结果与业务数据进行关联，长度限制 128 字符。 |
| User | 否 | [User](#user-对象) | 用户相关信息（可选）。 |
| Device | 否 | [Device](#device-对象) | 设备相关信息（可选）。 |

### Content 编码说明

```
原始文本 → UTF-8 编码 → Base64 编码 → 作为 Content 参数值
```

Python 示例：
```python
import base64
content = base64.b64encode("待检测文本".encode("utf-8")).decode("utf-8")
```

---

## 核心输出参数

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| Suggestion | String | 处置建议：`Block`（建议打击）、`Review`（建议人工复审）、`Pass`（建议通过） |
| Label | String | 恶意标签，当 `Suggestion=Pass` 时为 `Normal`。可能值包括：`Normal`（正常）、`Porn`（色情）、`Abuse`（谩骂）、`Ad`（广告）、`Custom`（自定义违规）等 |
| SubLabel | String | 二级标签分类 |
| Score | Integer | 风险置信度评分，范围 0-100。分数越高表示风险越大：<br>• 0-60：低风险<br>• 60-80：中风险<br>• 80-100：高风险 |
| Keywords | Array of String | 命中的关键词列表（如有） |
| DetailResults | Array of [DetailResults](#detailresults-对象) | 详细检测结果列表，包含各检测维度的具体信息 |
| RiskDetails | Array of [RiskDetails](#riskdetails-对象) | 风险详情列表 |
| Extra | String | 附加信息，JSON 字符串格式 |
| DataId | String | 请求时传入的 DataId |
| BizType | String | 使用的审核策略编号 |
| ContextText | String | 上下文命中信息 |
| RequestId | String | 唯一请求 ID |

### DetailResults 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| Label | String | 恶意标签 |
| Suggestion | String | 处置建议 |
| Score | Integer | 置信度评分 0-100 |
| Keywords | Array of String | 命中的关键词列表 |
| LibType | Integer | 库类型：1=黑白名单库，2=自定义关键词库 |
| LibId | String | 库 ID |
| LibName | String | 库名称 |
| SubLabel | String | 二级标签 |

### RiskDetails 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| Label | String | 风险标签 |
| Level | Integer | 风险等级 |
| Keywords | Array of String | 风险关键词 |

### User 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| UserId | String | 用户 ID |
| Nickname | String | 用户昵称 |
| AccountType | Integer | 账号类型 |
| Gender | Integer | 性别 |
| Age | Integer | 年龄 |
| Level | Integer | 等级 |

### Device 对象

| 参数名称 | 类型 | 描述 |
|---------|------|------|
| IP | String | 设备 IP |
| Mac | String | 设备 MAC |
| TokenId | String | 设备 Token |
| DeviceId | String | 设备 ID |
| IMEI | String | 设备 IMEI |

---

## AIGC 检测说明

当设置 `Type=TEXT_AIGC` 时，接口会对输入文本进行 AI 生成内容的判定：

- **Score**：AIGC 风险分值，分数越高表示文本越可能是 AI 生成
- **Label**：当判定为 AI 生成时，Label 会反映相应标签
- **Suggestion**：
  - `Pass`：文本大概率为人类撰写
  - `Review`：存疑，建议人工复审
  - `Block`：文本大概率为 AI 生成

---

## 请求频率限制

| 检测类型 | 默认 QPS 上限 |
|---------|-------------|
| TEXT_AIGC（AI 生成文本识别） | **50 次/秒** |
| 常规文本内容安全检测 | 以控制台配额为准 |

> 超过频率限制会返回 `RequestLimitExceeded` 错误。如需提升配额，请联系腾讯云商务或提工单申请。

---

## 常见错误码

| 错误码 | 描述 | 处理建议 |
|-------|------|---------|
| AuthFailure | 鉴权失败 | 检查 SecretId 和 SecretKey 是否正确 |
| AuthFailure.SignatureExpire | 签名过期 | 检查系统时间是否准确 |
| InternalError | 内部错误 | 稍后重试 |
| InvalidParameter | 参数错误 | 检查请求参数是否符合规范 |
| InvalidParameterValue | 参数取值错误 | 检查 Content 是否正确 Base64 编码 |
| MissingParameter | 缺少参数 | 检查必填参数是否传入 |
| RequestLimitExceeded | 请求频率超限 | 降低请求频率或申请提升配额 |
| ResourceNotFound | 资源不存在 | 检查 BizType 是否正确 |
| UnauthorizedOperation | 未授权操作 | 确认账号已开通文本内容安全服务 |
| UnsupportedOperation | 不支持的操作 | 检查 API 版本和接口名称 |

---

## 调用示例（Python SDK）

```python
import base64
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tms.v20201229 import tms_client, models

# 创建凭证
cred = credential.Credential("your-secret-id", "your-secret-key")

# 配置 HTTP 和 Client
httpProfile = HttpProfile()
httpProfile.endpoint = "tms.tencentcloudapi.com"
clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile

# 创建客户端
client = tms_client.TmsClient(cred, "ap-guangzhou", clientProfile)

# 构造请求
req = models.TextModerationRequest()
content = base64.b64encode("待检测的文本内容".encode("utf-8")).decode("utf-8")
req.Content = content
req.Type = "TEXT_AIGC"

# 发送请求
resp = client.TextModeration(req)
print(json.loads(resp.to_json_string()))
```
