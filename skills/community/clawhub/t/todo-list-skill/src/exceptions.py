#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""todo-list skill 自定义异常类型。

本模块定义数据访问层抛出的 4 个业务异常。每个异常对应特定的失败模式，
CLI 层会用友好错误消息和适当的退出码处理。

退出码映射（参考 sysexits.h）：
    - TodoNotFoundError     -> 1（业务错误：未找到）
    - TodoAmbiguousError    -> 1（业务错误：歧义）
    - TodoValidationError   -> 2（用法错误：参数非法）
    - TodoDatabaseError     -> 70（系统错误：数据库损坏/锁死）

参见：
    - DESIGN.md §4.1.2（异常类型定义）
    - SOUL.md 规则 6（错误处理）

License:
    MIT

Version:
    1.4.0

Author:
    月海巫师 (Chen Qing)
"""
from __future__ import annotations  # PEP 563：延后求值类型注解

from typing import Any


class TodoNotFoundError(Exception):
    """未找到匹配的 TODO 时抛出。

    示例：
        - ``done(999)`` 当 id=999 不存在时
        - ``delete("不存在的关键词")`` 当无 TODO 匹配时
    """

    pass


class TodoAmbiguousError(Exception):
    """多个 TODO 匹配模糊查询时抛出。

    携带候选列表供 CLI 层提示用户消歧。

    Attributes:
        candidates: 匹配的 TODO 字典列表。

    示例：
        - ``done("检查")`` 同时匹配 "检查止损" 和 "检查持仓"
    """

    def __init__(self, candidates: list[dict[str, Any]]):
        self.candidates = candidates
        count = len(candidates)
        names = [c.get("content", "") for c in candidates]
        super().__init__(
            f"找到 {count} 个匹配的 TODO，请确认：{names}"
        )


class TodoValidationError(Exception):
    """输入校验失败时抛出。

    校验规则：
        - content 不能为空
        - content 不能超过 500 字符
        - due_at 不能距今超过 365 天
        - priority 必须在 {high, medium, low} 之内
        - status 必须是合法状态
    """

    pass


class TodoDatabaseError(Exception):
    """数据库不可用时抛出。

    触发场景：
        - SQLite ``OperationalError: database is locked``（3 次重试后）
        - SQLite ``DatabaseError``（数据库损坏）
    """

    pass


__all__ = [
    "TodoNotFoundError",
    "TodoAmbiguousError",
    "TodoValidationError",
    "TodoDatabaseError",
]