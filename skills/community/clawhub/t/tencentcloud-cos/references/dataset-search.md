# 数据集智能检索接口映射（Dataset Search）

> 本文件是 `image-search / doc-search / video-search / face-search / face-clip-search` 五个命令的字段映射与请求/响应结构依据。其中 `doc-search` 与 `video-search` 均走 `POST /datasetquery/hybridsearch`（仅 `Templates` 不同：`DocSearch` / `VideoSearch`）；`cos_node.mjs` 另提供统一入口 `hybrid-search --templates <DocSearch|VideoSearch|ImageSearch>` 与专用 `video-search` action。
> 全部挂在桶 CI 域名 `<bucket>.ci.<region>.myqcloud.com`，`Content-Type: application/json`、`Accept: application/json`，
> 由 `scripts/lib/ci_client.mjs` 的 `cosRequest`（COS XML 签名）发出。
> 简单检索（元数据筛选/聚合）见 `references/dataset-simple-query.md`；数据集/字段目录见 `references/dataset-catalog.md`。

## 0. 通用约定

- 任意命令均可用 `--body '<json>'` 完全覆盖自动拼装的请求体（覆盖时 CLI 不再校验单项 flag）。
- 检索类命令统一返回：`{ ok, tool, bucket, region, datasetName, data | error, request }`。
- 前置条件：数据集需绑定对应算子模板并完成入库（建索引）。

| 检索类型 | 数据集模板 | 说明 | 对应 Skill action |
|---|---|---|---|
| 图片检索 | `ImageSearch` | 文搜图 / 图搜图 | `image-search-pic` / `image-search-text`；或 `hybrid-search --templates ImageSearch` |
| 视频检索 | `VideoSearch` | 仅以文搜视频片段（不支持图搜） | `video-search`；或 `hybrid-search --templates VideoSearch` |
| 文档检索 | `DocSearch` | 仅以文搜文档 | `hybrid-search --templates DocSearch`（默认） |
| 人脸检索 | `VideoSearch` / `ImageSearch`（需开白） | 复用图片 / 视频数据集 | `face-search` / `face-clip-search` |

> ⚠️ **模板决定可用接口（重要）**：数据集绑定的 `Templates` 不同，能调用的检索接口也不同——`ImageSearch` 数据集**不能**用 `doc-search`，`DocSearch` 数据集**不能**用 `image-search` / `video-search`。调用前务必先用 `find-datasets-by-bucket` / `list-datasets` 确认目标数据集的模板类型，再选匹配命令；用错模板接口会报错或返回空。
> 另：`get-ai-media-info`（按 URI 拉单文件 AI 详情，见 `dataset-catalog.md` 第六节）**仅支持已加入智能检索，并在 `ImageSearch`、`VideoSearch` 模板数据集中完成入库的目标文件**。仅存在数据集不代表目标文件已入库；`DocSearch` 数据集不支持。

子账号授权 action：`ci:DatasetImageSearch` / `ci:DatasetHybridSearch` / `ci:DatasetFaceSearch` 类。

---

## 1. 图片检索（image-search）

`POST /datasetquery/imagesearch`，`Templates=ImageSearch`。文搜图（`Mode=text`）或图搜图（`Mode=pic`）。

请求体（CLI 拼装）：

```json
{
  "DatasetName": "carsonxu-mi-image",
  "Mode": "text",
  "Templates": "ImageSearch",
  "Text": "海边的日落",
  "SearchText": "海边的日落",
  "Limit": 10,
  "MatchThreshold": 80,
  "Filter": { "Operation": "and", "SubQueries": [] }
}
```

| 字段 | 必选 | CLI flag | 说明 |
|---|---|---|---|
| `DatasetName` | 是 | `--dataset-name` | 数据集名 |
| `Mode` | 否 | `--mode text\|pic` | 默认 `text` |
| `Templates` | 是 | （固定） | `ImageSearch` |
| `Text` / `SearchText` | text 必选 | `--text` | 检索语句 ≤60 UTF-8 字符；两字段同下发以兼容不同网关版本 |
| `URI` / `URIs` / `SearchURIs` | pic 必选 | `--uri`（逗号分隔多个） | 图片 `cos://` URI；三字段同下发以兼容 |
| `Limit` | 否 | `--limit` | 返回条数 (0,100]，默认 10 |
| `MatchThreshold` | 否 | `--match-threshold` | 最低相关度分 (0,100]，推荐 80 |
| `Filter` | 否 | `--filter '<json>'` | 元数据过滤（同简单检索 Query 结构） |

响应：`data.ImageResult[]{ URI, Score }`。

---

## 2. 文档检索（doc-search）

`POST /datasetquery/hybridsearch`，`Templates=DocSearch`、`Mode=text`。**仅支持以文搜文档**，无 pic 模式。

请求体：

