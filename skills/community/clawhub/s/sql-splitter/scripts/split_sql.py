#!/usr/bin/env python3
"""
SQL 文件拆分工具 - 多数据库方言支持
支持 MySQL, PostgreSQL, Oracle, SQL Server, 达梦(DM) 等数据库

v2.0 重写要点:
- 使用 BEGIN...END 深度匹配确定存储过程/函数/触发器边界
- 不再依赖"下一个 CREATE"作为上界，正确处理嵌套 CREATE
- 正则改用 [\w.]+ 匹配 schema.name，引号内名字统一处理
- 共享 common.py 中的枚举和工具函数
- 拆分后自动生成依赖排序的合并脚本
"""

import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# 同目录导入
from common import (
    SQLDialect, OBJECT_PREFIXES, TYPE_PRIORITY, BLOCK_OBJECT_TYPES,
    clean_object_name, strip_sql_comments, find_matching_end,
)
from error_handler import (
    ErrorHandler, SplitError, SplitWarning, SplitResult, ErrorType,
)


# ============================================================
# 各方言的正则模式
# 对象名统一用 [\w."`\[\]]+ 匹配，支持 schema.name 和引号
# ============================================================

# 通用标识符模式（可匹配 schema.name、带引号名字等）
_IDENT = r'[\w."`\[\]]+'

