# 数据集字段目录与术语映射（Dataset Catalog）

> 本目录是 NL → QuerySpec 的「接地」依据：模型只能从这里列出的 `field key` 中选列、做筛选。
> 数据集信息来自数据万象（Cloud Infinite）MetaInsight / 数据集相关接口。

字段 key 采用 `dimension` 或 `dimension.subfield` 形式。

## 数据集名称选择规则

所有数据集查询统一按以下顺序确定 `DatasetName`：

1. 使用用户显式指定的名称或命令参数。
2. 使用对应场景的专用环境变量；没有专用变量时再使用 `TENCENT_COS_DATASET_NAME`。
3. 已知存储桶时，执行 `find-datasets-by-bucket` 获取候选数据集，并按模板筛选。
4. 仍有多个候选或缺少必要上下文时，再向用户确认。

不得臆造数据集名称，也不要在能够通过桶反查时立即追问。

## 一、数据集基础信息（来自 DescribeDatasets）

| field key | 业务名 | 说明 |
| --- | --- | --- |
| `datasetName` | 数据集名称 | 用户可读的数据集名；优先使用用户指定值或 `TENCENT_COS_DATASET_NAME` |
| `datasetId` | 数据集 ID | 后端唯一标识 |
| `datasetType` | 数据集类型 | 如 `MetaInsight` |
| `createdAt` | 创建时间 | ISO 时间 |
| `status` | 状态 | 启用 / 停用等 |
| `description` | 描述 | 数据集备注 |
| `bindingBucket` | 绑定存储桶 | 数据集关联 COS 桶 |
| `templateId` | 模板 ID | 数据集使用的索引模板 |

## 二、数据集字段（来自 DescribeDatasetFields）

| field key | 业务名 | 说明 |
| --- | --- | --- |
| `fieldName` | 字段名 | 数据集中的字段标识 |
| `fieldType` | 字段类型 | String / Long / Double / Boolean 等 |
| `fieldRequired` | 是否必填 | 必填 / 可选 |
| `fieldSource` | 字段来源 | 系统 / 自定义 |

## 三、术语映射表（口语 → field key / 取值）

| 用户口语 | 映射 |
| --- | --- |
| 数据集名称 / 数据集叫什么 | `datasetName` |
| 数据集 ID | `datasetId` |
| 数据集类型 | `datasetType` |
| 创建时间 | `createdAt` |
| 状态 | `status` |
| 绑定的桶 / 关联存储桶 | `bindingBucket` |
| MetaInsight 数据集 | `datasetType = MetaInsight`；名称来自查询结果、用户输入或 `TENCENT_COS_DATASET_NAME` |
| 数据集字段 / 有哪些字段 | 走 `describeDatasetFields`，列 `fieldName,fieldType,fieldRequired` |

## 四、类型别名（用户说"某类"时展开）

| 用户说 | 展开为 columns |
| --- | --- |
| 基础信息 | `datasetName,datasetId,datasetType,createdAt,status` |
| 全部信息 | 以上所有维度 |

## 五、数据集绑定关系（来自 DescribeDatasetBindings）

查询某数据集与 COS Bucket 的绑定关系列表。`GET /datasetbindings`，挂账号级 CI 域名 `<AppId>.ci.<Region>.myqcloud.com`，无请求体，返回 JSON。授权 action：`ci:DescribeDatasetBindings`。

由 `scripts/ci_api.mjs list-bindings --appid <AppId> --region <region> --dataset-name <d> [--maxresults N] [--nexttoken <token>]` 执行。

### 请求参数（query）

| 参数 | CLI flag | 必选 | 说明 |
| --- | --- | --- | --- |
| `datasetname` | `--dataset-name` | 是 | 数据集名称（账户内唯一） |
| `maxresults` | `--maxresults` | 否 | 返回条数上限 0~200，默认 100 |
| `nexttoken` | `--nexttoken` | 否 | 翻页 token，首次为空；结果中 `NextToken` 非空表示还有下一页 |

### 响应字段

顶层：`Bindings[]`（绑定关系列表）、`NextToken`（翻页 token，仅未全部返回时有值）、`RequestId`。

| Bindings 内字段 | 说明 |
| --- | --- |
| `DatasetName` | 数据集名称 |
| `URI` | 绑定资源，形如 `cos://<BucketName>` |
| `State` | 绑定关系状态，`Running`=运行中 |
| `StockState` | 存量索引状态：`NoIndexing`/`Indexing`/`Success` |
| `CreateTime` | 创建时间戳（RFC3339Nano） |
| `UpdateTime` | 修改时间戳（RFC3339Nano），未变更时与 `CreateTime` 相同 |

## 六、媒资 AI 信息查询（GetAIMediaInfo）

