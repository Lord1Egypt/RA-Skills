# 视频特效 API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/1616/119001

## 接口信息

- **接口域名**：vclm.tencentcloudapi.com
- **Action**：SubmitTemplateToVideoJob
- **Version**：2024-05-23
- **图片限制**：≤10MB

## 输入参数

| 参数名称       | 必选  | 类型                                                                          | 描述                                                                                                                                                                                                                                                  |
| ---------- | --- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Action     | 是   | String                                                                      | [公共参数](https://cloud.tencent.com/document/api/1616/107789)，本接口取值：SubmitTemplateToVideoJob。                                                                                                                                                          |
| Version    | 是   | String                                                                      | [公共参数](https://cloud.tencent.com/document/api/1616/107789)，本接口取值：2024-05-23。                                                                                                                                                                        |
| Region     | 是   | String                                                                      | [公共参数](https://cloud.tencent.com/document/api/1616/107789)，详见产品支持的 [地域列表](https://cloud.tencent.com/document/api/1616/107789#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8)。                                                                                 |
| Template   | 是   | String                                                                      | 特效模板名称。请在 [视频特效模板列表](https://cloud.tencent.com/document/product/1616/119194) 中选择想要生成的特效对应的 template 名称。<br>示例值：hug                                                                                                                                  |
| Images.N   | 是   | Array of [Image](https://cloud.tencent.com/document/api/1616/107808#Image)  | 参考图像，不同特效输入图片的数量详见： [视频特效模板-图片要求说明](https://cloud.tencent.com/document/product/1616/119194)<br>- 支持传入图片Base64编码或图片URL（确保可访问）<br>- 图片格式：支持png、jpg、jpeg、webp、bmp、tiff<br>- 图片文件：大小不能超过10MB（base64后），图片分辨率不小于300*300px，不大于4096*4096，图片宽高比应在1:4 ~ 4:1之间 |
| LogoAdd    | 否   | Integer                                                                     | 为生成视频添加标识的开关，默认为1。传0 需前往 [控制台](https://console.cloud.tencent.com/vtc/setting) 申请开启显式标识自主完成后方可生效。<br>1：添加标识；<br>0：不添加标识；<br>其他数值：默认按1处理。<br>建议您使用显著标识来提示，该视频是 AI 生成的视频。<br>示例值：1                                                                     |
| LogoParam  | 否   | [LogoParam](https://cloud.tencent.com/document/api/1616/107808#LogoParam)   | 标识内容设置。<br>默认在生成视频的右下角添加“ AI 生成”或“视频由 AI 生成”字样，如需替换为其他的标识图片，需前往 [控制台](https://console.cloud.tencent.com/vtc/setting) 申请开启显式标识自主完成。<br>                                                                                                              |
| Resolution | 否   | String                                                                      | 视频输出分辨率，默认值：360p 。不同特效支持的清晰度及消耗积分数详见：[视频特效模板-单次调用消耗积分数列](https://cloud.tencent.com/document/product/1616/119194)<br>示例值：360p                                                                                                                        |
| BGM        | 否   | Boolean                                                                     | 是否为生成的视频添加背景音乐。默认：false， 传 true 时系统将从预设 BGM 库中自动挑选合适的音乐并添加；不传或为 false 则不添加 BGM。<br>示例值：false                                                                                                                                                        |
| ExtraParam | 否   | [ExtraParam](https://cloud.tencent.com/document/api/1616/107808#ExtraParam) | 扩展字段。                                                                                                                                                                                                                                               |

## 输出参数

| 参数名称      | 类型     | 描述                                                                                     |
| --------- | ------ | -------------------------------------------------------------------------------------- |
| JobId     | String | 任务ID。<br>示例值：1194931538865782784                                                       |
| RequestId | String | 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。 |

## 错误码

| 错误码                                     | 描述                |
| --------------------------------------- | ----------------- |
| FailedOperation.ImageDecodeFailed       | 图片解码失败。           |
| FailedOperation.ImageDownloadError      | 图片下载失败。           |
| FailedOperation.ImageSizeExceed         | base64编码后的图片数据过大。 |
| FailedOperation.ModerationFailed        | 内容审核不通过。          |
| FailedOperation.ModerationResponseError | ModerationFailed  |
| FailedOperation.RequestTimeout          | 后端服务超时。           |
| InvalidParameter.InvalidParameter       | 参数不合法。            |
| InvalidParameterValue.UrlIllegal        | URL格式不合法。         |
| MissingParameter                        | 缺少参数错误。           |
| RequestLimitExceeded.JobNumExceed       | 提交任务数超过最大并发。      |
| ResourceUnavailable.NotExist            | 计费状态未知。           |
| ResourcesSoldOut.ChargeStatusException  | 账号已欠费。            |