```json
{
  "DatasetName": "carsonxu-mi-doc",
  "Mode": "text",
  "Templates": "DocSearch",
  "Text": "包含财务数据的文档",
  "SearchText": "包含财务数据的文档",
  "Limit": 5,
  "MatchThreshold": 80
}
```

字段同图片检索的 text 模式（`--dataset-name` / `--text` / `--limit` / `--match-threshold` / `--filter`）。

响应：`data.DocResult[]{ URI, Score, Text, TextPage, ImageUrls }`。

- `Text` 可能含 `{Image_x}` 占位符。
- `TextPage` 为命中文本所在页码。

> 提示：文档检索腾讯云侧可能处于内测/需开白，且仅支持北京/上海/成都地域。

---

## 3. 视频检索（video-search）

`POST /datasetquery/hybridsearch`，`Templates=VideoSearch`。**仅支持 `Mode=text`（以文搜视频片段），不支持图搜**（`Mode=pic` 不适用）。

请求体（以文搜）：

```json
{
  "DatasetName": "carsonxu-mi-video",
  "Mode": "text",
  "Templates": "VideoSearch",
  "Text": "骑行",
  "SearchText": "骑行",
  "Limit": 10,
  "MatchThreshold": 80
}
```

字段与 flag 同图片检索的 text 模式（`--dataset-name` / `--text` / `--limit` / `--match-threshold` / `--filter`），视频检索仅文搜、无 `--uri`。

响应：`data.VideoResult[]{ URI, Score, From, To }`（`From`/`To` 为命中片段起止秒）。

---

## 4. 人脸粗搜（face-search）

`POST /datasetquery/mediafacesearch`。传外部人脸图，返回库内匹配的 `FaceId` 与命中媒资 URI 列表。

请求体：

```json
{ "DatasetName": "carsonxu-mi-image", "URI": "cos://bucket/face_query.jpg" }
```

| 字段 | 必选 | CLI flag | 说明 |
|---|---|---|---|
| `DatasetName` | 是 | `--dataset-name` | 数据集名 |
| `URI` | 是 | `--uri` | 外部人脸图 `cos://` URI |
| `Limit` | 否 | `--limit` | 返回条数 |
| `MatchThreshold` | 否 | `--match-threshold` | 最低相关度分 |

响应：`data.MediaInfoList[]{ FaceId, UriList }`。

> 限制：最多返回 20 个 `FaceId`，每个 `UriList` 最多 500 个 URI。

---

## 5. 人脸精搜（face-clip-search）

`POST /datasetquery/mediafaceclipsearch`。传粗搜返回的 `FaceId` + 目标媒资 `URI`，定位该人脸在媒资中出现的时间片段与逐帧坐标框。

请求体：

```json
{
  "DatasetName": "your-dataset-001",
  "URI": "cos://bucket/photo_001.jpg",
  "FaceId": "face_20260206_0001"
}
```

| 字段 | 必选 | CLI flag | 说明 |
|---|---|---|---|
| `DatasetName` | 是 | `--dataset-name` | 数据集名 |
| `URI` | 是 | `--uri` | 目标媒资 `cos://` URI |
| `FaceId` | 是 | `--face-id` | 粗搜返回的 FaceId |

响应：`data.MediaClipList[]{ Score, LabelName, Category, OccurrencesInfos[]{ From, To, TrackData[]{ Timestamp, BoxPosition } } }`。

| 字段 | 说明 |
|---|---|
| `Score` | 匹配得分 [0,100] |
| `Category` | `celebrity/sensitive/politician/custom/unknown` |
| `OccurrencesInfos[].From/To` | 出现片段起止秒 |
| `TrackData[].BoxPosition` | 逐帧人脸框（像素 Left/Top/Width/Height） |

### 典型流程

```
外部人脸图 URI ──▶ face-search（粗搜）──▶ FaceId + UriList
                                       │
                     选一个 URI + FaceId ▼
                            face-clip-search（精搜）
                                       ▼
                    该脸在媒资中的时间片段 + 逐帧坐标框
```

---

## 6. 一览对照表

| 命令 | HTTP 端点 | 关键参数 | 输入 | 返回 |
|---|---|---|---|---|
| image-search | `POST /datasetquery/imagesearch` | `Templates=ImageSearch`,`Mode` | 文本 / 图片 URI | `ImageResult[]{URI,Score}` |
| doc-search | `POST /datasetquery/hybridsearch` | `Templates=DocSearch`,`Mode=text` | 文本 | `DocResult[]{URI,Text,TextPage,Score}` |
| video-search | `POST /datasetquery/hybridsearch` | `Templates=VideoSearch`,`Mode` | 文本 / 图片 URI | `VideoResult[]{URI,Score,From,To}` |
| face-search | `POST /datasetquery/mediafacesearch` | `URI,DatasetName` | 外部人脸图 | `MediaInfoList[]{FaceId,UriList}` |
| face-clip-search | `POST /datasetquery/mediafaceclipsearch` | `URI,FaceId` | FaceId+媒资 URI | `MediaClipList[]{From,To,TrackData}` |
