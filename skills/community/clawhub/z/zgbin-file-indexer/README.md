# File Indexer - 文件索引工具

快速查找和管理项目文件的工具，自动跟踪文件创建、修改和删除。

## 功能特性

- **自动索引**: 自动记录 agent 新建的文件（技能、脚本、配置等）
- **删除标记**: 文件删除时自动标记
- **快速搜索**: 根据关键词或功能描述快速查找相关文件
- **意图推荐**: 根据用户意图智能推荐相关文件
- **实时监控**: 支持 watchdog 实时监控或轮询模式

## 安装

```bash
# 克隆或复制文件到项目目录
# 文件已位于：/home/t/cc_workspace/file_indexer/

# 可选：安装 watchdog 用于实时监控
pip install watchdog
```

## 使用方法

### 基本用法

```bash
# 显示帮助
./file_indexer help

# 搜索文件
./file_indexer search "加密"

# 根据意图推荐文件
./file_indexer intent "文件加密功能"

# 添加文件到索引
./file_indexer add /path/to/file.py

# 标记文件为已删除
./file_indexer delete /path/to/file

# 查看文件信息
./file_indexer info /path/to/file.py

# 查看最近修改的文件
./file_indexer recent

# 按文件类型列出文件
./file_indexer type python_script

# 显示索引统计
./file_indexer stats

# 扫描目录
./file_indexer scan /home/t/cc_workspace

# 启动实时监控
./file_indexer watch

# 启动轮询监控（无需 watchdog）
./file_indexer watch-polling
```

### 搜索示例

```bash
# 搜索包含"加密"的文件
./file_indexer search "加密"

# 搜索 Python 脚本
./file_indexer search "python"

# 根据意图查找加密相关文件
./file_indexer intent "实现文件加密功能"

# 查看最近 20 个修改的文件
./file_indexer recent 20

# 列出所有 Python 脚本
./file_indexer type python_script
```

## 自动索引配置

文件索引器已配置为自动运行。当 agent 创建或修改文件时，会自动记录到索引中。

配置位置：`/home/t/cc_workspace/.claude/settings.local.json`

## 支持的命令

| 命令 | 描述 |
|------|------|
| `search <query>` | 搜索文件 |
| `intent <description>` | 根据意图推荐文件 |
| `add <filepath>` | 添加文件到索引 |
| `delete <filepath>` | 标记文件为已删除 |
| `info <filepath>` | 显示文件详细信息 |
| `recent [count]` | 显示最近修改的文件 |
| `type <file_type>` | 按文件类型列出文件 |
| `stats` | 显示索引统计 |
| `scan <dirpath>` | 扫描目录 |
| `watch` | 启动实时监控 |
| `watch-polling` | 启动轮询监控 |

## 文件类型

- `python_script` - Python 脚本
- `javascript` - JavaScript 文件
- `typescript` - TypeScript 文件
- `config` - 配置文件 (JSON, YAML)
- `documentation` - 文档 (Markdown)
- `shell_script` - Shell 脚本
- `database` - SQL 文件
- `web` - HTML/CSS
- `vue_component` - Vue 组件
- `react_component` - React 组件
- `other` - 其他类型

## 数据库

索引数据存储在 SQLite 数据库中：
- 数据库路径：`/home/t/cc_workspace/file_indexer/file_index.db`

## 监控目录

默认监控以下目录：
- `/home/t/.claude/projects/-home-t--openclaw-workspace/`
- `/home/t/cc_workspace/`

## 扩展性

可以通过修改以下文件来自定义：
- `indexer.py` - 索引管理逻辑
- `searcher.py` - 搜索逻辑
- `watcher.py` - 监控逻辑
- `hook_handler.py` - Hook 处理逻辑

## 许可证

MIT
