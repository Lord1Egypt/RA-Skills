#!/usr/bin/env python3
"""
达梦数据库转换器 v3.3.0
将 SQL Server 语法转换为达梦数据库语法

v3.0 重写改进:
- 回调式函数转换: CONVERT/DATEADD/DATEDIFF等正确重排参数
- 精确变量转换: 上下文匹配防误改, 支持多变量SELECT赋值
- 补全缺失转换: EXEC动态SQL、临时表#temp、PRINT/RAISERROR、TOP n、方括号标识符、MERGE
- TRY-CATCH: 括号深度匹配替代正则贪婪
- GOTO/LABEL: 排除时间格式等误判
- 更健壮的token化保护
"""

import re
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ConversionType(Enum):
    """转换类型枚举"""
    PROCEDURE = 'procedure'
    FUNCTION = 'function'
    VIEW = 'view'
    TRIGGER = 'trigger'
    TABLE = 'table'
    INDEX = 'index'
    CONSTRAINT = 'constraint'
    SEQUENCE = 'sequence'
    GENERIC = 'generic'


class ConversionResult:
    """转换结果"""

    def __init__(self, original: str, converted: str, changes: List[Dict]):
        self.original = original
        self.converted = converted
        self.changes = changes  # [{type, line, old, new, desc}]

    @property
    def has_changes(self) -> bool:
        return len(self.changes) > 0

    @property
    def change_count(self) -> int:
        return len(self.changes)

    def summary(self) -> str:
        if not self.has_changes:
            return "无需转换"
        lines = [f"共 {self.change_count} 处转换:"]
        for i, c in enumerate(self.changes, 1):
            lines.append(f"  {i}. [{c['type']}] 行{c.get('line', '?')}: {c['old']} -> {c['new']}")
            if c.get('desc'):
                lines.append(f"     ({c['desc']})")
        return '\n'.join(lines)


# ================================================================
# 括号深度匹配工具函数
# ================================================================

def _find_matching_paren(content: str, start: int) -> int:
    """从start位置(必须是'(')找到匹配的')'位置，支持嵌套"""
    depth = 0
    i = start
    in_string = False
    string_char = None
    while i < len(content):
        ch = content[i]
        if in_string:
            if ch == string_char and (i + 1 >= len(content) or content[i + 1] != string_char):
                in_string = False
            elif ch == string_char and i + 1 < len(content) and content[i + 1] == string_char:
                i += 1  # skip escaped quote
        else:
            if ch in ("'",):
                in_string = True
                string_char = ch
            elif ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def _extract_balanced_parens(content: str, open_pos: int) -> Tuple[str, int]:
    """提取从open_pos开始的平衡括号内容(含括号本身)，返回(内容, 闭合位置)"""
    close_pos = _find_matching_paren(content, open_pos)
    if close_pos == -1:
        return content[open_pos:], len(content) - 1
    return content[open_pos:close_pos + 1], close_pos


def _split_args_by_comma(args_str: str) -> List[str]:
    """按顶层逗号分割参数列表(忽略括号/字符串内的逗号)"""
    args = []
    depth = 0
    current = []
    in_string = False
    string_char = None
    i = 0
    while i < len(args_str):
        ch = args_str[i]
        if in_string:
            current.append(ch)
            if ch == string_char:
                if i + 1 < len(args_str) and args_str[i + 1] == string_char:
                    current.append(args_str[i + 1])
                    i += 2
                    continue
                else:
                    in_string = False
        else:
            if ch in ("'",):
                in_string = True
                string_char = ch
                current.append(ch)
            elif ch == '(':
                depth += 1
                current.append(ch)
            elif ch == ')':
                depth -= 1
                current.append(ch)
            elif ch == ',' and depth == 0:
                args.append(''.join(current).strip())
                current = []
            else:
                current.append(ch)
        i += 1
    remainder = ''.join(current).strip()
    if remainder:
        args.append(remainder)
    return args


# ================================================================
# 达梦数据类型映射 (SQL Server -> 达梦)
# ================================================================

TYPE_MAPPINGS = {
    'bit': 'BOOLEAN',
    'tinyint': 'SMALLINT',
    'smallint': 'SMALLINT',
    'int': 'INTEGER',
    'integer': 'INTEGER',
    'bigint': 'BIGINT',
    'decimal': 'DECIMAL',
    'numeric': 'NUMERIC',
    'float': 'DOUBLE',
    'real': 'REAL',
    'money': 'DECIMAL(19,4)',
    'smallmoney': 'DECIMAL(10,4)',
    'datetime': 'TIMESTAMP',
    'datetime2': 'TIMESTAMP',
    'datetimeoffset': 'TIMESTAMP WITH TIME ZONE',
    'smalldatetime': 'TIMESTAMP',
    'date': 'DATE',
    'time': 'TIME',
    'char': 'CHAR',
    'varchar': 'VARCHAR',
    'varchar2': 'VARCHAR2',
    'text': 'TEXT',
    'nchar': 'CHAR',
    'nvarchar': 'VARCHAR',
    'ntext': 'TEXT',
    'binary': 'BINARY',
    'varbinary': 'VARBINARY',
    'image': 'BLOB',
    'uniqueidentifier': 'VARCHAR(36)',
    'xml': 'TEXT',
    'sysname': 'VARCHAR(128)',
    'rowversion': 'TIMESTAMP',
    'timestamp': 'TIMESTAMP',
    'hierarchyid': 'VARCHAR(256)',
    'geometry': 'BLOB',
    'geography': 'BLOB',
}

# SQL关键字不能作为列名出现(排除INSERT INTO等误匹配)
_SQL_KEYWORDS_AS_NAME = frozenset({
    'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'MERGE', 'REPLACE',
    'CREATE', 'ALTER', 'DROP', 'GRANT', 'REVOKE', 'TRUNCATE',
    'BEGIN', 'END', 'IF', 'ELSE', 'WHILE', 'FOR', 'LOOP',
    'RETURN', 'GOTO', 'BREAK', 'CONTINUE', 'WAITFOR',
    'EXEC', 'EXECUTE', 'PRINT', 'RAISERROR', 'SET',
    'INTO', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'NULL',
    'GROUP', 'ORDER', 'BY', 'HAVING', 'UNION', 'ALL',
    'AS', 'ON', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER',
    'VALUES', 'DEFAULT', 'PRIMARY', 'KEY', 'FOREIGN',
    'REFERENCES', 'CHECK', 'UNIQUE', 'INDEX', 'TABLE',
    'VIEW', 'PROCEDURE', 'FUNCTION', 'TRIGGER',
})

# 需要做类型映射的SQL Server类型名集合
# 重要: 按长度降序排列，避免 DATETIME 抢先匹配 DATETIME2 等
_TYPE_NAMES_PATTERN = '|'.join(
    k.upper() for k in sorted(TYPE_MAPPINGS.keys(), key=len, reverse=True)
    if k not in ('date', 'time', 'text', 'char', 'real', 'float')  # 避免歧义太高的短词单独匹配
)
# 补充上面排除的(在声明上下文中足够安全) - 同样按长度降序
_FULL_TYPE_NAMES_PATTERN = '|'.join(
    k.upper() for k in sorted(TYPE_MAPPINGS.keys(), key=len, reverse=True)
)


