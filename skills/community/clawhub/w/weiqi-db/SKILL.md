---
name: 围棋棋谱数据库
description: weiqi-db 围棋棋谱数据库 - 本地棋谱管理工具，支持SGF导入、元数据编辑、标签管理、全文搜索。数据存储于单个JSON文件，AI友好的JSON接口设计。
tags: ["围棋", "weiqi", "go", "棋谱", "数据库", "SGF", "管理"]
---

# 围棋棋谱数据库 (weiqi-db)

> **🔒 安全说明**: 本技能为纯本地工具，所有数据存储在用户主目录下的 `~/.weiqi-db/database.json`，不涉及任何网络请求或外部服务。

本地围棋棋谱数据库，统一收纳来自野狐、本地SGF文件等来源的棋谱，支持全文搜索、标签管理、元数据编辑。

## 核心特性

- **单文件存储**: 所有数据（含SGF内容）存储在一个JSON文件中
- **AI友好接口**: 默认JSON输出，便于程序解析
- **灵活查询**: JSON表达式查询语法，支持精确匹配和模糊搜索
- **元数据编辑**: 支持自动解析SGF + 手动覆盖补充
- **标签系统**: 多标签分类管理
- **SGF压缩**: 自动压缩存储，节省约75%磁盘空间

## AI 执行规范（必读）

最短执行路径，最少 token 消耗：

### 1. 查询棋谱（使用简化参数）
```bash
python3 ~/.openclaw/workspace/weiqi-db/scripts/db.py query --date YYYY-MM-DD --limit 10
python3 ~/.openclaw/workspace/weiqi-db/scripts/db.py query --player "柯洁"
python3 ~/.openclaw/workspace/weiqi-db/scripts/db.py query --event-like "烂柯杯"
```

### 2. 导出 SGF 文件（最高效方式）
```bash
python3 ~/.openclaw/workspace/weiqi-db/scripts/db.py get --id "棋谱ID" -o /tmp/game.sgf
```

### 3. 生成打谱网页（与 weiqi-sgf 配合）
```bash
python3 ~/.openclaw/workspace/weiqi-db/scripts/db.py get --id "棋谱ID" -o /tmp/game.sgf
python3 ~/.openclaw/workspace/weiqi-sgf/scripts/replay.py /tmp/game.sgf -o /tmp/
```

### 4. 禁止行为 ❌
- **禁止**直接读取 `~/.weiqi-db/database.json` 文件
- **禁止**使用 JSON 输出后再用 Python 解析提取 SGF
- **禁止**不必要的 `cd` 命令，直接使用绝对路径

## 安装依赖

```bash
pip3 install tinydb
```

## CLI 接口

### 初始化数据库

```bash
python3 db.py init
```

创建 `~/.weiqi-db/database.json` 空数据库。

### 添加棋谱

```bash
# 添加单个SGF文件
python3 db.py add --file game.sgf

# 添加整个目录
python3 db.py add --dir <TEMP_DIR>/foxwq_downloads/2026-03-23/ --tag "野狐"

# 添加时补充/覆盖元数据
python3 db.py add --file game.sgf --black "棋手A" --white "棋手B" --event "示例赛事"

# 冲突处理策略
python3 db.py add --dir ./downloads/ --conflict skip     # 默认：跳过重复
python3 db.py add --dir ./downloads/ --conflict overwrite # 覆盖已有棋谱
python3 db.py add --dir ./downloads/ --conflict keep      # 保留两者
```

**冲突检测类型：**
- `hash`: SGF内容完全相同（基于MD5哈希）
- `metadata`: 元数据重复（同棋手+同日期+同手数/结果，可能是同一局棋的不同来源）

### 查询棋谱

```bash
# 查询棋手（自动匹配黑棋或白棋）
python3 db.py query --where '{"player": "示例棋手"}'

# 查询赛事
python3 db.py query --where '{"event": "示例赛事"}'

# 模糊搜索赛事
python3 db.py query --where '{"event~": "联赛"}'

# 按标签查询
python3 db.py query --where '{"tags": "名局"}'

# 日期范围
python3 db.py query --where '{"date>=": "2026-01-01"}'

# 全字段模糊搜索
python3 db.py query --where '{"keyword": "中盘胜"}'

# 组合条件
python3 db.py query --where '{"player": "示例棋手", "tags": "名局"}'

# AND/OR 组合
python3 db.py query --where '{"$and": [{"player": "示例棋手"}, {"date": "2026-03-23"}]}'

# 使用简化参数（无需 JSON）
python3 db.py query --player "柯洁"
python3 db.py query --date "2024-01-15"
python3 db.py query --event "LG杯"
python3 db.py query --event-like "杯赛"

# 组合简化参数
python3 db.py query --player "柯洁" --date "2024-01-15"

# 从文件读取查询条件（解决 exec 安全限制）
echo '{"player": "柯洁"}' > /tmp/where.json
python3 db.py query --where-file /tmp/where.json
```

