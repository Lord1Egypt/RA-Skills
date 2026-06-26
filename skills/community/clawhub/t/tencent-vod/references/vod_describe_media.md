# vod_describe_media — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_describe_media.py`

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `vod_describe_media.py 5145403721233902989` | `vod_describe_media.py --file-id 5145403721233902989` | FileId **必须用 `--file-id` 参数传入**，不支持位置参数 |
| `vod_describe_media.py --file-id xxx` (无 `--json`) | `vod_describe_media.py --file-id xxx --json` | **用户要求 JSON 格式输出、或要提取播放地址/字幕/封面等字段时，必须加 `--json`**，再用 `jq` 处理 |
| `--filters meta` | `--filters metaData` | filters 值区分大小写，必须完整拼写 |

> 🚨 **强制规则**：用户说"提取播放地址"、"提取字幕地址"、"提取封面 URL"、"JSON 格式输出"等需要解析响应字段的场景，**必须加 `--json` 参数**，然后用 `jq` 提取所需字段。不加 `--json` 时输出为人类可读格式，无法用 `jq` 解析。

## 目录

**参数说明**
- [通用参数](#通用参数)
- [filters 可选值](#filters-可选值)
- [响应字段说明](#响应字段说明)（MediaInfoSet / BasicInfo / MetaData / TranscodeInfo / AdaptiveDynamicStreamingInfo / ReviewInfo 等）

**使用示例**
- [媒体信息查询](#媒体信息查询)

---

## 参数说明


### 通用参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string list | ✅ | 媒体文件 ID（支持多个，最多 20 个） |
| `--filters` | string list | - | 指定返回的信息类型（不指定则返回所有，支持以下 14 种类型） |
| `--region` | string | - | 地域，默认 `ap-guangzhou` |
| `--sub-app-id` | int | - | VOD 子应用 ID（2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--json` | flag | - | JSON 格式输出 |
| `--dry-run` | flag | - | 预览参数，不调用 API |

### filters 可选值

| filter 值 | 说明 | 包含内容 |
|-----------|------|---------|
| `basicInfo` | 基础信息 | 名称、描述、分类、类型、创建/更新时间、播放地址、封面、存储信息、来源信息（直播/TRTC/网页录制等） |
| `metaData` | 元信息 | 大小、容器格式、码率、分辨率、时长、旋转角度、MD5、视频流信息（编码、帧率）、音频流信息（采样率） |
| `transcodeInfo` | 转码结果信息 | 各规格转码输出（URL、容器、大小、时长、分辨率、码率、MD5、数字水印、视频/音频流信息） |
| `animatedGraphicsInfo` | 转动图结果信息 | 动图输出（URL、格式、大小、分辨率、码率、起始/结束时间） |
| `imageSpriteInfo` | 雪碧图信息 | 小图宽度/高度、每图数量、大图数量、大图地址、WebVtt 地址 |
| `snapshotByTimeOffsetInfo` | 指定时间点截图信息 | 各模板截图输出（时间点、URL、水印模板） |
| `sampleSnapshotInfo` | 采样截图信息 | 采样类型、采样间隔、截图数量、截图地址、水印模板 |
| `keyFrameDescInfo` | 打点信息 | 时间点和内容描述 |
| `adaptiveDynamicStreamingInfo` | 转自适应码流信息 | 播放地址、打包格式、加密类型、大小、数字水印、字幕信息、子流信息 |
| `miniProgramReviewInfo` | 小程序审核信息 | 模板 ID、审核结果、播放地址、审核元素、元信息 |
| `subtitleInfo` | 字幕信息 | 字幕 ID、名称、语言、格式、来源、URL |
| `reviewInfo` | 审核信息 | 媒体审核信息（模板 ID、审核建议、审核时间、违禁类型）、封面审核信息 |
| `mpsAiMediaInfo` | MPS 智能媒资信息 | 智能分析任务列表（任务类型、模板 ID、输出文件、输出文本） |
| `imageUnderstandingInfo` | 图片理解信息 | 图片理解结果列表（模板 ID、输出文件） |

### 响应字段说明

#### MediaInfoSet（媒体信息集合）
| 字段 | 类型 | 说明 |
|------|------|------|
| `BasicInfo` | object | 基础信息（详情见下表） |
| `MetaData` | object | 元信息（详情见下表） |
| `TranscodeInfo` | object | 转码信息（详情见下表） |
| `AnimatedGraphicsInfo` | object | 转动图信息 |
| `ImageSpriteInfo` | object | 雪碧图信息 |
| `SnapshotByTimeOffsetInfo` | object | 指定时间点截图信息 |
| `SampleSnapshotInfo` | object | 采样截图信息 |
| `KeyFrameDescInfo` | object | 打点信息 |
| `AdaptiveDynamicStreamingInfo` | object | 自适应码流信息 |
| `MiniProgramReviewInfo` | object | 小程序审核信息 |
| `SubtitleInfo` | object | 字幕信息 |
| `ReviewInfo` | object | 审核信息 |
| `MPSAiMediaInfo` | object | MPS 智能媒资信息 |
| `ImageUnderstandingInfo` | object | 图片理解信息 |
| `FileId` | string | 媒体文件 ID |

#### BasicInfo（基础信息）字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `Name` | string | 媒体名称 |
| `Description` | string | 媒体描述 |
| `ClassId` | int | 分类 ID |
| `ClassName` | string | 分类名称（旧版字段，优先使用 `ClassPath`） |
| `ClassPath` | string | 分类路径（如 "娱乐/搞笑"） |
| `Category` | string | 类别（如 "Video"） |
| `Type` | string | 类型（如 "mp4"） |
| `CreateTime` | string | 创建时间 |
| `UpdateTime` | string | 更新时间 |
| `ExpireTime` | string | 过期时间 |
| `MediaUrl` | string | 媒体播放地址 |
| `CoverUrl` | string | 封面地址 |
| `StorageRegion` | string | 存储园区 |
| `StoragePath` | string | 存储路径 |
| `StorageClass` | string | 存储类别（STANDARD、MAZ_STANDARD、ARCHIVE 等） |
| `Status` | string | 状态（Normal、Forbidden、Processing 等） |
| `TagSet` | string list | 标签列表 |
| `SourceInfo` | object | 来源信息（包含 SourceType、SourceContext、LiveRecordInfo、TrtcRecordInfo、WebPageRecordInfo 等） |
| `Vid` | string | 视频 ID（部分场景下返回） |

#### MetaData（元信息）字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `Size` | int | 大小（字节） |
| `Container` | string | 容器格式（如 "mp4"） |
| `Bitrate` | int | 总码率（bps） |
| `Width` | int | 宽度（像素） |
| `Height` | int | 高度（像素） |
| `Duration` | int | 总时长（秒） |
| `VideoDuration` | int | 视频时长（秒） |
| `AudioDuration` | int | 音频时长（秒） |
| `Rotate` | int | 旋转角度（度） |
| `Md5` | string | MD5 值 |
| `VideoStreamSet` | object list | 视频流信息数组（包含 Bitrate、Width、Height、Fps、Codec、CodecTag、DynamicRangeInfo 等） |
| `AudioStreamSet` | object list | 音频流信息数组（包含 Bitrate、SamplingRate、Codec 等） |

#### TranscodeInfo（转码信息）字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `TranscodeSet` | object list | 转码输出数组 |
| `TranscodeSet[].Definition` | int | 转码规格 ID |
| `TranscodeSet[].Url` | string | 转码输出地址 |
| `TranscodeSet[].Container` | string | 容器格式 |
| `TranscodeSet[].Size` | int | 大小（字节） |
| `TranscodeSet[].Duration` | int | 时长（秒） |
| `TranscodeSet[].Width` | int | 宽度（像素） |
| `TranscodeSet[].Height` | int | 高度（像素） |
| `TranscodeSet[].Bitrate` | int | 码率（bps） |
| `TranscodeSet[].Md5` | string | MD5 值 |
| `TranscodeSet[].DigitalWatermarkType` | string | 数字水印类型 |
| `TranscodeSet[].VideoStreamSet` | object list | 视频流信息 |
| `TranscodeSet[].AudioStreamSet` | object list | 音频流信息 |
| `TranscodeSet[].CopyRightWatermarkText` | string | 版权水印文本 |
| `TranscodeSet[].BlindWatermarkDefinition` | int | 盲水印模板 ID |

#### AdaptiveDynamicStreamingInfo（自适应码流信息）字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `AdaptiveDynamicStreamingSet` | object list | 自适应码流输出数组 |
| `AdaptiveDynamicStreamingSet[].Definition` | int | 自适应码流规格 ID |
| `AdaptiveDynamicStreamingSet[].Url` | string | 播放地址 |
| `AdaptiveDynamicStreamingSet[].Package` | string | 打包格式（HLS、DASH 等） |
| `AdaptiveDynamicStreamingSet[].DrmType` | string | 加密类型（FairPlay、Widevine、SimpleAES 等） |
| `AdaptiveDynamicStreamingSet[].Size` | int | 大小（字节） |
| `AdaptiveDynamicStreamingSet[].DigitalWatermarkType` | string | 数字水印类型 |
| `AdaptiveDynamicStreamingSet[].SubtitleSet` | object list | 字幕信息数组（包含 Id、Name、Language、Format、Source、Url） |
| `AdaptiveDynamicStreamingSet[].DefaultSubtitleId` | string | 默认字幕 ID |
| `AdaptiveDynamicStreamingSet[].SubStreamSet` | object list | 子流信息数组（包含 Type、Width、Height、Size） |
| `AdaptiveDynamicStreamingSet[].CopyRightWatermarkText` | string | 版权水印文本 |
| `AdaptiveDynamicStreamingSet[].BlindWatermarkDefinition` | int | 盲水印模板 ID |

#### ReviewInfo（审核信息）字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `MediaReviewInfo` | object | 媒体审核信息（包含 Definition、Suggestion、ReviewTime、TypeSet 等） |
| `CoverReviewInfo` | object | 封面审核信息（包含 Definition、Suggestion、ReviewTime、TypeSet 等） |

#### MPSAiMediaInfo（MPS 智能媒资信息）字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `AiMediaList` | object list | 智能媒资任务列表 |
| `AiMediaList[].TaskType` | string | 任务类型（如 `AIRecognition`、`AIAnalysis` 等） |
| `AiMediaList[].AiMediaTasks` | object list | 该类型下的任务结果列表 |
| `AiMediaList[].AiMediaTasks[].Definition` | int | 任务模板 ID |
| `AiMediaList[].AiMediaTasks[].OutputFile` | object list | 输出文件列表（包含 `FileType`、`Url`） |
| `AiMediaList[].AiMediaTasks[].OutputText` | string | 输出文本内容 |

#### ImageUnderstandingInfo（图片理解信息）字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `ImageUnderstandingSet` | object list | 图片理解结果列表 |
| `ImageUnderstandingSet[].Definition` | int | 任务模板 ID |
| `ImageUnderstandingSet[].OutputFile` | object list | 输出文件列表（包含 `FileType`、`Url`） |

### API 接口对应关系

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 查询媒体信息 | `DescribeMediaInfos` | https://cloud.tencent.com/document/product/266/31763 |

### 错误码说明

| 错误类型 | 原因 | 处理建议 |
|---------|------|---------|
| FileId 不存在 | 提供的 FileId 错误或媒体已被删除 | 检查 FileId 是否正确 |
| FileId 数量超过限制 | 一次查询超过 20 个 FileId | 分批次查询 |
| SubAppId 不匹配 | 指定的 SubAppId 与媒体所属子应用不一致 | 检查 SubAppId 是否正确 |
### 基础查询

#### 查询单个媒体的所有信息
```bash
python scripts/vod_describe_media.py --file-id 5285485487985271487
```

#### 查询多个媒体（批量）
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 5285485487985271488 5285485487985271489
```

#### 查询单个媒体的基础信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters basicInfo
```

#### JSON 格式输出
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --json
```

#### dry-run 预览参数
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters basicInfo \
    --dry-run
```

---

### 指定信息类型查询

#### 查询基础信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters basicInfo
```

#### 查询元信息（码率、分辨率、时长等）
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters metaData
```

#### 查询转码信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters transcodeInfo
```

#### 查询转动图信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters animatedGraphicsInfo
```

#### 查询雪碧图信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters imageSpriteInfo
```

#### 查询指定时间点截图信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters snapshotByTimeOffsetInfo
```

#### 查询采样截图信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters sampleSnapshotInfo
```

#### 查询打点信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters keyFrameDescInfo
```

#### 查询自适应码流信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters adaptiveDynamicStreamingInfo
```

#### 查询小程序审核信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters miniProgramReviewInfo
```

#### 查询字幕信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters subtitleInfo
```

#### 查询审核信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters reviewInfo
```

#### 查询 MPS 智能媒资信息（智能分类、标签、高光等）
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters mpsAiMediaInfo
```

#### 查询图片理解信息（物体检测、人脸识别、OCR 等）
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters imageUnderstandingInfo
```

#### 查询所有智能信息（智能媒资+图片理解）
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters mpsAiMediaInfo imageUnderstandingInfo
```

---

### 组合信息类型查询

#### 查询基础信息和元信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters basicInfo metaData
```

#### 查询转码信息和自适应码流信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters transcodeInfo adaptiveDynamicStreamingInfo
```

#### 查询所有截图相关信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters imageSpriteInfo snapshotByTimeOffsetInfo sampleSnapshotInfo
```

#### 查询媒体基础信息、转码信息和审核信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters basicInfo transcodeInfo reviewInfo
```

---

### 使用子应用 ID

#### 查询指定子应用的媒体信息
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --sub-app-id 1500000001
```

---

### 高级用法

#### 批量查询多个媒体并保存结果
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 5285485487985271488 \
    --json > media_infos.json
```

#### 查询并提取播放地址
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters basicInfo --json | jq -r '.MediaInfoSet[0].BasicInfo.MediaUrl'
```

#### 查询并提取转码输出地址列表
```bash
python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --filters transcodeInfo --json | jq -r '.MediaInfoSet[0].TranscodeInfo.TranscodeSet[].Url'
```

#### 查询并判断媒体是否存在
```bash
RESULT=$(python scripts/vod_describe_media.py \
    --file-id 5285485487985271487 \
    --json)
NOT_EXIST=$(echo "$RESULT" | jq -r '.NotExistFileIdSet | length')
if [ "$NOT_EXIST" -eq 0 ]; then
    echo "媒体存在"
else
    echo "媒体不存在"
fi
```

---

