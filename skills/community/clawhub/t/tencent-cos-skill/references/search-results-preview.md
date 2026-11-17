# 检索结果可视化预览（preview_gen.mjs + exportFile + iframe artifact）

> 适用：**数据集检索**（`simple-query` / `image-search` / `doc-search` / `video-search` / `face-search` / `face-clip-search`）与**存储桶文件查找**（`GetBucket` / `cos_node.mjs list`）。
> 目标：除文字结论外，**额外产出一个可交互的 HTML 预览卡片**，展示命中文件缩略图墙，点击图片新标签打开源文件。
> 支持类型：**图片 / 视频 / 文档 / 音频**（视频用数据万象截帧作封面，文档用首页预览图）。

---

## 一、总流程（两步，务必走脚本）

```
① 执行检索 → 拿命中文件 URI 列表
② node scripts/preview_gen.mjs --spec-file <spec.json> --out <out.html>
      ↳ 脚本内部一次性完成：本地批量签名 + 视频截帧地址 + 文档首页图 + 填充模板 + 落盘 HTML
③ 用 sandbox-export 的 exportFile 导出该 HTML → 取 artifactId
④ 输出预览标记
```

```
[iframe:artifact|{artifactId}|maxWidth=720|maxHeight=186|title=检索结果]
```

> ⛔ **不要手写 HTML、不要逐个调用 `sign-url`**。手工拼装是本场景最主要的耗时来源（模型逐字输出上百行 HTML + N 次子进程签名）。`preview_gen.mjs` 把这些压成一次调用：签名是**本地纯计算、零网络请求**，几十个文件也是毫秒级。

---

## 二、固化入参 Spec（唯一需要模型产出的内容）

模型**只需产出这份极简 JSON**，其余全部由脚本补全（签名地址、缩略图地址、类型推断、文件名、角标、模板填充）。

```json
{
  "bucket": "example-1250000000",
  "region": "ap-guangzhou",
  "query": "海边日落",
  "datasetName": "example-dataset",
  "tool": "image-search",
  "total": 42,
  "expires": 3600,
  "items": [                          // 必填：命中文件，建议 <=20
    { "uri":"cos://b/a.jpg" },                              // 最简：只给 uri，类型由后缀推断
    { "uri":"cos://b/v.mp4", "from":12.5, "to":18.2 },       // 视频：命中片段，封面自动截 from 那刻
    { "uri":"cos://b/d.pdf", "text":"命中片段…", "page":3 },  // 文档：缩略图渲染第 3 页
    { "uri":"cos://b/t.xlsx", "sheet":2, "excelPaperDirection":1 }, // 表格：第 2 张表、横向
    { "uri":"cos://b/noext", "srcType":"docx" }              // 无后缀对象：必须给 srcType
  ]
}
```

### 字段说明

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `region` | ✅ | 桶地域 |
| `items[]` | ✅ | 命中文件，**建议 ≤20**；每项最简只需 `uri`（`cos://bucket/key`），也可直接写字符串 |
| `bucket` | ⭕ | `items[].uri` 已含桶名时可省略 |
| `query` | ⭕ | 说明行展示的检索条件，**填用户原话**（如 `海边日落`、`大于 1MB 的 JPEG`、`前缀 album/`），不要填内部 JSON |
| `datasetName` | ⭕ | 无数据集（`GetBucket` 直接列举）时**省略**，说明行会自动不显示该项 |
| `tool` | ⭕ | 实际执行的命令名 |
| `total` | ⭕ | 命中**总数**（可大于展示数），标题显示「共 N 个文件」；缺省取 `items.length` |
| `expires` | ⭕ | 签名有效期秒，默认 3600 |

### items[] 可选字段（按检索类型补）

| 字段 | 适用 | 作用 |
| --- | --- | --- |
| `from` / `to` | `video-search` | 命中片段起止秒；**截帧封面自动取 `from` 那一刻**，角标显示 `0:12` |
| `snapshotTime` | 视频 | 显式指定截帧秒（优先于 `from`），默认第 1 秒 |
| `text` / `page` | `doc-search` | 命中文本片段与页码；**文档缩略图自动渲染该 `page`**，角标显示 `P.3` |
| `srcType` | 文档 | 源文件后缀。**对象无后缀名时必填**，否则 `doc-preview` 无法识别格式（给了也会据此判定为文档类型） |
| `sheet` | 表格（xlsx/xls/csv/et…） | 渲染第几张表，默认 1 |
| `excelPaperDirection` | 表格 | 纸张方向 `0` 垂直（默认）/ `1` 水平；**列很多的表建议填 1** |
| `password` | 加密 Office 文档 | 打开密码，不填会渲染失败 |
| `comment` | Word 等 | `0` 隐藏批注（默认）/ `1` 显示批注和修订 |
| `dstType` | 文档 | 缩略图输出格式 `jpg`（默认）/ `png` |
| `imageParams` | 文档 | 自定义 `ImageParams`（imageMogr2 / watermark 管道），给了则忽略默认宽度设置 |
| `faceId` | `face-search` | 人脸 ID，顶部 chip 展示 |
| `type` | 全部 | 显式指定 `image` / `video` / `doc` / `audio`；**默认按扩展名自动推断，通常无需填** |
| `name` | 全部 | 图下展示名，默认取 URI 文件名 |
| `label` | 全部 | 自定义角标文字 |

