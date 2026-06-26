# MCP 工具参考

> 所有 Unified Memory MCP 工具的完整参考。

## 核心工具

### memory_search

使用 BM25 + 向量 + RRF 融合的混合搜索。

**参数：**

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `query` | `string` | *必填* | 搜索查询文本 |
| `topK` | `number` | `5` | 返回结果数量 |
| `mode` | `string` | `"hybrid"` | 搜索模式：`"hybrid"`, `"bm25"`, `"vector"` |
| `scope` | `string` | `null` | 范围过滤：`"AGENT"`, `"USER"`, `"TEAM"`, `"GLOBAL"` |
| `vectorWeight` | `number` | `0.7` | 混合中向量权重 (0-1) |
| `bm25Weight` | `number` | `0.3` | 混合中 BM25 权重 (0-1) |
| `filters` | `object` | `null` | 元数据过滤器 |

**示例：**
```json
{
  "query": "用户偏好的编程语言",
  "topK": 5,
  "mode": "hybrid",
  "scope": "USER"
}
```

---

### memory_store

存储新记忆。

**参数：**

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `text` | `string` | *必填* | 记忆内容 |
| `category` | `string` | `"general"` | 类别：`"preference"`, `"fact"`, `"decision"`, `"entity"`, `"reflection"` |
| `importance` | `number` | `0.5` | 重要性评分 0-1 |
| `tags` | `string[]` | `[]` | 记忆的标签 |
| `scope` | `string` | `null` | 范围：`"AGENT"`, `"USER"`, `"TEAM"`, `"GLOBAL"` |
| `source` | `string` | `"manual"` | 来源：`"manual"`, `"auto"`, `"extraction"` |
| `metadata` | `object` | `{}` | 自定义元数据 |

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

## 提示组合

### memory_compose

为提示注入组合记忆上下文块。

**参数：**

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `messages` | `object[]` | `[]` | 对话消息 `{role, content}` |
| `targetTokens` | `number` | `2000` | 目标 token 预算 |
| `categories` | `string[]` | `[]` | 按类别过滤 |
| `query` | `string` | `null` | 搜索查询以偏置选择 |
| `messageWindow` | `number` | `10` | 包含的最近消息数 |

**优先级顺序：** PIN → HOT → WARM → COLD

---

## 高级工具

### memory_export

导出记忆为 JSON、Markdown 或 CSV 格式。

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `format` | `string` | `"json"` | 导出格式：`"json"`, `"markdown"`, `"csv"` |
| `output` | `string` | `null` | 输出文件路径 |
| `category` | `string` | `null` | 按类别过滤 |
| `minImportance` | `number` | `null` | 最低重要性阈值 |

---

### memory_dedup

检测并合并重复记忆。

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `threshold` | `number` | `0.85` | 相似度阈值 0-1 |
| `dryRun` | `boolean` | `true` | 为 true 时仅预览 |

---

### memory_profile

获取具有静态/动态分离的用户画像。

| 参数 | 类型 | 默认 | 描述 |
|------|------|---------|-------------|
| `scope` | `string` | `"user"` | 范围：`"agent"`, `"user"`, `"team"`, `"global"` |
| `container_tag` | `string` | `null` | 项目/泳道标签 |
| `static_days` | `number` | `30` | 天数无访问则标记为静态 |
| `limit` | `number` | `100` | 最大分析记忆数 |

---

### memory_preference

统一偏好管理。

| 参数 | 类型 | 描述 |
|------|------|-------------|
| `action` | `string` | 操作：`"get"`, `"set"`, `"update"`, `"merge"`, `"delete"`, `"reset"`, `"stats"`, `"explain"`, `"infer"` |
| `key` | `string` | 槽位键 |
| `value` | `any` | 槽位值 |
| `confidence` | `number` | 置信度 0-1 |
| `source` | `string` | `"explicit"`, `"inferred"`, `"historical"` |
| `slots` | `object` | 键值映射（用于 merge） |

---

## 版本控制

### memory_version

记忆版本控制。

| 参数 | 类型 | 描述 |
|------|------|-------------|
| `action` | `string` | 操作：`"list"`, `"diff"`, `"restore"` |
| `memoryId` | `string` | 记忆 ID |
| `versionId` | `string` | 版本 ID |
| `limit` | `number` | `10` | 最大版本数 |

---

## 层级管理

### memory_tier

HOT/WARM/COLD 层级管理。

| 参数 | 类型 | 描述 |
|------|------|-------------|
| `action` | `string` | 操作：`"status"`, `"migrate"`, `"compress"`, `"redistribute"` |
| `apply` | `boolean` | `false` | 应用更改 |

**层级阈值：**
- HOT：≤ 7 天
- WARM：7–30 天
- COLD：> 30 天

---

## 系统工具

### memory_stats

记忆系统统计。

**参数：** 无

返回：总数、分类、标签、层级分布。

---

### memory_health

MCP 服务器和依赖的健康检查。

**参数：** 无

---

### memory_pin / memory_unpin / memory_pins

固定（锁定）记忆，使其永不压缩或去重。

---

## 错误响应

所有工具在出错时返回带 `isError: true` 的错误响应：

```json
{
  "content": [{ "type": "text", "text": "Search error: connection timeout" }],
  "isError": true
}
```