DIALECT_PATTERNS = {
    SQLDialect.MYSQL: {
        'procedure': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?PROCEDURE\s+({_IDENT})\s*\(',
                re.IGNORECASE),
        ],
        'function': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+({_IDENT})\s*\([^)]*\)\s*RETURNS\s+\w+',
                re.IGNORECASE),
        ],
        'trigger': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?TRIGGER\s+({_IDENT})\s+(?:BEFORE|AFTER|INSTEAD\s+OF)\s+',
                re.IGNORECASE),
        ],
        'view': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?(?:ALGORITHM\s*=\s*\w+\s+)?VIEW\s+({_IDENT})\s*(?:\([^)]*\))?\s*AS\s+',
                re.IGNORECASE),
        ],
        'table': [
            re.compile(
                rf'CREATE\s+(?:TEMPORARY\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?({_IDENT})\s*\(',
                re.IGNORECASE),
        ],
        'event': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?EVENT\s+({_IDENT})\s+',
                re.IGNORECASE),
        ],
        'index': [
            re.compile(
                rf'CREATE\s+(?:ONLINE\s+)?(?:UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(
                rf'CREATE\s+(?:ONLINE\s+)?UNIQUE\s+INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'constraint': [
            re.compile(
                rf'ALTER\s+TABLE\s+({_IDENT})\s+ADD\s+(?:CONSTRAINT\s+)?({_IDENT})\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)',
                re.IGNORECASE),
        ],
    },

    SQLDialect.POSTGRESQL: {
        'procedure': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?PROCEDURE\s+({_IDENT})\s*\(',
                re.IGNORECASE),
        ],
        'function': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+({_IDENT})\s*\([^)]*\)\s*RETURNS\s+\w+',
                re.IGNORECASE),
        ],
        'trigger': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?TRIGGER\s+({_IDENT})\s+(?:BEFORE|AFTER|INSTEAD\s+OF)\s+',
                re.IGNORECASE),
        ],
        'view': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+({_IDENT})\s*(?:\([^)]*\))?\s*AS\s+',
                re.IGNORECASE),
        ],
        'table': [
            re.compile(
                rf'CREATE\s+(?:TEMP\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?({_IDENT})\s*\(',
                re.IGNORECASE),
        ],
        'materialized_view': [
            re.compile(
                rf'CREATE\s+(?:UNLOGGED\s+)?MATERIALIZED\s+VIEW\s+({_IDENT})\s*(?:\([^)]*\))?\s*AS\s+',
                re.IGNORECASE),
        ],
        'type': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?TYPE\s+({_IDENT})\s+AS\s+',
                re.IGNORECASE),
        ],
        'index': [
            re.compile(
                rf'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(
                rf'CREATE\s+UNIQUE\s+INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'constraint': [
            re.compile(
                rf'ALTER\s+TABLE\s+({_IDENT})\s+ADD\s+(?:CONSTRAINT\s+)?({_IDENT})\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)',
                re.IGNORECASE),
        ],
    },

    SQLDialect.ORACLE: {
        'procedure': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?PROCEDURE\s+({_IDENT})\s*(?:\([^)]*\))?\s*(?:IS|AS)\s+',
                re.IGNORECASE),
        ],
        'function': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?FUNCTION\s+({_IDENT})\s*(?:\([^)]*\))?\s*RETURN\s+\w+\s*(?:IS|AS)\s+',
                re.IGNORECASE),
        ],
        'trigger': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?TRIGGER\s+({_IDENT})\s+(?:BEFORE|AFTER|INSTEAD\s+OF|FOR\s+EACH\s+ROW)\s+',
                re.IGNORECASE),
        ],
        'view': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?(?:FORCE\s+)?VIEW\s+({_IDENT})\s*(?:\([^)]*\))?\s*AS\s+',
                re.IGNORECASE),
        ],
        'table': [
            re.compile(
                rf'CREATE\s+(?:GLOBAL\s+TEMPORARY\s+)?TABLE\s+({_IDENT})\s*\(',
                re.IGNORECASE),
        ],
        'package': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?(?:EDITIONABLE\s+)?PACKAGE\s+(?:BODY\s+)?({_IDENT})\s*(?:IS|AS)\s+',
                re.IGNORECASE),
        ],
        'synonym': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?(?:PUBLIC\s+)?SYNONYM\s+({_IDENT})\s+FOR\s+',
                re.IGNORECASE),
        ],
        'sequence': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?SEQUENCE\s+({_IDENT})\s+',
                re.IGNORECASE),
        ],
        'index': [
            re.compile(
                rf'CREATE\s+(?:UNIQUE\s+)?(?:BITMAP\s+)?INDEX\s+({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(
                rf'CREATE\s+UNIQUE\s+(?:BITMAP\s+)?INDEX\s+({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'constraint': [
            re.compile(
                rf'ALTER\s+TABLE\s+({_IDENT})\s+ADD\s+(?:CONSTRAINT\s+)?({_IDENT})\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)',
                re.IGNORECASE),
        ],
    },

    SQLDialect.SQLSERVER: {
        'procedure': [
            re.compile(
                rf'CREATE\s+(?:OR\s+ALTER\s+)?PROC(?:EDURE)?\s+(?:\[[\w]+\]\.)?\[?({_IDENT})\]?\s*(?:\(|@)',
                re.IGNORECASE),
            re.compile(
                rf'CREATE\s+(?:OR\s+ALTER\s+)?PROC(?:EDURE)?\s+({_IDENT})\s*(?:\(|@)',
                re.IGNORECASE),
        ],
        'function': [
            re.compile(
                rf'CREATE\s+(?:OR\s+ALTER\s+)?FUNCTION\s+(?:\[[\w]+\]\.)?\[?({_IDENT})\]?\s*\([^)]*\)\s*RETURNS\s+',
                re.IGNORECASE),
        ],
        'trigger': [
            re.compile(
                rf'CREATE\s+(?:OR\s+ALTER\s+)?TRIGGER\s+(?:\[[\w]+\]\.)?\[?({_IDENT})\]?\s+ON\s+',
                re.IGNORECASE),
        ],
        'view': [
            re.compile(
                rf'CREATE\s+(?:OR\s+ALTER\s+)?VIEW\s+(?:\[[\w]+\]\.)?\[?({_IDENT})\]?\s*(?:\([^)]*\))?\s*AS\s+',
                re.IGNORECASE),
        ],
        'table': [
            re.compile(
                rf'CREATE\s+TABLE\s+(?:\[[\w]+\]\.)?\[?({_IDENT})\]?\s*\(',
                re.IGNORECASE),
        ],
        'type': [
            re.compile(
                rf'CREATE\s+TYPE\s+(?:\[[\w]+\]\.)?\[?({_IDENT})\]?\s+AS\s+',
                re.IGNORECASE),
        ],
        'index': [
            re.compile(
                rf'CREATE\s+(?:UNIQUE\s+)?(?:CLUSTERED|NONCLUSTERED\s+)?INDEX\s+\[?({_IDENT})\]?\s+ON\s+(?:\[[\w]+\]\.)?\[?({_IDENT})\]?',
                re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(
                rf'CREATE\s+UNIQUE\s+(?:CLUSTERED|NONCLUSTERED\s+)?INDEX\s+\[?({_IDENT})\]?\s+ON\s+(?:\[[\w]+\]\.)?\[?({_IDENT})\]?',
                re.IGNORECASE),
        ],
        'constraint': [
            re.compile(
                rf'ALTER\s+TABLE\s+(?:\[[\w]+\]\.)?\[?({_IDENT})\]?\s+ADD\s+(?:CONSTRAINT\s+)?\[?({_IDENT})\]?\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)',
                re.IGNORECASE),
        ],
    },

    SQLDialect.DM: {
        'procedure': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?PROCEDURE\s+({_IDENT})\s*(?:\([^)]*\))?\s*(?:IS|AS)\s+',
                re.IGNORECASE),
        ],
        'function': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+({_IDENT})\s*(?:\([^)]*\))?\s*RETURN\s+\w+\s*(?:IS|AS)\s+',
                re.IGNORECASE),
        ],
        'trigger': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?TRIGGER\s+({_IDENT})\s+(?:BEFORE|AFTER|INSTEAD\s+OF)\s+',
                re.IGNORECASE),
        ],
        'view': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+({_IDENT})\s*(?:\([^)]*\))?\s*AS\s+',
                re.IGNORECASE),
        ],
        'table': [
            re.compile(
                rf'CREATE\s+(?:GLOBAL\s+TEMPORARY\s+)?TABLE\s+({_IDENT})\s*\(',
                re.IGNORECASE),
        ],
        'package': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?PACKAGE\s+(?:BODY\s+)?({_IDENT})\s*(?:IS|AS)\s+',
                re.IGNORECASE),
        ],
        'sequence': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?SEQUENCE\s+({_IDENT})\s+',
                re.IGNORECASE),
        ],
        'index': [
            re.compile(
                rf'CREATE\s+(?:UNIQUE\s+)?(?:BITMAP\s+)?INDEX\s+({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(
                rf'CREATE\s+UNIQUE\s+(?:BITMAP\s+)?INDEX\s+({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'constraint': [
            re.compile(
                rf'ALTER\s+TABLE\s+({_IDENT})\s+ADD\s+(?:CONSTRAINT\s+)?({_IDENT})\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)',
                re.IGNORECASE),
        ],
    },

    SQLDialect.GENERIC: {
        'procedure': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?PROCEDURE\s+({_IDENT})\s*[\(\w\s,@=]',
                re.IGNORECASE),
        ],
        'function': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+({_IDENT})\s*(?:\([^)]*\))?\s*RETURN',
                re.IGNORECASE),
        ],
        'trigger': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?TRIGGER\s+({_IDENT})\s+(?:BEFORE|AFTER|INSTEAD\s+OF)\s+',
                re.IGNORECASE),
        ],
        'view': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+({_IDENT})\s*(?:\([^)]*\))?\s*AS\s+',
                re.IGNORECASE),
        ],
        'table': [
            re.compile(
                rf'CREATE\s+(?:TEMP(?:ORARY)?\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?({_IDENT})\s*\(',
                re.IGNORECASE),
        ],
        'package': [
            re.compile(
                rf'CREATE\s+(?:OR\s+REPLACE\s+)?PACKAGE\s+(?:BODY\s+)?({_IDENT})\s+(?:IS|AS)\s+',
                re.IGNORECASE),
        ],
        'index': [
            re.compile(
                rf'CREATE\s+(?:UNIQUE\s+)?INDEX\s+({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'unique_index': [
            re.compile(
                rf'CREATE\s+UNIQUE\s+INDEX\s+({_IDENT})\s+ON\s+({_IDENT})',
                re.IGNORECASE),
        ],
        'constraint': [
            re.compile(
                rf'ALTER\s+TABLE\s+({_IDENT})\s+ADD\s+(?:CONSTRAINT\s+)?({_IDENT})\s+(?:PRIMARY|UNIQUE|FOREIGN|CHECK)',
                re.IGNORECASE),
        ],
    },
}