按 URI 拉取**已加入智能检索，并在 `ImageSearch` / `VideoSearch` 数据集中完成入库的单个媒资**（图片 / 视频）的 AI 分析详情：AI 标签、语音识别（ASR）、字幕识别（OCR）、粗分类与整体描述等。普通 COS 文件、尚未入库的文件和 `DocSearch` 数据集文件不能使用本接口。区别于「检索」（找相似文件），本接口是**按 URI 拉取单文件的 AI 详情**，用于详情页展示标签 / 台词字幕、二次筛选、AI 标签回写。图片与视频**共用同一接口**，返回结构不同（视频更丰富）。

`POST /datasetquery/getaimediainfo`，挂桶 CI 域名 `<bucket>.ci.<region>.myqcloud.com`，`Content-Type / Accept: application/json`。

由 `scripts/ci_api.mjs get-ai-media-info --bucket <b> --region <r> --dataset-name <d> --uri <cos://file> [--body '<json>']` 执行。

### 请求体

| 字段 | CLI flag | 必选 | 说明 |
| --- | --- | --- | --- |
| `URI` | `--uri` | 是 | 目标媒资完整 `cos://` 路径（图片或视频） |
| `DatasetName` | `--dataset-name` | 是 | 该媒资所属数据集 |

> 也可用 `--body '<json>'` 完全覆盖自动拼装的请求体。

### 响应字段

顶层：`MediaInfo`、`RequestId`。`MediaInfo` 结构：

| MediaInfo 内字段 | 说明 |
| --- | --- |
| `URI` | 媒资地址 |
| `CosTagging` / `CustomLabels` / `CosUserMeta` | COS 标签 / 自定义标签 / 自定义头部（可作筛选项） |
| `ModifiedTime` | 修改时间 |
| `FileInfo` | `{ FileBasicInfo, AiData }` |

`FileInfo.FileBasicInfo`：`FileName`/`FileSize`/`FileUrl`/`Region`/`ModifiedTime`（图片视频通用）；`FormatName`/`Duration`/`Bitrate`/`Width`/`Height`（视频特有，图片为 0/空）。

`FileInfo.AiData`：

| 字段 | 图片 | 视频 | 说明 |
| --- | --- | --- | --- |
| `AiLabelInfo[]` | ✅ | ✅ | AI 标签；视频每项带 `From/To/Timestamp`（片段秒），图片无时间维度 |
| `AsrInfo[]` | ❌ | ✅ | 语音识别：`{From,To,ClipId,Content,Timestamp}` |
| `OcrInfo[]` | ✅ | ✅ | 文字识别。视频：`{From,To,ClipId,Content,BoxPosition,Score,Timestamp}`；图片：`{Content,BoxPosition,Score}`（无时间维度） |
| `AiRoughData` | ❌ | ✅ | 粗分类 + **整体描述**：`{ AiCategory, Description }`；`Description` 为视频整体自然语言描述（图片为 `null`） |
| `FaceInfo[]` | 视情况 | 视情况 | 人脸信息（需开白）；视频按人物聚合，`OccurrencesInfos` 给出多段时间片段，图片 `TrackData` 直接挂在人物元素下 |

`AiLabelInfo[].LabelDetail[]`：`LabelInfos`（map，如 `{first_label,second_label,third_label}` 或 `{Type,Category,Name}`，随模板而定）、`Confidence`（`high`/`medium`/…）。

**整体描述 vs 片段描述**：

- **整体描述**取 `AiRoughData.Description`（仅视频），一句话概括整个视频讲了什么，回答"这个视频讲了什么"时优先用它。
- **片段描述**没有单独字段，由视频的片段级数据拼装：`AiLabelInfo` / `AsrInfo` / `OcrInfo` 都带 `From`/`To`/`Timestamp`，`AsrInfo`/`OcrInfo` 额外带 `ClipId`。按 `ClipId` 聚合同一片段的 ASR 与 OCR，或按 `From`~`To` 时间窗归并，即可得到"第 X 秒到第 Y 秒出现了什么、说了什么、画面上有什么字"。`FaceInfo[].OccurrencesInfos` 同理，给出某人物的多段出现时间。
- 图片没有时间维度，因此没有片段描述；只有标签、OCR 文字和人脸信息。

> 各字段仅在媒资存在对应分析结果时返回；缺字段说明该维度未分析或未产出结果，不要编造。

> 前置：目标文件必须已加入智能检索，并在 `ImageSearch` / `VideoSearch` 数据集中完成入库。仅存在数据集或仅知道文件 URI 不代表文件已入库；未入库、未分析完成或属于 `DocSearch` 时不要调用。

## 七、图片理解（AIImageAnalysis · 大模型图片分析）

**无需数据集**，直接对**桶内单张图片**做大模型理解。区别于前几节的数据集检索 / 媒资详情，本接口是 COS 桶级 `ci-process`，适合"没有可用 MetaInsight 数据集、但想让模型看懂某张图片"的兜底方案（方案二）。

