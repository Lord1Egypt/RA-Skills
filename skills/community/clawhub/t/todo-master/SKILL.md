---
name: todo-master
description: 用于本地待办管理的技能，支持基于 Python CLI 和 SQLite 存储待办；首次必须由用户确认数据目录（默认使用当前 skill 目录下的 data，或指定一个已存在的绝对路径）；支持添加待办、快速添加今日/明日待办、查看今日待办、按状态/优先级/关键字筛选查看全部待办、查看单条、更新、完成、重开、归档，并通过数据库 schema migration 保护升级后的已有数据。
---

# Todo Skill

## 适用场景

- 需要在 OpenClaw 中维护本地待办，而不是依赖在线服务。
- 需要一个稳定的 Python 脚本入口，方便被代理或自动化直接调用。
- 需要让 skill 迭代升级时继续复用已有数据，而不是重建存储。

## 运行结构

脚本入口：

```bash
python3 ./todo-master/scripts/todo.py
```

主要文件：

1. `./todo-master/config.json`
2. `<data_dir>/todos.sqlite3`
3. `./todo-master/requirements.txt`

默认数据目录：

1. `./todo-master/data`

## 依赖说明

运行环境：

1. Python 3.10 或更高版本
2. 当前实现仅依赖 Python 标准库，不需要额外第三方包

如需按统一流程安装，可执行：

```bash
python3 -m pip install -r ./todo-master/requirements.txt
```

## 初始化

首次使用前必须先让用户确认数据目录：

```bash
python3 ./todo-master/scripts/todo.py init --default
python3 ./todo-master/scripts/todo.py init --data-dir /absolute/existing/path
```

规则：

1. `--default` 会使用当前 skill 目录下的 `data/`
2. `--data-dir` 必须是一个已存在的绝对路径
3. 未初始化前，除 `init` 和 `show-config` 外不要执行其他命令

## 命令说明

查看当前配置：

```bash
python3 ./todo-master/scripts/todo.py show-config
```

添加普通待办：

```bash
python3 ./todo-master/scripts/todo.py add --title "准备周报" --content "汇总本周项目进展" --priority 4
python3 ./todo-master/scripts/todo.py add --title "整理材料" --content "补齐投标附件" --priority 5 --due 2026-03-20
python3 ./todo-master/scripts/todo.py add --title "联系客户" --content "确认下周演示时间" --priority 3 --due 2026-03-20T18:30
```

快速添加今日/明日待办：

```bash
python3 ./todo-master/scripts/todo.py add-today --title "回邮件" --content "回复合作方案" --priority 3
python3 ./todo-master/scripts/todo.py add-tomorrow --title "开复盘会" --content "准备会议提纲" --priority 4
```

查看今日待办（按今天到期）：

```bash
python3 ./todo-master/scripts/todo.py list-today
python3 ./todo-master/scripts/todo.py list-today --json
```

查看全部待办：

```bash
python3 ./todo-master/scripts/todo.py list-all
python3 ./todo-master/scripts/todo.py list-all --json
python3 ./todo-master/scripts/todo.py list-all --status open --min-priority 4
python3 ./todo-master/scripts/todo.py list-all --keyword "周报" --limit 10
python3 ./todo-master/scripts/todo.py list-all --overdue
```

查看单条：

```bash
python3 ./todo-master/scripts/todo.py show --id <todo_id>
python3 ./todo-master/scripts/todo.py show --id <todo_id> --json
```

更新、完成、重开、归档：

```bash
python3 ./todo-master/scripts/todo.py update --id <todo_id> --title "新标题" --priority 5
python3 ./todo-master/scripts/todo.py update --id <todo_id> --due 2026-03-21T18:00
python3 ./todo-master/scripts/todo.py update --id <todo_id> --clear-due
python3 ./todo-master/scripts/todo.py done --id <todo_id>
python3 ./todo-master/scripts/todo.py reopen --id <todo_id>
python3 ./todo-master/scripts/todo.py archive --id <todo_id>
```

查看统计：

```bash
python3 ./todo-master/scripts/todo.py stats
```

## 数据与升级规则

1. 配置和数据分离：`config.json` 只保存数据目录和数据库文件名
2. SQLite 使用 `PRAGMA user_version` 管理 schema 版本
3. 启动时会自动执行向前兼容的 migration
4. 若发现旧版 JSON 数据文件，会在首次打开 SQLite 时自动导入，避免已有数据丢失
5. 不要手工修改 SQLite 文件

## 给代理的执行规则

1. 新增待办时，`title`、`content`、`priority` 都必填
2. `priority` 只能是 `1` 到 `5`
3. `list-today` 的语义是“今天到期的待办”
4. `archive` 是保留数据的软归档，不是物理删除
5. 所有数据读写必须走 CLI，不要绕过脚本直接写数据库