# ============================================================
# 方言检测
# ============================================================

def detect_dialect(sql_content: str) -> SQLDialect:
    """自动检测 SQL 方言"""
    sql_upper = sql_content.upper()

    # Oracle 特征
    # 1. 有 / 终止符 + PL/SQL 语法
    if re.search(r'^/\s*$', sql_content, re.MULTILINE):
        # / 是 Oracle/DM 特有的，再看 IS/AS 语法区分 Oracle vs DM
        if re.search(r'\b(?:PROCEDURE|FUNCTION)\s+[\w."]+\s*(?:\([^)]*\))?\s*(?:IS|AS)\s+', sql_upper):
            # DM 用双引号标识符较多；Oracle 更多用 EDITIONABLE, SYNONYM
            if re.search(r'\bEDITIONABLE\b', sql_upper):
                return SQLDialect.ORACLE
            if re.search(r'\bSYNONYM\s+[\w."]+\s+FOR\b', sql_upper):
                return SQLDialect.ORACLE
            if re.search(r'\bPACKAGE\s+(?:BODY\s+)?[\w."]+\s+(?:IS|AS)\b', sql_upper):
                return SQLDialect.ORACLE
            # 有 / 终止符 + PROCEDURE IS/AS 但无 DM 明显特征 → 默认 Oracle
            return SQLDialect.ORACLE
    if re.search(r'\bEDITIONABLE\b', sql_upper):
        return SQLDialect.ORACLE
    if re.search(r'\bSYNONYM\s+[\w."]+\s+FOR\b', sql_upper):
        return SQLDialect.ORACLE

    # SQL Server 特征
    if re.search(r'^GO\s*$', sql_content, re.IGNORECASE | re.MULTILINE):
        return SQLDialect.SQLSERVER
    if re.search(r'\bCREATE\s+PROC\s+[\w.\[\]]+', sql_upper):
        return SQLDialect.SQLSERVER
    if re.search(r'\bALTER\s+PROC(?:EDURE)?\s+', sql_upper):
        return SQLDialect.SQLSERVER

    # PostgreSQL 特征
    if re.search(r'\$\$', sql_content):
        return SQLDialect.POSTGRESQL
    if re.search(r'\bLANGUAGE\s+(?:plpgsql|plpython|plperl)\b', sql_upper):
        return SQLDialect.POSTGRESQL
    if re.search(r'\bMATERIALIZED\s+VIEW\b', sql_upper):
        return SQLDialect.POSTGRESQL
    if re.search(r'\bRETURNS\s+(?:SETOF|TABLE)\b', sql_upper):
        return SQLDialect.POSTGRESQL

    # MySQL 特征
    if re.search(r'`[\w]+`', sql_content):
        if re.search(r'\bENGINE\s*=\s*\w+\b', sql_upper):
            return SQLDialect.MYSQL
    if re.search(r'\bCREATE\s+(?:OR\s+REPLACE\s+)?EVENT\b', sql_upper):
        return SQLDialect.MYSQL
    if re.search(r'\bALGORITHM\s*=\s*(?:UNDEFINED|MERGE|TEMPTABLE)\b', sql_upper):
        return SQLDialect.MYSQL

    # 达梦特征
    if re.search(r'"[\w.]+"\s*\(', sql_content):
        if re.search(r'\b(?:IS|AS)\s*BEGIN\b', sql_upper):
            return SQLDialect.DM

    return SQLDialect.GENERIC


