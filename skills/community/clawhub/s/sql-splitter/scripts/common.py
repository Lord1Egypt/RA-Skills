#!/usr/bin/env python3
"""
SQL 拆分工具 — 共享模块
统一方言枚举、对象前缀映射、公共工具函数
"""

import re
from enum import Enum
from typing import Dict


class SQLDialect(Enum):
    """支持的 SQL 方言"""
    MYSQL = 'mysql'
    POSTGRESQL = 'postgresql'
    ORACLE = 'oracle'
    SQLSERVER = 'sqlserver'
    DM = 'dm'
    GENERIC = 'generic'


# 对象类型 → 文件前缀
OBJECT_PREFIXES: Dict[str, str] = {
    'procedure': 'proc',
    'function': 'func',
    'trigger': 'trig',
    'view': 'view',
    'table': 'table',
    'package': 'pkg',
    'sequence': 'seq',
    'merge': 'merge_',
    'replace': 'repl_',
    'ddl_trigger': 'ddltrig_',
    'synonym': 'syn',
    'event': 'evt',
    'materialized_view': 'mv',
    'type': 'type',
    'index': 'idx',
    'unique_index': 'uidx',
    'constraint': 'con',
    'primary_key': 'pk',
    'foreign_key': 'fk',
    'check': 'chk',
}

# 导入优先级（数字越小越先导入）
TYPE_PRIORITY: Dict[str, int] = {
    'table': 1,
    'sequence': 2,
    'type': 3,
    'synonym': 4,
    'view': 5,
    'materialized_view': 6,
    'function': 7,
    'procedure': 8,
    'package': 9,
    'trigger': 10,
    'index': 11,
    'unique_index': 12,
    'constraint': 13,
}

# 需要进入 BEGIN...END 块的对象类型
BLOCK_OBJECT_TYPES = frozenset({
    'procedure', 'function', 'trigger', 'package',
    'ddl_trigger', 'type',  # Oracle TYPE ... IS / AS ... END;
})

# SQL 关键字全集（用于依赖分析过滤）
SQL_KEYWORDS = frozenset({
    # DML
    'select', 'insert', 'update', 'delete', 'merge', 'replace',
    # DDL
    'create', 'alter', 'drop', 'grant', 'revoke', 'truncate', 'rename',
    # 控制流
    'if', 'while', 'for', 'loop', 'exit', 'return', 'raise', 'goto',
    'begin', 'end', 'case', 'when', 'then', 'else', 'elsif',
    # 逻辑
    'and', 'or', 'not', 'in', 'exists', 'between', 'like', 'is',
    'null', 'true', 'false',
    # 集合
    'union', 'intersect', 'minus', 'except', 'all', 'any', 'some',
    # 聚合
    'count', 'sum', 'avg', 'min', 'max', 'group', 'having',
    # 内置函数
    'coalesce', 'nvl', 'nvl2', 'decode', 'cast', 'convert',
    'substr', 'substring', 'length', 'char_length',
    'upper', 'lower', 'trim', 'ltrim', 'rtrim', 'replace', 'concat',
    'to_char', 'to_date', 'to_number', 'to_timestamp',
    'round', 'trunc', 'ceil', 'floor', 'abs', 'sign',
    'instr', 'locate', 'position', 'split_part',
    'row_number', 'rank', 'dense_rank', 'lead', 'lag',
    'first_value', 'last_value', 'nth_value',
    'dateadd', 'datediff', 'date_trunc', 'extract',
    'current_date', 'current_time', 'current_timestamp',
    'now', 'sysdate', 'getdate',
    'newid', 'uuid', 'gen_random_uuid',
    # 游标
    'open', 'fetch', 'close', 'cursor',
    # 事务
    'commit', 'rollback', 'savepoint', 'set',
    # 其他
    'declare', 'execute', 'exec', 'call', 'perform',
    'print', 'raise', 'notice', 'exception',
    'values', 'from', 'where', 'join', 'on', 'as',
    'into', 'set', 'order', 'by', 'asc', 'desc',
    'limit', 'offset', 'fetch', 'next', 'rows',
    'primary', 'foreign', 'unique', 'check', 'references',
    'constraint', 'index', 'key', 'default',
    'inner', 'left', 'right', 'full', 'cross', 'natural',
    'outer', 'using', 'with', 'recursive',
    'over', 'partition', 'window',
    'table', 'view', 'procedure', 'function', 'trigger',
    'sequence', 'schema', 'database', 'catalog',
})


def clean_object_name(name: str) -> str:
    """清理对象名称：去引号/方括号，取 schema.name 的 name 部分"""
    name = re.sub(r'[`"\'>\[\]]', '', name)
    if '.' in name:
        name = name.split('.')[-1]
    return name.strip()


