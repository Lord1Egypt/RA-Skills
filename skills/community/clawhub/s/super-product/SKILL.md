---
name: super-productivity
description: 任务管理 CLI 工具，用于 Super Productivity 数据的命令行管理。支持任务管理、计数器管理、项目管理、今日状态查看等功能。当用户提到 super-productivity、sp 任务管理、命令行任务管理时触发。
---

# Super Productivity CLI

命令行接口，用于管理 Super Productivity 应用中的任务、计数器和项目。

## 安装

```bash
pip install super-productivity-cli
```

## 核心命令

### 今日状态
```bash
sp status
```
查看今天的任务摘要和统计数据。

### 任务管理 (sp task)

| 命令 | 说明 |
|------|------|
| `sp task list` | 列出所有任务 |
| `sp task search <关键词>` | 搜索任务 |
| `sp task view <task-id>` | 查看任务详情 |
| `sp task add --title "<标题>"` | 添加新任务 |
| `sp task edit <task-id> --title "<新标题>"` | 编辑任务 |
| `sp task done <task-id>` | 标记任务完成 |
| `sp task estimate <task-id> <时间>` | 估算时间，如 `2h`、`30m` |
| `sp task log <task-id> <时间>` | 记录实际花费时间 |
| `sp task plan <task-id> <日期> <时间>` | 计划任务时间 |
| `sp task delete <task-id>` | 删除任务 |

### 计数器管理 (sp counter)

| 命令 | 说明 |
|------|------|
| `sp counter list` | 列出所有计数器 |
| `sp counter search <关键词>` | 搜索计数器 |
| `sp counter add --title "<名称>"` | 添加计数器 |
| `sp counter edit <counter-id> --title "<新名称>"` | 编辑计数器 |
| `sp counter log <counter-id>` | 记录一次计数 |
| `sp counter toggle <counter-id>` | 切换计数器状态 |
| `sp counter delete <counter-id>` | 删除计数器 |

### 项目管理 (sp project)
```bash
sp project list
sp project view <project-id>
```

## 输出选项

- `--json`: JSON 格式输出
- `--ndjson`: NDJSON 格式输出（每行一个 JSON 对象）
- `--full`: 包含完整实体数据

## 工作流示例

1. 查看今日任务：`sp status`
2. 搜索任务：`sp task search "报告"`
3. 查看任务详情：`sp task view <task-id>`
4. 标记完成：`sp task done <task-id>`

## 注意事项

- 所有修改命令需要使用 ID，不是标题模糊匹配
- 先用 `list` 或 `search` 获取 ID
- 支持通配符 `*` 搜索，如 `sp task search "open*"`
- **Windows 兼容性问题**：
  - 该包在 Python 3.11 上有 f-string 语法兼容问题（需手动修复源码）
  - Windows 控制台默认编码为 GBK，使用 `--json` 输出避免中文乱码
  - 可通过设置环境变量 `PYTHONIOENCODING=utf-8` 解决编码问题
- **数据初始化**：首次使用需创建数据文件或配置 rclone 进行云同步
