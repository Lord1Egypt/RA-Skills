# Board 模块

管理看板，用于组织生成的结果（图片、视频、音频）。用户可通过看板链接在网页上查看和编辑结果。

## 使用场景

- **会话首次任务前** — 运行 `list --default -q` 获取默认看板 ID
- **用户想要新看板** — 运行 `create --name "..."`
- **用户想浏览结果** — 运行 `tasks --board-id <id>`
- **用户需要看板管理** — list、detail、update、delete

## 子命令

| 子命令 | 说明 |
|------------|-------------|
| `list` | 列出看板（分页）。使用 `--default` 供 Agent 自动发现 |
| `create` | 创建新看板 |
| `detail` | 获取看板详情（成员、分享令牌） |
| `update` | 重命名看板 |
| `delete` | 删除看板 |
| `tasks` | 列出看板中的任务（支持筛选） |
| `task-detail` | 获取单个任务的完整详情 |

## 用法

```bash
python {baseDir}/scripts/board.py <subcommand> [options]
```

## 示例

### 获取默认看板 ID（Agent 启动时）

```bash
BOARD_ID=$(python {baseDir}/scripts/board.py list --default -q)
```

Agent 应在会话开始时运行一次，之后所有任务复用该看板 ID。

### 列出所有看板

```bash
python {baseDir}/scripts/board.py list
```

输出（制表符分隔）：

```
board_123456    My First Board    5 tasks [default]
board_789012    Campaign Q3       12 tasks
```

### 创建新看板

```bash
python {baseDir}/scripts/board.py create --name "Campaign Q3"
```

输出新看板 ID。用户明确要求新看板时使用此命令。

### 查看看板详情

```bash
python {baseDir}/scripts/board.py detail --board-id <boardId>
```

### 重命名看板

```bash
python {baseDir}/scripts/board.py update --board-id <boardId> --name "Campaign Q4"
```

### 删除看板

```bash
python {baseDir}/scripts/board.py delete --board-id <boardId>
```

### 列出看板中的任务

```bash
python {baseDir}/scripts/board.py tasks --board-id <boardId>
```

带筛选条件：

```bash
python {baseDir}/scripts/board.py tasks --board-id <boardId> \
  --media-type video \
  --sort-field gmtCreate --sort-order desc \
  --page 1 --size 50
```

### 获取任务详情

```bash
python {baseDir}/scripts/board.py task-detail --task-id <taskId>
```

显示完整任务信息，包括编辑链接：

```
Task: task_abc123
  boardTaskId: bt_xyz789
  boardId:     board_abc123
  status:      success
  tool:        text2video
  cost:        10 credits
  edit: https://tekan.cn/board/board_abc123?boardResultId=bt_xyz789
```

## 选项

### `list`

| 选项 | 说明 |
|--------|-------------|
| `--default` | 仅输出默认看板 ID（供 Agent 自动发现） |
| `--page N` | 页码（默认：1） |
| `--size N` | 每页条数（默认：20） |

### `create`

| 选项 | 说明 |
|--------|-------------|
| `--name TEXT` | 看板名称，最长 200 字符（必需） |

### `detail`

| 选项 | 说明 |
|--------|-------------|
| `--board-id ID` | 看板 ID（必需） |

### `update`

| 选项 | 说明 |
|--------|-------------|
| `--board-id ID` | 看板 ID（必需） |
| `--name TEXT` | 新名称，最长 200 字符（必需） |

### `delete`

| 选项 | 说明 |
|--------|-------------|
| `--board-id ID` | 看板 ID（必需） |

### `tasks`

| 选项 | 说明 |
|--------|-------------|
| `--board-id ID` | 看板 ID（必需） |
| `--media-type` | 筛选：`image` / `video` |
| `--rating N` | 按评分筛选：0-3 |
| `--tool-category` | 按工具类别筛选 |
| `--tool-type` | 按工具类型筛选 |
| `--sort-field` | 排序字段：`gmtCreate` / `sortWeight` |
| `--sort-order` | `asc` / `desc` |
| `--page N` | 页码 |
| `--size N` | 每页条数 |

### `task-detail`

| 选项 | 说明 |
|--------|-------------|
| `--task-id ID` | 任务 ID（必需） |

### 全局

| 选项 | 说明 |
|--------|-------------|
| `--json` | 输出完整 JSON 响应 |
| `-q, --quiet` | 静默模式，抑制状态消息 |

## 看板网页 URL

在网页上查看和编辑看板结果：

```
https://tekan.cn/board/{boardId}
```

查看特定结果：

```
https://tekan.cn/board/{boardId}?boardResultId={boardTaskId}
```

## Agent 协议

1. **会话开始**：运行 `board.py list --default -q` 获取默认看板 ID
2. **传递给所有任务**：为每个生成命令添加 `--board-id <id>`
3. **任务完成后**：如果响应中包含 `boardTaskId`，向用户展示编辑链接
4. **用户想要新看板**：运行 `board.py create --name "..."` 并使用返回的 ID
5. **用户指定看板**：使用用户提供的看板 ID
