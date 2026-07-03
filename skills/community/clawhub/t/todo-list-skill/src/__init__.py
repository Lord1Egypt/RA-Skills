#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""todo-list skill 数据层。

本包提供 todo-list skill 的核心模块：

    - exceptions：4 个自定义异常类型
    - store：SQLite 数据访问层（单例 + WAL）
    - cli：8 子命令 CLI 入口
    - nl_parser：自然语言解析器（regex + dateutil + jieba）
    - reminder：基于 cron 的定时提醒

公共 API：
    TodosStore：主数据访问类（单例模式）。

技术决策：
    - 单例：避免重复创建连接
    - WAL：读写并发（多读单写）
    - 降级：DB 异常时写入 /tmp/todos_fallback.json

参见：
    - DESIGN.md §4.1（数据层设计）
    - references/commands.md（CLI 参考）
    - references/errors.md（错误处理 + 降级路径）

License:
    MIT

Version:
    1.4.0

Author:
    月海巫师 (Chen Qing)
"""
from .store import TodosStore

__all__ = ["TodosStore"]