#!/usr/bin/env python3
"""
SQL 文件拆分工具 - 多数据库方言支持
支持 MySQL, PostgreSQL, Oracle, SQL Server, 达梦(DM) 等数据库

v2.1 新功能:
- 集成详细错误处理和修复建议
- 添加进度条显示（支持 tqdm）
- 支持 dry-run 预览模式
- 返回结构化的 SplitResult 对象

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

# 尝试导入 tqdm，如果不可用则使用简单进度显示
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


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


def find_semicolon_end(sql: str, start: int, bound: int, dialect: SQLDialect = None) -> int:
    """简单语句：找到分号或GO终止符后返回
    
    对于 SQL Server，GO 是对象的终止符，优先级高于分号。
    """
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
        # SQL Server: GO 也是终止符
        if dialect == SQLDialect.SQLSERVER and sql[i] in ('G', 'g'):
            # 检查是否为独立一行的 GO
            line_start = i
            # 回退到行首
            while line_start > 0 and sql[line_start - 1] != '\n':
                line_start -= 1
            # 检查行首到当前位置是否只有空白+GO
            prefix = sql[line_start:i]
            if prefix.strip() == '':
                # 检查GO后面
                j = i
                go_len = 0
                while j < bound and go_len < 2 and sql[j] in ('G', 'g', 'O', 'o'):
                    j += 1
                    go_len += 1
                if go_len == 2:
                    # 检查GO后面到行尾只有空白
                    k = j
                    while k < bound and sql[k] in ' \t\r':
                        k += 1
                    if k >= bound or sql[k] == '\n':
                        return k + 1 if k < bound else k
        i += 1
    return bound


def find_paren_end(sql: str, start: int, bound: int, dialect: SQLDialect = None) -> int:
    """匹配括号，找到 ) 后的分号或GO终止符（用于 CREATE TABLE）
    
    对于 SQL Server，表定义以 GO 结束（如 ) ON [PRIMARY] GO），
    需要在右括号后找到 GO 而非分号。
    """
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
                # 找到匹配的 )，继续找到分号或GO终止符
                # 可能有表级约束 / storage 参数在 ) 后面（如 ON [PRIMARY]）
                j = i + 1
                return find_semicolon_end(sql, j, bound, dialect=dialect)
        i += 1
    return bound


def find_view_end(sql: str, start: int, bound: int, dialect: SQLDialect = None) -> int:
    """视图：找 AS 之后的第一个分号或GO终止符（需考虑子查询中的 AS）
    
    对于 SQL Server，视图也以 GO 结束。
    """
    return find_semicolon_end(sql, start, bound, dialect=dialect)


def find_object_end(sql: str, dialect: SQLDialect, obj_type: str, start: int) -> int:
    """
    查找对象的结束位置（核心调度函数）。
    不再依赖 next_create_pos 作为上界，直接扫描到文件末尾。
    
    对于 SQL Server，所有非 BLOCK 对象（table/view/index/constraint等）
    都以 GO 终止符结束，而非分号。必须把 dialect 传递到各子函数中。
    """
    n = len(sql)

    if obj_type in BLOCK_OBJECT_TYPES:
        return find_block_end(sql, start, dialect)

    if obj_type == 'table':
        paren_pos = sql.find('(', start)
        if paren_pos != -1 and paren_pos < n:
            return find_paren_end(sql, paren_pos, n, dialect=dialect)
        return find_semicolon_end(sql, start, n, dialect=dialect)

    if obj_type in ('view', 'materialized_view'):
        return find_view_end(sql, start, n, dialect=dialect)

    if obj_type in ('index', 'unique_index', 'constraint', 'synonym', 'sequence', 'event'):
        return find_semicolon_end(sql, start, n, dialect=dialect)

    # 兜底
    return find_semicolon_end(sql, start, n, dialect=dialect)


# ============================================================
# 文件读取（自动编码检测）
# ============================================================

def _read_sql_file(filepath: str) -> str:
    """读取 SQL 文件，自动检测编码。
    
    SQL Server 导出的脚本通常是 UTF-16 LE 编码（带 BOM），
    而 MySQL/PostgreSQL 通常是 UTF-8。本函数依次尝试：
    1. UTF-8 (最常见)
    2. UTF-16 LE (SQL Server 导出)
    3. UTF-16 BE
    4. Latin-1 (兜底，不会解码失败)
    """
    # 先读取原始字节来检测BOM
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    # BOM 检测
    if raw[:2] == b'\xff\xfe':
        # UTF-16 LE BOM
        return raw.decode('utf-16-le').lstrip('\ufeff')
    if raw[:2] == b'\xfe\xff':
        # UTF-16 BE BOM
        return raw.decode('utf-16-be').lstrip('\ufeff')
    if raw[:3] == b'\xef\xbb\xbf':
        # UTF-8 BOM
        return raw[3:].decode('utf-8', errors='replace')
    
    # 无BOM：尝试UTF-8，如果失败则用Latin-1兜底
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('latin-1')


# ============================================================
# 主拆分逻辑
# ============================================================

def split_sql_file(
    input_file: str,
    output_dir: Optional[str] = None,
    dialect: Optional[SQLDialect] = None,
    verbose: bool = True,
    generate_merge: bool = True,
    dry_run: bool = False,
    show_progress: bool = True,
    convert_to: Optional[str] = None,
) -> SplitResult:
    """
    拆分 SQL 文件（增强版）
    
    Args:
        input_file: 输入文件路径
        output_dir: 输出目录（可选）
        dialect: SQL方言（可选，自动检测）
        verbose: 是否显示详细信息
        generate_merge: 是否生成合并脚本
        dry_run: 预览模式，不实际生成文件
        show_progress: 是否显示进度条
        convert_to: 转换目标方言（可选，如 'dm' 将SQL Server拆分结果转换为达梦语法）
    
    Returns:
        SplitResult: 拆分结果对象
    """
    errors = []
    warnings = []
    created_files = []
    stats = defaultdict(int)
    
    # 读取文件（自动检测编码，支持 UTF-16 LE 等 SQL Server 导出格式）
    try:
        sql_content = _read_sql_file(input_file)
    except Exception as e:
        errors.append(ErrorHandler.create_file_read_error(input_file, str(e)))
        return SplitResult(
            success=False,
            output_dir=None,
            files_created=[],
            errors=errors,
            warnings=warnings,
            stats={},
            total=0,
            dry_run=dry_run,
        )

    if dialect is None:
        dialect = detect_dialect(sql_content)

    if verbose:
        print(f"[detect] 方言: {dialect.value.upper()}")

    if output_dir is None:
        output_dir = os.path.splitext(input_file)[0] + '_split'

    if not dry_run:
        os.makedirs(output_dir, exist_ok=True)
    elif verbose:
        print(f"[dry-run] 预览模式：将输出到 {output_dir}")

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

    # ---- 社区版限制检查 ----
    try:
        from license_checker import check_object_limit, check_file_size
    except ImportError:
        from .license_checker import check_object_limit, check_file_size

    file_size = len(sql_content.encode('utf-8')) if isinstance(sql_content, str) else os.path.getsize(input_file)
    size_allowed, size_msg = check_file_size(file_size)
    if not size_allowed:
        print(size_msg)
        return SplitResult(
            success=False, output_dir=None, files_created=[],
            errors=[ErrorHandler.create_file_read_error(input_file, '文件大小超出社区版限制，升级专业版: https://sqlsplitter.com')],
            warnings=[], stats={}, total=len(found_objects), dry_run=dry_run,
        )

    obj_allowed, obj_msg = check_object_limit(len(found_objects))
    if not obj_allowed:
        print(obj_msg)
        return SplitResult(
            success=False, output_dir=None, files_created=[],
            errors=[ErrorHandler.create_file_read_error(input_file, '对象数量超出社区版限制，升级专业版: https://sqlsplitter.com')],
            warnings=[], stats={}, total=len(found_objects), dry_run=dry_run,
        )

    # ---- 提取并保存每个对象 ----
    all_objects_info = [] # 用于依赖分析

    # 创建进度条
    if show_progress and HAS_TQDM and len(found_objects) > 0:
        iterator = tqdm(found_objects, desc="拆分对象", unit="个")
    else:
        iterator = found_objects

    for obj in iterator:
        end_pos = find_object_end(sql_content, dialect, obj['type'], obj['start'])

        obj_content = sql_content[obj['start']:end_pos].strip()

        # 去掉末尾的 / (Oracle/DM 终止符)
        if dialect in (SQLDialect.ORACLE, SQLDialect.DM):
            obj_content = re.sub(r'\n/\s*$', '', obj_content)

        # 对于 procedure/function/view/trigger，自动添加 OR REPLACE
        # 达梦和Oracle要求这些对象使用 CREATE OR REPLACE，否则对象已存在时会报错
        if obj['type'] in ('procedure', 'function', 'view', 'trigger'):
            obj_content = re.sub(
                r'\bCREATE\s+(PROC(?:EDURE)?|FUNC(?:TION)?|VIEW|TRIGGER)\b',
                r'CREATE OR REPLACE \1',
                obj_content,
                count=1,
                flags=re.IGNORECASE
            )

        if not obj_content:
            continue

        prefix = OBJECT_PREFIXES.get(obj['type'], 'obj')
        # 安全校验: 对象名中不应含路径分隔符或..
        safe_name = obj['name'].replace('/', '_').replace('\\', '_').replace('..', '_')
        filename = f"{prefix}_{safe_name}.sql"
        filepath = os.path.join(output_dir, filename)
        # 二次校验: 确保写入路径在输出目录内
        if not dry_run:
            file_realpath = os.path.realpath(filepath)
            output_realpath = os.path.realpath(output_dir)
            if not file_realpath.startswith(output_realpath + os.sep):
                if verbose:
                    print(f" [warn] 路径遍历风险，已安全化对象名: {obj['name']} -> {safe_name}")

        # 处理同名文件（追加序号）
        if not dry_run and os.path.exists(filepath):
            seq = 2
            while os.path.exists(f"{prefix}_{safe_name}_{seq}.sql"):
                seq += 1
            filename = f"{prefix}_{safe_name}_{seq}.sql"
            filepath = os.path.join(output_dir, filename)

        try:
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(obj_content)
                    if not obj_content.rstrip().endswith(';'):
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
                mode_str = "[dry-run] " if dry_run else ""
                print(f" {mode_str}[ok] {filename}")
        except Exception as e:
            error = ErrorHandler.create_file_write_error(filename, str(e))
            errors.append(error)
            if verbose:
                print(f" [error] {filename}: {e}")

    # ---- 生成依赖排序的合并脚本 ----
    merge_script_path = None
    if generate_merge and all_objects_info and not dry_run:
        try:
            from dependency_analyzer import DependencyAnalyzer
            analyzer = DependencyAnalyzer(dialect)
            for obj_info in all_objects_info:
                analyzer.add_object(obj_info['type'], obj_info['name'], obj_info['content'])
            analyzer.analyze_all()
            merge_script_path = os.path.join(output_dir, 'merge_all.sql')
            analyzer.generate_merge_script(merge_script_path, output_dir, dialect=dialect)
            if verbose:
                print(f" [merge] 已生成 {merge_script_path}")
        except ImportError:
            if verbose:
                print(" [skip] 依赖分析器不可用，跳过合并脚本生成")
        except Exception as e:
            warning = ErrorHandler.create_warning(f"合并脚本生成失败: {e}")
            warnings.append(warning)
            if verbose:
                print(f" [warn] 合并脚本生成失败: {e}")

    # ---- 拆分后转换 ----
    converted_dir = None
    converted_files = []
    if convert_to and not dry_run and all_objects_info:
        converted_dir, converted_files = _convert_split_output(
            output_dir, all_objects_info, convert_to, dialect, verbose
        )

    # 返回结构化结果
    success = len(errors) == 0
    return SplitResult(
        success=success,
        output_dir=output_dir,
        files_created=created_files,
        errors=errors,
        warnings=warnings,
        stats=dict(stats),
        total=len(created_files),
        merge_script=merge_script_path,
        dry_run=dry_run,
    )


def _convert_split_output(
    output_dir: str,
    all_objects_info: List[Dict],
    target_dialect: str,
    source_dialect: SQLDialect,
    verbose: bool = True,
) -> Tuple[Optional[str], List[str]]:
    """
    将拆分后的文件转换为目标方言，输出到子目录
    
    Args:
        output_dir: 拆分输出目录
        all_objects_info: 对象信息列表
        target_dialect: 目标方言 ('dm')
        source_dialect: 源方言
        verbose: 是否显示详细信息
    
    Returns:
        (converted_dir, converted_files) 转换目录和文件列表
    """
    target = target_dialect.lower()
    
    # 目前只支持 sqlserver -> dm
    if target != 'dm':
        if verbose:
            print(f" [skip] 不支持转换到 {target_dialect}")
        return None, []
    
    if source_dialect != SQLDialect.SQLSERVER:
        if verbose:
            print(f" [skip] 当前仅支持 SQL Server -> 达梦，源方言为 {source_dialect.value}")
        return None, []
    
    try:
        from dm_converter import convert_sqlserver_to_dm_with_result, ConversionType
    except ImportError:
        if verbose:
            print(" [skip] dm_converter 模块不可用，跳过转换")
        return None, []
    
    # 转换输出目录: output_split -> output_split_dm
    converted_dir = output_dir.rstrip('/') + '_dm'
    os.makedirs(converted_dir, exist_ok=True)
    
    converted_files = []
    total_changes = 0
    
    if verbose:
        print(f"\n[convert] SQL Server -> 达梦数据库")
        print(f" [dir] 转换输出: {converted_dir}")
    
    for obj_info in all_objects_info:
        obj_type = obj_info['type']
        obj_content = obj_info['content']
        filename = obj_info['filename']
        
        # 对象类型映射到转换类型
        type_map = {
            'procedure': 'procedure',
            'function': 'function',
            'view': 'view',
            'trigger': 'trigger',
            'table': 'table',
            'index': 'index',
            'unique_index': 'index',
            'constraint': 'constraint',
            'sequence': 'sequence',
        }
        conv_type = type_map.get(obj_type, 'generic')
        
        # 执行转换
        result = convert_sqlserver_to_dm_with_result(obj_content, conv_type)
        
        # 写入转换后的文件
        # 安全校验: 防止路径遍历 (filename中不应含..或路径分隔符)
        safe_filename = filename.replace('/', '_').replace('\\', '_').replace('..', '_')
        if safe_filename != filename:
            if verbose:
                print(f" [warn] 文件名含路径字符，已安全化: {filename} -> {safe_filename}")
            filename = safe_filename
        conv_filepath = os.path.join(converted_dir, filename)
        # 二次校验: 确保写入路径在目标目录内
        conv_realpath = os.path.realpath(conv_filepath)
        converted_dir_real = os.path.realpath(converted_dir)
        if not conv_realpath.startswith(converted_dir_real + os.sep) and conv_realpath != converted_dir_real:
            if verbose:
                print(f" [error] 路径遍历风险，跳过: {filename}")
            continue
        try:
            with open(conv_filepath, 'w', encoding='utf-8') as f:
                f.write(result.converted)
                f.write('\n')
            converted_files.append(conv_filepath)
            total_changes += result.change_count
            
            if verbose:
                change_info = f" ({result.change_count}处转换)" if result.has_changes else " (无需转换)"
                print(f" [ok] {filename}{change_info}")
        except Exception as e:
            if verbose:
                print(f" [error] {filename}: {e}")
    
    # 生成达梦版合并脚本
    if converted_files:
        _generate_dm_merge_script(converted_dir, all_objects_info, verbose)
    
    if verbose:
        print(f"\n[convert] 完成! 共 {len(converted_files)} 个文件, {total_changes} 处转换")
        print(f" [dir] 原始拆分: {output_dir}/")
        print(f" [dir] 达梦版本: {converted_dir}/")
    
    return converted_dir, converted_files


def _generate_dm_merge_script(converted_dir: str, all_objects_info: List[Dict], verbose: bool = True):
    """为达梦转换结果生成合并脚本"""
    try:
        from dependency_analyzer import DependencyAnalyzer
        analyzer = DependencyAnalyzer(SQLDialect.DM)
        for obj_info in all_objects_info:
            analyzer.add_object(obj_info['type'], obj_info['name'], obj_info['content'])
        analyzer.analyze_all()
        merge_path = os.path.join(converted_dir, 'merge_all.sql')
        analyzer.generate_merge_script(merge_path, converted_dir, dialect=SQLDialect.DM)
        if verbose:
            print(f" [merge] 已生成达梦版合并脚本: {merge_path}")
    except ImportError:
        if verbose:
            print(" [skip] 依赖分析器不可用，跳过达梦版合并脚本生成")
    except Exception as e:
        if verbose:
            print(f" [warn] 达梦版合并脚本生成失败: {e}")


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

    parser = argparse.ArgumentParser(description='SQL 文件拆分工具 v2.1')
    parser.add_argument('input', help='输入 SQL 文件或目录')
    parser.add_argument('output', nargs='?', help='输出目录')
    parser.add_argument('--batch', action='store_true', help='批量处理目录')
    parser.add_argument('--dialect',
                        choices=['mysql', 'postgresql', 'oracle', 'sqlserver', 'dm', 'generic'],
                        help='指定 SQL 方言')
    parser.add_argument('--no-merge', action='store_true', help='不生成合并脚本')
    parser.add_argument('-q', '--quiet', action='store_true', help='静默模式')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际生成文件')
    parser.add_argument('--no-progress', action='store_true', help='不显示进度条')

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
    dry_run = args.dry_run
    show_progress = not args.no_progress

    if args.batch:
        input_paths = [args.input] if ',' not in args.input else args.input.split(',')
        results = split_sql_batch(input_paths, args.output, dialect, verbose)
        total_files = sum(r['total'] for r in results)
        print(f"\n[done] 共创建 {total_files} 个文件")
    else:
        result = split_sql_file(
            args.input, 
            args.output, 
            dialect, 
            verbose, 
            generate_merge,
            dry_run=dry_run,
            show_progress=show_progress,
        )
        
        # 显示错误和警告
        if result.errors:
            print("\n[error] 错误信息:")
            for err in result.errors:
                if isinstance(err, SplitError):
                    print(f"  - {err.message}")
                    if err.suggestion:
                        print(f"    建议: {err.suggestion}")
                else:
                    print(f"  - {err}")
        
        if result.warnings:
            print("\n[warning] 警告信息:")
            for warn in result.warnings:
                if isinstance(warn, SplitWarning):
                    print(f"  - {warn.message}")
                else:
                    print(f"  - {warn}")
        
        # 显示统计信息
        if verbose:
            print(f"\n[done] 共拆分 {result.total} 个对象")
            if result.stats:
                print("[统计]")
                for obj_type, count in result.stats.items():
                    print(f"  {obj_type}: {count}")
            if result.merge_script:
                print(f"[merge] 合并脚本: {result.merge_script}")
            if dry_run:
                print("[dry-run] 预览模式完成，未实际生成文件")


if __name__ == '__main__':
    main()