def strip_sql_comments(sql: str) -> str:
    """去除 SQL 中的注释，保留字符串字面量内的内容不被误删"""
    result = []
    i = 0
    n = len(sql)
    while i < n:
        # 单行注释 --
        if sql[i] == '-' and i + 1 < n and sql[i + 1] == '-':
            while i < n and sql[i] != '\n':
                i += 1
            continue
        # 多行注释 /* */
        if sql[i] == '/' and i + 1 < n and sql[i + 1] == '*':
            i += 2
            while i + 1 < n and not (sql[i] == '*' and sql[i + 1] == '/'):
                i += 1
            i += 2  # skip */
            continue
        # 字符串字面量 — 不处理内部
        if sql[i] in ("'", '"'):
            quote = sql[i]
            result.append(sql[i])
            i += 1
            while i < n and sql[i] != quote:
                if sql[i] == quote and i + 1 < n and sql[i + 1] == quote:
                    # escaped quote
                    result.append(sql[i])
                    result.append(sql[i + 1])
                    i += 2
                    continue
                result.append(sql[i])
                i += 1
            if i < n:
                result.append(sql[i])
                i += 1
            continue
        result.append(sql[i])
        i += 1
    return ''.join(result)


def find_matching_end(sql: str, start: int, end_bound: int) -> int:
    """
    从 start 位置开始，匹配 BEGIN...END 块的结束位置。
    返回 END 关键字之后的偏移量（相对于 sql 整体）。
    如果匹配失败，返回 end_bound。

    算法：
    1. 扫描到第一个 BEGIN（跳过字符串/注释）
    2. 维护嵌套深度
    3. 遇到 END 且深度归零时返回
    """
    depth = 0
    i = start
    n = min(len(sql), end_bound)

    while i < n:
        c = sql[i]
        # 跳过字符串
        if c in ("'", '"'):
            i = _skip_string(sql, i, n)
            continue
        # 跳过单行注释
        if c == '-' and i + 1 < n and sql[i + 1] == '-':
            while i < n and sql[i] != '\n':
                i += 1
            continue
        # 跳过多行注释
        if c == '/' and i + 1 < n and sql[i + 1] == '*':
            i += 2
            while i + 1 < n and not (sql[i] == '*' and sql[i + 1] == '/'):
                i += 1
            i += 2
            continue

        # 检测 BEGIN 关键字（词边界）
        if _is_keyword_at(sql, i, n, 'BEGIN'):
            depth += 1
            i += 5
            continue
        # IF ... THEN / CASE ... WHEN ... THEN 也增加 depth（对应 END IF / END CASE）
        # 只有 PL/SQL 中的 IF（后跟 THEN）才算，避免 IF() 函数误匹配
        if _is_keyword_at(sql, i, n, 'IF'):
            # 检查后面是否有 THEN（简单向前扫描）
            j = i + 2
            while j < n and sql[j] in ' \t\r\n':
                j += 1
            # 跳过条件表达式中的简单内容，看是否在合理距离内出现 THEN
            # 简化策略：IF 后100字符内有 THEN → 认为是 PL/SQL IF 块
            peek = sql[j:min(j+100, n)].upper()
            if 'THEN' in peek:
                depth += 1
            i += 2
            continue
        if _is_keyword_at(sql, i, n, 'CASE'):
            depth += 1
            i += 4
            continue
        # Oracle/PG: LOOP 也算嵌套
        if _is_keyword_at(sql, i, n, 'LOOP'):
            depth += 1
            i += 4
            continue
        # 检测 END 关键字
        if _is_keyword_at(sql, i, n, 'END'):
            depth -= 1
            i += 3
            if depth <= 0:
                # 跳过 END 后面可能跟的 ; / 或标识符（如 END IF;）
                while i < n and sql[i] in ' \t\r\n':
                    i += 1
                # 跳过 END IF / END LOOP / END CASE 等后缀
                for kw in ('IF', 'LOOP', 'CASE'):
                    if _is_keyword_at(sql, i, n, kw):
                        i += len(kw)
                        while i < n and sql[i] in ' \t\r\n':
                            i += 1
                        break
                # 跳到分号
                if i < n and sql[i] == ';':
                    i += 1
                return i
            continue
        i += 1

    return end_bound


def _skip_string(sql: str, start: int, bound: int) -> int:
    """跳过引号字符串，返回字符串结束后的位置"""
    quote = sql[start]
    i = start + 1
    while i < bound:
        if sql[i] == quote:
            if i + 1 < bound and sql[i + 1] == quote:
                i += 2  # escaped
                continue
            return i + 1
        i += 1
    return i


def _is_keyword_at(sql: str, pos: int, bound: int, keyword: str) -> bool:
    """检查 sql[pos:] 是否以 keyword 开头（词边界）"""
    kw_len = len(keyword)
    if pos + kw_len > bound:
        return False
    if sql[pos:pos + kw_len].upper() != keyword:
        return False
    # 前面必须是词边界
    if pos > 0 and sql[pos - 1].isalnum() or (pos > 0 and sql[pos - 1] == '_'):
        return False
    # 后面必须是词边界
    after = pos + kw_len
    if after < bound and (sql[after].isalnum() or sql[after] == '_'):
        return False
    return True
