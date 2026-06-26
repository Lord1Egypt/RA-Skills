# 录音文件识别极速版 API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/1093/52097

## 接口信息

- **请求地址**：`https://asr.cloud.tencent.com/asr/flash/v1/<appid>?{请求参数}`
- **请求方式**：HTTPS POST（Body 为音频原始二进制数据）
- **签名方式**：HMAC-SHA1（非云 API 签名 v3）
- **音频限制**：≤100MB，≤2h
- **并发限制**：普通版 20 / 大模型版 5

## 支持语言

中文普通话、粤语、英语、韩语、日语、泰语、印度尼西亚语、越南语、马来语、菲律宾语、葡萄牙语、土耳其语、阿拉伯语、西班牙语、印地语、法语、德语 + 23 种方言

## 支持格式

wav、pcm、ogg-opus、speex、silk、mp3、m4a、aac、amr

## 引擎类型 (engine_type)

### 电话场景
| 引擎 | 语言 | 备注 |
|------|------|------|
| 8k_zh | 中文电话通用 | |
| 8k_en | 英文电话通用 | |
| 8k_zh_large | 中文电话大模型 | 【大模型版】 |

### 非电话场景
| 引擎 | 语言 | 备注 |
|------|------|------|
| 16k_zh_en | 中英粤+9种方言大模型 | 【大模型版】 |
| 16k_zh | 中文通用 | |
| 16k_zh_large | 普方英大模型 | 【大模型版】 |
| 16k_multi_lang | 多语种大模型 | 【大模型版】15 语种自动识别 |
| 16k_zh-PY | 中英粤 | |
| 16k_yue | 粤语 | |
| 16k_en | 英语 | |
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

## 请求参数 (URL)

| 参数 | 必选 | 类型 | 描述 |
|------|------|------|------|
| appid | 是 | Integer | 腾讯云 AppId |
| secretid | 是 | String | SecretId |
| engine_type | 是 | String | 引擎类型 |
| voice_format | 是 | String | 音频格式 |
| timestamp | 是 | Integer | UNIX 时间戳（±3 分钟） |
| speaker_diarization | 否 | Integer | 0=关闭, 1=开启（仅中文） |
| hotword_id | 否 | String | 热词表 ID |
| customization_id | 否 | String | 自学习模型 ID |
| filter_dirty | 否 | Integer | 0=不过滤, 1=过滤, 2=替换 |
| filter_modal | 否 | Integer | 0=不过滤, 1=部分, 2=严格 |
| filter_punc | 否 | Integer | 0=不过滤, 1=句末, 2=全部 |
| convert_num_mode | 否 | Integer | 0=中文, 1=智能转换 |
| word_info | 否 | Integer | 0=关闭, 1=词级, 2=含标点, 3=字幕模式 |
| first_channel_only | 否 | Integer | 0=所有声道, 1=仅首声道 |
| sentence_max_length | 否 | Integer | 单标点最大字数 [6,40] |
| hotword_list | 否 | String | 临时热词表 |
| input_sample_rate | 否 | Integer | PCM 8k 升采样，仅 8000 |

## 请求 Header

| 参数 | 描述 |
|------|------|
| Host | asr.cloud.tencent.com |
| Authorization | HMAC-SHA1 签名 |
| Content-Type | application/octet-stream |
| Content-Length | 音频数据字节数 |

## 签名生成

1. 按字典序排列所有 URL 参数
2. 拼接签名原文：`POST` + `asr.cloud.tencent.com/asr/flash/v1/{appid}?{sorted_params}`
3. 使用 SecretKey 进行 HMAC-SHA1 加密，再 Base64 编码

## 响应结构

### 顶层
| 参数 | 类型 | 描述 |
|------|------|------|
| code | Integer | 0=正常 |
| message | String | 错误信息 |
| request_id | String | 请求 ID |
| audio_duration | Integer | 音频时长 (ms) |
| flash_result | []Result | 声道识别结果 |

### Result
| 参数 | 类型 | 描述 |
|------|------|------|
| channel_id | Integer | 声道 ID |
| text | String | 完整识别结果 |
| sentence_list | []Sentence | 句子级结果 |

### Sentence
| 参数 | 类型 | 描述 |
|------|------|------|
| text | String | 句子文本 |
| start_time | Integer | 开始时间 (ms) |
| end_time | Integer | 结束时间 (ms) |
| speaker_id | Integer | 说话人 ID |
| word_list | []Word | 词级结果 |

### Word
| 参数 | 类型 | 描述 |
|------|------|------|
| word | String | 词文本 |
| start_time | Integer | 开始时间 (ms) |
| end_time | Integer | 结束时间 (ms) |
| stable_flag | Integer | 稳定标志 |

## 错误码

| 错误码 | 描述 |
|--------|------|
| 4001 | 参数不合法 |
| 4002 | 鉴权失败 |
| 4003 | 服务未开通 |
| 4004 | 资源包耗尽 |
| 4005 | 账户欠费 |
| 4006 | 并发超限 |
| 4007 | 音频解码失败 |
| 4008 | 数据上传超时 |
| 4009 | 连接断开 |
| 4010 | 上传未知文本消息 |
| 4011 | 音频数据太大 |
| 4012 | 音频数据为空 |
| 5001 | 机器负载/网络抖动导致失败（偶发可忽略） |
| 5002 | 音频识别失败 |
| 5003 | 音频识别超时 |