class DMConverter:
    """达梦数据库转换器 v3.0 - SQL Server 到达梦"""

    def __init__(self):
        self._changes: List[Dict] = []
        self._change_set: set = set() # 去重
        self._schema_prefix: str = ''  # dbo替换前缀

    @staticmethod
    def _quote_name(name: str) -> str:
        """对象名加双引号辅助方法
        处理 schema.name 格式 -> schema"."name (外部调用方包裹双引号)
        处理已经是双引号的 -> 去掉外层引号重新处理
        处理方括号 [name] -> name
        """
        name = name.strip()
        # 处理schema.name格式: [dbo].[xxx] -> dbo"."xxx 或 hrbi_stage.Users
        # 必须先拆分再逐段去方括号，否则[dbo].[xxx]整体被误当成单个方括号标识符
        if '.' in name:
            parts = name.split('.')
            cleaned = []
            for p in parts:
                p = p.strip()
                # 去掉方括号
                if p.startswith('[') and p.endswith(']'):
                    p = p[1:-1]
                # 去掉双引号
                if p.startswith('"') and p.endswith('"'):
                    p = p[1:-1]
                cleaned.append(p)
            return '"."'.join(cleaned)
        # 单段名字: 去掉方括号
        if name.startswith('[') and name.endswith(']'):
            name = name[1:-1]
        # 如果已经双引号包裹,先去掉
        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1]
        return name


    def _add_change(self, change: Dict):
        """添加变更记录(去重)"""
        key = (change.get('type', ''), change.get('old', ''), change.get('new', ''))
        if key not in self._change_set:
            self._change_set.add(key)
            self._changes.append(change)

    def convert(self, content: str, conversion_type: str = 'generic', schema_prefix: str = '') -> ConversionResult:
        """
        将 SQL Server 语法转换为达梦数据库语法

        Args:
            content: SQL Server SQL内容
            conversion_type: 转换类型
            schema_prefix: dbo替换前缀(如源文件名hrbi_stage)，用于替换dbo前缀

        Returns:
            ConversionResult: 转换结果对象
        """
        self._schema_prefix = schema_prefix
        if not content or not content.strip():
            return ConversionResult(content, content, [])

        self._changes = []
        self._change_set = set()
        result = content

        # Step 1: 提取字符串和注释，避免误替换
        result, token_map = self._tokenize(result)

        # Step 2: 按对象类型做特定转换
        ctype = ConversionType(conversion_type) if conversion_type in [e.value for e in ConversionType] else ConversionType.GENERIC
        original_token_map = dict(token_map)

        if ctype == ConversionType.PROCEDURE:
            result = self._convert_procedure(result)
        elif ctype == ConversionType.FUNCTION:
            result = self._convert_function(result)
        elif ctype == ConversionType.VIEW:
            result = self._convert_view(result)
        elif ctype == ConversionType.TRIGGER:
            result = self._convert_trigger(result)
        elif ctype == ConversionType.TABLE:
            result = self._convert_table(result)
        elif ctype == ConversionType.INDEX:
            result = self._convert_index(result)
        elif ctype == ConversionType.CONSTRAINT:
            result = self._convert_constraint(result)
        elif ctype == ConversionType.SEQUENCE:
            result = self._convert_sequence(result)

        # Step 3: 重新tokenize + 合并token_map
        # 使用start_counter避免和original_token_map的key碰撞
        def _extract_token_num(key):
            m = re.match(r'__TOKEN_(\d+)__', key)
            return int(m.group(1)) if m else -1
        max_key = max((_extract_token_num(k) for k in original_token_map), default=-1)
        result, new_token_map = self._tokenize(result, start_counter=max_key + 1)
        merged_map = dict(original_token_map)
        merged_map.update(new_token_map)

    # Step 4: 通用转换(在token保护下)
    # 先去方括号标识符，否则类型名[nvarchar]等无法匹配
        result = self._convert_bracket_identifiers(result)
        result = self._convert_data_types(result)
        result = self._convert_functions(result)
        result = self._convert_global_vars(result)
        result = self._convert_statements(result)
        result = self._convert_truncate(result)
        result = self._convert_try_catch(result)
        result = self._convert_transaction(result)
        result = self._convert_top(result)
        result = self._convert_temp_tables(result)
        result = self._convert_exec_dynamic(result)
        result = self._convert_print_raiserror(result)
        result = self._convert_merge(result)
        result = self._convert_isnull_pattern(result)

        # Step 5: 还原token
        result = self._detokenize(result, merged_map)

        # Step 6: 变量语法转换(在还原后做，用轻量级tokenize只保护字符串)
        safe_result, safe_map = self._tokenize_strings_only(result)
        safe_result = self._convert_variable_syntax(safe_result)
        result = self._detokenize(safe_result, safe_map)

        # Step 6.5: 修复INTERVAL里变量被引号包裹的问题
        # DATEADD(day, @n, @date) -> @date + INTERVAL '@n' DAY
        # 变量@去掉后变成 INTERVAL 'n' DAY，但n应该是不带引号的变量
        result = self._fix_interval_variables(result)

        # Step 6.6: 字符串连接 + -> ||
        # 在还原后做，此时能看到真实的字符串字面量
        result = self._convert_string_concat(result)

        # Step 6.7: 方括号替换 + 类型映射 + dbo前缀替换（所有对象类型）
        # 在token还原后做，此时能看到真实类型名如[nvarchar]、[int]等
        if ctype in (ConversionType.TABLE, ConversionType.VIEW):
            result = self._post_convert_table_types(result)
        else:
            # 非表/视图也需要: 方括号→双引号 + 类型映射 + dbo替换
            result = self._post_convert_generic_types(result)

        # Step 7: IF/WHILE控制流转换(在还原后做，需要看到真实文本)
        result = self._convert_if_else(result)
        result = self._convert_while_loop(result)

        # Step 8: GOTO/LABEL 转换(在还原后做，需要看到真实文本)
        result = self._convert_goto_label(result)

        # Step 8.5: 过程体内DDL语句结尾补分号
        if ctype in (ConversionType.PROCEDURE, ConversionType.FUNCTION,
                    ConversionType.TRIGGER):
            result = self._ensure_ddl_semicolons(result)

        # Step 8.6: 过程体内所有语句(DML/变量赋值)结尾补分号
        if ctype in (ConversionType.PROCEDURE, ConversionType.FUNCTION,
                    ConversionType.TRIGGER):
            result = self._ensure_statement_semicolons(result)

        # Step 8: 后处理 - 为存储过程/函数/触发器添加达梦终止符 /
        if ctype in (ConversionType.PROCEDURE, ConversionType.FUNCTION,
                    ConversionType.TRIGGER):
            result = self._add_terminator(result)

        # Step 9: 为TABLE/VIEW/INDEX/CONSTRAINT/SEQUENCE确保结尾有分号
        if ctype in (ConversionType.TABLE, ConversionType.VIEW,
                    ConversionType.INDEX, ConversionType.CONSTRAINT,
                    ConversionType.SEQUENCE):
            result = self._add_ending_semicolon(result)

        return ConversionResult(content, result, self._changes)

    # ================================================================
    # Token化 - 保护字符串和注释不被误替换
    # ================================================================

    def _tokenize(self, content: str, start_counter: int = 0) -> Tuple[str, Dict[str, str]]:
        """将字符串字面量和注释替换为占位符"""
        token_map = {}
        counter = [start_counter]

        def _replace(m):
            key = f"__TOKEN_{counter[0]}__"
            token_map[key] = m.group(0)
            counter[0] += 1
            return key

        # 先替换多行注释
        result = re.sub(r'/\*.*?\*/', _replace, content, flags=re.DOTALL)
        # 再替换单行注释
        result = re.sub(r'--[^\n]*', _replace, result)
        # 再替换字符串字面量 (N'...' 也要处理)
        result = re.sub(r"N?'[^']*(?:''[^']*)*'", _replace, result)
        # 双引号标识符
        result = re.sub(r'"[^"]*(?:""[^"]*)*"', _replace, result)
        # 注意: 方括号标识符 [name] 不在tokenize中替换
        # 因为类型映射需要匹配 [int] [varchar] 等方括号内的类型名
        # 方括号标识符的处理交给 _convert_bracket_identifiers() 完成

        return result, token_map

    def _tokenize_strings_only(self, content: str) -> Tuple[str, Dict[str, str]]:
        """只替换字符串字面量为占位符（注释不替换，用于变量@转换时保护字符串）"""
        token_map = {}
        counter = [0]

        def _replace(m):
            key = f"__STOK_{counter[0]}__"
            token_map[key] = m.group(0)
            counter[0] += 1
            return key

        # N'...' 和 '...'
        result = re.sub(r"N?'[^']*(?:''[^']*)*'", _replace, content)
        # 双引号标识符
        result = re.sub(r'"[^"]*(?:""[^"]*)*"', _replace, result)

        return result, token_map

    def _detokenize(self, content: str, token_map: Dict[str, str]) -> str:
        """还原占位符为原始内容"""
        # 按key长度降序排列，避免短key替换长key的一部分
        for placeholder in sorted(token_map.keys(), key=len, reverse=True):
            content = content.replace(placeholder, token_map[placeholder])
        return content

    # ================================================================
    # 对象类型特定转换
    # ================================================================

    def _convert_procedure(self, tokens: str) -> str:
        """存储过程特定转换"""
        # SQL Server存储过程参数无括号: CREATE PROC name @p1 INT, @p2 VARCHAR(100) AS
        # 也有带括号的写法: CREATE PROC name(@p1 INT, @p2 VARCHAR(100)) AS
        # 也可能是: CREATE OR REPLACE PROC name @p1 INT AS (拆分阶段已加OR REPLACE)
        # -> CREATE OR REPLACE PROCEDURE name (p1 INT, p2 VARCHAR(100)) AS
        # 注意: 达梦存储过程用AS，函数用IS
        #
        # 重要: 用单一正则+分支回调，避免三个正则顺序执行时
        # 第一个替换后的结果被后续正则再次匹配导致引号叠加

        # 统一正则: 识别三种参数形式(括号/无括号@参数/无参数)
        # Group 1: name, Group 2: 括号参数(可选), Group 3: 无括号@参数(可选)
        _PROC_PATTERN = (
            r'CREATE\s+(?:OR\s+REPLACE\s+)?PROC(?:EDURE)?\s+'
            r'(.+?)'  # group 1: name (non-greedy)
            r'(?:'
            r'\s*(\([^)]*(?:\([^)]*\)[^)]*)*\))'  # group 2: 括号参数
            r'|'
            r'\s+(@[\s\S]+?)'  # group 3: 无括号@参数列表
            r')?'
            r'\s*AS\b'
        )

        def _format_proc(m):
            name = m.group(1).strip()
            bracket_params = m.group(2)  # 含括号 或 None
            raw_params = m.group(3)      # @p1 INT, @p2 ... 或 None

            if bracket_params:
                # 有括号的参数列表
                params = re.sub(r'@(\w+)', r'\1', bracket_params)
                return f'CREATE OR REPLACE PROCEDURE "{DMConverter._quote_name(name)}" {params} AS'
            elif raw_params:
                # 无括号参数列表（SQL Server标准写法）
                params_clean = re.sub(r'@(\w+)', r'\1', raw_params)
                param_list = _split_args_by_comma(params_clean.strip())
                param_list = [p.strip() for p in param_list if p.strip()]
                if len(param_list) <= 1:
                    return f'CREATE OR REPLACE PROCEDURE "{DMConverter._quote_name(name)}" ({params_clean.strip()}) AS'
                formatted = '(\n' + ',\n'.join(f'    {p}' for p in param_list) + '\n)'
                return f'CREATE OR REPLACE PROCEDURE "{DMConverter._quote_name(name)}" {formatted} AS'
            else:
                # 无参数的存储过程
                return f'CREATE OR REPLACE PROCEDURE "{DMConverter._quote_name(name)}" AS'

        tokens = re.sub(_PROC_PATTERN, _format_proc, tokens, flags=re.IGNORECASE | re.DOTALL)
        # GO 分隔符 -> /
        tokens = re.sub(r'^\s*GO\s*;?\s*$', '/', tokens, flags=re.MULTILINE | re.IGNORECASE)

        self._add_change({'type': 'procedure', 'line': 0, 'old': 'CREATE PROCEDURE', 'new': 'CREATE OR REPLACE PROCEDURE ... AS', 'desc': '存储过程声明语法'})
        return tokens

    def _convert_function(self, tokens: str) -> str:
        """函数特定转换"""
        # CREATE FUNCTION name(@p1 INT) RETURNS INT AS
        # -> CREATE OR REPLACE FUNCTION name(p1 INT) RETURN INT IS
        def _fmt_func(m):
            name = m.group(1)
            params = m.group(2)
            ret_type = m.group(3)
            return f'CREATE OR REPLACE FUNCTION "{DMConverter._quote_name(name)}" ({params}) RETURN {ret_type} IS'
        tokens = re.sub(
            r'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+(.+?)\s*\(([^)]*)\)\s*RETURNS\s+(\w+(?:\s*\([^)]*\))?)\s*AS\b',
            _fmt_func,
            tokens,
            flags=re.IGNORECASE
        )
        # 表值函数 (RETURNS TABLE / RETURNS @table TABLE...)
        tokens = re.sub(
            r'RETURNS\s+@(\w+)\s+TABLE\s*\(',
            r'RETURN TABLE(',
            tokens,
            flags=re.IGNORECASE
        )
        # GO/GO; -> /
        tokens = re.sub(r'^\s*GO\s*;?\s*$', '/', tokens, flags=re.MULTILINE | re.IGNORECASE)

        self._add_change({'type': 'function', 'line': 0, 'old': 'CREATE FUNCTION', 'new': 'CREATE OR REPLACE FUNCTION ... IS', 'desc': '函数声明语法'})
        return tokens

    def _convert_view(self, tokens: str) -> str:
        """视图特定转换"""
        def _fmt_view(m):
            name = m.group(1)
            return f'CREATE OR REPLACE VIEW "{DMConverter._quote_name(name)}" AS'
        tokens = re.sub(
            r'CREATE\s+VIEW\s+([\w.]+)\s+AS\b',
            _fmt_view,
            tokens,
            flags=re.IGNORECASE
        )
        # WITH SCHEMABINDING -> 去掉
        tokens = re.sub(r'\bWITH\s+SCHEMABINDING\b', '-- WITH SCHEMABINDING (达梦不支持)', tokens, flags=re.IGNORECASE)
        # GO -> /
        tokens = re.sub(r'^\s*GO\s*$', '/', tokens, flags=re.MULTILINE | re.IGNORECASE)

        self._add_change({'type': 'view', 'line': 0, 'old': 'CREATE VIEW', 'new': 'CREATE OR REPLACE VIEW', 'desc': '视图声明语法'})
        return tokens

    def _convert_trigger(self, tokens: str) -> str:
        """触发器特定转换"""
        # AFTER 触发器
        def _fmt_trig_after(m):
            name = m.group(1)
            tbl = m.group(2)
            events = m.group(3)
            return f'CREATE OR REPLACE TRIGGER "{DMConverter._quote_name(name)}" AFTER {events} ON "{DMConverter._quote_name(tbl)}"'
        tokens = re.sub(
            r'CREATE\s+TRIGGER\s+([\w.]+)\s+ON\s+([\w.]+)\s+AFTER\s+([\w,\s]+?)(?:\s+AS\b|\s+FOR\s+EACH\s+ROW\b)',
            _fmt_trig_after,
            tokens,
            flags=re.IGNORECASE
        )
        # INSTEAD OF 触发器 -> BEFORE
        def _fmt_trig_instead(m):
            name = m.group(1)
            tbl = m.group(2)
            events = m.group(3)
            return f'CREATE OR REPLACE TRIGGER "{DMConverter._quote_name(name)}" BEFORE {events} ON "{DMConverter._quote_name(tbl)}"'
        tokens = re.sub(
            r'CREATE\s+TRIGGER\s+([\w.]+)\s+ON\s+([\w.]+)\s+INSTEAD\s+OF\s+([\w,\s]+?)(?:\s+AS\b|\s+FOR\s+EACH\s+ROW\b)',
            _fmt_trig_instead,
            tokens,
            flags=re.IGNORECASE
        )
        # FOR 触发器 (SQL Server 的 FOR 等同于 AFTER)
        def _fmt_trig_for(m):
            name = m.group(1)
            tbl = m.group(2)
            events = m.group(3)
            return f'CREATE OR REPLACE TRIGGER "{DMConverter._quote_name(name)}" AFTER {events} ON "{DMConverter._quote_name(tbl)}"'
        tokens = re.sub(
            r'CREATE\s+TRIGGER\s+([\w.]+)\s+ON\s+([\w.]+)\s+FOR\s+([\w,\s]+?)(?:\s+AS\b|\s+FOR\s+EACH\s+ROW\b)',
            _fmt_trig_for,
            tokens,
            flags=re.IGNORECASE
        )
        # inserted/deleted 伪表 -> NEW/OLD
        tokens = re.sub(r'\binserted\b', 'NEW', tokens, flags=re.IGNORECASE)
        tokens = re.sub(r'\bdeleted\b', 'OLD', tokens, flags=re.IGNORECASE)
        # GO -> /
        tokens = re.sub(r'^\s*GO\s*$', '/', tokens, flags=re.MULTILINE | re.IGNORECASE)

        self._add_change({'type': 'trigger', 'line': 0, 'old': 'CREATE TRIGGER', 'new': 'CREATE OR REPLACE TRIGGER', 'desc': '触发器声明语法'})
        return tokens

    def _convert_table(self, tokens: str) -> str:
        """表特定转换"""
        # CREATE TABLE name -> CREATE TABLE "name" (对象名加双引号)
        def _fmt_table_name(m):
            name = m.group(1)
            return f'CREATE TABLE "{DMConverter._quote_name(name)}"'
        tokens = re.sub(
            r'CREATE\s+TABLE\s+([\w.]+)',
            _fmt_table_name,
            tokens,
            flags=re.IGNORECASE
        )

        # === 规则2: IDENTITY自增列处理 ===
        # 达梦要求: 列定义中不写IDENTITY,而在表定义外单独声明 IDENTITY("列名", start, step)
        # SQL Server: "id" INTEGER IDENTITY(1,1) NOT NULL
        # 达梦:       "id" INTEGER NOT NULL
        #             IDENTITY("id", 1, 1)
        identity_info = None  # (col_name, start, step)

        # 步骤1: 提取IDENTITY列名和参数
        # 匹配: col_name TYPE IDENTITY(start, step) — 在token阶段col_name可能是标识符占位符
        # 也可能是原始名: [id] INTEGER IDENTITY(1,1) 或 "id" INTEGER IDENTITY(1,1) 或 id INTEGER IDENTITY(1,1)
        m_id = re.search(
            r'(?:"(\w+)"|\[(\w+)\]|(\w+))\s+\w+(?:\s*\([^)]*\))?\s+IDENTITY\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)',
            tokens, re.IGNORECASE
        )
        if m_id:
            col_name = m_id.group(1) or m_id.group(2) or m_id.group(3)
            identity_info = (col_name, m_id.group(4), m_id.group(5))
        else:
            # IDENTITY(无参数)
            m_id = re.search(
                r'(?:"(\w+)"|\[(\w+)\]|(\w+))\s+\w+(?:\s*\([^)]*\))?\s+IDENTITY\b(?!\s*\()',
                tokens, re.IGNORECASE
            )
            if m_id:
                col_name = m_id.group(1) or m_id.group(2) or m_id.group(3)
                identity_info = (col_name, '1', '1')

        # 步骤2: 从列定义中删除IDENTITY关键字(含参数)和NOT FOR REPLICATION
        # 先删: IDENTITY(1,1) NOT FOR REPLICATION
        tokens = re.sub(
            r'\s+IDENTITY\s*\(\s*\d+\s*,\s*\d+\s*\)(\s+NOT\s+FOR\s+REPLICATION)?',
            '',
            tokens,
            flags=re.IGNORECASE
        )
        # 再删: IDENTITY(无参数) NOT FOR REPLICATION
        tokens = re.sub(
            r'\s+IDENTITY\b(?!\s*\()(\s+NOT\s+FOR\s+REPLICATION)?',
            '',
            tokens,
            flags=re.IGNORECASE
        )
        # 残留 NOT FOR REPLICATION
        tokens = re.sub(r'\bNOT\s+FOR\s+REPLICATION\b', '', tokens, flags=re.IGNORECASE)

        # 步骤3: 在CREATE TABLE最后的右括号后添加IDENTITY子句
        # 达梦语法: CREATE TABLE "name" (...) IDENTITY("col", start, step)
        # 必须匹配表定义的结束括号)，避免误匹配列定义中的)
        if identity_info:
            col_name, start_val, step_val = identity_info
            id_clause = f' IDENTITY("{col_name}", {start_val}, {step_val})'
            # 先删除ON [PRIMARY]等表级后缀(在插入IDENTITY前)，避免干扰匹配
            tokens = re.sub(r'\)\s+ON\s+\S+\s*$', ')', tokens, flags=re.MULTILINE | re.IGNORECASE)
            # 匹配表结束的)：独占一行的) 或 行内最后一个)后紧跟行尾/;'等
            # 优先匹配独占一行的)，否则匹配行尾的)
            inserted = False
            # 尝试1: ) 独占一行
            m1 = re.search(r'^(\s*)\)(\s*$)', tokens, re.MULTILINE | re.IGNORECASE)
            if m1:
                tokens = tokens[:m1.start()] + m1.group(1) + ')' + id_clause + m1.group(2) + tokens[m1.end():]
                inserted = True
            # 尝试2: ) 在行尾(紧跟NOT NULL等之后)
            if not inserted:
                tokens = re.sub(
                    r'\)(\s*(?:;|\n|$))',
                    ')' + id_clause + r'\1',
                    tokens,
                    count=1,
                    flags=re.IGNORECASE
                )
            self._add_change({'type': 'table', 'line': 0, 'old': 'IDENTITY in column def',
                            'new': f'IDENTITY("{col_name}", {start_val}, {step_val}) after table',
                            'desc': '自增列单独拆出(规则2)'})
        # WITH (PAD_INDEX = ...) 等表选项 -> 去掉
        tokens = re.sub(r'\bWITH\s*\([^)]*(?:PAD_INDEX|FILLFACTOR|IGNORE_DUP_KEY|STATISTICS_NORECOMPUTE)[^)]*\)', '', tokens, flags=re.IGNORECASE)
        # ON [PRIMARY] / ON __TOKEN_?__ -> 去掉(表级存储子句)
        # 匹配: 行尾的 ) ON xxx 或单独一行的 ON xxx
        tokens = re.sub(r'\)\s+ON\s+\S+\s*$', ')', tokens, flags=re.MULTILINE | re.IGNORECASE)
        tokens = re.sub(r'^\s*ON\s+\S+\s*$', '', tokens, flags=re.MULTILINE | re.IGNORECASE)
        # TEXTIMAGE_ON ... -> 去掉
        tokens = re.sub(r'\bTEXTIMAGE_ON\s+\S+', '', tokens, flags=re.IGNORECASE)
        # GO -> /
        tokens = re.sub(r'^\s*GO\s*$', '/', tokens, flags=re.MULTILINE | re.IGNORECASE)

        self._add_change({'type': 'table', 'line': 0, 'old': 'IDENTITY/表选项', 'new': 'IDENTITY/注释', 'desc': '表结构选项转换'})
        return tokens

    def _convert_index(self, tokens: str) -> str:
        """索引特定转换"""
        tokens = re.sub(r'\bCLUSTERED\b', '', tokens, flags=re.IGNORECASE)
        tokens = re.sub(r'\bNONCLUSTERED\b', '', tokens, flags=re.IGNORECASE)
        tokens = re.sub(r'\bINCLUDE\s*\([^)]*\)', '-- INCLUDE (达梦不支持)', tokens, flags=re.IGNORECASE)
        tokens = re.sub(r'\bWHERE\s+.*$', '-- WHERE 条件索引 (达梦不支持)', tokens, flags=re.MULTILINE | re.IGNORECASE)
        tokens = re.sub(r'\bWITH\s*\([^)]*(?:DROP_EXISTING|ONLINE|SORT_IN_TEMPDB)[^)]*\)', '', tokens, flags=re.IGNORECASE)
        tokens = re.sub(r'\bON\s+\[?\w+\]?\s*\([^)]*\)', '', tokens, flags=re.IGNORECASE)
        tokens = re.sub(r'^\s*GO\s*$', '/', tokens, flags=re.MULTILINE | re.IGNORECASE)

        self._add_change({'type': 'index', 'line': 0, 'old': 'CLUSTERED/INCLUDE/WHERE', 'new': '移除', 'desc': '索引选项转换'})
        return tokens

    def _convert_constraint(self, tokens: str) -> str:
        """约束特定转换"""
        tokens = re.sub(r'\bWITH\s+(NO)?CHECK\b', '', tokens, flags=re.IGNORECASE)
        tokens = re.sub(r'\bNOCHECK\s+CONSTRAINT\b', '-- NOCHECK CONSTRAINT (达梦不支持)', tokens, flags=re.IGNORECASE)
        tokens = re.sub(r'^\s*GO\s*$', '/', tokens, flags=re.MULTILINE | re.IGNORECASE)
        return tokens

    def _convert_sequence(self, tokens: str) -> str:
        """序列特定转换"""
        tokens = re.sub(r'^\s*GO\s*$', '/', tokens, flags=re.MULTILINE | re.IGNORECASE)
        return tokens

    # ================================================================
    # 通用转换 - 数据类型
    # ================================================================

    def _convert_data_types(self, tokens: str) -> str:
        """数据类型转换 - 在列定义/变量声明/参数上下文中替换
        支持 [type_name] 方括号格式（SQL Server脚本中常见）
        """

        def _replace_type(m):
            prefix = m.group(1)
            col_name = m.group(2)
            type_name = m.group(3)  # 可能是 int 或 [int]
            suffix = m.group(4) or ''

            # 去掉方括号获取裸类型名
            bare_type = type_name.strip('[]')

            # 排除SQL关键字作为列名的误匹配
            if col_name.upper() in _SQL_KEYWORDS_AS_NAME:
                return m.group(0)

            base_type = bare_type.lower().strip()
            if base_type in TYPE_MAPPINGS:
                new_type = TYPE_MAPPINGS[base_type]
                # varchar(max) / nvarchar(max) / varchar2(max) -> VARCHAR(4096 CHAR) / VARCHAR2(4096 CHAR)
                if base_type in ('varchar', 'nvarchar', 'varchar2') and '(max)' in suffix.lower():
                    new_type = 'VARCHAR2' if base_type == 'varchar2' else 'VARCHAR'
                    suffix = '(4096 CHAR)'
                new_result = f"{prefix}{col_name} {new_type}{suffix}"
                if new_result != m.group(0):
                    self._add_change({
                        'type': 'data_type', 'line': 0,
                        'old': f"{col_name} {type_name}{suffix}",
                        'new': f"{col_name} {new_type}{suffix}",
                        'desc': '数据类型映射'
                    })
                return new_result
            return m.group(0)

        # 匹配: (前缀)(列名)(类型名)(长度?)
        # 前缀包括: , ( DECLARE 换行
        # 类型名支持裸名(int)和方括号包裹([int])
        tokens = re.sub(
            r'([,\(]\s*|DECLARE\s+|\n\s*)([\w@]+)\s+(\[?(?:' + _FULL_TYPE_NAMES_PATTERN + r')\]?)(\([^)]*(?:\([^)]*\)[^)]*)*\))?',
            _replace_type,
            tokens,
            flags=re.IGNORECASE
        )

        return tokens
    def _convert_functions(self, tokens: str) -> str:
        """函数转换 - 使用回调函数正确处理参数"""

        # ---- 简单替换(无需参数重排) ----
        simple_funcs = [
            (r'\bGETDATE\s*\(\s*\)', 'CURRENT_TIMESTAMP', '日期函数'),
            (r'\bSYSDATETIME\s*\(\s*\)', 'CURRENT_TIMESTAMP', '日期函数'),
            (r'\bSYSUTCDATETIME\s*\(\s*\)', 'CURRENT_TIMESTAMP', '日期函数'),
            (r'\bLEN\s*\(', 'LENGTH(', '字符串函数'),
            (r'\bSUBSTRING\s*\(', 'SUBSTR(', '字符串函数'),
            (r'\bCHARINDEX\s*\(', 'INSTR(', '字符串函数'),
            (r'\bISNULL\s*\(', 'NVL(', '空值函数'),
            (r'\bCEILING\s*\(', 'CEIL(', '数学函数'),
            (r'\bNEWID\s*\(\s*\)', 'SYS_GUID()', '标识函数'),
            (r'\bSCOPE_IDENTITY\s*\(\s*\)', 'IDENT_CURRENT()', '标识函数'),
        ]

        for pattern, replacement, desc in simple_funcs:
            new_tokens = re.sub(pattern, replacement, tokens, flags=re.IGNORECASE)
            if new_tokens != tokens:
                self._add_change({'type': 'function', 'line': 0, 'old': pattern, 'new': replacement, 'desc': desc})
                tokens = new_tokens

        # ---- 回调式转换(需要参数重排) ----
        tokens = self._convert_convert_func(tokens)
        tokens = self._convert_dateadd_func(tokens)
        tokens = self._convert_datediff_func(tokens)
        tokens = self._convert_datepart_func(tokens)
        tokens = self._convert_string_agg_func(tokens)
        tokens = self._convert_stuff_func(tokens)
        tokens = self._convert_replicate_func(tokens)
        tokens = self._convert_year_month_day(tokens)

        return tokens

    def _find_func_call(self, content: str, func_name: str, start: int = 0) -> Optional[Tuple[int, int, str, List[str]]]:
        """
        查找函数调用，返回 (match_start, match_end, func_prefix, [args])
        支持嵌套括号内的参数分割
        """
        pattern = re.compile(r'\b' + re.escape(func_name) + r'\s*\(', re.IGNORECASE)
        m = pattern.search(content, start)
        if not m:
            return None

        # 找到匹配的右括号
        open_pos = m.end() - 1  # '(' 的位置
        close_pos = _find_matching_paren(content, open_pos)
        if close_pos == -1:
            return None

        args_str = content[open_pos + 1:close_pos].strip()
        args = _split_args_by_comma(args_str)

        return (m.start(), close_pos + 1, content[m.start():m.end()], args)

    def _convert_convert_func(self, tokens: str) -> str:
        """CONVERT(type, expr) -> CAST(expr AS type)"""
        result = tokens
        offset = 0
        while True:
            search_in = result[offset:]
            found = self._find_func_call(search_in, 'CONVERT')
            if not found:
                break
            local_start, local_end, _, args = found
            global_start = offset + local_start
            global_end = offset + local_end

            if len(args) >= 2:
                target_type = args[0].strip()
                expr = args[1].strip()
                # style参数(第3个)在达梦不需要
                # 映射类型
                mapped_type = TYPE_MAPPINGS.get(target_type.lower(), target_type)
                # NVARCHAR(100) 等带长度的类型保持
                replacement = f"CAST({expr} AS {mapped_type})"
                result = result[:global_start] + replacement + result[global_end:]
                self._add_change({
                    'type': 'function', 'line': 0,
                    'old': f'CONVERT({target_type}, {expr})',
                    'new': f'CAST({expr} AS {mapped_type})',
                    'desc': '类型转换函数'
                })
                offset = global_start + len(replacement)
            else:
                offset = global_end
        return result

    def _convert_dateadd_func(self, tokens: str) -> str:
        """DATEADD(part, n, date) -> date + INTERVAL 'n' part"""
        result = tokens
        offset = 0
        while True:
            search_in = result[offset:]
            found = self._find_func_call(search_in, 'DATEADD')
            if not found:
                break
            local_start, local_end, _, args = found
            global_start = offset + local_start
            global_end = offset + local_end

            if len(args) >= 3:
                part = args[0].strip().lower()
                n = args[1].strip()
                date_expr = args[2].strip()

                # 达梦用 date + INTERVAL 语法
                part_map = {
                    'day': 'DAY', 'dd': 'DAY', 'd': 'DAY',
                    'month': 'MONTH', 'mm': 'MONTH', 'm': 'MONTH',
                    'year': 'YEAR', 'yy': 'YEAR', 'yyyy': 'YEAR',
                    'hour': 'HOUR', 'hh': 'HOUR',
                    'minute': 'MINUTE', 'mi': 'MINUTE', 'n': 'MINUTE',
                    'second': 'SECOND', 'ss': 'SECOND', 's': 'SECOND',
                }
                dm_part = part_map.get(part, part.upper())

                # INTERVAL 语法: date_expr + INTERVAL 'n' PART
                # 注意: 负数需要用 date - INTERVAL
                replacement = f"{date_expr} + INTERVAL '{n}' {dm_part}"
                result = result[:global_start] + replacement + result[global_end:]
                self._add_change({
                    'type': 'function', 'line': 0,
                    'old': f'DATEADD({part}, {n}, {date_expr})',
                    'new': replacement,
                    'desc': '日期加减函数'
                })
                offset = global_start + len(replacement)
            else:
                offset = global_end
        return result

    def _convert_datediff_func(self, tokens: str) -> str:
        """DATEDIFF(part, start, end) -> (end - start) 单位需要用EXTRACT或除法"""
        result = tokens
        offset = 0
        while True:
            search_in = result[offset:]
            found = self._find_func_call(search_in, 'DATEDIFF')
            if not found:
                break
            local_start, local_end, _, args = found
            global_start = offset + local_start
            global_end = offset + local_end

            if len(args) >= 3:
                part = args[0].strip().lower()
                start_expr = args[1].strip()
                end_expr = args[2].strip()

                # 达梦: 天数用 (end - start)，月数/年数需要特殊处理
                part_map = {
                    'day': 'DAY', 'dd': 'DAY', 'd': 'DAY',
                    'month': 'MONTH', 'mm': 'MONTH', 'm': 'MONTH',
                    'year': 'YEAR', 'yy': 'YEAR', 'yyyy': 'YEAR',
                    'hour': 'HOUR', 'hh': 'HOUR',
                    'minute': 'MINUTE', 'mi': 'MINUTE', 'n': 'MINUTE',
                    'second': 'SECOND', 'ss': 'SECOND', 's': 'SECOND',
                }
                dm_part = part_map.get(part, part.upper())

                if dm_part == 'DAY':
                    replacement = f"({end_expr} - {start_expr})"
                elif dm_part == 'MONTH':
                    replacement = f"MONTHS_BETWEEN({end_expr}, {start_expr})"
                elif dm_part == 'YEAR':
                    replacement = f"TRUNC(MONTHS_BETWEEN({end_expr}, {start_expr}) / 12)"
                elif dm_part == 'HOUR':
                    replacement = f"(({end_expr} - {start_expr}) * 24)"
                elif dm_part == 'MINUTE':
                    replacement = f"(({end_expr} - {start_expr}) * 24 * 60)"
                elif dm_part == 'SECOND':
                    replacement = f"(({end_expr} - {start_expr}) * 24 * 60 * 60)"
                else:
                    replacement = f"({end_expr} - {start_expr})"

                result = result[:global_start] + replacement + result[global_end:]
                self._add_change({
                    'type': 'function', 'line': 0,
                    'old': f'DATEDIFF({part}, {start_expr}, {end_expr})',
                    'new': replacement,
                    'desc': '日期差函数'
                })
                offset = global_start + len(replacement)
            else:
                offset = global_end
        return result

    def _convert_datepart_func(self, tokens: str) -> str:
        """DATEPART(part, date) -> EXTRACT(PART FROM date)"""
        result = tokens
        offset = 0
        while True:
            search_in = result[offset:]
            found = self._find_func_call(search_in, 'DATEPART')
            if not found:
                break
            local_start, local_end, _, args = found
            global_start = offset + local_start
            global_end = offset + local_end

            if len(args) >= 2:
                part = args[0].strip().lower()
                date_expr = args[1].strip()

                part_map = {
                    'year': 'YEAR', 'yy': 'YEAR', 'yyyy': 'YEAR',
                    'month': 'MONTH', 'mm': 'MONTH', 'm': 'MONTH',
                    'day': 'DAY', 'dd': 'DAY', 'd': 'DAY',
                    'hour': 'HOUR', 'hh': 'HOUR',
                    'minute': 'MINUTE', 'mi': 'MINUTE', 'n': 'MINUTE',
                    'second': 'SECOND', 'ss': 'SECOND', 's': 'SECOND',
                    'weekday': 'DAY', 'dw': 'DAY',
                    'week': 'WEEK', 'wk': 'WEEK', 'ww': 'WEEK',
                    'quarter': 'QUARTER', 'qq': 'QUARTER', 'q': 'QUARTER',
                }
                dm_part = part_map.get(part, part.upper())
                replacement = f"EXTRACT({dm_part} FROM {date_expr})"
                result = result[:global_start] + replacement + result[global_end:]
                self._add_change({
                    'type': 'function', 'line': 0,
                    'old': f'DATEPART({part}, {date_expr})',
                    'new': replacement,
                    'desc': '日期部分函数'
                })
                offset = global_start + len(replacement)
            else:
                offset = global_end
        return result

    def _convert_string_agg_func(self, tokens: str) -> str:
        """STRING_AGG(expr, separator) -> LISTAGG(expr, separator) WITHIN GROUP (ORDER BY 1)"""
        result = tokens
        offset = 0
        while True:
            search_in = result[offset:]
            found = self._find_func_call(search_in, 'STRING_AGG')
            if not found:
                break
            local_start, local_end, _, args = found
            global_start = offset + local_start
            global_end = offset + local_end

            if len(args) >= 2:
                expr = args[0].strip()
                sep = args[1].strip()
                # LISTAGG 需要 WITHIN GROUP 语法
                replacement = f"LISTAGG({expr}, {sep}) WITHIN GROUP (ORDER BY 1)"
                result = result[:global_start] + replacement + result[global_end:]
                self._add_change({
                    'type': 'function', 'line': 0,
                    'old': f'STRING_AGG({expr}, {sep})',
                    'new': replacement,
                    'desc': '字符串聚合函数'
                })
                offset = global_start + len(replacement)
            else:
                offset = global_end
        return result

    def _convert_stuff_func(self, tokens: str) -> str:
        """STUFF(str, start, length, replace) -> 达梦用OVERLAY或SUBSTR拼接"""
        result = tokens
        offset = 0
        while True:
            search_in = result[offset:]
            found = self._find_func_call(search_in, 'STUFF')
            if not found:
                break
            local_start, local_end, _, args = found
            global_start = offset + local_start
            global_end = offset + local_end

            if len(args) >= 4:
                s = args[0].strip()
                start = args[1].strip()
                length = args[2].strip()
                replace_str = args[3].strip()
                # 达梦没有STUFF，用SUBSTR拼接: SUBSTR(s,1,start-1) || replace || SUBSTR(s,start+length)
                replacement = f"SUBSTR({s}, 1, {start}-1) || {replace_str} || SUBSTR({s}, {start}+{length})"
                result = result[:global_start] + replacement + result[global_end:]
                self._add_change({
                    'type': 'function', 'line': 0,
                    'old': f'STUFF({s}, {start}, {length}, {replace_str})',
                    'new': replacement,
                    'desc': '字符串替换函数(用SUBSTR拼接替代)'
                })
                offset = global_start + len(replacement)
            else:
                offset = global_end
        return result

    def _convert_replicate_func(self, tokens: str) -> str:
        """REPLICATE(str, count) -> RPAD(str, count * LENGTH(str), str) 或 LPAD"""
        result = tokens
        offset = 0
        while True:
            search_in = result[offset:]
            found = self._find_func_call(search_in, 'REPLICATE')
            if not found:
                break
            local_start, local_end, _, args = found
            global_start = offset + local_start
            global_end = offset + local_end

            if len(args) >= 2:
                s = args[0].strip()
                count = args[1].strip()
                # 达梦用 RPAD/LPAD + REPEAT 组合: REPEAT 在达梦中不存在
                # 最安全: LPAD('', count * LENGTH(str), str) 但达梦的LPAD只接受单字符pad
                # 实际做法: 用循环或简单替换为注释提醒
                replacement = f"LPAD('', {count} * LENGTH({s}), {s})"
                result = result[:global_start] + replacement + result[global_end:]
                self._add_change({
                    'type': 'function', 'line': 0,
                    'old': f'REPLICATE({s}, {count})',
                    'new': replacement,
                    'desc': '字符串重复函数(需验证达梦LPAD是否支持多字符pad)'
                })
                offset = global_start + len(replacement)
            else:
                offset = global_end
        return result

    def _convert_year_month_day(self, tokens: str) -> str:
        """YEAR(date) -> EXTRACT(YEAR FROM date), MONTH/DAY同理"""
        for func, part in [('YEAR', 'YEAR'), ('MONTH', 'MONTH'), ('DAY', 'DAY')]:
            # 匹配 YEAR(  但不是 YEAR(数字) (可能是 EXTRACT(YEAR FROM ...) 已转换的)
            pattern = re.compile(r'\b' + func + r'\s*\(', re.IGNORECASE)
            result = tokens
            offset = 0
            while True:
                search_in = result[offset:]
                m = pattern.search(search_in)
                if not m:
                    break
                global_start = offset + m.start()
                open_pos = offset + m.end() - 1
                close_pos = _find_matching_paren(result, open_pos)
                if close_pos == -1:
                    offset = offset + m.end()
                    continue
                args_str = result[open_pos + 1:close_pos].strip()
                # 检查是否只有一个参数(避免多参数函数)
                if ',' not in args_str:
                    replacement = f"EXTRACT({part} FROM {args_str})"
                    result = result[:global_start] + replacement + result[close_pos + 1:]
                    self._add_change({
                        'type': 'function', 'line': 0,
                        'old': f'{func}({args_str})',
                        'new': replacement,
                        'desc': '日期部分函数'
                    })
                    offset = global_start + len(replacement)
                else:
                    offset = close_pos + 1
            tokens = result
        return tokens

    # ================================================================
    # 通用转换 - 全局变量
    # ================================================================

    def _convert_global_vars(self, tokens: str) -> str:
        """全局变量 @@ 转换"""
        global_var_mappings = {
            '@@ROWCOUNT': 'SQL%ROWCOUNT',
            '@@ERROR': 'SQL%ERROR_CODE',
            '@@IDENTITY': 'IDENT_CURRENT()',
            '@@TRANCOUNT': '1',  # 达梦不支持
            '@@VERSION': '-- @@VERSION 不支持',
            '@@SERVERNAME': '-- @@SERVERNAME 不支持',
            '@@SPID': '-- @@SPID 不支持',
        }
        for old_var, new_var in global_var_mappings.items():
            pattern = re.escape(old_var)
            new_tokens = re.sub(pattern, new_var, tokens, flags=re.IGNORECASE)
            if new_tokens != tokens:
                self._add_change({'type': 'global_var', 'line': 0, 'old': old_var, 'new': new_var, 'desc': '全局变量映射'})
                tokens = new_tokens
        return tokens

    # ================================================================
    # 通用转换 - SET语句
    # ================================================================

    def _convert_statements(self, tokens: str) -> str:
        """语句级转换"""
        statement_mappings = {
            'SET NOCOUNT ON': '',
            'SET NOCOUNT OFF': '',
            'SET XACT_ABORT ON': '-- SET XACT_ABORT ON (达梦不需要)',
            'SET ANSI_NULLS ON': '-- SET ANSI_NULLS ON (达梦不需要)',
            'SET ANSI_NULLS OFF': '-- SET ANSI_NULLS OFF (达梦不需要)',
            'SET ANSI_PADDING ON': '-- SET ANSI_PADDING ON (达梦不需要)',
            'SET ANSI_WARNINGS ON': '-- SET ANSI_WARNINGS ON (达梦不需要)',
            'SET QUOTED_IDENTIFIER ON': '-- SET QUOTED_IDENTIFIER ON (达梦不需要)',
            'SET QUOTED_IDENTIFIER OFF': '-- SET QUOTED_IDENTIFIER OFF (达梦不需要)',
            'SET CONCAT_NULL_YIELDS_NULL ON': '-- SET CONCAT_NULL_YIELDS_NULL ON (达梦不需要)',
        }
        for old_stmt, new_stmt in statement_mappings.items():
            pattern = r'^\s*' + re.escape(old_stmt) + r'\s*;?\s*\n?'
            if new_stmt:
                replacement = new_stmt + '\n'
            else:
                replacement = ''
            new_tokens = re.sub(pattern, replacement, tokens, flags=re.MULTILINE | re.IGNORECASE)
            if new_tokens != tokens:
                self._add_change({'type': 'statement', 'line': 0, 'old': old_stmt, 'new': new_stmt, 'desc': '语句映射'})
                tokens = new_tokens
        return tokens

    def _convert_truncate(self, tokens: str) -> str:
        """TRUNCATE TABLE xxx -> DELETE FROM xxx (达梦不支持TRUNCATE在存储过程内)"""
        new_tokens = re.sub(
            r'\bTRUNCATE\s+TABLE\s+',
            'DELETE FROM ',
            tokens,
            flags=re.IGNORECASE
        )
        if new_tokens != tokens:
            self._add_change({'type': 'statement', 'line': 0, 'old': 'TRUNCATE TABLE', 'new': 'DELETE FROM', 'desc': '达梦不支持TRUNCATE在存储过程内'})
        return new_tokens

    # ================================================================
    # 通用转换 - TRY-CATCH (括号深度匹配)
    # ================================================================

    def _convert_try_catch(self, tokens: str) -> str:
        """TRY...CATCH -> EXCEPTION
        改进: 用END TRY/END CATCH精确匹配，深度追踪只计数非TRY/CATCH的BEGIN/END
        """
        result = tokens
        max_iterations = 20

        for _ in range(max_iterations):
            # 找 BEGIN TRY
            m = re.search(r'\bBEGIN\s+TRY\b', result, re.IGNORECASE)
            if not m:
                break

            try_start = m.start()
            try_body_start = m.end()

            # 找对应的 END TRY (追踪非TRY/CATCH的BEGIN/END深度)
            depth = 0
            pos = try_body_start
            end_try_abs = None
            end_try_end_abs = None

            while pos < len(result):
                # 找下一个关键的BEGIN/END
                next_begin = re.search(r'\bBEGIN\b(?!\s+(?:TRY|CATCH)\b)', result[pos:], re.IGNORECASE)
                next_end_try = re.search(r'\bEND\s+TRY\b', result[pos:], re.IGNORECASE)
                next_end_catch = re.search(r'\bEND\s+CATCH\b', result[pos:], re.IGNORECASE)
                next_end_other = re.search(r'\bEND\b(?!\s+(?:TRY|CATCH)\b)', result[pos:], re.IGNORECASE)

                # 收集所有候选并按位置排序
                candidates = []
                if next_end_try:
                    candidates.append(('end_try', pos + next_end_try.start(), pos + next_end_try.end(), next_end_try))
                if next_begin:
                    candidates.append(('begin', pos + next_begin.start(), pos + next_begin.end(), next_begin))
                if next_end_other:
                    candidates.append(('end_other', pos + next_end_other.start(), pos + next_end_other.end(), next_end_other))
                if next_end_catch:
                    candidates.append(('end_catch', pos + next_end_catch.start(), pos + next_end_catch.end(), next_end_catch))

                if not candidates:
                    break

                candidates.sort(key=lambda x: x[1])
                kind, abs_start, abs_end, match = candidates[0]

                if kind == 'begin':
                    depth += 1
                    pos = abs_end
                elif kind == 'end_try':
                    if depth == 0:
                        end_try_abs = abs_start
                        end_try_end_abs = abs_end
                        break
                    else:
                        # 嵌套TRY-CATCH（罕见），降低深度
                        depth -= 1
                        pos = abs_end
                elif kind == 'end_other':
                    if depth > 0:
                        depth -= 1
                    pos = abs_end
                elif kind == 'end_catch':
                    # 不应该在这里遇到END CATCH
                    pos = abs_end

            if end_try_abs is None:
                break

            # 找 BEGIN CATCH
            catch_m = re.search(r'\bBEGIN\s+CATCH\b', result[end_try_end_abs:], re.IGNORECASE)
            if not catch_m:
                break

            catch_body_start = end_try_end_abs + catch_m.end()
            end_catch_m = re.search(r'\bEND\s+CATCH\b', result[catch_body_start:], re.IGNORECASE)
            if not end_catch_m:
                break

            catch_body = result[catch_body_start:catch_body_start + end_catch_m.start()].strip()
            end_catch_end_abs = catch_body_start + end_catch_m.end()

            try_body = result[try_body_start:end_try_abs].strip()

            # 替换整个 TRY-CATCH 块
            replacement = f"BEGIN\n{try_body}\nEXCEPTION WHEN OTHERS THEN\n{catch_body}\nEND;"
            result = result[:try_start] + replacement + result[end_catch_end_abs:]
            self._add_change({
                'type': 'try_catch', 'line': 0,
                'old': 'BEGIN TRY...END TRY BEGIN CATCH...END CATCH',
                'new': 'BEGIN...EXCEPTION WHEN OTHERS THEN...END;',
                'desc': '异常处理语法'
            })

        return result

    def _convert_transaction(self, tokens: str) -> str:
        """事务语句转换"""
        for old_t, new_t in [('COMMIT TRANSACTION', 'COMMIT'), ('ROLLBACK TRANSACTION', 'ROLLBACK'), ('SAVE TRANSACTION', 'SAVEPOINT')]:
            new_tokens = re.sub(r'\b' + old_t.replace(' ', r'\s+') + r'\b', new_t, tokens, flags=re.IGNORECASE)
            if new_tokens != tokens:
                self._add_change({'type': 'transaction', 'line': 0, 'old': old_t, 'new': new_t, 'desc': '事务语法'})
                tokens = new_tokens
        return tokens

    # ================================================================
    # 新增: TOP n 转换
    # ================================================================

    def _convert_top(self, tokens: str) -> str:
        """TOP n -> FETCH FIRST n ROWS ONLY / ROWNUM"""
        # SELECT TOP n ... -> SELECT ... FETCH FIRST n ROWS ONLY
        # 注意: 这个转换在token保护下做，所以字符串内的TOP不会被改
        def _replace_top(m):
            prefix = m.group(1)  # SELECT
            top_n = m.group(2)   # TOP后面的数字/表达式
            percent = m.group(3) # 是否有PERCENT
            rest = m.group(4)    # 后续内容
            if percent:
                # TOP n PERCENT -> 注释提醒(达梦不支持PERCENT)
                return f"{prefix}/* TOP {top_n} PERCENT - 需手动转换为达梦语法 */ {rest}"
            else:
                # 返回不加TOP的SELECT，后续加FETCH FIRST
                # 但FETCH FIRST要在ORDER BY之后...简单处理: 去掉TOP，加注释提醒
                # 更好的做法: SELECT ... FETCH FIRST n ROWS ONLY
                # 但如果有ORDER BY，FETCH要在ORDER BY之后
                # 这里简单处理: 去TOP，加FETCH到语句末尾(如果没ORDER BY则需要手动调)
                return f"{prefix}{rest}\nFETCH FIRST {top_n} ROWS ONLY"

        # 匹配 SELECT TOP n [PERCENT] ...
        new_tokens = re.sub(
            r'(SELECT\s+)TOP\s+(\d+|\@?\w+)(\s+PERCENT)?\s+(.*)',
            _replace_top,
            tokens,
            flags=re.IGNORECASE | re.DOTALL
        )
        if new_tokens != tokens:
            self._add_change({'type': 'top', 'line': 0, 'old': 'SELECT TOP n', 'new': 'SELECT ... FETCH FIRST n ROWS ONLY', 'desc': 'TOP子句转换'})
            tokens = new_tokens
        return tokens

    # ================================================================
    # 新增: 临时表 #temp 转换
    # ================================================================

    def _convert_temp_tables(self, tokens: str) -> str:
        """临时表 #temp / ##temp -> 达梦GTT或普通表
        v3.3.0: #开头的临时表单独给出建表语句(规则3)
        SQL Server临时表在存储过程中使用CREATE TABLE #xxx创建,
        达梦需要改为全局临时表(GTT),并单独给出建表语句。
        """
        # #table -> tmp_table (会话级临时表)
        # ##table -> gtmp_table (全局临时表)
        # 注意: 在token保护下做，所以字符串内的#不会被改

        # === 规则3: 提取所有#临时表建表语句 ===
        temp_table_defs = []  # [(原表名, 达梦表名, 列定义)]
        # 匹配 CREATE TABLE #xxx(...) 或 CREATE TABLE ##xxx(...)
        # 使用贪婪(.+)匹配到最后一个)，避免NVARCHAR(100)等中间)被误当表结束
        for m in re.finditer(
            r'CREATE\s+TABLE\s+(#{1,2})(\w+)\s*\((.+)\)',
            tokens,
            re.IGNORECASE | re.DOTALL
        ):
            hash_prefix = m.group(1)  # # 或 ##
            table_name = m.group(2)
            table_body = m.group(3)
            if hash_prefix == '##':
                original_name = f'##{table_name}'
                dm_name = f'gtmp_{table_name}'
            else:
                original_name = f'#{table_name}'
                dm_name = f'tmp_{table_name}'
            temp_table_defs.append((original_name, dm_name, table_body))

        # 替换 #表名引用(先##双#再#单#，避免##变成#tmp_)
        new_tokens = re.sub(r'##(\w+)', r'gtmp_\1', tokens)
        new_tokens = re.sub(r'#(\w+)', r'tmp_\1', new_tokens)
        if new_tokens != tokens:
            self._add_change({'type': 'temp_table', 'line': 0, 'old': '#table', 'new': 'tmp_table', 'desc': '临时表名转换(需确认达梦GTT定义)'})

        # CREATE TABLE tmp_xxx -> CREATE GLOBAL TEMPORARY TABLE tmp_xxx (过程中内联)
        new_tokens = re.sub(
            r'CREATE\s+TABLE\s+(tmp_|gtmp_)(\w+)',
            r'CREATE GLOBAL TEMPORARY TABLE \1\2',
            new_tokens,
            flags=re.IGNORECASE
        )

        # === 规则3: 在文件末尾追加独立的临时表建表语句 ===
        if temp_table_defs:
            new_tokens += '\n-- ========================================'
            new_tokens += '\n-- 以下为临时表独立建表语句(规则3: SQL Server #临时表单独拆出)'
            new_tokens += '\n-- 请根据实际情况选择GTT(全局临时表)或普通临时表\n'
            for original_name, dm_name, table_body in temp_table_defs:
                body = table_body.rstrip('\n')
                new_tokens += (
                    f'\n-- 原SQL Server临时表: {original_name}\n'
                    f'CREATE GLOBAL TEMPORARY TABLE "{dm_name}"\n'
                    f'({body}\n'
                    f') ON COMMIT PRESERVE ROWS;\n'
                )
                self._add_change({
                    'type': 'temp_table', 'line': 0,
                    'old': f'CREATE TABLE {original_name}',
                    'new': f'独立建表: CREATE GLOBAL TEMPORARY TABLE "{dm_name}"',
                    'desc': '临时表单独拆出建表语句(规则3)'
                })
            new_tokens += '-- ========================================\n'

        tokens = new_tokens

        # === SELECT INTO 转换 (达梦不支持 SELECT ... INTO 新表) ===
        # SQL Server: SELECT col1, col2 INTO #tmp_table FROM src WHERE ...
        # 达梦两种情况:
        #   1) INTO #临时表: CREATE GLOBAL TEMPORARY TABLE "tmp_xxx" AS SELECT ... FROM src WHERE ...
        #   2) INTO 普通表: INSERT INTO table SELECT ... FROM src WHERE ... (需要目标表已存在)

        def _convert_select_into(m):
            """SELECT col INTO table FROM rest -> CTAS(临时表) / INSERT SELECT(普通表)"""
            select_cols = m.group(1).strip()
            into_table = m.group(2).strip()
            from_clause = m.group(3).strip()

            is_temp = into_table.lower().startswith('tmp_') or into_table.lower().startswith('gtmp_')

            if is_temp:
                dm_table = into_table
                result = f'CREATE GLOBAL TEMPORARY TABLE "{dm_table}" AS SELECT {select_cols} FROM {from_clause}'
                self._add_change({
                    'type': 'select_into', 'line': 0,
                    'old': f'SELECT ... INTO {into_table}',
                    'new': f'CREATE GLOBAL TEMPORARY TABLE AS SELECT',
                    'desc': 'SELECT INTO临时表→CTAS创建GTT'
                })
            else:
                result = f'INSERT INTO {into_table} SELECT {select_cols} FROM {from_clause}'
                self._add_change({
                    'type': 'select_into', 'line': 0,
                    'old': f'SELECT ... INTO {into_table}',
                    'new': f'INSERT INTO {into_table} SELECT ...',
                    'desc': 'SELECT INTO普通表→INSERT INTO SELECT(需目标表已存在)'
                })
            return result

        # 匹配: SELECT <cols> INTO <tmp_table> FROM <rest>
        # #表名已在上一步被替换成tmp_/gtmp_
        tokens = re.sub(
            r'\bSELECT\s+(.+?)\s+INTO\s+(tmp_\w+|gtmp_\w+)\s+FROM\s+(.+)',
            _convert_select_into,
            tokens,
            flags=re.IGNORECASE
        )
        # 匹配还保留#的临时表名(如漏掉#替换的情况)
        tokens = re.sub(
            r'\bSELECT\s+(.+?)\s+INTO\s+(#\w+)\s+FROM\s+(.+)',
            lambda m: _convert_select_into(
                type('Match', (), {
                    'group': lambda self, i: [None, m.group(1), 'tmp_' + m.group(2).lstrip('#'), m.group(3)][i]
                })()
            ),
            tokens,
            flags=re.IGNORECASE
        )
        # 注意: 非临时表的 SELECT INTO 普通 FROM ... 暂不转换
        # 因为达梦 SELECT INTO 变量 的语法形式相同，无法区分
        # 用户需手动处理非临时表的 SELECT INTO

        # === DDL语句结尾加分号 (达梦过程体内DDL必须有;) ===
        # 处理过程体内的: CREATE GLOBAL TEMPORARY TABLE / DROP TABLE / ALTER TABLE / CREATE INDEX
        # 单行DDL: DROP TABLE xxx -> DROP TABLE xxx;
        # 跨行DDL: CREATE GLOBAL TEMPORARY TABLE "tmp_xxx"\n(id INT)\n ->
        #          CREATE GLOBAL TEMPORARY TABLE "tmp_xxx"\n(id INT);\n
        # 注意: 此时在token保护下,字符串内的DDL不会被误处理

        # 1) 单行DROP/ALTER TABLE缺分号
        tokens = re.sub(
            r'^(\s*(?:DROP|ALTER)\s+TABLE\s+\S+?)(\s*)$',
            r'\1;\2',
            tokens,
            flags=re.IGNORECASE | re.MULTILINE
        )
        # 2) 单行DROP INDEX缺分号
        tokens = re.sub(
            r'^(\s*DROP\s+INDEX\s+\S+?)(\s*)$',
            r'\1;\2',
            tokens,
            flags=re.IGNORECASE | re.MULTILINE
        )
        # 3) CREATE GLOBAL TEMPORARY TABLE 跨行建表: 用状态机在最后的)行加分号
        #    CTAS(AS SELECT)行已在SELECT INTO转换时加了分号，这里处理的是内联建表
        lines = tokens.split('\n')
        new_lines = []
        in_gtt_create = False
        for line in lines:
            stripped = line.strip()
            if re.match(r'\s*CREATE\s+GLOBAL\s+TEMPORARY\s+TABLE\b', stripped, re.IGNORECASE):
                # CTAS单行(AS SELECT ...)已在SELECT INTO转换时加了;，跳过
                if 'AS SELECT' in stripped.upper() and stripped.rstrip().endswith(';'):
                    in_gtt_create = False
                    new_lines.append(line)
                else:
                    in_gtt_create = True
                    new_lines.append(line)
            elif in_gtt_create:
                # 在GTT建表块内，找结束行: 以)结尾(可能带ON COMMIT...)
                if re.match(r'\s*\)\s*(ON\s+COMMIT\s+PRESERVE\s+ROWS\s*)?$', stripped, re.IGNORECASE):
                    if not line.rstrip().endswith(';'):
                        line = line.rstrip() + ';'
                    in_gtt_create = False
                    new_lines.append(line)
                elif stripped.endswith(';'):
                    # 已经有分号，结束
                    in_gtt_create = False
                    new_lines.append(line)
                else:
                    # 还在建表块内(列定义行等)，保持状态
                    new_lines.append(line)
            else:
                new_lines.append(line)
        tokens = '\n'.join(new_lines)

        return tokens

    # ================================================================
    # 新增: EXEC动态SQL转换
    # ================================================================

    def _convert_exec_dynamic(self, tokens: str) -> str:
        """EXEC/EXECUTE 动态SQL转换"""
        # EXEC sp_executesql @sql, N'...', @p1=... -> EXECUTE IMMEDIATE sql
        # EXEC(@sql) -> EXECUTE IMMEDIATE sql

        # sp_executesql -> EXECUTE IMMEDIATE (简化处理)
        new_tokens = re.sub(
            r'\bsp_executesql\s+',
            'EXECUTE IMMEDIATE ',
            tokens,
            flags=re.IGNORECASE
        )
        if new_tokens != tokens:
            self._add_change({'type': 'exec', 'line': 0, 'old': 'sp_executesql', 'new': 'EXECUTE IMMEDIATE', 'desc': '动态SQL执行'})
            tokens = new_tokens

        # EXEC(@sql) 或 EXEC @sql -> EXECUTE IMMEDIATE @sql
        # 注意: 不匹配 EXEC proc_name (存储过程调用)
        new_tokens = re.sub(
            r'\bEXEC(?:UTE)?\s*\(\s*(@?\w+)\s*\)',
            r'EXECUTE IMMEDIATE \1',
            tokens,
            flags=re.IGNORECASE
        )
        if new_tokens != tokens:
            self._add_change({'type': 'exec', 'line': 0, 'old': 'EXEC(@sql)', 'new': 'EXECUTE IMMEDIATE @sql', 'desc': '动态SQL执行'})
            tokens = new_tokens

        return tokens

    # ================================================================
    # 新增: PRINT / RAISERROR 转换
    # ================================================================

    def _convert_print_raiserror(self, tokens: str) -> str:
        """PRINT -> DBMS_OUTPUT.PUT_LINE, RAISERROR -> RAISE_APPLICATION_ERROR"""

        # PRINT 'msg' -> DBMS_OUTPUT.PUT_LINE('msg');
        # PRINT @var -> DBMS_OUTPUT.PUT_LINE(@var);
        # 逐行处理，确保正确包裹参数和添加分号
        lines = tokens.split('\n')
        fixed_lines = []
        for line in lines:
            # 匹配行内独立的PRINT语句
            m = re.match(r'^(\s*)PRINT\s+(.+?)(\s*)$', line, re.IGNORECASE)
            if m:
                indent = m.group(1)
                arg = m.group(2).strip()
                # 如果arg末尾已经有分号，去掉
                if arg.endswith(';'):
                    arg = arg[:-1].strip()
                fixed_lines.append(f"{indent}DBMS_OUTPUT.PUT_LINE({arg});")
            else:
                fixed_lines.append(line)
        new_tokens = '\n'.join(fixed_lines)

        if new_tokens != tokens:
            self._add_change({'type': 'print', 'line': 0, 'old': 'PRINT', 'new': 'DBMS_OUTPUT.PUT_LINE', 'desc': '输出函数'})
            tokens = new_tokens

        # RAISERROR('msg', severity, state) -> RAISE_APPLICATION_ERROR(-severity*10000-1, 'msg')
        result = tokens
        offset = 0
        while True:
            search_in = result[offset:]
            found = self._find_func_call(search_in, 'RAISERROR')
            if not found:
                break
            local_start, local_end, _, args = found
            global_start = offset + local_start
            global_end = offset + local_end

            if len(args) >= 2:
                msg = args[0].strip()
                severity = args[1].strip() if len(args) > 1 else '16'
                # 达梦: RAISE_APPLICATION_ERROR(error_code, msg)
                # error_code 范围: -20000 到 -20999
                replacement = f"RAISE_APPLICATION_ERROR(-20001, {msg})"
                result = result[:global_start] + replacement + result[global_end:]
                self._add_change({
                    'type': 'raiserror', 'line': 0,
                    'old': f'RAISERROR({msg}, {severity}, ...)',
                    'new': replacement,
                    'desc': '错误抛出函数'
                })
                offset = global_start + len(replacement)
            else:
                offset = global_end
        tokens = result
        return tokens

    # ================================================================
    # 新增: MERGE 转换
    # ================================================================

    def _convert_merge(self, tokens: str) -> str:
        """MERGE语句转换提醒(达梦MERGE语法有差异)"""
        # 达梦支持MERGE但语法有差异，添加注释提醒
        new_tokens = re.sub(
            r'\bMERGE\s+',
            '/* TODO: 验证MERGE语法兼容性 */ MERGE ',
            tokens,
            flags=re.IGNORECASE
        )
        if new_tokens != tokens:
            self._add_change({'type': 'merge', 'line': 0, 'old': 'MERGE', 'new': '/* TODO */ MERGE', 'desc': 'MERGE语句需验证兼容性'})
            tokens = new_tokens
        return tokens

    # ================================================================
    # 新增: 方括号标识符转换 [name] -> "name"
    # ================================================================

    def _convert_bracket_identifiers(self, tokens: str) -> str:
        """方括号标识符转换 (在token化后做，注释和字符串已被保护)
        
        规则(v3.5.3起):
        - 非类型名: [name] -> "name" (去方括号加双引号)
          如: [aa] -> "aa", [hrbi].[xxx] -> "hrbi"."xxx"
        - 类型名: [int] -> int, [nvarchar] -> nvarchar (去方括号不加双引号，后续做类型映射)
        
        注意: 此时注释、字符串和双引号标识符已被tokenize保护为占位符，
        所以这里的[和]只会出现在真实的SQL代码中，不会误改注释/字符串。
        """
        # SQL Server类型名集合(小写)，类型名去[]不加双引号，后续_convert_data_types做类型映射
        type_names_lower = {k.lower() for k in TYPE_MAPPINGS.keys()}
        
        def _replace_bracket(m):
            inner = m.group(1)
            # 类型名: 去方括号不加双引号(如[int]->int, [nvarchar]->nvarchar)
            # inner可能含空格如"int identity"，首段判断
            first_token = inner.split()[0].lower() if inner.split() else inner.lower()
            if first_token in type_names_lower:
                return inner  # 去掉方括号，不加双引号
            # 非类型名: 加双引号(如[aa]->"aa", [hrbi]->"hrbi")
            return f'"{inner}"'
        
        tokens = re.sub(r'\[([^\]\n]+)\]', _replace_bracket, tokens)
        return tokens

    # ================================================================
    # 新增: ISNULL模式转换(补充NVL之外的场景)
    # ================================================================

    def _convert_isnull_pattern(self, tokens: str) -> str:
        """补充ISNULL -> NVL的转换(ISNULL在简单替换中已处理，这里处理COALESCE等)"""
        # COALESCE 在达梦也支持，不需要转换
        return tokens

    # ================================================================
    # 变量语法转换(精确化)
    # ================================================================

    def _convert_variable_syntax(self, content: str) -> str:
        """
        变量语法转换（在token还原后执行，字符串已被保护）
        改进:
        - DECLARE @var TYPE -> var MAPPED_TYPE; (达梦过程体内不需要DECLARE,类型映射,加分号)
        - SET @var = expr -> var := expr
        - SELECT @var = expr FROM ... -> SELECT expr INTO var FROM ...; (达梦SELECT INTO语法)
        - @var -> var (去掉@前缀，但排除email等误改)
        """

        # 1. DECLARE @var TYPE -> v_var MAPPED_TYPE;
        #    支持: DECLARE @v1 INT
        #          DECLARE @v1 INT, @v2 VARCHAR(100)
        #          DECLARE @v1 VARCHAR(100), @v2 DECIMAL(18,2), @v3 INT
        #    达梦规范: 局部变量加v_前缀, 每个声明独立一行, 加分号
        #    同时收集DECLARE变量名, 用于步骤4中区分参数和局部变量
        self._declared_vars = set()  # 记录DECLARE中声明的变量名(不含@和v_)

        def _replace_declare_single(var_name, type_name, suffix):
            """替换单个变量声明"""
            base_type = type_name.lower().strip()
            mapped = TYPE_MAPPINGS.get(base_type, type_name)
            sfx = suffix or ''
            if base_type in ('varchar', 'nvarchar', 'varchar2') and '(max)' in sfx.lower():
                mapped = 'VARCHAR2' if base_type == 'varchar2' else 'VARCHAR'
                sfx = '(4096 CHAR)'
            # 记录变量名
            self._declared_vars.add(var_name.lower())
            # 变量加v_前缀(达梦规范), 如果原名已有v_前缀则不重复添加
            if var_name.lower().startswith('v_'):
                dm_name = var_name
            else:
                dm_name = 'v_' + var_name
            return f"{dm_name} {mapped}{sfx};"

        def _replace_declare_line(m):
            """替换一整行DECLARE(可能含多个变量)"""
            line = m.group(0)
            var_pattern = re.compile(
                r'@([\w]+)\s+([\w]+)(\([^)]*(?:\([^]]*\)[^]]*)*\))?'
            )
            parts = []
            for vm in var_pattern.finditer(line):
                vname = vm.group(1)
                tname = vm.group(2)
                tsuffix = vm.group(3) or ''
                parts.append(_replace_declare_single(vname, tname, tsuffix))
            indent_m = re.match(r'^(\s*)', line)
            indent = indent_m.group(1) if indent_m else ''
            return '\n'.join(indent + p for p in parts)

        # 匹配整行DECLARE
        new_content = re.sub(
            r'^(\s*)DECLARE\s+[\s\S]+?$',
            _replace_declare_line,
            content,
            flags=re.IGNORECASE | re.MULTILINE
        )
        if new_content != content:
            self._add_change({'type': 'variable', 'line': 0, 'old': 'DECLARE @var TYPE', 'new': 'v_var MAPPED_TYPE;', 'desc': '变量声明(v_前缀+类型映射+分号)'})
            content = new_content

        # 2. SET @var = expr -> v_var := expr (局部变量) 或 var := expr (参数)
        declared_set = getattr(self, '_declared_vars', set())
        def _replace_set_assign(m):
            var_name = m.group(1)
            if var_name.lower() in declared_set:
                if var_name.lower().startswith('v_'):
                    return var_name + ' :='
                return 'v_' + var_name + ' :='
            else:
                return var_name + ' :='
        new_content = re.sub(
            r'\bSET\s+@([\w]+)\s*=',
            _replace_set_assign,
            content,
            flags=re.IGNORECASE
        )
        if new_content != content:
            self._add_change({'type': 'variable', 'line': 0, 'old': 'SET @var =', 'new': 'v_var :=', 'desc': '变量赋值'})
            content = new_content

        # 3. SELECT @var = expr [FROM ...] -> SELECT INTO / 直接赋值
        # 策略: 逐行扫描，只在本行内做SELECT @var=匹配
        # 如果本行不包含FROM，在后续行中寻找FROM(但仅到分号/空行/下一个关键字为止)
        lines = content.split('\n')
        new_lines = []
        changed = False
        consumed = set()  # 被前面SELECT赋值消费掉的行号

        for i, line in enumerate(lines):
            if i in consumed:
                continue

            m = re.match(r'(\s*)SELECT\s+(@[\w]+\s*=\s*)', line, re.IGNORECASE)
            if not m:
                new_lines.append(line)
                continue

            indent = m.group(1)
            after_eq = line[m.end():]

            # 在本行找FROM
            from_m_in_line = re.search(r'\bFROM\b', after_eq, re.IGNORECASE)

            if from_m_in_line:
                # 本行有FROM: 直接分割
                assign_text = after_eq[:from_m_in_line.start()].strip()
                from_text = after_eq[from_m_in_line.end():].strip()
                # 去掉末尾分号
                if from_text.endswith(';'):
                    from_text = from_text[:-1]

                assigns = self._parse_select_assigns(m.group(2) + assign_text)
                if assigns:
                    exprs = ', '.join(e for _, e in assigns)
                    vars = ', '.join(self._dm_var_name(v) for v, _ in assigns)
                    new_lines.append(f"{indent}SELECT {exprs} INTO {vars} FROM {from_text};")
                    changed = True
                    continue
            else:
                # 本行无FROM: 需要检查后续行是否有FROM
                # 收集连续行(到分号/空行/非赋值续行)
                combined = after_eq
                end_line = i
                for j in range(i + 1, len(lines)):
                    if j in consumed:
                        break
                    next_line = lines[j]
                    # 空行或以关键字开头 -> 终止
                    stripped = next_line.strip()
                    if not stripped:
                        break
                    if re.match(r'\b(IF|WHILE|BEGIN|END|DECLARE|SET|SELECT|INSERT|UPDATE|DELETE|RETURN|PRINT|EXEC|GO)\b', stripped, re.IGNORECASE):
                        break
                    combined += ' ' + stripped
                    end_line = j
                    # 如果这行有分号，停止
                    if ';' in stripped:
                        break

                # 在combined文本中找顶层FROM
                from_pos = self._find_toplevel_from(combined)
                if from_pos is not None:
                    assign_text = combined[:from_pos].strip()
                    from_text = combined[from_pos + len('FROM'):].strip()
                    if from_text.endswith(';'):
                        from_text = from_text[:-1]

                    assigns = self._parse_select_assigns(m.group(2) + assign_text)
                    if assigns:
                        exprs = ', '.join(e for _, e in assigns)
                        vars = ', '.join(self._dm_var_name(v) for v, _ in assigns)
                        new_lines.append(f"{indent}SELECT {exprs} INTO {vars} FROM {from_text};")
                        # 标记被消费的行
                        for j in range(i + 1, end_line + 1):
                            consumed.add(j)
                        changed = True
                        continue
                else:
                    # 无FROM: 直接赋值
                    stmt_end = re.search(r';', combined)
                    if stmt_end:
                        assign_text = combined[:stmt_end.start()].strip()
                    else:
                        assign_text = combined.strip()

                    assigns = self._parse_select_assigns(m.group(2) + assign_text)
                    if assigns:
                        for var_name, expr in assigns:
                            new_lines.append(f"{indent}{self._dm_var_name(var_name)} := {expr.strip()};")
                        for j in range(i + 1, end_line + 1):
                            consumed.add(j)
                        changed = True
                        continue

            # 解析失败，保留原行
            new_lines.append(line)

        if changed:
            content = '\n'.join(new_lines)
            self._add_change({'type': 'variable', 'line': 0, 'old': 'SELECT @var = expr FROM', 'new': 'SELECT INTO / :=', 'desc': '变量赋值(SELECT INTO)'})

        # 4. 所有剩余的 @var -> var 或 v_var (排除@@全局变量、字符串已被保护)
        #    DECLARE过的局部变量加v_前缀(与声明一致), 参数/其他@var保持原名
        declared = getattr(self, '_declared_vars', set())
        def _replace_at_var(m):
            var_name = m.group(1)
            if var_name.lower() in declared:
                # 局部变量: 加v_前缀(除非原名已有v_)
                if var_name.lower().startswith('v_'):
                    return var_name
                return 'v_' + var_name
            else:
                # 参数或其他: 保持原名, 只去掉@
                return var_name
        new_content = re.sub(r'@([\w]+)', _replace_at_var, content)
        if new_content != content:
            self._add_change({'type': 'variable', 'line': 0, 'old': '@var', 'new': 'v_var(局部)/var(参数)', 'desc': '变量前缀(区分参数和局部变量)'})
            content = new_content

        return content

    def _dm_var_name(self, var_name: str) -> str:
        """将SQL Server变量名转为达梦变量名
        DECLARE过的局部变量加v_前缀, 参数/其他保持原名
        """
        declared = getattr(self, '_declared_vars', set())
        if var_name.lower() in declared:
            if var_name.lower().startswith('v_'):
                return var_name
            return 'v_' + var_name
        return var_name

    def _parse_select_assigns(self, text: str) -> list:
        """解析 SELECT @var1=expr1, @var2=expr2 格式的赋值列表
        返回 [(var_name, expr), ...] 或空列表
        """
        assigns = []
        remaining = text.strip()

        while remaining:
            am = re.match(r'\s*@([\w]+)\s*=\s*', remaining)
            if not am:
                break
            var_name = am.group(1)
            rest = remaining[am.end():]
            # 找下一个 @var= 的位置
            next_assign = re.search(r',\s*@[\w]+\s*=', rest)
            if next_assign:
                expr = rest[:next_assign.start()].strip().rstrip(',')
                # next_assign匹配的是 ", @var="，需要跳过逗号
                remaining = rest[next_assign.start():].lstrip(',').strip()
            else:
                expr = rest.strip().rstrip(',')
                remaining = ''
            if expr:
                assigns.append((var_name, expr))

        return assigns

    def _find_toplevel_from(self, text: str) -> Optional[int]:
        """在text中找顶层FROM关键字的位置(不在括号内的FROM)
        返回FROM的起始位置，或None
        """
        depth = 0
        pos = 0
        while pos < len(text):
            from_m = re.search(r'\bFROM\b', text[pos:], re.IGNORECASE)
            if not from_m:
                return None
            abs_pos = pos + from_m.start()
            # 计算到这个FROM位置之前的括号深度
            check = text[:abs_pos]
            d = 0
            for ch in check:
                if ch == '(':
                    d += 1
                elif ch == ')':
                    d -= 1
            if d == 0:
                return abs_pos
            pos = abs_pos + len('FROM')
        return None

    # ================================================================
    # GOTO/LABEL转换(修复误判)
    # ================================================================

    def _convert_goto_label(self, content: str) -> str:
        """
        GOTO/LABEL 转换
        改进: 排除时间格式(hh:mm:ss)、CASE WHEN等非标签冒号
        """
        lines = content.split('\n')
        result_lines = []

        for line in lines:
            stripped = line.strip()
            # 匹配: 独立一行的 label: (标签定义)
            # 排除: 时间格式(12:30:00)、:=赋值、CASE WHEN、数据类型等
            m = re.match(r'^(\s*)([\w]+)\s*:\s*$', line)
            if m:
                label_name = m.group(2)
                # 排除时间格式(数字开头的label)
                if re.match(r'^\d', label_name):
                    result_lines.append(line)
                    continue
                # 排除常见非标签的关键字
                non_labels = {'CASE', 'BEGIN', 'END', 'ELSE', 'THEN', 'WHEN', 'LOOP', 'IF'}
                if label_name.upper() in non_labels:
                    result_lines.append(line)
                    continue
                # 转换: label: -> <<label>>
                result_lines.append(f"{m.group(1)}<<{label_name}>>")
                self._add_change({'type': 'label', 'line': 0, 'old': f'{label_name}:', 'new': f'<<{label_name}>>', 'desc': '标签语法'})
            else:
                result_lines.append(line)

        return '\n'.join(result_lines)

    # ================================================================
    # Fix 1: 修复INTERVAL里变量被引号包裹
    # ================================================================

    def _fix_interval_variables(self, content: str) -> str:
        """
        修复INTERVAL里变量被引号包裹的问题
        INTERVAL '@days' DAY -> INTERVAL days DAY (变量,去掉引号和@)
        INTERVAL '7' DAY -> INTERVAL '7' DAY (数字字面量,保留引号)
        注意: @前缀在此步骤去掉(因为变量@替换可能在引号保护下漏掉了)
        """
        def _fix_interval(m):
            var_or_num = m.group(1)
            unit = m.group(2)
            # 去掉可能的@前缀
            var_or_num = var_or_num.lstrip('@')
            # 纯数字(可能带负号)保留引号
            if re.match(r'^-?\d+$', var_or_num):
                return m.group(0)
            # 标识符(变量名)去掉引号
            return f"INTERVAL {var_or_num} {unit}"

        result = re.sub(
            r"INTERVAL\s*'@?([a-zA-Z_]\w*)'\s+(DAY|MONTH|YEAR|HOUR|MINUTE|SECOND)",
            _fix_interval,
            content,
            flags=re.IGNORECASE
        )
        if result != content:
            self._add_change({'type': 'interval', 'line': 0, 'old': "INTERVAL 'var' UNIT", 'new': 'INTERVAL var UNIT', 'desc': 'INTERVAL变量去引号'})
        return result

    # ================================================================
    # Fix 5: 字符串连接 + -> ||
    # ================================================================

    def _replace_dbo_prefix(self, content: str) -> str:
        """替换dbo前缀为schema_prefix + 双点号处理 — 所有对象类型通用
        
        转换规则:
        - 三段式: "xxx"."dbo"."yyy" -> "xxx"."yyy" (dbo是SQL Server默认schema，删除)
        - 三段式裸名: xxx.dbo.yyy -> xxx.yyy (删dbo)
        - 三段式混合: xxx."dbo"."yyy" -> xxx."yyy" (删dbo)
        - 两段式有引号: "dbo"."yyy" -> "{prefix}""yyy" (dbo替换为schema_prefix)
        - 两段式裸名: dbo.yyy -> {prefix}.yyy (dbo替换为schema_prefix)
        - 双点号: xxx..yyy -> xxx.yyy
        
        schema_prefix来自输入文件名，如hrbi_stage.sql → hrbi_stage
        """
        prefix = self._schema_prefix
        # 双点号: xxx..yyy -> xxx.yyy (SQL Server省略dbo的写法)
        # 必须在三段式之前处理
        content = re.sub(r'"([^"]+)"\.\.', r'"\1".', content, flags=re.IGNORECASE)  # "xxx"."yyy"
        content = re.sub(r'\b(\w+)\.\.', r'\1.', content, flags=re.IGNORECASE)  # xxx..yyy
        # 三段式全引号: "xxx"."dbo"."yyy" -> "xxx"."yyy" (dbo是默认schema，直接删)
        content = re.sub(r'"([^"]+)"\."dbo"\.', r'"\1".', content, flags=re.IGNORECASE)
        # 三段式全裸名: xxx.dbo.yyy -> xxx.yyy (删dbo)
        content = re.sub(r'\b(\w+)\.dbo\.', r'\1.', content, flags=re.IGNORECASE)
        # 三段式混合(裸名+引号dbo): xxx."dbo"."yyy" -> xxx."yyy" (删dbo)
        content = re.sub(r'\b(\w+)\."dbo"\.', r'\1.', content, flags=re.IGNORECASE)
        # 两段式有引号: "dbo"."yyy" -> "{prefix}""yyy" (dbo替换为schema_prefix)
        if prefix:
            content = re.sub(r'"dbo"\.', f'"{prefix}".', content, flags=re.IGNORECASE)
        # 两段式裸名: dbo.yyy -> {prefix}.yyy (dbo替换为schema_prefix)
        if prefix:
            content = re.sub(r'\bdbo\.', f'{prefix}.', content, flags=re.IGNORECASE)
        return content

    def _post_convert_table_types(self, content: str) -> str:
        """表/视图数据类型后处理 - 在token还原后执行
        处理tokenize时被保护的方括号类型名如 [nvarchar]、[int] 等
        以及VARCHAR加CHAR定义
        """
        # 数据类型映射 — 方括号已在Step4去掉,这里只做裸类型名映射
        # 优化: 用单次正则+回调替代循环35+次全文替换
        # 重要: 按key长度降序排列，避免 DATETIME 抢先匹配 DATETIME2
        _type_map = TYPE_MAPPINGS
        _sorted_type_keys = sorted(_type_map.keys(), key=len, reverse=True)
        _bare_type_pattern = re.compile(
            r'(?<=\s)(' + '|'.join(re.escape(t) for t in _sorted_type_keys) + r')(?=\s*\(|\s+NULL|\s+NOT|\s+IDENTITY|\s+DEFAULT|\s+,|\s*\)|\s*$)',
            re.IGNORECASE
        )
        def _type_replacer(m):
            return _type_map[m.group(1).lower()]
        content = _bare_type_pattern.sub(_type_replacer, content)

        # dbo前缀替换 — 使用通用方法
        content = self._replace_dbo_prefix(content)

        # VARCHAR(n) -> VARCHAR(n CHAR) (达梦要求显式指定char语义)
        content = re.sub(
            r'\bVARCHAR\s*\(\s*(\d+)\s*\)',
            r'VARCHAR(\1 CHAR)',
            content,
            flags=re.IGNORECASE
        )

        # 去掉 ON [PRIMARY] / ON "PRIMARY" (可能在行尾带注释)
        content = re.sub(r'\s+ON\s+"?PRIMARY"?\s*$', '', content, flags=re.MULTILINE | re.IGNORECASE)
        content = re.sub(r'\s+ON\s+"?PRIMARY"?\s*(--.*)?$', '', content, flags=re.MULTILINE | re.IGNORECASE)

        # 去掉 GO 行（已转为 / 的不需要处理）
        content = re.sub(r'^\s*GO\s*$', '/', content, flags=re.MULTILINE | re.IGNORECASE)

        # GO; -> /
        content = re.sub(r'^\s*GO\s*;\s*$', '/', content, flags=re.MULTILINE | re.IGNORECASE)

        return content

    def _post_convert_generic_types(self, content):
        """非表/视图对象(存储过程/函数/触发器等)的方括号+类型映射+dbo替换
        与 _post_convert_table_types 类似但:
        - 不去 ON [PRIMARY] (过程体内没有)
        - 仍然做: 方括号类型映射 + [xxx]->"xxx" + dbo替换 + VARCHAR(n CHAR)
        """
        # 数据类型映射 - 方括号已在Step4去掉,这里只做裸类型名映射
        # 重要: 按key长度降序排列，避免 DATETIME 抢先匹配 DATETIME2
        _type_map = TYPE_MAPPINGS
        _sorted_type_keys = sorted(_type_map.keys(), key=len, reverse=True)
        _bare_type_pattern = re.compile(
            r'(?<=\s)(' + '|'.join(re.escape(t) for t in _sorted_type_keys) + r')(?=\s*\(|\s+NULL|\s+NOT|\s+IDENTITY|\s+DEFAULT|\s+,|\s*\)|\s*$)',
            re.IGNORECASE
        )
        def _type_replacer(m):
            return _type_map[m.group(1).lower()]
        content = _bare_type_pattern.sub(_type_replacer, content)

        # dbo前缀替换
        content = self._replace_dbo_prefix(content)

        # VARCHAR(n) -> VARCHAR(n CHAR) (达梦要求显式指定char语义)
        # 存储过程中变量声明和CAST中的VARCHAR也需要加CHAR语义
        content = re.sub(
            r'\bVARCHAR\s*\(\s*(\d+)\s*\)',
            r'VARCHAR(\1 CHAR)',
            content,
            flags=re.IGNORECASE
        )

        # GO -> /
        content = re.sub(r'^\s*GO\s*$', '/', content, flags=re.MULTILINE | re.IGNORECASE)

        return content

    def _convert_string_concat(self, content: str) -> str:
        """
        SQL Server字符串连接用+，达梦用||
        判断规则: +两边至少有一个是字符串字面量('...')时，+ -> ||
        注意: 数值加法不能改，如 1 + 2
        """
        # 模式1: '...' + (字符串在左边) -> '...' ||
        result = re.sub(r"('[^']*(?:''[^']*)*')\s*\+\s*", r'\1 || ', content)
        # 模式2: + '...' (字符串在右边) -> || '...'
        # 注意: 避免匹配 || 后面再跟 + '...'
        result = re.sub(r"\s*\+\s*('[^']*(?:''[^']*)*')", r' || \1', result)

        if result != content:
            self._add_change({'type': 'string_concat', 'line': 0, 'old': '+ (string)', 'new': '||', 'desc': '字符串连接运算符'})
        return result

    # ================================================================
    # Fix 4: IF...BEGIN...END -> IF...THEN...END IF
    # ================================================================

    def _convert_if_else(self, content: str) -> str:
        """
        IF condition BEGIN ... END -> IF condition THEN ... END IF;
        IF condition BEGIN ... END ELSE BEGIN ... END -> IF condition THEN ... ELSE ... END IF;
        ELSE IF -> ELSIF (达梦用ELSIF)
        """
        result = content
        max_iterations = 50

        for _ in range(max_iterations):
            # 匹配 IF condition BEGIN
            # condition: 不能包含 THEN/END IF/EXCEPTION等已转换关键字
            # 条件约束: condition不跨行(如果跨行则在同一行内匹配)
            # 使用排除THEN的模式: condition不能包含THEN关键字
            m = re.search(
                r'\bIF\s+([^\n]*?)\s+BEGIN\b',
                result,
                re.IGNORECASE
            )
            if not m:
                break

            condition = m.group(1).strip()
            # 跳过已经转换过的IF (条件包含THEN说明是已转换的)
            if 'THEN' in condition.upper():
                # 跳过这个匹配，从后面继续找
                # 方法: 在这个IF后面继续搜索
                # 但re.search每次从头开始，所以需要删除已处理的部分
                # 改用更精确的正则
                m2 = re.search(
                    r'(?:^|\n)\s*IF\s+(.+?)\s+BEGIN\b',
                    result,
                    re.IGNORECASE
                )
                if not m2:
                    break
                condition2 = m2.group(1).strip()
                if 'THEN' in condition2.upper():
                    break
                m = m2
                condition = condition2

            if_start = m.start()
            body_start = m.end()

            # 找匹配的END (考虑嵌套BEGIN...END)
            body_end, end_abs = self._find_matching_end(result, body_start)
            if body_end == -1:
                break

            body = result[body_start:body_end].strip()
            end_keyword_end = end_abs

            # 检查END后面是否有ELSE
            after_end = result[end_keyword_end:]
            else_match = re.match(r'\s*ELSE\b\s*BEGIN\b', after_end, re.IGNORECASE)

            if else_match:
                else_begin_pos = end_keyword_end + else_match.end()
                else_body_end, else_end_abs = self._find_matching_end(result, else_begin_pos)
                if else_body_end != -1:
                    else_body = result[else_begin_pos:else_body_end].strip()
                    total_end = else_end_abs
                    replacement = f"IF {condition} THEN\n{body}\nELSE\n{else_body}\nEND IF;"
                    result = result[:if_start] + replacement + result[total_end:]
                    self._add_change({'type': 'if_else', 'line': 0, 'old': 'IF...BEGIN...END ELSE BEGIN...END', 'new': 'IF...THEN...ELSE...END IF;', 'desc': 'IF-ELSE控制流'})
                    continue

            # 只有IF，没有ELSE
            replacement = f"IF {condition} THEN\n{body}\nEND IF;"
            result = result[:if_start] + replacement + result[end_keyword_end:]
            self._add_change({'type': 'if_else', 'line': 0, 'old': 'IF...BEGIN...END', 'new': 'IF...THEN...END IF;', 'desc': 'IF控制流'})

        # ELSE IF -> ELSIF
        result = re.sub(r'\bELSE\s+IF\b', 'ELSIF', result, flags=re.IGNORECASE)

        return result

    def _find_matching_end(self, content: str, start: int) -> tuple:
        """从start位置开始找匹配的END关键字（考虑嵌套BEGIN...END）
        返回 (body_end_pos, end_keyword_end_pos) 
        body_end_pos: body结束位置(不含END关键字)
        end_keyword_end_pos: END关键字之后的绝对位置
        如果没找到返回 (-1, -1)
        
        注意: 排除 END TRY / END CATCH 等复合END关键字
        """
        depth = 1
        pos = start
        while pos < len(content) and depth > 0:
            # 找下一个BEGIN或END关键字
            # 但需要排除 BEGIN TRY, BEGIN CATCH, END TRY, END CATCH
            next_begin = re.search(r'\bBEGIN\b(?!\s+(?:TRY|CATCH)\b)', content[pos:], re.IGNORECASE)
            next_end = re.search(r'\bEND\b(?!\s+(?:TRY|CATCH)\b)', content[pos:], re.IGNORECASE)

            if next_end and (not next_begin or next_end.start() <= next_begin.start()):
                depth -= 1
                if depth == 0:
                    body_end = pos + next_end.start()
                    end_keyword_end = pos + next_end.end()
                    return (body_end, end_keyword_end)
                pos += next_end.end()
            elif next_begin:
                depth += 1
                pos += next_begin.end()
            else:
                break

        return (-1, -1)

    # ================================================================
    # Fix 7: WHILE...BEGIN...END -> WHILE...LOOP...END LOOP
    # ================================================================

    def _convert_while_loop(self, content: str) -> str:
        """
        WHILE condition BEGIN ... END -> WHILE condition LOOP ... END LOOP;
        """
        result = content
        max_iterations = 50

        for _ in range(max_iterations):
            m = re.search(
                r'\bWHILE\s+(.+?)\s+BEGIN\b',
                result,
                re.IGNORECASE | re.DOTALL
            )
            if not m:
                break

            while_start = m.start()
            condition = m.group(1).strip()
            body_start = m.end()

            body_end, end_abs = self._find_matching_end(result, body_start)
            if body_end == -1:
                break

            body = result[body_start:body_end].strip()
            replacement = f"WHILE {condition} LOOP\n{body}\nEND LOOP;"
            result = result[:while_start] + replacement + result[end_abs:]
            self._add_change({'type': 'while', 'line': 0, 'old': 'WHILE...BEGIN...END', 'new': 'WHILE...LOOP...END LOOP;', 'desc': 'WHILE循环语法'})

        return result

    # ================================================================
    # 后处理
    # ================================================================

    def _add_ending_semicolon(self, content: str) -> str:
        """为TABLE/VIEW/INDEX/CONSTRAINT/SEQUENCE对象确保结尾有分号"""
        content = content.rstrip()
        # 去掉末尾的GO
        if re.search(r'\bGO\s*$', content, re.IGNORECASE):
            content = re.sub(r'\bGO\s*$', '', content, flags=re.IGNORECASE).rstrip()
        # 去掉末尾多余的分号(后面统一加一个)
        while content.endswith(';'):
            content = content[:-1].rstrip()
        content += ';\n'
        return content

    def _ensure_ddl_semicolons(self, content: str) -> str:
        """确保过程体内的DDL语句结尾有分号
        
        达梦存储过程体内，每条DDL(CREATE/ALTER/DROP TABLE/INDEX等)
        必须以分号结尾。此方法扫描过程体，为缺分号的DDL补上。
        注意: 只处理过程体内的DDL，不影响PROCEDURE声明和END;
        """
        lines = content.split('\n')
        new_lines = []
        # DDL关键字(排除PROCEDURE/FUNCTION声明)
        ddl_start = re.compile(
            r'^\s*(?:CREATE\s+(?:GLOBAL\s+TEMPORARY\s+)?(?!OR\s+REPLACE\s+(?:PROCEDURE|FUNCTION))'
            r'TABLE|CREATE\s+(?:GLOBAL\s+TEMPORARY\s+)?(?:INDEX|UNIQUE|VIEW)\b'
            r'|ALTER\s+(?:GLOBAL\s+TEMPORARY\s+)?TABLE\b'
            r'|DROP\s+(?:GLOBAL\s+TEMPORARY\s+)?TABLE\b'
            r'|DROP\s+INDEX\b)',
            re.IGNORECASE
        )
        # 也匹配 CREATE TABLE #xxx 形式(漏掉#替换的)
        ddl_start2 = re.compile(
            r'^\s*CREATE\s+TABLE\s+#?\w+',
            re.IGNORECASE
        )
        # 典型DML/PL语句开头(遇到表示上一条DDL已结束)，允许前导空白
        stmt_start = re.compile(
            r'^\s*(?:INSERT\s+INTO|SELECT\s|DELETE\s+FROM|UPDATE\s+\w|'
            r'CREATE|ALTER|DROP|EXEC(?:UTE)?(?:\s+IMMEDIATE)?\b|SET\s+@|SET\s+\w|'
            r'IF\s|WHILE\s|BEGIN\b|END\b|RETURN\b|PRINT\b|declare\s|'
            r'v_\w+\s+:=|COMMIT|ROLLBACK|MERGE\s)',
            re.IGNORECASE
        )
        in_ddl = False
        paren_depth = 0
        
        for line in lines:
            stripped = line.strip()
            # 保留注释行和空行，但不中断DDL状态
            if stripped.startswith('--') or not stripped:
                new_lines.append(line)
                continue
            
            if not in_ddl:
                # 检测DDL起始
                if ddl_start.match(stripped) or ddl_start2.match(stripped):
                    # 单行且已有分号
                    if stripped.endswith(';'):
                        new_lines.append(line)
                        continue
                    in_ddl = True
                    paren_depth = stripped.count('(') - stripped.count(')')
                    # 单行DDL: 如 DROP TABLE xxx 或 CREATE TABLE xxx(id INT)
                    if paren_depth <= 0 and not stripped.endswith('(') and not stripped.endswith(','):
                        if re.search(r'\)\s*$', stripped) or re.match(r'^\s*(?:DROP|ALTER)\s+TABLE', stripped, re.IGNORECASE):
                            if not stripped.endswith(';'):
                                line = line.rstrip() + ';'
                            in_ddl = False
                    new_lines.append(line)
                else:
                    new_lines.append(line)
            else:
                # 在DDL块内
                paren_depth += stripped.count('(') - stripped.count(')')
                
                # 检查这行是否是DDL块的结束行
                ends_ddl = False
                if paren_depth <= 0 and stripped.endswith(')'):
                    ends_ddl = True
                elif stripped.endswith(';'):
                    ends_ddl = True
                elif re.match(r'\s*\)\s*ON\s+COMMIT', stripped, re.IGNORECASE):
                    ends_ddl = True
                elif re.match(r'\s*\)\s+ON\s+PRIMARY\s*$', stripped, re.IGNORECASE):
                    # ) ON PRIMARY -> 去掉ON PRIMARY, 替换为);
                    line = re.sub(r'\s+ON\s+PRIMARY\s*$', ';', line.rstrip(), flags=re.IGNORECASE)
                    # 此行已有分号，不需要再补
                    in_ddl = False
                    new_lines.append(line)
                    continue
                # CTAS跨行: AS SELECT ... 子查询跨多行, 当遇到下一个语句开头时,
                # 说明CTAS在上一行结束但缺分号
                elif stmt_start.match(stripped) and not stripped.startswith(')'):
                    # 上一行应该结束DDL，补分号到上一行
                    if new_lines and not new_lines[-1].rstrip().endswith(';'):
                        new_lines[-1] = new_lines[-1].rstrip() + ';'
                    in_ddl = False
                    new_lines.append(line)
                    continue
                
                if ends_ddl:
                    if not stripped.endswith(';') and not stripped.rstrip().endswith(';'):
                        line = line.rstrip() + ';'
                    in_ddl = False
                    new_lines.append(line)
                else:
                    new_lines.append(line)
        
        # 兜底: DDL块到底未闭合,给最后非空行加分号
        if in_ddl and new_lines:
            for i in range(len(new_lines) - 1, -1, -1):
                s = new_lines[i].strip()
                if s and not s.startswith('--') and not s.endswith(';'):
                    new_lines[i] = new_lines[i].rstrip() + ';'
                    break
        
        result = '\n'.join(new_lines)
        return result

    def _ensure_statement_semicolons(self, content: str) -> str:
        """确保过程体内所有语句结尾有分号(DML + 变量赋值)
        
        达梦存储过程体内，每条DML(INSERT/DELETE/UPDATE/SELECT)和
        变量赋值(var := expr)都必须以分号结尾。
        此方法扫描过程体，为缺分号的语句补上。
        注意: 只处理过程体内的语句，不影响PROCEDURE声明和END;
        
        跨行语句处理:
        - INSERT INTO table_name (columns) SELECT ...  → 在SELECT结束后加分号
        - v_xxx := expr (非跨行) → 直接加分号
        - v_xxx := '(' 开头 → 跨行赋值，等到')'行加分号
        """
        lines = content.split('\n')
        new_lines = []
        
        def line_has_semicolon(s):
            """判断一行是否以分号结尾(忽略注释)"""
            stripped = s.rstrip()
            comment_pos = stripped.find('--')
            if comment_pos >= 0:
                stripped = stripped[:comment_pos].rstrip()
            return stripped.endswith(';')
        
        def is_comment_or_blank(s):
            stripped = s.strip()
            return stripped == '' or stripped.startswith('--')
        
        def is_end_keyword(s):
            stripped = s.strip()
            return bool(re.match(r'^END\s*$', stripped, re.IGNORECASE))
        
        def is_begin_keyword(s):
            stripped = s.strip()
            return bool(re.match(r'^BEGIN\s*$', stripped, re.IGNORECASE))
        
        def is_control_keyword(s):
            stripped = s.strip()
            return bool(re.match(r'^(IF|WHILE|CASE|EXCEPTION|THEN|ELSE)\b', stripped, re.IGNORECASE))
        
        # 判断一行是否是跨行语句的延续(列定义/括号内)
        def is_continuation_line(s):
            stripped = s.strip()
            # 以逗号结尾 → 列定义
            if stripped.endswith(','):
                return True
            # 以左括号开头 → 列定义列表
            if stripped.startswith('('):
                return True
            # 以右括号结尾 → 可能是跨行语句结束
            if stripped.endswith(')'):
                return True
            return False
        
        # 判断一行是否以表名结尾(INSERT INTO xxx)
        def ends_with_table_name(s):
            """INSERT INTO table_name 后面没有括号，说明列定义在下一行"""
            stripped = s.strip()
            if not re.match(r'(?:INSERT\s+INTO|UPDATE)\b', stripped, re.IGNORECASE):
                return False
            # 如果后面直接跟表名(不以(开头)，说明是跨行INSERT
            if not stripped.endswith('(') and not stripped.endswith(',') and not stripped.endswith(';'):
                return True
            return False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # 注释行和空行直接保留
            if is_comment_or_blank(line):
                new_lines.append(line)
                i += 1
                continue
            
            # END/BEGIN/控制流关键字直接保留
            if is_end_keyword(stripped) or is_begin_keyword(stripped) or is_control_keyword(stripped):
                new_lines.append(line)
                i += 1
                continue
            
            # 已有分号的行直接保留
            if line_has_semicolon(line):
                new_lines.append(line)
                i += 1
                continue
            
            # 跨行INSERT INTO table_name (列定义在下一行) → 不加分号
            if ends_with_table_name(stripped):
                new_lines.append(line)
                i += 1
                continue
            
            # 变量赋值行(v_xxx := 或 xxx :=)
            if re.match(r'^\s*(?:v_\w+|\w+)\s*:=', line, re.IGNORECASE):
                # 跨行赋值(以(或+或,结尾) → 不加分号
                if stripped.endswith('(') or stripped.endswith(',') or stripped.endswith('+'):
                    new_lines.append(line)
                    i += 1
                    continue
                else:
                    new_lines.append(line.rstrip() + ';')
                    i += 1
                    continue
            
            # DML: INSERT INTO (有括号) / DELETE FROM / UPDATE
            if re.match(r'^\s*(?:INSERT\s+INTO\s+\w|DELETE\s+FROM|UPDATE\s+\w)\b', line, re.IGNORECASE):
                # 单行DML(有括号或FROM/表名后直接结束) → 补分号
                new_lines.append(line.rstrip() + ';')
                i += 1
                continue
            
            # INSERT INTO (无括号，列定义在下一行) → 已在上面ends_with_table_name处理
            
            # SELECT 单独一行(CTAS的SELECT) → 不加分号，等后续处理
            if re.match(r'^\s*SELECT\b', line, re.IGNORECASE):
                # 如果前面是AS(CTAS)，AS行应该加分号
                if new_lines and re.search(r'\bAS\s*$', new_lines[-1].strip(), re.IGNORECASE):
                    new_lines[-1] = new_lines[-1].rstrip() + ';'
                new_lines.append(line)
                i += 1
                continue
            
            # COMMIT/ROLLBACK/RETURN/EXEC
            if re.match(r'^\s*(?:COMMIT|ROLLBACK|RETURN|GOTO)\b', line, re.IGNORECASE):
                new_lines.append(line.rstrip() + ';')
                i += 1
                continue
            if re.match(r'^\s*EXEC(?:UTE)?\b', line, re.IGNORECASE):
                new_lines.append(line.rstrip() + ';')
                i += 1
                continue
            
            # 其他情况：保留原样
            new_lines.append(line)
            i += 1
        
        # 处理跨行语句的结尾：
        # 如果某行以)结尾且前面是INSERT/SELECT/变量赋值，需要加分号
        result = '\n'.join(new_lines)
        return result

    def _add_terminator(self, content: str) -> str:
        """为存储过程/函数/触发器添加达梦终止符 /"""
        content = content.rstrip()
        # 去掉末尾的 GO 或 /（从GO转换来的）
        if re.search(r'\bGO\s*$', content, re.IGNORECASE):
            content = re.sub(r'\bGO\s*$', '', content, flags=re.IGNORECASE).rstrip()
        if content.endswith('/'):
            content = content[:-1].rstrip()
        # 去掉末尾的分号
        if content.endswith(';'):
            content = content[:-1].rstrip()
        # 确保END后有分号，然后加/
        if not content.endswith(';'):
            content += ';'
        content += '\n/\n'
        return content

    # ================================================================
    # 工具方法
    # ================================================================

    def get_conversion_summary(self) -> Dict[str, List[str]]:
        """获取转换摘要"""
        return {
            'supported_conversions': [
                'SQL Server -> 达梦数据库',
                '数据类型转换 (40+种类型映射)',
                '函数转换 (30+种函数映射, 参数正确重排)',
                'CONVERT(type,val) -> CAST(val AS type)',
                'DATEADD/DATEDIFF/DATEPART -> INTERVAL/EXTRACT',
                'STRING_AGG -> LISTAGG WITHIN GROUP',
                'STUFF -> SUBSTR拼接',
                '全局变量转换 (@@ROWCOUNT -> SQL%ROWCOUNT)',
                'TRY...CATCH -> EXCEPTION WHEN OTHERS THEN',
                '事务语句转换',
                '变量语法转换 (@var -> var, SET @var= -> var:=)',
                '触发器伪表转换 (inserted/deleted -> NEW/OLD)',
                '对象声明语法转换 (CREATE OR REPLACE)',
                'TOP n -> FETCH FIRST n ROWS ONLY',
                '临时表 #temp -> GTT tmp_temp',
                'EXEC动态SQL -> EXECUTE IMMEDIATE',
                'PRINT -> DBMS_OUTPUT.PUT_LINE',
                'RAISERROR -> RAISE_APPLICATION_ERROR',
                'MERGE兼容性提醒',
                '方括号标识符 [name] -> "name"',
            ],
            'supported_objects': [
                '存储过程 (PROCEDURE)',
                '函数 (FUNCTION)',
                '视图 (VIEW)',
                '触发器 (TRIGGER)',
                '表 (TABLE)',
                '索引 (INDEX)',
                '约束 (CONSTRAINT)',
                '序列 (SEQUENCE)',
            ],
            'limitations': [
                '复杂动态SQL可能需要手动调整',
                '某些高级函数可能需要手动调整',
                '临时表转换后需手动确认GTT定义',
                'CLR函数/存储过程不支持',
                'MERGE语句需验证兼容性',
                '游标语法差异可能需调整(DECLARE CURSOR需手动)',
                'TOP n PERCENT需手动转换',
                '多个SELECT变量赋值的拆分可能需要微调',
                'REPLICATE/LPAD多字符pad需验证',
            ]
        }


# ================================================================
# 便捷函数
# ================================================================

_converter = None

def get_converter() -> DMConverter:
    """获取转换器实例"""
    global _converter
    if _converter is None:
        _converter = DMConverter()
    return _converter


def convert_sqlserver_to_dm(content: str, conversion_type: str = 'generic', schema_prefix: str = '') -> str:
    """将SQL Server语法转换为达梦数据库语法（便捷函数，返回字符串）"""
    # 每次创建新实例，避免状态污染
    converter = DMConverter()
    result = converter.convert(content, conversion_type, schema_prefix)
    return result.converted


def convert_sqlserver_to_dm_with_result(content: str, conversion_type: str = 'generic', schema_prefix: str = '') -> ConversionResult:
    """将SQL Server语法转换为达梦数据库语法（返回完整结果）"""
    converter = DMConverter()
    return converter.convert(content, conversion_type, schema_prefix)


def get_conversion_summary() -> Dict[str, List[str]]:
    """获取转换摘要信息"""
    converter = get_converter()
    return converter.get_conversion_summary()