# ============================================================
# 对象边界检测（核心重写）
# ============================================================

def find_block_end(sql: str, start: int, dialect: SQLDialect) -> int:
    """
    对需要 BEGIN...END 的对象类型（存储过程、函数、触发器、包），
    使用深度匹配找到完整块结束位置。

    返回 END; 或 / 之后的偏移量。
    """
    n = len(sql)

    # Oracle/DM: 先找 / 终止符
    if dialect in (SQLDialect.ORACLE, SQLDialect.DM):
        # 从 start 开始，找独立一行的 /
        i = start
        while i < n:
            # 跳过字符串
            if sql[i] in ("'", '"'):
                i = _skip_quoted(sql, i, n)
                continue
            # 匹配 ^/\s*$
            if sql[i] == '/' and (i == 0 or sql[i-1] == '\n'):
                # 检查 / 后面到行尾只有空白
                j = i + 1
                while j < n and sql[j] in ' \t\r':
                    j += 1
                if j >= n or sql[j] == '\n':
                    return j + 1 if j < n else j
            i += 1

    # SQL Server: 找 GO
    if dialect == SQLDialect.SQLSERVER:
        go_pat = re.compile(r'^GO\s*$', re.IGNORECASE | re.MULTILINE)
        m = go_pat.search(sql, start)
        if m:
            return m.end()

    # PostgreSQL: $$ 包裹语法
    if dialect == SQLDialect.POSTGRESQL:
        # 先尝试 $$...$$
        dollar_start = sql.find('$$', start)
        if dollar_start != -1:
            dollar_end = sql.find('$$', dollar_start + 2)
            if dollar_end != -1:
                # $$ 结束后可能有分号
                after = dollar_end + 2
                while after < n and sql[after] in ' \t\r\n':
                    after += 1
                if after < n and sql[after] == ';':
                    after += 1
                return after
        # 也可能用 BEGIN...END（plpgsql）
        return find_matching_end(sql, start, n)

    # 通用: BEGIN...END 深度匹配
    return find_matching_end(sql, start, n)


