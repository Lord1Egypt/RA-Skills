# MCP 工具 API 参考

> Unified Memory 所有 MCP 工具的完整参考。基于 `src/index.js` v1.1.0。

## 目录

- [核心工具](#核心工具) — Search、Store、List、Delete
- [Prompt 组合](#prompt-组合) — memory_compose
- [v4.0 存储网关](#v40-存储网关) — memory_v4_*
- [高级工具](#高级工具) — Export、Dedup、Decay、QA
- [偏好与画像](#偏好与画像) — memory_preference、memory_profile
- [版本控制](#版本控制) — memory_version
- [搜索引擎](#搜索引擎) — memory_engine、memory_qmd
- [分层管理](#分层管理) — memory_tier
- [系统工具](#系统工具) — Stats、Health、Metrics、WAL

---

## 核心工具

### memory_search

使用 BM25 + 向量 + RRF 融合的混合搜索。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `query` | `string` | *必填* | 搜索查询文本 |
| `topK` | `number` | `5` | 返回结果数量 |
| `mode` | `"hybrid" \| "bm25" \| "vector"` | `"hybrid"` | 搜索模式 |
| `scope` | `string` | `null` | 范围过滤：`AGENT`、`USER`、`TEAM`、`GLOBAL` |

**示例：**
```json
{
  "query": "用户偏好的编程语言",
  "topK": 5,
  "mode": "hybrid",
  "scope": "USER"
}
```

**返回：**
```json
{
  "count": 3,
  "query": "用户偏好的编程语言",
  "mode": "hybrid",
  "results": [
    {
      "id": "mem_xxx",
      "text": "用户偏好用 Python 做数据工作",
      "category": "preference",
      "importance": 0.85,
      "score": 0.923,
      "created_at": "2026-04-15T10:00:00Z"
    }
  ],
  "token_budget": {
    "used_tokens": 1200,
    "max_tokens": 2000,
    "remaining_tokens": 800,
    "percent_used": 60.0
  }
}
```

---

### memory_store

存储新记忆。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `text` | `string` | *必填* | 记忆内容 |
| `category` | `string` | `"general"` | 类别：`preference`、`fact`、`decision`、`entity`、`reflection` |
| `importance` | `number` | `0.5` | 重要性评分 0–1 |
| `tags` | `string[]` | `[]` | 标签 |
| `scope` | `string` | `null` | 范围：`AGENT`、`USER`、`TEAM`、`GLOBAL` |
| `source` | `string` | `"manual"` | 来源：`manual`、`auto`、`extraction` |

**自动抽取：** 当 `category="general"` 且 `importance > 0.7` 时，自动抽取结构化事实。

---

### memory_list

列出所有已存储的记忆及其元数据。

**参数：** 无

---

### memory_delete

根据 ID 删除记忆。已写入 WAL 和 transcript 日志。

**参数：**

| 参数 | 类型 | 描述 |
|------|------|------|
| `id` | `string` | 要删除的记忆 ID |

---

## Prompt 组合

### memory_compose

为 prompt 注入组合记忆上下文块。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `messages` | `object[]` | `[]` | 对话消息 `{role, content}` |
| `targetTokens` | `number` | `2000` | 目标 token 预算 |
| `categories` | `string[]` | `[]` | 按类别过滤 |
| `query` | `string` | `null` | 偏置记忆选择的搜索查询 |
| `messageWindow` | `number` | `10` | 包含的最近消息数 |

**优先级顺序：** PIN → HOT → WARM → COLD

---

## 高级工具

### memory_export

导出记忆为 JSON、Markdown 或 CSV 格式。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `format` | `"json" \| "markdown" \| "csv"` | `"json"` | 导出格式 |
| `output` | `string` | `null` | 输出文件路径 |
| `category` | `string` | `null` | 按类别过滤 |
| `minImportance` | `number` | `null` | 最低重要性阈值 |

---

### memory_dedup

检测并合并重复记忆。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `threshold` | `number` | `0.85` | 相似度阈值 0–1 |
| `dryRun` | `boolean` | `true` | 为 true 时仅预览 |

---

### memory_qa

基于相关记忆回答问题（RAG）。

| 参数 | 类型 | 描述 |
|------|------|------|
| `question` | `string` | 要回答的问题 |

---

### memory_profile

获取具有静态/动态分离的用户画像。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `scope` | `string` | `"user"` | 范围：`agent`、`user`、`team`、`global` |
| `container_tag` | `string` | `null` | 项目/泳道标签 |
| `entity_filter` | `string` | `null` | 聚焦特定实体 |
| `static_days` | `number` | `30` | 天数无访问则标记为静态 |
| `limit` | `number` | `100` | 最大分析记忆数 |

---

## 偏好与画像

### memory_preference

统一偏好管理。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `get`、`set`、`update`、`merge`、`delete`、`reset`、`stats`、`explain`、`infer` |
| `key` | `string` | 槽位键（用于 get/set/update/delete/explain） |
| `value` | `any` | 槽位值（用于 set/update） |
| `confidence` | `number` | 置信度 0–1 |
| `source` | `string` | `explicit`、`inferred`、`historical` |
| `slots` | `object` | 键值映射（用于 merge） |
| `messageCount` | `number` | `20` — infer 用消息数 |

---

## 版本控制

### memory_version

记忆版本控制。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `list`、`diff`、`restore` |
| `memoryId` | `string` | 记忆 ID（用于 diff/restore） |
| `versionId` | `string` | 版本 ID（用于 diff/restore） |
| `versionId1` | `string` | 第一个版本（用于 diff） |
| `versionId2` | `string` | 第二个版本（用于 diff） |
| `limit` | `number` | `10` — 最大版本数（用于 list） |
| `preview` | `boolean` | `false` — 不还原仅预览 |

---

## 搜索引擎

### memory_engine

统一搜索引擎。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `bm25`、`embed`、`search`、`mmr`、`rerank`、`qmd` |
| `query` | `string` | 查询字符串 |
| `text` | `string` | 要嵌入的文本 |
| `documents` | `object[]` | 用于 mmr/rerank 的文档 |
| `topK` | `number` | `10` — 结果数量 |
| `build` | `boolean` | `false` — 重建 BM25 索引 |
| `lambda` | `number` | `0.5` — MMR 平衡参数 |
| `method` | `enum` | `keyword`、`llm`、`cross`（用于 rerank） |

### memory_qmd

QMD 本地文件搜索。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `search`、`get`、`vsearch`、`list`、`status` |
| `query` | `string` | 搜索查询 |
| `path` | `string` | 文件路径（用于 get） |
| `mode` | `enum` | `bm25`、`vector`、`hybrid`、`auto` |

---

## 分层管理

### memory_tier

HOT/WARM/COLD 分层管理。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `status`、`migrate`、`compress`、`assign`、`partition`、`redistribute` |
| `apply` | `boolean` | `false` — 应用更改 |
| `memories` | `object[]` | 记忆（用于 assign/partition/compress） |

**分层阈值：**
- HOT：≤ 7 天
- WARM：7–30 天
- COLD：> 30 天

---

## 系统工具

### memory_stats

记忆系统统计。

**参数：** 无

返回：总数、分类、标签、分层分布、范围分布、质量分布。

---

### memory_health

MCP 服务器和依赖的健康检查。

**参数：** 无

返回：Ollama 状态、WAL 完整性、向量缓存完整率、分层分布、陈旧记忆。

---

### memory_metrics

操作指标：搜索延迟、存储计数、错误率。

**参数：** 无

---

### memory_wal

预写日志操作。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `init`、`flush`、`list` |
| `runId` | `string` | 运行 ID（用于 init） |

---

### memory_pin / memory_unpin / memory_pins

固定（锁定）记忆，使其永不压缩或去重。

---

## v4.0 存储网关

完整 `memory_v4_*` 工具文档请参见 [v4 API 参考](./v4.md)。

---

## 错误响应

所有工具在出错时返回带 `isError: true` 的错误响应：

```json
{
  "content": [{ "type": "text", "text": "Search error: connection timeout" }],
  "isError": true
}
```
