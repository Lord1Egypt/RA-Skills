# 视频特效 API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/1616/119002

## 接口信息

- **接口域名**：vclm.tencentcloudapi.com
- **Action**：DescribeTemplateToVideoJob
- **Version**：2024-05-23
- **图片限制**：≤10MB

## 输入参数

| 参数名称    | 必选  | 类型     | 描述                                                                                                                                                                  |
| ------- | --- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Action  | 是   | String | [公共参数](https://cloud.tencent.com/document/api/1616/107789)，本接口取值：DescribeTemplateToVideoJob。                                                                        |
| Version | 是   | String | [公共参数](https://cloud.tencent.com/document/api/1616/107789)，本接口取值：2024-05-23。                                                                                        |
| Region  | 是   | String | [公共参数](https://cloud.tencent.com/document/api/1616/107789)，详见产品支持的 [地域列表](https://cloud.tencent.com/document/api/1616/107789#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8)。 |
| JobId   | 是   | String | 任务ID。<br>示例值：1305546906952867840                                                                                                                                    |

## 输出参数

| 参数名称           | 类型     | 描述                                                                                     |
| -------------- | ------ | -------------------------------------------------------------------------------------- |
| Status         | String | 任务状态。WAIT：等待中，RUN：执行中，FAIL：任务失败，DONE：任务成功<br>示例值：RUN                                   |
| ErrorCode      | String | 任务执行错误码。当任务状态不为 FAIL 时，该值为""。<br>示例值：FailedOperation.DriverFailed                      |
| ErrorMessage   | String | 任务执行错误信息。当任务状态不为 FAIL 时，该值为""。<br>示例值：驱动失败                                             |
| ResultVideoUrl | String | 结果视频 URL。有效期 24 小时。<br>示例值：https://console.cloud.tencent.com/result.mp4                |
| RequestId      | String | 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。 |

## 错误码

| 错误码                           | 描述           |
| ----------------------------- | ------------ |
| AuthFailure                   | CAM签名/鉴权错误。  |
| FailedOperation.InnerError    | 服务内部错误，请重试。  |
| FailedOperation.JobNotExist   | 任务不存在。       |
| ResourceInsufficient          | 资源不足。        |
| ResourceUnavailable.IsOpening | 服务正在开通中，请稍等。 |
| ResourceUnavailable.NotExist  | 计费状态未知。      |
| UnauthorizedOperation         | 未授权操作。       |