def _skip_quoted(sql: str, start: int, bound: int) -> int:
    """跳过引号内容，返回引号结束后的位置"""
    quote = sql[start]
    i = start + 1
    while i < bound:
        if sql[i] == quote:
            if i + 1 < bound and sql[i + 1] == quote:
                i += 2
                continue
            return i + 1
        i += 1
    return i


def find_semicolon_end(sql: str, start: int, bound: int, dialect: SQLDialect = SQLDialect.GENERIC) -> int:
    """简单语句：找到分号或GO分隔符后返回"""
    import re as _re
    i = start
    while i < bound:
        if sql[i] in ("'", '"'):
            i = _skip_quoted(sql, i, bound)
            continue
        if sql[i] == '-' and i + 1 < bound and sql[i + 1] == '-':
            while i < bound and sql[i] != '\n':
                i += 1
            continue
        if sql[i] == '/' and i + 1 < bound and sql[i + 1] == '*':
            i += 2
            while i + 1 < bound and not (sql[i] == '*' and sql[i + 1] == '/'):
                i += 1
            i += 2
            continue
        if sql[i] == ';':
            return i + 1
        # SQL Server: 识别行首GO作为对象结束标记
        if dialect == SQLDialect.SQLSERVER and sql[i] in ('G', 'g'):
            # 检查是否是行首的GO
            line_start = sql.rfind('\n', 0, i)
            if line_start == -1:
                line_start = 0
            before = sql[line_start:i].strip()
            if before == '' or before == '\r':
                rest = sql[i:i+10]
                m = _re.match(r'GO\s*(?:\r?\n|$)', rest, _re.IGNORECASE)
                if m:
                    # GO后面可能有换行，返回GO结束位置
                    return i + len(m.group(0))
        i += 1
    return bound

def find_paren_end(sql: str, start: int, bound: int, dialect: SQLDialect = SQLDialect.GENERIC) -> int:
    """匹配括号，找到 ) 后的分号或GO（用于 CREATE TABLE）"""
    import re as _re
    i = start
    depth = 0
    while i < bound:
        if sql[i] in ("'", '"'):
            i = _skip_quoted(sql, i, bound)
            continue
        if sql[i] == '-' and i + 1 < bound and sql[i + 1] == '-':
            while i < bound and sql[i] != '\n':
                i += 1
            continue
        if sql[i] == '/' and i + 1 < bound and sql[i + 1] == '*':
            i += 2
            while i + 1 < bound and not (sql[i] == '*' and sql[i + 1] == '/'):
                i += 1
            i += 2
            continue
        if sql[i] == '(':
            depth += 1
        elif sql[i] == ')':
            depth -= 1
            if depth == 0:
                # 找到匹配的 )，继续找分号或GO
                j = i + 1
                while j < bound and sql[j] in ' \t\r\n':
                    j += 1
                # 可能有表级约束 / storage 参数在 ) 后面
                # 比如 ON [PRIMARY] 等
                # 先检查 ) 后面到下一个GO或分号之间的内容
                return find_semicolon_end(sql, j, bound, dialect)
        i += 1
    return bound