### 列出所有棋谱

```bash
python3 db.py list
python3 db.py list --limit 10
```

### 获取单个棋谱（含SGF）

```bash
python3 db.py get --id "2026032383118500"

# 导出到文件（推荐，最高效）
python3 db.py get --id "2026032383118500" -o /tmp/game.sgf
```

返回完整的棋谱数据，包括 `sgf` 字段（SGF文件内容）。

### 更新元数据

```bash
python3 db.py update --id "2026032383118500" --set '{"black": "修正名", "event": "测试赛事"}'

# 从文件读取更新内容（解决 exec 安全限制）
echo '{"black": "修正名", "event": "测试赛事"}' > /tmp/set.json
python3 db.py update --id "2026032383118500" --set-file /tmp/set.json
```

### 标签管理

```bash
# 添加单个标签
python3 db.py tag --id "xxx" --add "名局"

# 移除单个标签
python3 db.py tag --id "xxx" --remove "测试"

# 从文件批量添加标签（JSON 数组）
echo '["名局", "经典", "AI讲解"]' > /tmp/tags.json
python3 db.py tag --id "xxx" --add-file /tmp/tags.json

# 从文件批量移除标签（JSON 数组）
echo '["临时标签", "测试"]' > /tmp/remove_tags.json
python3 db.py tag --id "xxx" --remove-file /tmp/remove_tags.json
```

### 删除棋谱

```bash
python3 db.py delete --id "xxx"
```

### 统计信息

```bash
python3 db.py stats
```

## 查询语法（--where 参数）

| 语法 | 含义 | 示例 |
|------|------|------|
| `{"player": "示例棋手"}` | 棋手名（搜 black 或 white） | 找该棋手的所有对局 |
| `{"black": "黑方"}` | 只搜执黑 | 找黑方执黑的对局 |
| `{"white": "白方"}` | 只搜执白 | 找白方执白的对局 |
| `{"event": "示例赛事"}` | 赛事精确匹配 | 找特定比赛 |
| `{"event~": "示例"}` | 赛事模糊匹配（~后缀） | 找含"示例"的比赛 |
| `{"tags": "名局"}` | 包含标签 | 找标为"名局"的棋 |
| `{"date": "2026-03-23"}` | 日期精确匹配 | 找特定日期 |
| `{"date>=": "2026-01-01"}` | 日期大于等于 | 日期范围查询 |
| `{"keyword": "中盘"}` | 全字段模糊搜索 | 任意字段含"中盘" |
| `{"$and": [{}, {}]}` | AND 组合 | 同时满足多个条件 |
| `{"$or": [{}, {}]}` | OR 组合 | 满足任一条件 |

## Exec 安全限制与 Workaround

在某些环境中（如受限的 exec 调用），直接传递 JSON 参数可能会遇到转义或安全限制问题。

### 问题示例
```bash
# 复杂的 JSON 参数在 exec 中可能无法正常传递
python3 db.py query --where '{"$and": [{"player": "柯洁"}, {"date>=": "2024-01-01"}]}'
python3 db.py update --id "xxx" --set '{"black": "新名字", "event": "新赛事", "tags": ["标签1", "标签2"]}'
```

### 解决方案：使用文件传递参数

**1. 将 JSON 内容写入临时文件**
```bash
# 查询条件
cat > /tmp/where.json << 'EOF'
{"$and": [{"player": "柯洁"}, {"date>=": "2024-01-01"}]}
EOF

# 更新内容
cat > /tmp/set.json << 'EOF'
{"black": "新名字", "event": "新赛事"}
EOF
```

