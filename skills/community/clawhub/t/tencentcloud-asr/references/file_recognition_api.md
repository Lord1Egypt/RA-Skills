# 录音文件识别请求 API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/1093/37823

## 接口信息

- **接口域名**：asr.tencentcloudapi.com
- **Action**：CreateRecTask
- **Version**：2019-06-14
- **限频**：20 次/秒
- **音频限制**：URL ≤5h / 上传 ≤5MB

## 引擎类型 (EngineModelType)

### 电话场景
| 引擎 | 语言 | 备注 |
|------|------|------|
| 8k_zh | 中文电话通用 | |
| 8k_en | 英文电话通用 | |
| 8k_zh_large | 中文电话大模型 | 【大模型版】支持中文 + 23 种方言 + 闽南语/客家话/粤语/南宁话 |

### 通用场景
| 引擎 | 语言 | 备注 |
|------|------|------|
| 16k_zh_en | 中英粤+9种方言大模型 | 【大模型版】中英粤+四川/陕西/河南/上海/湖南/湖北/安徽/闽南/潮汕 |
| 16k_zh_large | 普方英大模型 | 【大模型版】中英+多方言 |
| 16k_multi_lang | 多语种大模型 | 【大模型版】15 语种自动识别 |
| 16k_zh | 中文普通话通用 | |
| 16k_en | 英语 | |
| 16k_en_large | 英语大模型 | |
| 16k_yue | 粤语 | |
| 16k_zh-PY | 中英粤混合 | |
| 16k_zh-TW | 中文繁体 | |
| 16k_ja | 日语 | |
| 16k_ko | 韩语 | |
| 16k_vi | 越南语 | |
| 16k_ms | 马来语 | |
| 16k_id | 印度尼西亚语 | |
| 16k_fil | 菲律宾语 | |
| 16k_th | 泰语 | |
| 16k_pt | 葡萄牙语 | |
| 16k_tr | 土耳其语 | |
| 16k_ar | 阿拉伯语 | |
| 16k_es | 西班牙语 | |
| 16k_hi | 印地语 | |
| 16k_fr | 法语 | |
| 16k_de | 德语 | |
| 16k_zh_medical | 中文医疗 | |

## 输入参数

| 参数 | 必选 | 类型 | 描述 |
|------|------|------|------|
| EngineModelType | 是 | String | 引擎模型类型 |
| ChannelNum | 是 | Integer | 1=单声道, 2=双声道（仅 8k） |
| ResTextFormat | 是 | Integer | 0=基础, 1=词级(无标点), 2=词级(含标点), 3=标点分段(字幕), 4=语义分段(增值), 5=口语转书面(增值) |
| SourceType | 是 | Integer | 0=URL, 1=POST body |
| Data | 否 | String | SourceType=1 时必填，base64 编码，≤5MB |
| DataLen | 否 | Integer | 原始数据长度 |
| Url | 否 | String | SourceType=0 时必填 |
| CallbackUrl | 否 | String | 回调 URL |
| SpeakerDiarization | 否 | Integer | 0=关闭, 1=开启, 3=角色分离(需 SpeakerRoles) |
| SpeakerNumber | 否 | Integer | 0=自动(最多20人), 1-10=指定人数 |
| HotwordId | 否 | String | 热词表 ID |
| CustomizationId | 否 | String | 自学习模型 ID |
| EmotionRecognition | 否 | Integer | 0=关闭, 1=开启(不显示标签), 2=开启(显示标签)【增值】 |
| EmotionalEnergy | 否 | Integer | 0=关闭, 1=开启 |
| ConvertNumMode | 否 | Integer | 0=中文数字, 1=智能转换, 3=数学符号转换 |
| FilterDirty | 否 | Integer | 0=不过滤, 1=过滤, 2=替换 |
| FilterPunc | 否 | Integer | 0=不过滤, 1=句末, 2=全部 |
| FilterModal | 否 | Integer | 0=不过滤, 1=部分, 2=严格 |
| SentenceMaxLength | 否 | Integer | 单标点最大字数 [6,40], 0=关闭 |
| HotwordList | 否 | String | 临时热词表 |
| ReplaceTextId | 否 | String | 替换词表 ID |

