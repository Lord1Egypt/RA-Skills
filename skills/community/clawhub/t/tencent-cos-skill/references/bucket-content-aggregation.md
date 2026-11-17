# 场景 SOP：桶文件内容聚合分析（基于数据集）

> 本文件是 SKILL「场景七：桶文件内容聚合分析」的完整执行流程（SOP），从主 SKILL 抽出以减少干扰。
> 触发场景：用户说「按文件类型统计数量」「各标签分别有多少」「这批文件总大小 / 平均大小」「有多少种 ContentType」「存储类型分布」等**统计 / 聚合**类需求。
> 前提：目标桶 / 目录已**绑定数据集**（聚合走数据集的 `simple-query` 接口，不依赖具体检索模板）。

## 机制概述

聚合分析用 `simple-query` 接口（`POST /datasetquery/simple`）的 **`Aggregations`** 参数完成，无需逐个拉文件。

```bash
node scripts/ci_api.mjs simple-query --bucket <b> --region <r> --body '<json>'
```

请求体里 `Aggregations` 是一个数组，每项 `{ "Field": "<聚合字段>", "Operation": "<聚合操作>" }`，可同时下发多项。可选配合 `Query`（先过滤再聚合）与 `MaxResults`（聚合结果上限，最多 2000 条）。

> ⚠️ **聚合与文件列表互斥**：请求含 `Aggregations` 时，响应只返回聚合结果，不返回 `Files` 列表。

## 支持的聚合字段与操作符（权威来源）

字段与操作符的**支持列表以 `references/dataset-simple-query.md` 第二部分为准**，对应官方文档：
- 聚合参数与 simple-query 请求结构：[DatasetSimpleQuery](https://cloud.tencent.com/document/product/436/113309)
- 字段与操作符支持列表：[460/106154](https://cloud.tencent.com/document/product/460/106154)

聚合操作符：

| 操作符 | 含义 | 自然语言关键词 |
| --- | --- | --- |
| `group` | 按值分组计数（降序） | "按…分组""各类别分别统计""分布" |
| `count` | 计数 | "多少个""数量""统计个数" |
| `distinct` | 去重计数（**近似值**，大数据量有误差） | "有多少种""不重复的" |
| `sum` | 求和 | "总和""合计""一共多大" |
| `average` | 平均值 | "平均""均值" |
| `max` / `min` | 最大 / 最小值 | "最大""最小" |

字段支持范围（关键约束）：

- **仅 `Size`、`COSTaggingCount` 两个 Int 字段** 支持数值聚合 `sum` / `average` / `max` / `min`（也支持 count/distinct/group）。
- **其余标量字段**（`ContentType` / `MediaType` / `COSStorageClass` / `CreateTime` / `Filename` / `URI` / `ObjectACL` / `ServerSideEncryption` / `CustomId` / `ETag` / `FileModifiedTime` / `UpdateTime` / `ContentEncoding` / `ContentLanguage` / `ContentDisposition` / `COSCRC64` 等）**只支持** `count` / `distinct` / `group`。
- **Container 字段**（`CustomLabels.*` / `COSTagging.*` / `COSUserMeta.*`）**不支持聚合**——若用户想按自定义标签统计，只能对**具体某个 key** 先用 `Query` 过滤，或改用 `CustomId` 之类标量字段。

> 精度提示：`distinct` 去重计数、`group` 分组在数据量大时为近似值（`distinct` 1 亿量级误差约 2%）。给结论时可注明"近似"。

## 典型流程

1. **确认数据集**：遵循 `dataset-catalog.md` 的"数据集名称选择规则"，由显式值、环境默认值和桶绑定关系依次解析。**若没有合适的元数据数据集，引导用户创建**（`create-dataset --template "Official:COSBasicMeta"`）并绑定目标桶、开启存量索引（`Mode=1`），而不是直接失败。
2. **映射聚合维度**：把用户的统计诉求映射到「字段 + 操作符」——校验该字段是否支持该操作（见上表），不支持则告知并给最接近的替代（如"按自定义标签统计"→ 提示 Container 不可聚合，建议改 `CustomId` 或先过滤）。
3. **可选加过滤**：只统计某子集时，用 `Query` 先筛（结构同简单检索）。
4. **产出请求体并执行**：直接输出 JSON 交 `simple-query`，无需长篇解释。
5. **解读结果**：把 `group` 结果整理成"类别→数量"表，`sum/average` 给数值并注明单位（`Size` 为字节，按需换算 MB/GB）。

## 示例

### 例 1：按文件类型分组计数 + 平均大小

> "按文件类型分组统计数量，并算平均大小"

```bash
node scripts/ci_api.mjs simple-query --bucket <b> --region <r> --body '{
  "DatasetName":"example-dataset",
  "Aggregations":[
    {"Field":"MediaType","Operation":"group"},
    {"Field":"Size","Operation":"average"}
  ],
  "MaxResults":100
}'
```

### 例 2：先过滤再聚合（只统计图片的存储类型分布）

> "看看图片文件都存在哪些存储类型，各多少"

```bash
node scripts/ci_api.mjs simple-query --bucket <b> --region <r> --body '{
  "DatasetName":"example-dataset",
  "Query":{"Field":"MediaType","Value":"image","Operation":"eq"},
  "Aggregations":[
    {"Field":"COSStorageClass","Operation":"group"}
  ],
  "MaxResults":100
}'
```

### 例 3：总量与去重种类

> "这个数据集里文件总大小是多少？一共有多少种 ContentType？"

```bash
node scripts/ci_api.mjs simple-query --bucket <b> --region <r> --body '{
  "DatasetName":"example-dataset",
  "Aggregations":[
    {"Field":"Size","Operation":"sum"},
    {"Field":"ContentType","Operation":"distinct"}
  ]
}'
```

## 注意事项

1. **字段/操作符必须查表**：以 `dataset-simple-query.md` 第二部分为准，不臆造；数值聚合只有 `Size`、`COSTaggingCount`。
2. **聚合互斥文件列表**：需要"既统计又列文件"时，分两次请求（一次聚合、一次筛选列表）。
3. **单位换算**：`Size` 单位字节，结果按需换算。
4. **近似值提醒**：`distinct` / `group` 大数据量为近似值。
5. **自定义标签统计受限**：Container 字段不可聚合，按需改用标量字段或先过滤。
