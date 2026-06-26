# 一句话识别 API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/1093/35646

## 接口信息

- **接口域名**：asr.tencentcloudapi.com
- **Action**：SentenceRecognition
- **Version**：2019-06-14
- **限频**：30 次/秒
- **音频限制**：≤60s，≤3MB

## 引擎类型 (EngSerViceType)

### 电话场景
| 引擎 | 语言 |
|------|------|
| 8k_zh | 中文电话通用 |
| 8k_en | 英文电话通用 |

### 非电话场景
| 引擎 | 语言 |
|------|------|
| 16k_zh | 中文通用 |
| 16k_zh-PY | 中英粤 |
| 16k_zh_medical | 中文医疗 |
| 16k_en | 英语 |
| 16k_yue | 粤语 |
| 16k_ja | 日语 |
| 16k_ko | 韩语 |
| 16k_vi | 越南语 |
| 16k_ms | 马来语 |
| 16k_id | 印度尼西亚语 |
| 16k_fil | 菲律宾语 |
| 16k_th | 泰语 |
| 16k_pt | 葡萄牙语 |
| 16k_tr | 土耳其语 |
| 16k_ar | 阿拉伯语 |
| 16k_es | 西班牙语 |
| 16k_hi | 印地语 |
| 16k_fr | 法语 |
| 16k_de | 德语 |
| 16k_zh_dialect | 多方言（23种） |

## 输入参数

| 参数 | 必选 | 类型 | 描述 |
|------|------|------|------|
| EngSerViceType | 是 | String | 引擎模型类型 |
| SourceType | 是 | Integer | 0=URL, 1=POST body |
| VoiceFormat | 是 | String | 音频格式：wav/pcm/ogg-opus/speex/silk/mp3/m4a/aac/amr |
| Url | 否 | String | SourceType=0 时必填 |
| Data | 否 | String | SourceType=1 时必填，base64 编码 |
| DataLen | 否 | Integer | SourceType=1 时必填，原始数据长度 |
| WordInfo | 否 | Integer | 0=不显示词时间戳, 1=显示, 2=含标点 |
| FilterDirty | 否 | Integer | 0=不过滤, 1=过滤, 2=替换为 * |
| FilterModal | 否 | Integer | 0=不过滤, 1=部分, 2=严格 |
| FilterPunc | 否 | Integer | 0=不过滤, 1=句末, 2=全部 |
| ConvertNumMode | 否 | Integer | 0=中文数字, 1=智能转阿拉伯 |
| HotwordId | 否 | String | 热词表 ID |
| CustomizationId | 否 | String | 自学习模型 ID |
| HotwordList | 否 | String | 临时热词表 |
| InputSampleRate | 否 | Integer | PCM 8k 升采样，仅支持 8000 |
| ReplaceTextId | 否 | String | 替换词 ID |

## 输出参数

| 参数 | 类型 | 描述 |
|------|------|------|
| Result | String | 识别结果文本 |
| AudioDuration | Integer | 音频时长 (ms) |
| WordSize | Integer | 词时间戳列表长度 |
| WordList | Array of SentenceWord | 词时间戳列表 |
| RequestId | String | 请求 ID |

## 错误码

| 错误码 | 描述 |
|--------|------|
| FailedOperation.ErrorRecognize | 识别失败 |
| FailedOperation.ServiceIsolate | 欠费停止服务 |
| FailedOperation.UserHasNoAmount | 资源包耗尽 |
| FailedOperation.UserHasNoFreeAmount | 免费资源包耗尽 |
| FailedOperation.UserNotRegistered | 服务未开通 |
| InternalError | 内部错误 |
| InternalError.ErrorConfigure | 初始化配置失败 |
| InternalError.ErrorDownFile | 下载音频文件失败 |
| InternalError.ErrorFailNewprequest | 新建数组失败 |
| InternalError.ErrorFailWritetodb | 写入数据库失败 |
| InternalError.ErrorFileCannotopen | 文件无法打开 |
| InternalError.ErrorGetRoute | 获取路由失败 |
| InternalError.ErrorMakeLogpath | 创建日志路径失败 |
| InternalError.ErrorRecognize | 识别失败 |
| InvalidParameter.ErrorContentlength | 请求数据长度无效 |
| InvalidParameter.ErrorParamsMissing | 参数不全 |
| InvalidParameter.ErrorParsequest | 解析请求数据失败 |
| InvalidParameterValue | 参数取值错误 |
| InvalidParameterValue.ErrorInvalidAppid | AppId 无效 |
| InvalidParameterValue.ErrorInvalidClientip | ClientIp 无效 |
| InvalidParameterValue.ErrorInvalidEngservice | EngSerViceType 无效 |
| InvalidParameterValue.ErrorInvalidProjectid | ProjectId 无效 |
| InvalidParameterValue.ErrorInvalidRequestid | RequestId 无效 |
| InvalidParameterValue.ErrorInvalidSourcetype | SourceType 无效 |
| InvalidParameterValue.ErrorInvalidSubservicetype | SubserviceType 无效 |
| InvalidParameterValue.ErrorInvalidUrl | Url 无效 |
| InvalidParameterValue.ErrorInvalidUseraudiokey | UsrAudioKey 无效 |
| InvalidParameterValue.ErrorInvalidVoiceFormat | 音频编码格式不支持 |
| InvalidParameterValue.ErrorInvalidVoicedata | 音频数据无效 |
| InvalidParameterValue.ErrorVoicedataTooLong | 音频时长超过限制 |