---

## 三、调用方式（三选一）

```bash
# 推荐：写到临时文件再传，避免 shell 转义问题
node scripts/preview_gen.mjs --spec-file /tmp/spec.json --out /tmp/search-results.html

# 直接传 JSON 字符串
node scripts/preview_gen.mjs --spec '{"region":"ap-guangzhou","items":[{"uri":"cos://b-125/a.jpg"}]}' --out /tmp/search-results.html

# 从 stdin 读
cat /tmp/spec.json | node scripts/preview_gen.mjs --out /tmp/search-results.html
```

成功返回（stdout JSON）：

```json
{
  "ok": true,
  "htmlPath": "/tmp/search-results.html",
  "bytes": 16675,
  "fileCount": 3,
  "total": 42,
  "typeStats": { "image": 1, "video": 1, "doc": 1, "audio": 0, "other": 0, "signed": 3 },
  "expiresIn": 3600,
  "nextStep": "用 sandbox-export 的 exportFile 导出该 HTML，取 artifactId 后输出：[iframe:artifact|{artifactId}|maxWidth=720|maxHeight=186|title=检索结果]"
}
```

失败返回 `{ ok:false, error:{ code, message } }`，常见 code：`MissingRegion` / `MissingItems` / `BadSpecJson` / `EmptyItems` / `MissingCredentials`。

---

## 四、不同检索类型的缩略图策略（脚本自动处理）

| 类型 | 缩略图来源 | 角标 |
| --- | --- | --- |
| **图片** | 源文件签名地址直接展示 | 无 / 自定义 |
| **视频** | 数据万象截帧 `?ci-process=snapshot&time=<from或1>&format=jpg&width=240` | 命中时间点 `0:12` + ▶ 播放角标 |
| **文档** | 文档转码同步请求 `?ci-process=doc-preview&page=<page或1>&dstType=jpg&ImageParams=imageMogr2/thumbnail/240x` | 页码 `P.3` |
| **音频 / 其他** | 无缩略图，走 🎵 / 📦 类型占位图标 | 类型文案 |

### 文档预览细则（doc-preview）