`GET /<ObjectKey>?ci-process=AIImageAnalysis&...`，挂**桶 COS 域名** `<bucket>.cos.<region>.myqcloud.com`，同步返回 **XML**（本工具已解析为 JSON）。

由 `scripts/ci_api.mjs image-analysis --bucket <b> --region <r> (--uri <cos://key> | --object <ObjectKey> | --detect-url <url>) [--type ImageLabels|Custom] [--label-scenes General] [--prompt <p>] [--ai-model <m>]` 执行。

### 请求参数（query）

| 参数 | CLI flag | 必选 | 说明 |
| --- | --- | --- | --- |
| `ci-process` | （固定） | 是 | 固定 `AIImageAnalysis` |
| 目标图片 | `--uri` / `--object` / `--detect-url` | 三选一 | `--uri cos://bucket/key` 或 `--object <ObjectKey>`（桶内对象）；`--detect-url` 传公网图片 URL |
| `type` | `--type` | 否 | `ImageLabels`（默认，图片打标）\| `Custom`（自定义 prompt 提问） |
| `label-scenes` | `--label-scenes` | 否 | 仅 `ImageLabels`：标签场景，默认 `General` |
| `prompt` | `--prompt` | Custom 必填 | 自定义提问（≤1024 字符），工具自动做 URL 安全 Base64 |
| `ai-model` | `--ai-model` | 否 | 指定底层模型（不传用默认） |

### 响应字段

顶层：`AnalysisResult{ Type, ... }` + `RequestId`（工具解析后放在 `data`）。

**`type=ImageLabels`**（`data` 内）：

| 字段 | 说明 |
| --- | --- |
| `type` | `ImageLabels` |
| `description` | 图片整体自然语言描述 |
| `labelDetails[]` | 每个检测项一组：`{ labelInfos, confidence }` |
| `labelDetails[].labelInfos` | 分层标签 map，如 `{first_label:"风景", second_label:"城市", third_label:"树影天空"}` |
| `labelDetails[].confidence` | 置信度 `high`/`medium`/… |
| `labels[]` | 扁平化标签 `{ name, value, confidence }`，便于直接遍历 |

> XML 真实结构：`ImageLabelsResult` 下 `Description` + 多个 `LabelDetail`；每个 `LabelDetail` = 1 个 `Confidence` + 多个 `LabelInfos`（每个 `LabelInfos` 直接含小写标签 `labelName`/`labelValue`）。

**`type=Custom`**（`data.custom` 内）：

| 字段 | 说明 |
| --- | --- |
| `custom.outputBase64` | 接口原始返回（`CustomOutput`，Base64） |
| `custom.output` | 工具已 Base64 解码后的分析文本（直接可用） |

> 前置：需桶所在地域开通数据万象并启用图像大模型分析能力；对象须为可访问的图片。

## 八、图片 EXIF 信息（EXIF · 基础图片处理）

**无需数据集**，读取**桶内单张图片**的 EXIF 元数据（拍摄参数 / 时间 / 相机型号 / GPS 等）。同为 COS 桶级图片处理能力，是「方案二」拿图片客观元信息（而非语义理解）的手段。

`GET /<ObjectKey>?exif`，挂**桶 COS 域名** `<bucket>.cos.<region>.myqcloud.com`，同步返回 **JSON**（每字段形如 `{"val":"..."}`）。

由 `scripts/ci_api.mjs image-exif --bucket <b> --region <r> (--uri <cos://key> | --object <ObjectKey>)` 执行。

### 请求参数（query）

| 参数 | CLI flag | 必选 | 说明 |
| --- | --- | --- | --- |
| `exif` | （固定子资源） | 是 | 固定 `?exif`（无值） |
| 目标图片 | `--uri` / `--object` | 二选一 | `--uri cos://bucket/key` 或 `--object <ObjectKey>`（桶内对象） |

支持格式：JPG / PNG / BMP / WebP / TIFF / AVIF / HEIF。

### 响应字段

接口原始返回是 `{ Field: { "val": "..." } }` 的扁平 JSON；本工具处理为：

| 字段 | 说明 |
| --- | --- |
| `data.exif` | 摊平后的便捷 map：`Field -> 值`（直接取用，如 `data.exif.Make`、`data.exif.DateTimeOriginal`） |
| `data.raw` | 接口原始结构（保留 `{val}` 包裹，便于溯源） |

常见字段：`Make`/`Model`（相机厂商 / 型号）、`DateTimeOriginal`（拍摄时间）、`ExposureTime`/`FNumber`/`ISOSpeedRatings`/`FocalLength`（曝光参数）、`GPSLatitude`/`GPSLongitude`（经纬度）、`ImageWidth`/`ImageLength`（尺寸）等。

> 无 EXIF 信息时，接口返回 `{"error":"no exif data"}`；本工具归一化为 `ok:false` + `error.code=NoExifData`。
> 前置：对象须为桶内可访问的图片；无需开通任何 AI 能力。
