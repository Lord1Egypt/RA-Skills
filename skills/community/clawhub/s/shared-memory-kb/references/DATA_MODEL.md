# Data Model - 数据模型

## 目录
- [记忆条目结构（Memory Entry）](#记忆条目结构memory-entry)
- [字段规范](#字段规范)
- [索引文件结构](#索引文件结构)
- [元数据结构（meta.json）](#元数据结构metajson)
- [存储架构](#存储架构)

---

## 记忆条目结构（Memory Entry）

### JSON 示例

```json
{
  "id": "mem_20260411_a3f7c2",
  "created_at": "2026-04-11T20:00:00+08:00",
  "updated_at": "2026-04-11T20:00:00+08:00",
  "deleted": false,
  "persona": "工作",
  "category": "方法论",
  "scene": "产品需求评审",
  "content": "需求评审时先对齐目的，比直接进入方案讨论效率更高，能减少后期返工。",
  "tags": ["需求管理", "沟通", "效率", "评审"],
  "type": "经验",
  "importance": 4,
  "linked_ids": ["mem_20260110_b2e1a9"],
  "source_context": "工作 Agent / 2026-04-11 产品需求讨论"
}
```

---

## 字段规范

| 字段 | 类型 | 约束 | 说明 | 默认值 |
|------|------|------|------|--------|
| `id` | string | 唯一、不可变 | 格式：mem_{YYYYMMDD}_{6位小写字母数字} | 自动生成 |
| `created_at` | string | 必填 | ISO8601 格式，含时区 | 当前时间 |
| `updated_at` | string | 必填 | ISO8601 格式，含时区 | 当前时间 |
| `deleted` | boolean | - | 软删除标记，不物理删除 | false |
| `persona` | string | 枚举+自定义 | 见 [TAXONOMY.md](TAXONOMY.md) | "通用" |
| `category` | string | 枚举+自定义 | 见 [TAXONOMY.md](TAXONOMY.md) | 由 AI 推断 |
| `scene` | string | ≤100 字符 | 场景描述，自由文本 | - |
| `content` | string | 20-2000 字符 | 记忆正文 | 必填 |
| `tags` | array[string] | ≤10 个，每个 ≤20 字符 | 小写中英文 | 由 AI 提取 |
| `type` | string | 枚举 | 见 [TAXONOMY.md](TAXONOMY.md) | "经验" |
| `importance` | int | 1-5 | 重要度评分 | 3 |
| `linked_ids` | array[string] | - | 关联记忆 ID 列表 | [] |
| `source_context` | string | ≤200 字符 | 来源描述 | - |

### ID 生成规则
格式：`mem_{YYYYMMDD}_{6位小写字母数字}`
- 前缀：固定 "mem"
- 日期：创建日期（YYYYMMDD）
- 随机码：6 位小写字母和数字（a-z, 0-9）
- 示例：mem_20260411_a3f7c2

### 软删除机制
- 删除操作不物理移除数据
- 将 `deleted` 字段设为 `true`
- 更新 `updated_at` 时间戳
- 索引重建时会自动过滤已删除记录

### 更新操作
- 不修改原始记录
- 写入新版本，旧版本标记 `deleted: true`
- 新版本继承原 `id`，但 `updated_at` 更新为当前时间

---

## 索引文件结构

索引文件位于 `~/.openclaw/memory/index/` 目录下，用于加速查询。

### by_persona.json
按身份索引，记录每个身份对应的记忆 ID 列表。

```json
{
  "工作": ["mem_20260411_a3f7c2", "mem_20260315_x9b2k1"],
  "私人": ["mem_20260405_p2m3n4"],
  "通用": ["mem_20260201_z8y7x6"]
}
```

### by_category.json
按分类索引，记录每个分类对应的记忆 ID 列表。

```json
{
  "方法论": ["mem_20260411_a3f7c2", "mem_20260320_l4j5h6"],
  "经验教训": ["mem_20260315_x9b2k1"],
  "观察": ["mem_20260405_p2m3n4"]
}
```

### by_tag.json
按标签索引，记录每个标签对应的记忆 ID 列表。

```json
{
  "效率": ["mem_20260411_a3f7c2", "mem_20260320_l4j5h6"],
  "沟通": ["mem_20260411_a3f7c2"],
  "需求管理": ["mem_20260411_a3f7c2"],
  "健康": ["mem_20260405_p2m3n4"]
}
```

### by_date.json
按日期索引，记录每天对应的记忆 ID 列表。

```json
{
  "2026-04-11": ["mem_20260411_a3f7c2"],
  "2026-04-05": ["mem_20260405_p2m3n4"],
  "2026-03-15": ["mem_20260315_x9b2k1"]
}
```

---

## 元数据结构（meta.json）

元数据文件位于 `~/.openclaw/memory/meta.json`，记录知识库的统计信息。

```json
{
  "version": "1.0.0",
  "total_entries": 42,
  "active_entries": 40,
  "deleted_entries": 2,
  "last_updated": "2026-04-11T20:00:00+08:00",
  "personas": {
    "工作": 18,
    "私人": 12,
    "兴趣": 8,
    "通用": 4
  },
  "categories": {
    "方法论": 15,
    "经验教训": 10,
    "观察": 8,
    "决策": 5,
    "知识点": 4
  },
  "top_tags": [
    "效率",
    "沟通",
    "健康",
    "学习",
    "产品"
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | string | 数据模型版本号 |
| `total_entries` | int | 总条目数（包含已删除） |
| `active_entries` | int | 活跃条目数（未删除） |
| `deleted_entries` | int | 已删除条目数 |
| `last_updated` | string | 最后更新时间（ISO8601） |
| `personas` | object | 各身份的条目数统计 |
| `categories` | object | 各分类的条目数统计 |
| `top_tags` | array[string] | 高频标签列表（按出现频次排序） |

---

## 存储架构

### 目录结构

```
~/.openclaw/memory/           # 默认路径，可通过 MEMORY_KB_PATH 自定义
├── memories.jsonl            # 主存储（每行一个 JSON 条目，追加写入）
├── index/
│   ├── by_persona.json       # 按身份索引
│   ├── by_category.json      # 按分类索引
│   ├── by_tag.json           # 按标签索引
│   └── by_date.json          # 按日期索引
└── meta.json                 # 统计元信息
```

### 主文件（memories.jsonl）
- 格式：JSON Lines（每行一个独立的 JSON 对象）
- 写入方式：追加写入（append），不修改历史记录
- 读取方式：逐行读取，过滤 `deleted: true` 的记录

### 索引更新策略
- **写入时更新**：每次 store 操作后，同步更新四个索引文件
- **原子性保证**：先写入主文件，成功后再更新索引
- **重建机制**：支持从 memories.jsonl 重建所有索引

### 并发安全
- 使用文件锁机制（`fcntl.flock`）保证写入原子性
- 避免并发写入导致的数据损坏

### 路径配置
通过环境变量 `MEMORY_KB_PATH` 自定义存储路径：

```bash
export MEMORY_KB_PATH="/your/custom/path/memory"
```

适用场景：
- 云盘同步（iCloud Drive、Dropbox）
- 多设备共享
- 自定义存储位置

### 索引重建
当索引损坏或数据不一致时，可手动重建：

```bash
python3 /workspace/projects/shared-memory-kb/scripts/memory_kb.py \
  action=rebuild-index
```

重建流程：
1. 读取 memories.jsonl，过滤已删除记录
2. 按 persona、category、tag、date 重新聚合
3. 更新所有索引文件
4. 重新计算 meta.json 统计信息
