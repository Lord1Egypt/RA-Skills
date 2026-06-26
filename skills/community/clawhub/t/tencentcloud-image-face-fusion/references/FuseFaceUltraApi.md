# 图片人脸融合（专业版）API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/670/106891

## 接口信息

- **接口域名**：facefusion.tencentcloudapi.com
- **Action**：FuseFaceUltra
- **Version**：2022-09-27
- **图片限制**：base64 编码后 ≤10M，URL ≤20M

## 输入参数

| 参数名称           | 必选 | 类型               | 描述                                                                                                                                                                                                                                                                                                                                              |
| ---------------- | ---- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Action           | 是   | String             | 公共参数，本接口取值：FuseFaceUltra。                                                                                                                                                                                                                                                                                                                     |
| Version          | 是   | String             | 公共参数，本接口取值：2022-09-27。                                                                                                                                                                                                                                                                                                                        |
| Region           | 是   | String             | 公共参数，详见产品支持的地域列表。                                                                                                                                                                                                                                                                                                                           |
| RspImgType       | 否   | String             | 返回融合结果图片方式（url 或 base64），二选一。url有效期为1天。                                                                                                                                                                                                                                                                                                        |
| MergeInfos       | 否   | Array of MergeInfo | 用户人脸图片、素材模板图的人脸位置信息。主要用于素材模版中人脸以及用作融合的用户人脸相关信息，两种人脸都需要提供人脸图片，可选择提供人脸框位置。目前最多支持融合模板图片中的6张人脸。                                                                                                                                                                                                                                                  |
| ModelUrl         | 否   | String             | 素材模版图片的url地址。base64 和 url 必须提供一个，如果都提供以 url 为准。图片分辨率限制：图片中面部尺寸大于34×34；图片尺寸大于64×64，小于8000×8000（单边限制）。图片大小限制：base64 编码后大小不可超过10M，url不超过20M。图片格式：支持jpg或png。                                                                                                                                                                                       |
| ModelImage       | 否   | String             | 素材模版图片base64数据。base64 和 url 必须提供一个，如果都提供以 url 为准。素材图片限制：图片中面部尺寸大于34×34；图片尺寸大于64×64，小于8000×8000（单边限制）。图片大小限制：base64 编码后大小不可超过10M，url不超过20M。支持图片格式：支持jpg或png。                                                                                                                                                                                  |
| FusionUltraParam | 否   | FusionUltraParam   | 图片人脸融合（专业版）效果参数。可用于设置拉脸、人脸增强、磨皮、牙齿增强、妆容迁移等融合效果参数，生成理想的融合效果。不传默认使用接口推荐值。                                                                                                                                                                                                                                                                        |
| LogoAdd          | 否   | Integer            | 为融合结果图添加合成标识的开关，默认为1。1：添加标识。0：不添加标识。其他数值：默认按1处理。建议您使用显著标识来提示结果图使用了人脸融合技术，是AI合成的图片。                                                                                                                                                                                                                                                              |
| LogoParam        | 否   | LogoParam          | 标识内容设置。默认在融合结果图右下角添加"本图片为AI合成图片"字样，您可根据自身需要替换为其他的Logo图片。                                                                                                                                                                                                                                                                                         |
| SwapModelType    | 否   | Integer            | 融合模型类型参数：默认为1。1：默认泛娱乐场景，画面偏锐。2：影视级场景，画面偏自然。3：影视级场景，高分辨率，画面偏自然。4：影视级场景，高分辨率，高人脸相似度，画面偏自然，可用于证件照等场景。5：影视级场景，高分辨率，对闭眼和遮挡更友好。6：影视级场景，高分辨率，极高人脸相似度，可用于电商照片、证件照、文旅照片等场景。                                                                                                                                                     |

### MergeInfo 结构

| 参数名称              | 必选 | 类型     | 描述                                                                                                                              |
| ------------------- | ---- | -------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Image               | 否   | String   | 输入图片base64。base64 和 url 必须提供一个，如果都提供以 url 为准。素材图片限制：图片中面部尺寸大于34×34；图片尺寸大于64×64。支持图片格式：支持jpg或png。                                 |
| Url                 | 否   | String   | 输入图片url。base64 和 url 必须提供一个，如果都提供以 url 为准。素材图片限制：图片中面部尺寸大于34×34；图片尺寸大于64×64。支持图片格式：支持jpg或png。                                    |
| InputImageFaceRect  | 否   | FaceRect | 上传的图片人脸位置信息（人脸框），Width、Height >= 30。                                                                                              |
| TemplateFaceID      | 否   | String   | 素材人脸ID，不填默认取最大人脸。                                                                                                               |
| TemplateFaceRect    | 否   | FaceRect | 模板中人脸位置信息(人脸框)，不填默认取最大人脸。此字段仅适用于图片融合自定义模板素材场景。Width、Height >= 30。                                                                 |

### FusionUltraParam 结构

