# DescribeTaskDetail API 参考

> 来源：[腾讯云文档 - 查看任务详情](https://cloud.tencent.com/document/product/1265/80016)

## 接口描述

- **接口名称**：DescribeTaskDetail
- **接口功能**：查看视频内容审核任务的详细信息，包括任务状态、审核结果等。
- **产品**：视频内容安全（VM）
- **默认接口请求频率限制**：20 次/秒

## 请求参数

### 公共参数

| 名称 | 类型 | 必选 | 描述 |
|------|------|------|------|
| Action | String | 是 | 公共参数，本接口取值：DescribeTaskDetail |
| Version | String | 是 | 公共参数，本接口取值：2021-09-22 |
| Region | String | 否 | 公共参数 |

### 请求正文参数

| 名称 | 类型 | 必选 | 描述 |
|------|------|------|------|
| TaskId | String | 是 | 任务 ID，由 CreateVideoModerationTask 接口返回。 |
| ShowAllSegments | Boolean | 否 | 是否展示所有分片审核信息。默认只展示命中审核规则的分片信息。 |

## 输出参数

| 名称 | 类型 | 描述 |
|------|------|------|
| TaskId | String | 任务 ID。 |
| DataId | String | 该字段用于返回创建任务时传入的 DataId。 |
| BizType | String | 该字段用于返回任务使用的策略类型。 |
| Name | String | 该字段用于返回任务名称。 |
| Status | String | 任务状态。取值：`PENDING`（排队中）、`RUNNING`（处理中）、`FINISH`（已完成）、`ERROR`（处理出错）、`CANCELLED`（任务已取消）。 |
| Type | String | 任务类型。 |
| Suggestion | String | 该字段用于返回检测结果的建议值。取值：`Pass`（正常）、`Review`（疑似违规，建议人工复审）、`Block`（确认违规，建议直接处置）。 |
| Label | String | 该字段用于返回检测结果中所对应的恶意标签。当为 `Normal` 时表示正常内容。 |
| CreatedAt | String | 任务创建时间。 |
| UpdatedAt | String | 任务更新时间。 |
| Labels | Array of [TaskLabel](#tasklabel) | 任务标签信息。 |
| InputInfo | Object | 任务输入的音视频内容信息。 |
| AudioText | String | 音频文本审核中的文字内容（若有）。 |
| ImageSegments | Array of [ImageSegments](#imagesegments) | 视频截帧审核结果。 |
| AudioSegments | Array of [AudioSegments](#audiosegments) | 音频审核结果。 |
| ErrorMessage | String | 如果任务状态为 ERROR，此字段为错误原因。 |
| ErrorDescription | String | 错误描述。 |
| RequestId | String | 唯一请求 ID。 |

### TaskLabel

| 名称 | 类型 | 描述 |
|------|------|------|
| Label | String | 恶意标签名称。 |
| Suggestion | String | 审核建议。 |
| Score | Integer | 置信度分值（0-100）。 |

### ImageSegments

| 名称 | 类型 | 描述 |
|------|------|------|
| OffsetTime | String | 截帧时间偏移，单位：毫秒。 |
| Result | [ImageResult](#imageresult) | 截帧审核结果。 |

### ImageResult

| 名称 | 类型 | 描述 |
|------|------|------|
| Suggestion | String | 审核建议。取值：`Pass`、`Review`、`Block`。 |
| Label | String | 恶意标签。 |
| SubLabel | String | 子标签名称。 |
| Score | Integer | 置信度分值（0-100）。 |
| Url | String | 截帧图片 URL。 |

### AudioSegments

| 名称 | 类型 | 描述 |
|------|------|------|
| Offset | Float | 音频片段偏移量，单位：秒。 |
| Duration | String | 音频片段时长。 |
| Result | [AudioResult](#audioresult) | 音频审核结果。 |

### AudioResult

| 名称 | 类型 | 描述 |
|------|------|------|
| Suggestion | String | 审核建议。取值：`Pass`、`Review`、`Block`。 |
| Label | String | 恶意标签。 |
| SubLabel | String | 子标签名称。 |
| Score | Integer | 置信度分值（0-100）。 |
| Text | String | 识别出的文本内容（若有）。 |
| Url | String | 音频片段地址。 |

## 示例

### 请求示例

```
POST https://vm.tencentcloudapi.com
Content-Type: application/json

{
    "TaskId": "tvm-xxx"
}
```

### 响应示例（任务完成）

```json
{
    "Response": {
        "TaskId": "tvm-xxx",
        "DataId": "",
        "BizType": "your_biz_type",
        "Name": "",
        "Status": "FINISH",
        "Type": "VIDEO_AIGC",
        "Suggestion": "Block",
        "Label": "GeneratedContentRisk",
        "CreatedAt": "2025-01-01 12:00:00",
        "UpdatedAt": "2025-01-01 12:01:30",
        "Labels": [
            {
                "Label": "GeneratedContentRisk",
                "Suggestion": "Block",
                "Score": 95
            }
        ],
        "ImageSegments": [
            {
                "OffsetTime": "1000",
                "Result": {
                    "Suggestion": "Block",
                    "Label": "GeneratedContentRisk",
                    "SubLabel": "AIVideoGenerated",
                    "Score": 95,
                    "Url": "https://example.com/snapshot.jpg"
                }
            }
        ],
        "AudioSegments": [],
        "AudioText": "",
        "RequestId": "xxx"
    }
}
```

### 响应示例（任务处理中）

```json
{
    "Response": {
        "TaskId": "tvm-xxx",
        "Status": "RUNNING",
        "RequestId": "xxx"
    }
}
```

## 错误码

| 错误码 | 描述 |
|--------|------|
| DryRunOperation | DryRun 操作，代表请求将会是成功的，只是多传了 DryRun 参数。 |
| InternalError | 内部错误。 |
| InvalidParameter | 参数错误。 |
| InvalidParameterValue | 参数取值错误。 |
| LimitExceeded | 超过配额限制。 |
| MissingParameter | 缺少参数错误。 |
| OperationDenied | 操作被拒绝。 |
| RequestLimitExceeded | 请求的次数超过了频率限制。 |
| ResourceInUse | 资源被占用。 |
| ResourceInsufficient | 资源不足。 |
| ResourceNotFound | 资源不存在。 |
| ResourceUnavailable | 资源不可用。 |
| UnauthorizedOperation | 未授权操作。 |
| UnauthorizedOperation.Unauthorized | 未授权操作。 |