## 输出参数

| 参数 | 类型 | 描述 |
|------|------|------|
| Data.TaskId | Integer | 任务 ID（有效期 24h） |
| RequestId | String | 请求 ID |

## ResTextFormat 引擎限制

以下引擎仅支持 ResTextFormat=0：
`16k_multi_lang`、`16k_ja`、`16k_ko`、`16k_vi`、`16k_ms`、`16k_id`、`16k_fil`、`16k_th`、`16k_pt`、`16k_tr`、`16k_ar`、`16k_es`、`16k_hi`、`16k_fr`、`16k_zh_medical`、`16k_de`

## 说话人分离支持引擎

SpeakerDiarization=1 支持：`8k_zh`、`8k_zh_large`、`16k_zh`、`16k_ms`、`16k_en`、`16k_id`、`16k_zh_large`、`16k_zh_dialect`、`16k_zh_en`、`16k_es`、`16k_fr`、`16k_ja`、`16k_ko`

## 错误码

| 错误码 | 描述 |
|--------|------|
| AuthFailure.InvalidAuthorization | 鉴权错误 |
| FailedOperation.CheckAuthInfoFailed | 鉴权错误 |
| FailedOperation.ErrorDownFile | 下载音频文件失败 |
| FailedOperation.ErrorRecognize | 识别失败 |
| FailedOperation.ServiceIsolate | 欠费停止服务 |
| FailedOperation.UserHasNoAmount | 资源包耗尽 |
| FailedOperation.UserHasNoFreeAmount | 免费资源包耗尽 |
| FailedOperation.UserNotRegistered | 服务未开通 |
| InternalError.ErrorDownFile | 下载音频文件失败 |
| InternalError.FailAccessDatabase | 访问数据库失败 |
| InternalError.FailAccessRedis | 访问 Redis 失败 |
| InvalidParameter | 参数错误 |
| InvalidParameterValue | 参数取值错误 |
| MissingParameter | 缺少参数 |
| RequestLimitExceeded.UinLimitExceeded | 超出请求频率 |
| UnknownParameter | 未知参数 |

---

# 录音文件识别结果查询 API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/1093/37822

## 接口信息

- **Action**：DescribeTaskStatus
- **Version**：2019-06-14
- **限频**：50 次/秒
- **TaskId 有效期**：24 小时

## 输入参数

| 参数 | 必选 | 类型 | 描述 |
|------|------|------|------|
| TaskId | 是 | Integer | 从 CreateRecTask 获取的 TaskId |

## 输出参数 (Data)

| 参数 | 类型 | 描述 |
|------|------|------|
| TaskId | Integer | 任务 ID |
| Status | Integer | 0=waiting, 1=doing, 2=success, 3=failed |
| StatusStr | String | 状态字符串 |
| AudioDuration | Float | 音频时长（秒） |
| Result | String | 识别结果文本 |
| ResultDetail | Array | 详细结果列表 |
| ErrorMsg | String | 错误信息 |

### ResultDetail 结构

| 参数 | 类型 | 描述 |
|------|------|------|
| FinalSentence | String | 最终句子 |
| SliceSentence | String | 分词句子 |
| StartMs | Integer | 开始时间 (ms) |
| EndMs | Integer | 结束时间 (ms) |
| SpeechSpeed | Float | 语速 |
| WordsNum | Integer | 词数 |
| SpeakerId | Integer | 说话人 ID |
| EmotionType | Array | 情绪类型 |
| Words | Array | 词级时间戳列表 |

## 错误码

| 错误码 | 描述 |
|--------|------|
| FailedOperation.ErrorDownFile | 下载音频文件失败 |
| FailedOperation.ErrorRecognize | 识别失败 |
| FailedOperation.NoSuchTask | 错误的 TaskId |
| FailedOperation.ServiceIsolate | 欠费停止服务 |
| FailedOperation.UserHasNoFreeAmount | 免费资源包耗尽 |
| InternalError.FailAccessDatabase | 访问数据库失败 |
| InternalError.FailAccessRedis | 访问 Redis 失败 |
| InvalidParameter | 参数错误 |
| MissingParameter | 缺少参数 |
| UnknownParameter | 未知参数 |
