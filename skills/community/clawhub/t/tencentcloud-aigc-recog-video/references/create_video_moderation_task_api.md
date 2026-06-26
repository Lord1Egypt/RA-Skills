# CreateVideoModerationTask API 参考

> 来源：[腾讯云文档 - 创建视频审核任务](https://cloud.tencent.com/document/product/1265/80017)

## 接口描述

- **接口名称**：CreateVideoModerationTask
- **接口功能**：创建视频内容审核任务，当审核任务完成后，可通过 DescribeTaskDetail 接口查看审核结果。
- **产品**：视频内容安全（VM）
- **默认接口请求频率限制**：20 次/秒

## 请求参数

### 公共参数

| 名称 | 类型 | 必选 | 描述 |
|------|------|------|------|
| Action | String | 是 | 公共参数，本接口取值：CreateVideoModerationTask |
| Version | String | 是 | 公共参数，本接口取值：2021-09-22 |
| Region | String | 否 | 公共参数 |

### 请求正文参数

| 名称 | 类型 | 必选 | 描述 |
|------|------|------|------|
| BizType | String | 是 | 该字段表示策略的具体编号，用于接口调度。需要提前在[内容安全控制台](https://console.cloud.tencent.com/cms/video/strategy)中创建策略，每个策略会有一个唯一编号。 |
| Type | String | 是 | 任务机型。取值包括：VIDEO（视频类型）、LIVE_VIDEO（直播类型）、**VIDEO_AIGC**（AI 生成视频检测）。本 Skill 固定使用 `VIDEO_AIGC`。 |
| Tasks | Array of [TaskInput](#taskinput) | 是 | 该字段表示输入的内容信息，最多支持同时传入 10 个任务。 |
| Seed | String | 否 | 用于回调的 Seed 参数。 |
| CallbackUrl | String | 否 | 回调地址，必须以 http 或 https 开头。 |
| Priority | Integer | 否 | 任务优先级，值越大优先级越高，范围 0-100，不填默认 0。 |

### TaskInput

| 名称 | 类型 | 必选 | 描述 |
|------|------|------|------|
| DataId | String | 否 | 选填参数，该字段表示您为待检测对象分配的数据 ID，传入后可识别对应的审核结果。长度不超过 128 字符。 |
| Name | String | 否 | 选填参数，该字段表示待审核文件的名称。 |
| Input | [StorageInfo](#storageinfo) | 是 | 该字段表示待审核文件的访问参数。 |

### StorageInfo

| 名称 | 类型 | 必选 | 描述 |
|------|------|------|------|
| Type | String | 否 | 该字段表示文件访问类型。取值：`URL`（资源链接）、`COS`（腾讯云对象存储）。 |
| Url | String | 否 | 该字段表示文件的 URL 地址。备注：当 Type 为 URL 时此字段生效。 |
| BucketInfo | Object | 否 | 该字段表示文件的腾讯云 COS 存储桶信息。备注：当 Type 为 COS 时此字段生效。 |

## 输出参数

| 名称 | 类型 | 描述 |
|------|------|------|
| Results | Array of [TaskResult](#taskresult) | 任务创建结果。若请求中仅创建一个任务，则该字段仅包含一个元素。 |
| RequestId | String | 唯一请求 ID。 |

### TaskResult

| 名称 | 类型 | 描述 |
|------|------|------|
| DataId | String | 该字段用于返回创建视频审核任务时在 TaskInput 结构内传入的 DataId。 |
| TaskId | String | 该字段用于返回视频审核任务的任务 ID，用于后续查询任务状态和结果。 |
| Code | String | 该字段表示任务创建的状态。取值：OK（创建成功）、其他值表示创建失败。 |
| Message | String | 该字段表示任务创建的详细信息。 |

## 示例

### 请求示例

```
POST https://vm.tencentcloudapi.com
Content-Type: application/json

{
    "BizType": "your_biz_type",
    "Type": "VIDEO_AIGC",
    "Tasks": [
        {
            "Input": {
                "Type": "URL",
                "Url": "https://example.com/video.mp4"
            }
        }
    ]
}
```

### 响应示例

```json
{
    "Response": {
        "Results": [
            {
                "Code": "",
                "DataId": "",
                "Message": "OK",
                "TaskId": "tvm-xxx"
            }
        ],
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