def find_view_end(sql: str, start: int, bound: int, dialect: SQLDialect = SQLDialect.GENERIC) -> int:
    """视图：找 AS 之后的第一个分号或GO（需考虑子查询中的 AS）"""
    # 视图的 AS 后面是 SELECT 语句，分号或GO就是结束
    # 但需要跳过子查询中的 AS
    return find_semicolon_end(sql, start, bound, dialect)


def find_object_end(sql: str, dialect: SQLDialect, obj_type: str, start: int) -> int:
    """
    查找对象的结束位置（核心调度函数）。
    不再依赖 next_create_pos 作为上界，直接扫描到文件末尾。
    """
    n = len(sql)

    if obj_type in BLOCK_OBJECT_TYPES:
        return find_block_end(sql, start, dialect)

    if obj_type == 'table':
        paren_pos = sql.find('(', start)
        if paren_pos != -1 and paren_pos < n:
            return find_paren_end(sql, paren_pos, n, dialect)
        return find_semicolon_end(sql, start, n, dialect)

    if obj_type in ('view', 'materialized_view'):
        return find_view_end(sql, start, n, dialect)

    if obj_type in ('index', 'unique_index', 'constraint', 'synonym', 'sequence', 'event'):
        return find_semicolon_end(sql, start, n, dialect)

    # 兜底
    return find_semicolon_end(sql, start, n, dialect)


# ============================================================
# 主拆分逻辑
# ============================================================

