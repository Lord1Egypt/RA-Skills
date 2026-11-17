# 项目列表、正文、结构化数据与附件

## 项目联合身份

后续详情调用统一保存：

```text
projectId = 列表记录的 id
publishTime = 列表记录的 publishTime
```

大多数详情接口需要 `projectId + publishTime`，只保存 ID 会导致详情查询不稳定。

## 职责划分

| 能力 | 接口 | 主要用途 |
| --- | --- | --- |
| 搜索列表 | `searchProjectApi` / `SearchProjectForAI` | 项目发现、分页和摘要展示 |
| 项目编号搜索 | `getProjectByProjectNumber` | 按编号找同项目的多条公告或阶段记录 |
| 正文详情 | `getZTBProjectDetail` | HTML原文、标题、展示字段和附件概要 |
| 官方结构化详情 | `getZTBStructreDetail` | 编号、标段、预算、中标金额、时间、主体、投标企业 |
| 附件列表 | `getZTBProjectFiles` | 下载 URL、文件类型、大小、处理状态 |
| 采集源网址 | `getCollectUrl` | 原始来源跳转兜底 |

## 标准调用链

列表页：

```text
自然语言条件 -> AI重写 -> 普通搜索 -> 摘要列表
```

正文详情页：

```text
列表记录 -> projectId + publishTime -> getZTBProjectDetail -> HTML正文
```

完整项目详情页：

```text
projectId + publishTime
  -> 正文详情
  -> 官方结构化详情
  -> 附件列表
  -> 采集源网址（collectUrl缺失或用户要求时）
```

正文、结构化数据和附件互不依赖时并行调用。结构化详情的 `collectUrl` 优先于独立采集源接口。

## 数据边界

- 列表摘要不是完整内容，不能代替详情接口。
- 正文中的项目金额主要是展示值；结构化 `budgetMoney`、`bidMoney` 是分析值。
- 正文详情的 `projectFiles` 只有概要；需要下载时必须调用附件列表。
- 官方结构化字段与 AI 推断字段必须分开标识。
- HTML 正文保留原始版本，同时可生成清洗版供展示或摘要。

## 项目编号入口

调用 `getProjectByProjectNumber` 后，结果可能包含招标、中标、合同等多个阶段记录。逐条保存 `id + publishTime`，再按照用户要求获取正文或结构化详情，不要只取第一条。