**2. 使用 --*-file 参数**
```bash
# 查询
python3 db.py query --where-file /tmp/where.json

# 更新
python3 db.py update --id "xxx" --set-file /tmp/set.json

# 批量添加标签
echo '["名局", "经典", "AI讲解"]' > /tmp/tags.json
python3 db.py tag --id "xxx" --add-file /tmp/tags.json
```

**3. 使用简化参数（无需 JSON）**
```bash
# 对于简单查询，可以直接使用简化参数
python3 db.py query --player "柯洁" --date "2024-01-15"
python3 db.py query --event-like "LG杯"
```

### 参数互斥规则
- `--where` 和 `--where-file` 不能同时使用
- `--set` 和 `--set-file` 不能同时使用
- `--add` 和 `--add-file` 不能同时使用
- `--remove` 和 `--remove-file` 不能同时使用

## 数据格式

数据库文件 `~/.weiqi-db/database.json` 结构：

```json
{
  "version": 1,
  "games": [
    {
      "id": "2026032383118500",
      "sgf": "(;GM[1]FF[4]...)",
      "black": "棋手A",
      "white": "棋手B",
      "black_rank": "九段",
      "white_rank": "九段",
      "date": "2026-03-23",
      "event": "示例围棋联赛",
      "result": "白中盘胜",
      "komi": "375",
      "movenum": 198,
      "tags": ["联赛", "AI讲解"],
      "hash": "a1b2c3d4...",
      "created": "2026-03-24T12:07:45"
    }
  ]
}
```

## AI 使用示例

**用户**: "找某棋手的棋"
```bash
python3 db.py query --where '{"player": "示例棋手"}'
```

**用户**: "某杯赛决赛的名局"
```bash
python3 db.py query --where '{"event~": "杯赛", "tags": "名局"}'
```

**用户**: "昨天下的棋"
```bash
python3 db.py query --where '{"date": "2026-03-23"}'
```

**用户**: "获取某盘棋的SGF"
```bash
python3 db.py get --id "xxx" -o /tmp/game.sgf
```

**用户**: "把刚才那盘棋标为名局"
```bash
python3 db.py tag --id "xxx" --add "名局"
```

## 技术说明

- **存储**: TinyDB (JSON-based，单文件)
- **去重**: 基于 SGF 内容哈希值
- **搜索**: 内存索引 + 遍历过滤（适合 <10k 数据量）

## 相关技能

- [weiqi-foxwq](../weiqi-foxwq) - 野狐棋谱下载（棋谱来源）
- [weiqi-yunbisai](../weiqi-yunbisai) - 云比赛网查询（比赛信息查询，不提供棋谱下载）

## 版本更新

### v1.0.5 (2026-04-11)
- ✅ 优化 AI 执行规范
  - 使用绝对路径执行，无需 `cd`
  - 突出 `-o` 参数的文件导出功能
  - 删除多余的步骤，最短执行路径
  - 明确禁止直接读取 database.json 和 JSON 解析

### v1.0.4 (2026-04-11)
- ✅ 解决 exec 安全限制导致的 JSON 参数传递问题
  - `query` 命令新增 `--where-file` 参数，支持从文件读取 JSON 查询条件
  - `update` 命令新增 `--set-file` 参数，支持从文件读取 JSON 更新内容
  - `tag` 命令新增 `--add-file` 和 `--remove-file` 参数，支持批量标签操作
  - 新增简化查询参数：`--date`, `--player`, `--event`, `--event-like`
  - 新参数与原有参数互斥，保持向后兼容

### v1.0.3 (2026-04-11)
- ✅ 实现 SGF 自动压缩功能
  - 使用 gzip + base64 压缩算法
  - 压缩率约 75%（实测 9.6MB → 2.4MB）
  - 读取时自动解压，向后兼容旧数据

### v1.0.2 (2026-04-11)
- ✅ 新增 `get` 命令，支持通过 ID 获取完整棋谱（含 SGF）
- ✅ 清理 `--json` 参数（默认始终 JSON 输出）

### v1.0.1 (2026-03-27)
- ✅ 导入冲突检测功能
  - 支持哈希级重复检测（相同SGF内容）
  - 支持元数据级重复检测（同棋手+同日期）
  - 三种冲突处理策略：`skip`(跳过)、`overwrite`(覆盖)、`keep`(保留两者)

### v1.0.0 (2026-03-24)
- ✅ 初始版本发布
- ✅ 支持 SGF 导入、元数据编辑、标签管理
- ✅ JSON 查询语法，AI 友好接口