| 参数名称               | 必选 | 类型   | 描述                                                                                         |
| -------------------- | ---- | ------ | -------------------------------------------------------------------------------------------- |
| WarpRadio            | 否   | Float  | 拉脸强度。取值越大越像用户人脸。取值范围：0-1，默认0.7。仅对SwapModelType 1-5生效。                                       |
| EnhanceRadio         | 否   | Float  | 人脸增强强度。取值越大增强越强。取值范围：0-1，默认0.5。仅对SwapModelType 1-5生效。                                        |
| MpRadio              | 否   | Float  | 磨皮强度。取值范围：0-1，默认0.5。仅对SwapModelType 1-5生效。                                                 |
| BlurRadio            | 否   | Float  | 人脸模糊开关（暂不支持）。仅对SwapModelType 1-5生效。                                                         |
| TeethEnhanceRadio    | 否   | Float  | 牙齿增强开关。0：关闭，1：打开（默认）。仅对SwapModelType 1-5生效。                                                 |
| MakeupTransferRadio  | 否   | Float  | 妆容迁移开关。0：关闭（默认），1：打开。仅对SwapModelType 1-5生效。                                                 |

### LogoParam 结构

| 参数名称    | 必选 | 类型     | 描述                                                                                                   |
| --------- | ---- | -------- | ------------------------------------------------------------------------------------------------------ |
| LogoRect  | 否   | FaceRect | 标识图片位于融合结果图中的坐标，将按照坐标对标识图片进行位置和大小的拉伸匹配。Width、Height <= 2160。                                          |
| LogoUrl   | 否   | String   | 标识图片Url地址。base64 和 url 必须提供一个，如果都提供以 url 为准。支持jpg或png，base64 编码后大小不超过10M。                              |
| LogoImage | 否   | String   | 标识图片base64数据。base64 和 url 必须提供一个，如果都提供以 url 为准。支持jpg或png，base64 编码后大小不超过10M。                           |

### FaceRect 结构

| 参数名称 | 必选 | 类型    | 描述           |
| -------- | ---- | ------- | -------------- |
| X        | 是   | Integer | 人脸框左上角横坐标。 |
| Y        | 是   | Integer | 人脸框左上角纵坐标。 |
| Width    | 是   | Integer | 人脸框宽度。       |
| Height   | 是   | Integer | 人脸框高度。       |

## 输出参数

| 参数名称     | 类型   | 描述                                                                                                        |
| ---------- | ------ | ----------------------------------------------------------------------------------------------------------- |
| FusedImage | String | RspImgType 为 url 时，返回结果的 url；RspImgType 为 base64 时返回 base64 数据。url有效期为1天。                                   |
| RequestId  | String | 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。                       |

## 错误码

| 错误码                                              | 描述                            |
| -------------------------------------------------- | ------------------------------- |
| FailedOperation.FaceBlurDetectFailed               | 人脸模糊检测失败。                   |
| FailedOperation.FaceBorderCheckFailed              | 人脸出框检测失败。                   |
| FailedOperation.FaceDetectFailed                   | 人脸检测失败。                       |
| FailedOperation.FaceExceedBorder                   | 人脸超出边界。                       |
| FailedOperation.FaceFusionFailed                   | 人脸融合失败。                       |
| FailedOperation.FaceRectInvalid                    | 人脸框不合法。                       |
| FailedOperation.FaceSizeTooSmall                   | 人脸尺寸过小。                       |
| FailedOperation.FuseFreqCtrl                       | 融合频率控制。                       |
| FailedOperation.FuseImageError                     | 融合图片错误。                       |
| FailedOperation.FuseInnerError                     | 融合内部错误。                       |
| FailedOperation.FuseMaterialNotAuth                | 素材未授权。                         |
| FailedOperation.FuseMaterialNotExist               | 素材不存在。                         |
| FailedOperation.FuseSavePhotoFailed                | 保存融合结果图失败。                   |
| FailedOperation.ImageDecodeFailed                  | 图片解码失败。                       |
| FailedOperation.ImageDownloadError                 | 图片下载错误。                       |
| FailedOperation.ImageResolutionExceed              | 图片分辨率过大。                       |
| FailedOperation.ImageResolutionTooSmall            | 图片分辨率过小。                       |
| FailedOperation.ImageSizeExceed                    | base64编码后的图片数据过大。               |
| FailedOperation.ImageSizeInvalid                   | 图片尺寸不合法。                       |
| FailedOperation.InnerError                         | 服务内部错误，请重试。                   |
| FailedOperation.NoFaceDetected                     | 未检测到人脸。                       |
| FailedOperation.ParameterValueError                | 参数值错误。                         |
| FailedOperation.RequestEntityTooLarge              | 整个请求体太大（通常主要是图片）。             |
| FailedOperation.RequestTimeout                     | 后端服务超时。                       |
| FailedOperation.RpcFail                            | RPC请求失败，一般为算法微服务故障。           |
| FailedOperation.ServerError                        | 算法服务异常，请重试。                   |
| FailedOperation.TemplateFaceIdNotExist             | 素材人脸ID不存在。                     |
| FailedOperation.UnKnowError                        | 内部错误。                           |
| InvalidParameterValue.FaceRectParameterValueError  | 人脸框参数值错误。                     |
| InvalidParameterValue.ImageEmpty                   | 图片为空。                           |
| InvalidParameterValue.MergeInfosIsEmpty            | MergeInfos 为空。                  |
| InvalidParameterValue.NoFaceInPhoto                | 图片中没有人脸。                       |
| InvalidParameterValue.UrlIllegal                   | URL格式不合法。                       |
| ResourceUnavailable.InArrears                      | 账号已欠费。                         |
| ResourceUnavailable.NotExist                       | 计费状态未知，请确认是否已在控制台开通服务。       |