依据官方文档 [436/121090 文档转码同步请求](https://cloud.tencent.com/document/product/436/121090)：

- **无 `width` / `height` 参数** —— 缩略图宽度只能通过 `ImageParams=imageMogr2/thumbnail/240x` 控制（脚本已默认这么拼）；也可用 `scale`（10~200）或 `imageDpi`（96~600）调清晰度。
- **每次请求只返回一页** —— 缩略图取 `page` 指定的那一页（`doc-search` 直接把命中 `TextPage` 填进 `page` 即可），默认第 1 页。
- **支持格式广** —— 演示（ppt/pptx/dps…）、文字（doc/docx/wps…）、表格（xls/xlsx/csv/et…）、其他（pdf/txt/rtf/xml/html 及 c/cpp/java 等代码文本）。脚本内置完整清单做类型推断。
- **表格类** —— 用 `sheet` 指定第几张表；列很多时加 `excelPaperDirection: 1` 横向输出（转换逻辑等同"本地打印"，方向不对会被压扁）。
- **无后缀对象必须给 `srcType`** —— 否则接口无法判断源格式。脚本会检测并在返回值的 `warnings[]` 中提示；给了 `srcType` 也会据此把该项判为文档类型。
- **加密文档** —— 必须带 `password`，否则渲染失败。
- **前置条件** —— 桶需已绑定数据万象并开通**文档处理服务**；子账号策略需含 `cos:GetObject` + `cos:HeadObject`；该接口**按次计费**（文档处理费 + 流量费）。
- **同步接口限制** —— 10 秒超时、建议 100 页以内、输入 ≤200MB。仅用于生成缩略图足够；大文档批量转码应走异步任务。

> 视频截帧 / 文档预览需桶已开通对应数据万象能力。**取图失败会自动降级为类型占位图标**（模板内置 `onerror` 兜底），不会出现破图，因此无需预先探测能力是否开通。

---

## 五、导出与输出

1. 把 `htmlPath` 指向的 HTML 通过宿主环境 **sandbox-export 技能的 `exportFile`** 导出（文件名建议 `search-results.html`，MIME `text/html`）。
2. 取返回的 **`artifactId`**。
3. 输出预览标记，**参数严格照抄**：

```
[iframe:artifact|{artifactId}|maxWidth=720|maxHeight=186|title=检索结果]
```

- `maxHeight=186` 对应「说明行 + 一排缩略图」的紧凑高度，**不要随意调大**。
- `{artifactId}` 必须是 `exportFile` 实际返回值，不得编造或留占位符。
- 脚本报错或 `exportFile` 失败 → **降级为纯文字结果**（照常输出各条 URI），简要说明预览生成失败，不要输出残缺标记。

---

## 六、触发与不触发

**必须生成预览**（命中文件含可视资源）：
- 场景三 `simple-query` 返回文件列表（非纯聚合）
- 场景四 全部语义检索（含 `video-search` 视频检索、`doc-search` 文档检索）
- 场景一 `GetBucket` / `cos_node.mjs list` 列举出的文件
- 场景六 内容总结采样出的文件（预览 + 文字总结并存）

**不生成预览**：
- 纯聚合统计（场景七，无文件列表）
- 数据集信息 / 绑定关系查询（场景二）
- 命中 0 条
- 单文件 AI 详情 / EXIF / 图片理解（结果是元信息而非文件集合）

> 预览是**文字结论的补充而非替代**。仍须遵守「结果输出规范」：把每条命中结果的原始 `URI` 原样输出给用户。

---

## 七、完整示例（视频检索）

**用户**：「在 example-dataset 里找有骑行画面的视频」

```bash
# ① 检索
node scripts/ci_api.mjs video-search --bucket example-1250000000 --region ap-guangzhou \
  --dataset-name example-dataset --mode text --text "骑行" --limit 10

# ② 按命中结果写 spec（把每条 URI 与 From/To 填进 items），一条命令生成 HTML
node scripts/preview_gen.mjs --spec-file /tmp/spec.json --out /tmp/search-results.html
```

`/tmp/spec.json`：

```json
{
  "bucket": "example-1250000000",
  "region": "ap-guangzhou",
  "datasetName": "example-dataset",
  "tool": "video-search",
  "query": "骑行",
  "total": 6,
  "items": [
    { "uri": "cos://example-1250000000/v/ride_01.mp4", "from": 12.5, "to": 18.2 },
    { "uri": "cos://example-1250000000/v/ride_02.mp4", "from": 45.0, "to": 52.3 }
  ]
}
```

③ `exportFile` 导出拿到 `artifactId`，回复：

```
在 example-dataset 里找到 6 个含骑行画面的视频片段：

1. cos://example-1250000000/v/ride_01.mp4（00:12 - 00:18）
2. cos://example-1250000000/v/ride_02.mp4（00:45 - 00:52）
...

[iframe:artifact|art_xxxxxxxx|maxWidth=720|maxHeight=186|title=检索结果]
```

### 文档检索示例

**用户**：「找包含财务数据的文档」

```bash
# ① 检索 → data.DocResult[]{URI, Text, TextPage, Score}
node scripts/ci_api.mjs doc-search --bucket example-1250000000 --region ap-guangzhou \
  --dataset-name example-dataset --text "包含财务数据的文档" --limit 5

# ② 把 URI / Text / TextPage 填进 items，一条命令生成 HTML
node scripts/preview_gen.mjs --spec-file /tmp/spec.json --out /tmp/search-results.html
```

`/tmp/spec.json`（`page` 用命中的 `TextPage`，缩略图就渲染命中那一页）：

```json
{
  "bucket": "example-1250000000",
  "region": "ap-guangzhou",
  "datasetName": "example-dataset",
  "tool": "doc-search",
  "query": "包含财务数据的文档",
  "total": 5,
  "items": [
    { "uri": "cos://example-1250000000/docs/report.pdf", "text": "2025 年财务数据汇总…", "page": 3 },
    { "uri": "cos://example-1250000000/docs/plan.pptx", "page": 7 },
    { "uri": "cos://example-1250000000/docs/budget.xlsx", "sheet": 2, "excelPaperDirection": 1 }
  ]
}
```

生成的文档缩略图地址形如：

```
https://example-1250000000.cos.ap-guangzhou.myqcloud.com/docs/report.pdf
  ?ci-process=doc-preview&page=0&dstType=jpg
  &ImageParams=imageMogr2/thumbnail/240x
  &q-sign-algorithm=sha1&...&q-signature=...
```

---

## 八、性能要点（为什么快）

| 环节 | 旧做法 | 现做法 |
| --- | --- | --- |
| 签名 | 每个文件跑一次 `cos_node.mjs sign-url` 子进程（N 次进程启动 + SDK 加载） | `lib/presign.mjs` **本地 HMAC 计算**，一次进程内批量完成，零网络 |
| 视频封面 | 需先跑 `media-snapshot` 异步作业、等结果、再签名 | 直接拼 `?ci-process=snapshot` **实时处理地址**，无需建作业 |
| 文档封面 | 需跑文档转 PDF / 预览异步任务、轮询、再取图 | 直接拼 `?ci-process=doc-preview` **同步转码地址**，无需建作业 |
| HTML 生成 | 模型逐字输出上百行 HTML（最大耗时项，且易出错） | 模型只产出 ~10 行 spec JSON，脚本读模板做**一次正则替换** |
| 模板一致性 | 手写易漏样式 / 破坏结构 | 模板文件唯一来源，样式不可能被改坏 |
