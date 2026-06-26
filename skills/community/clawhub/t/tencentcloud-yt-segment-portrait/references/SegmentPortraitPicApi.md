# 人像分割 API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/1208/42970

## 接口信息

- **接口域名**：bda.tencentcloudapi.com
- **Action**：SegmentPortraitPic
- **Version**：2020-03-24
- **图片限制**：≤5MB

## 输入参数

| 参数名称       | 必选  | 类型     | 描述                                                                                                                                                                                                                                                                    |
| ---------- | --- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Action     | 是   | String | [公共参数](https://cloud.tencent.com/document/api/1208/42965)，本接口取值：SegmentPortraitPic。                                                                                                                                                                                   |
| Version    | 是   | String | [公共参数](https://cloud.tencent.com/document/api/1208/42965)，本接口取值：2020-03-24。                                                                                                                                                                                           |
| Region     | 是   | String | [公共参数](https://cloud.tencent.com/document/api/1208/42965)，详见产品支持的 [地域列表](https://cloud.tencent.com/document/api/1208/42965#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8)。                                                                                                     |
| Image      | 否   | String | 图片 base64 数据，base64 编码后大小不可超过5M。<br>图片分辨率须小于2000*2000。<br>支持PNG、JPG、JPEG、BMP，不支持 GIF 图片。<br>示例值：/9j/4AAQSkZJRgABAQAAAQABAAD/4gIo...lftXF/DjFZNXoSP5V2U0HMt/1FQf/Z                                                                                                     |
| Url        | 否   | String | 图片的 Url 。<br>Url、Image必须提供一个，如果都提供，只使用 Url。<br>图片分辨率须小于2000*2000 ，图片 base64 编码后大小不可超过5M。<br>图片存储于腾讯云的Url可保障更高下载速度和稳定性，建议图片存储于腾讯云。<br>非腾讯云存储的Url速度和稳定性可能受一定影响。<br>支持PNG、JPG、JPEG、BMP，不支持 GIF 图片。<br>示例值：https://liudehua-9527.cos.ap-guangzhou.myqcloud.com/input.jpeg |
| RspImgType | 否   | String | 返回图像方式（base64 或 Url ) ，二选一。url有效期为30分钟。<br>示例值：url                                                                                                                                                                                                                    |
| Scene      | 否   | String | 适用场景类型。<br><br>取值：GEN/GS。GEN为通用场景模式；GS为绿幕场景模式，针对绿幕场景下的人像分割效果更好。<br>两种模式选择一种传入，默认为GEN。<br>示例值：GEN                                                                                                                                                                      |

## 输出参数

| 参数名称           | 类型      | 描述                                                                                                                                                                                                                                                                                                                                               |
| -------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ResultImage    | String  | 处理后的图片 base64 数据，透明背景图。<br>注意：此字段可能返回 null，表示取不到有效值。<br>示例值：/9j/4AAQSkZJRgABAQAAAQABAAD/4gIo...lftXF/DjFZNXoSP5V2U0HMt/1FQf/Z                                                                                                                                                                                                                    |
| ResultMask     | String  | 一个通过 base64 编码的文件，解码后文件由 Float 型浮点数组成。这些浮点数代表原图从左上角开始的每一行的每一个像素点，每一个浮点数的值是原图相应像素点位于人体轮廓内的置信度（0-1）转化的灰度值（0-255）。<br>注意：此字段可能返回 null，表示取不到有效值。<br>示例值：/9j/4AAQSkZJRgABAQAAAQABAAD/4gIo...lftXF/DjFZNXoSP5V2U0HMt/1FQf/Z                                                                                                                            |
| HasForeground  | Boolean | 图片是否存在前景。<br>注意：此字段可能返回 null，表示取不到有效值。<br>示例值：false                                                                                                                                                                                                                                                                                              |
| ResultImageUrl | String  | 支持将处理过的图片 base64 数据，透明背景图以Url的形式返回值，Url有效期为30分钟。<br>注意：此字段可能返回 null，表示取不到有效值。<br>示例值：https://liudehua-9527.cos.ap-guangzhou.myqcloud.com/result.mp4?q-sign-algorithm=sha1&q-ak=AKID********EXAMPLE&q-sign-time=8888;9999&q-key-time=8888;9999&q-header-list=&q-url-param-list=&q-signature=7de87f7bf9cfd23df9da32f46661e7cf97a5603c              |
| ResultMaskUrl  | String  | 一个通过 base64 编码的文件，解码后文件由 Float 型浮点数组成。支持以Url形式的返回值；Url有效期为30分钟。<br>注意：此字段可能返回 null，表示取不到有效值。<br>示例值：https://liudehua-9527.cos.ap-guangzhou.myqcloud.com/mask.mp4?q-sign-algorithm=sha1&q-ak=AKID********EXAMPLE&q-sign-time=8888;9999&q-key-time=8888;9999&q-header-list=&q-url-param-list=&q-signature=7de87f7bf9cfd23df9da32f46661e7cf97a5603c |
| RequestId      | String  | 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。                                                                                                                                                                                                                                                           |

## 错误码

| 错误码                                         | 描述                     |
| ------------------------------------------- | ---------------------- |
| FailedOperation.BalanceInsufficient         | 余额不足，开通失败，请充值后再开通。     |
| FailedOperation.DownloadError               | 文件下载失败。                |
| FailedOperation.ImageDecodeFailed           | 图片解码失败。                |
| FailedOperation.ImageDownloadError          | 图片下载错误。                |
| FailedOperation.ImageNotForeground          | 图片不存在前景。               |
| FailedOperation.ImageNotSupported           | 不支持的图片文件。              |
| FailedOperation.ImageResolutionExceed       | 图片分辨率过大。               |
| FailedOperation.ImageResolutionInsufficient | 图片分辨率过小。               |
| FailedOperation.ImageSizeExceed             | base64编码后的图片数据过大。      |
| FailedOperation.InnerError                  | 服务内部错误，请重试。            |
| FailedOperation.ProfileNumExceed            | 人像数过多。                 |
| FailedOperation.RequestEntityTooLarge       | 整个请求体太大（通常主要是图片）。      |
| FailedOperation.RequestTimeout              | 后端服务超时。                |
| FailedOperation.RpcFail                     | RPC请求失败，一般为算法微服务故障。    |
| FailedOperation.SegmentFailed               | 人像分割失败。                |
| FailedOperation.ServerError                 | 算法服务异常，请重试。            |
| FailedOperation.UnKnowError                 | 内部错误。                  |
| InvalidParameter.InvalidParameter           | 参数不合法。                 |
| InvalidParameterValue.ImageEmpty            | 图片为空。                  |
| InvalidParameterValue.UrlIllegal            | URL格式不合法。              |
| LimitExceeded.TooLargeFileError             | 文件太大。                  |
| ResourceUnavailable.InArrears               | 账号已欠费。                 |
| ResourceUnavailable.NotExist                | 计费状态未知，请确认是否已在控制台开通服务。 |
| UnsupportedOperation.UnknowMethod           | 未知方法名。                 |