def split_sql_file(
    input_file: str,
    output_dir: Optional[str] = None,
    dialect: Optional[SQLDialect] = None,
    verbose: bool = True,
    generate_merge: bool = True,
) -> Dict:
    """拆分 SQL 文件"""
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            sql_content = f.read()
    except Exception as e:
        return {
            'output_dir': None,
            'created_files': [],
            'errors': [f"无法读取文件: {e}"],
            'stats': {},
            'total': 0,
        }

    if dialect is None:
        dialect = detect_dialect(sql_content)

    if verbose:
        print(f"[detect] 方言: {dialect.value.upper()}")

    if output_dir is None:
        output_dir = os.path.splitext(input_file)[0] + '_split'

    os.makedirs(output_dir, exist_ok=True)

    patterns = DIALECT_PATTERNS.get(dialect, DIALECT_PATTERNS[SQLDialect.GENERIC])

    # ---- 收集所有对象 ----
    found_objects = []
    for obj_type, pattern_list in patterns.items():
        for pattern in pattern_list:
            for match in pattern.finditer(sql_content):
                name = clean_object_name(match.group(1))
                found_objects.append({
                    'type': obj_type,
                    'name': name,
                    'start': match.start(),
                    'match': match,
                })

    # 按位置排序
    found_objects.sort(key=lambda x: x['start'])

    # 去重：同一位置、同一类型、同一名称的对象只保留一个
    seen = set()
    unique_objects = []
    for obj in found_objects:
        key = (obj['start'], obj['type'], obj['name'])
        if key not in seen:
            seen.add(key)
            unique_objects.append(obj)
    found_objects = unique_objects

    if verbose:
        print(f"[scan] 找到 {len(found_objects)} 个对象")

    # ---- 提取并保存每个对象 ----
    created_files = []
    errors = []
    stats = defaultdict(int)
    all_objects_info = []  # 用于依赖分析

    for obj in found_objects:
        end_pos = find_object_end(sql_content, dialect, obj['type'], obj['start'])

        obj_content = sql_content[obj['start']:end_pos].strip()

        # 去掉末尾的 / (Oracle/DM 终止符)
        if dialect in (SQLDialect.ORACLE, SQLDialect.DM):
            obj_content = re.sub(r'\n/\s*$', '', obj_content)

        if not obj_content:
            continue

        prefix = OBJECT_PREFIXES.get(obj['type'], 'obj')
        filename = f"{prefix}_{obj['name']}.sql"
        filepath = os.path.join(output_dir, filename)

        # 处理同名文件（追加序号）
        if os.path.exists(filepath):
            seq = 2
            while os.path.exists(f"{prefix}_{obj['name']}_{seq}.sql"):
                seq += 1
            filename = f"{prefix}_{obj['name']}_{seq}.sql"
            filepath = os.path.join(output_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(obj_content)
                if not obj_content.rstrip().endswith(';'):
                    # Oracle/DM 不强制加分号（用 / 代替）
                    if dialect not in (SQLDialect.ORACLE, SQLDialect.DM):
                        f.write(';')
                f.write('\n')
            created_files.append(filepath)
            stats[obj['type']] += 1
            all_objects_info.append({
                'type': obj['type'],
                'name': obj['name'],
                'content': obj_content,
                'filename': filename,
            })
            if verbose:
                print(f"  [ok] {filename}")
        except Exception as e:
            errors.append(f"写入 {filename} 失败: {e}")

    # ---- 生成依赖排序的合并脚本 ----
    merge_script_path = None
    if generate_merge and all_objects_info:
        try:
            from dependency_analyzer import DependencyAnalyzer
            analyzer = DependencyAnalyzer(dialect)
            for obj_info in all_objects_info:
                analyzer.add_object(obj_info['type'], obj_info['name'], obj_info['content'])
            analyzer.analyze_all()
            merge_script_path = os.path.join(output_dir, 'merge_all.sql')
            analyzer.generate_merge_script(merge_script_path, output_dir, dialect=dialect)
            if verbose:
                print(f"  [merge] 已生成 {merge_script_path}")
        except ImportError:
            if verbose:
                print("  [skip] 依赖分析器不可用，跳过合并脚本生成")
        except Exception as e:
            if verbose:
                print(f"  [warn] 合并脚本生成失败: {e}")

    return {
        'output_dir': output_dir,
        'created_files': created_files,
        'errors': errors,
        'stats': dict(stats),
        'total': len(created_files),
        'merge_script': merge_script_path,
    }


def split_sql_batch(
    input_paths,
    output_dir: Optional[str] = None,
    dialect: Optional[SQLDialect] = None,
    verbose: bool = True,
) -> List[Dict]:
    """批量拆分 SQL 文件"""
    results = []

    for input_path in input_paths:
        if os.path.isdir(input_path):
            for filename in os.listdir(input_path):
                if filename.lower().endswith('.sql'):
                    filepath = os.path.join(input_path, filename)
                    result = split_sql_file(filepath, output_dir, dialect, verbose)
                    results.append(result)
        else:
            result = split_sql_file(input_path, output_dir, dialect, verbose)
            results.append(result)

    return results


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='SQL 文件拆分工具 v2.0')
    parser.add_argument('input', help='输入 SQL 文件或目录')
    parser.add_argument('output', nargs='?', help='输出目录')
    parser.add_argument('--batch', action='store_true', help='批量处理目录')
    parser.add_argument('--dialect',
                        choices=['mysql', 'postgresql', 'oracle', 'sqlserver', 'dm', 'generic'],
                        help='指定 SQL 方言')
    parser.add_argument('--no-merge', action='store_true', help='不生成合并脚本')
    parser.add_argument('-q', '--quiet', action='store_true', help='静默模式')

    args = parser.parse_args()

    dialect_map = {
        'mysql': SQLDialect.MYSQL,
        'postgresql': SQLDialect.POSTGRESQL,
        'oracle': SQLDialect.ORACLE,
        'sqlserver': SQLDialect.SQLSERVER,
        'dm': SQLDialect.DM,
        'generic': SQLDialect.GENERIC,
    }

    dialect = dialect_map.get(args.dialect) if args.dialect else None
    verbose = not args.quiet
    generate_merge = not args.no_merge

    if args.batch:
        input_paths = [args.input] if ',' not in args.input else args.input.split(',')
        results = split_sql_batch(input_paths, args.output, dialect, verbose)
        total_files = sum(r['total'] for r in results)
        print(f"\n[done] 共创建 {total_files} 个文件")
    else:
        result = split_sql_file(args.input, args.output, dialect, verbose, generate_merge)
        if result['errors']:
            print("\n[error]")
            for err in result['errors']:
                print(f"  {err}")
        print(f"\n[done] 共创建 {result['total']} 个文件")


if __name__ == '__main__':
    main()
