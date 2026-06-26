#!/usr/bin/env python3
"""
SQL 依赖分析器 v2.0
- 使用 common.py 共享枚举和关键字表，不再重复定义
- 函数调用检测改为限定模式（FROM/JOIN/INTO/SET 后的标识符 + 显式 CALL/EXEC）
- 大幅减少误报
- 合并脚本按方言适配（Oracle 用 @, SQL Server 用 :r, MySQL/PG 用 source）
"""

import re
from typing import Dict, List, Set, Optional
from collections import defaultdict
from datetime import datetime

from common import SQLDialect, OBJECT_PREFIXES, TYPE_PRIORITY, SQL_KEYWORDS


class DependencyAnalyzer:
    """SQL 对象依赖分析器"""

    # DML 引用模式 — 只在这些子句中提取表/视图/过程名
    _TABLE_REF_PATTERNS = [
        # FROM / JOIN 目标
        re.compile(r'\b(?:FROM|JOIN)\s+([a-zA-Z_][\w.]*)', re.IGNORECASE),
        # INSERT INTO / UPDATE / DELETE FROM
        re.compile(r'\bINSERT\s+INTO\s+([a-zA-Z_][\w.]*)', re.IGNORECASE),
        re.compile(r'\bUPDATE\s+([a-zA-Z_][\w.]*)', re.IGNORECASE),
        re.compile(r'\bDELETE\s+FROM\s+([a-zA-Z_][\w.]*)', re.IGNORECASE),
        # MERGE INTO
        re.compile(r'\bMERGE\s+INTO\s+([a-zA-Z_][\w.]*)', re.IGNORECASE),
        # CALL / EXEC(UTE) — 存储过程调用
        re.compile(r'\b(?:CALL|EXEC(?:UTE)?)\s+([a-zA-Z_][\w.]*)', re.IGNORECASE),
        # USING — MERGE source
        re.compile(r'\bUSING\s+([a-zA-Z_][\w.]*)', re.IGNORECASE),
    ]

    # 函数/过程调用模式 — 限定在赋值或表达式上下文
    # 例如: v_result := my_func(...), SELECT my_func(...) INTO ...
    _FUNC_CALL_PATTERNS = [
        # PL/SQL 赋值: var := func_name(
        re.compile(r':=\s*([a-zA-Z_][\w.]*)\s*\('),
        # SELECT ... INTO 中的函数
        re.compile(r'\bSELECT\s+.*?([a-zA-Z_][\w.]*)\s*\(', re.IGNORECASE),
        # WHERE/HAVING 中的函数
        re.compile(r'\b(?:WHERE|HAVING|ON|AND|OR)\s+.*?([a-zA-Z_][\w.]*)\s*\(', re.IGNORECASE),
    ]

    def __init__(self, dialect: SQLDialect = SQLDialect.GENERIC):
        self.dialect = dialect
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.objects: Dict[str, dict] = {}

    def add_object(self, obj_type: str, name: str, content: str):
        """添加一个 SQL 对象"""
        obj_key = f"{obj_type}:{name}"
        self.objects[obj_key] = {
            'type': obj_type,
            'name': name,
            'content': content,
            'dependencies': set(),
        }

    def analyze_references(self, content: str) -> Set[str]:
        """分析 SQL 内容中引用的其他对象（表、视图、过程、函数）"""
        refs = set()

        # 1. 表/视图/过程引用
        for pattern in self._TABLE_REF_PATTERNS:
            for m in pattern.finditer(content):
                name = m.group(1).lower()
                # 过滤掉 SQL 关键字和伪表
                if name not in SQL_KEYWORDS and name not in (
                    'dual', 'sysdummy1', 'deleted', 'inserted',
                ):
                    refs.add(name)

        # 2. 函数调用引用（限定上下文，大幅减少误报）
        for pattern in self._FUNC_CALL_PATTERNS:
            for m in pattern.finditer(content):
                name = m.group(1).lower()
                if name not in SQL_KEYWORDS:
                    refs.add(name)

        # 3. 排除自引用
        return refs

    def analyze_all(self):
        """分析所有对象的依赖关系"""
        for obj_key, obj in self.objects.items():
            refs = self.analyze_references(obj['content'])
            obj_name_lower = obj['name'].lower()

            for ref in refs:
                # 跳过自引用
                if ref == obj_name_lower or ref.endswith('.' + obj_name_lower):
                    continue

                # 检查引用是否指向已知对象
                for other_key in self.objects:
                    other_name = self.objects[other_key]['name'].lower()
                    if ref == other_name or ref.endswith('.' + other_name):
                        obj['dependencies'].add(other_key)
                        break

        return self.dependencies

    def topological_sort(self) -> List[str]:
        """拓扑排序，生成正确的导入顺序"""
        in_degree = defaultdict(int)
        graph = defaultdict(set)

        for obj_key in self.objects:
            in_degree[obj_key] = 0

        for obj_key, obj in self.objects.items():
            for dep in obj['dependencies']:
                graph[dep].add(obj_key)
                in_degree[obj_key] += 1

        # Kahn 算法
        queue = [k for k in self.objects if in_degree[k] == 0]
        result = []

        while queue:
            # 同层级按类型优先级排序
            queue.sort(key=lambda x: TYPE_PRIORITY.get(self.objects[x]['type'], 99))
            current = queue.pop(0)
            result.append(current)

            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 检测循环依赖
        if len(result) != len(self.objects):
            remaining = [k for k in self.objects if k not in result]
            # 循环依赖时，把剩余的按类型优先级追加（而不是报错中断）
            remaining.sort(key=lambda x: TYPE_PRIORITY.get(self.objects[x]['type'], 99))
            result.extend(remaining)

        return result

    def generate_merge_script(self, output_path: str, split_dir: str,
                              dialect: Optional[SQLDialect] = None) -> str:
        """生成合并脚本 merge_all.sql，按方言适配语法"""
        if dialect is None:
            dialect = self.dialect

        try:
            order = self.topological_sort()
        except ValueError:
            order = sorted(
                self.objects.keys(),
                key=lambda x: TYPE_PRIORITY.get(self.objects[x]['type'], 99),
            )

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "-- 自动生成的合并脚本",
            f"-- 生成时间: {ts}",
            f"-- 目标方言: {dialect.value.upper()}",
            "-- 按依赖关系排序导入",
            "",
        ]

        # 方言特定的头
        if dialect == SQLDialect.SQLSERVER:
            lines.extend(["SET NOCOUNT ON;", "GO", ""])
        elif dialect == SQLDialect.ORACLE:
            lines.extend(["SET ECHO OFF;", "SET DEFINE OFF;", ""])
        elif dialect == SQLDialect.DM:
            lines.extend(["SET ECHO OFF;", ""])
        elif dialect == SQLDialect.POSTGRESQL:
            lines.extend(["\\set ON_ERROR_STOP on", ""])
        elif dialect == SQLDialect.MYSQL:
            lines.extend(["SET @OLD_SQL_MODE=@@SQL_MODE;", ""])

        # 方言对应的文件包含方式
        include_map = {
            SQLDialect.ORACLE: '@@',       # @ 或 @@
            SQLDialect.SQLSERVER: ':r ',   # SQLCMD 模式
            SQLDialect.POSTGRESQL: '\\i ',  # psql
            SQLDialect.MYSQL: 'source ',   # mysql client
            SQLDialect.DM: '@@',           # 同 Oracle
            SQLDialect.GENERIC: '-- ',      # 通用：只注释
        }
        include_prefix = include_map.get(dialect, '-- ')

        for i, obj_key in enumerate(order):
            obj = self.objects[obj_key]
            obj_type = obj['type']
            name = obj['name']

            prefix = OBJECT_PREFIXES.get(obj_type, 'obj')
            filename = f"{prefix}_{name}.sql"

            dep_str = ''
            if obj['dependencies']:
                dep_names = [self.objects[d]['name'] for d in sorted(obj['dependencies'])]
                dep_str = f"  -- depends on: {', '.join(dep_names)}"

            lines.extend([
                f"-- [{i+1}/{len(order)}] {obj_type}: {name}{dep_str}",
                f"{include_prefix}{filename}",
                "",
            ])

        # 方言特定的尾
        if dialect == SQLDialect.SQLSERVER:
            lines.extend(["", "GO", "", "PRINT 'All objects loaded successfully';"])
        elif dialect in (SQLDialect.ORACLE, SQLDialect.DM):
            lines.extend(["", "/", "", "-- All objects loaded successfully"])
        elif dialect == SQLDialect.POSTGRESQL:
            lines.extend(["", "-- All objects loaded successfully"])
        elif dialect == SQLDialect.MYSQL:
            lines.extend(["", "SET SQL_MODE=@OLD_SQL_MODE;", "", "-- All objects loaded successfully"])
        else:
            lines.extend(["", "-- All objects loaded successfully"])

        content = '\n'.join(lines)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

        return content

    def generate_dependency_report(self) -> str:
        """生成依赖关系报告"""
        lines = [
            "# SQL 对象依赖分析报告",
            "",
            "## 对象列表",
            "",
        ]

        # 按类型分组
        by_type = defaultdict(list)
        for obj_key, obj in self.objects.items():
            by_type[obj['type']].append(obj['name'])

        for obj_type in sorted(by_type.keys()):
            lines.append(f"### {obj_type}")
            for name in sorted(by_type[obj_type]):
                lines.append(f"- {name}")
            lines.append("")

        lines.extend([
            "## 依赖关系",
            "",
        ])

        for obj_key in self.topological_sort():
            obj = self.objects[obj_key]
            if obj['dependencies']:
                lines.append(f"**{obj['name']}** ({obj['type']}):")
                for dep in sorted(obj['dependencies']):
                    dep_obj = self.objects[dep]
                    lines.append(f"  -> {dep_obj['name']} ({dep_obj['type']})")
                lines.append("")

        return '\n'.join(lines)


if __name__ == "__main__":
    # 测试
    analyzer = DependencyAnalyzer()

    analyzer.add_object('table', 'users', 'CREATE TABLE users (id INT PRIMARY KEY);')
    analyzer.add_object('table', 'orders', 'CREATE TABLE orders (id INT, user_id INT REFERENCES users(id));')
    analyzer.add_object('function', 'get_user_name', 'SELECT name FROM users WHERE id = ?')
    analyzer.add_object('procedure', 'create_order', 'INSERT INTO orders SELECT * FROM temp_orders')

    analyzer.analyze_all()

    print("导入顺序:", analyzer.topological_sort())
    print()
    print(analyzer.generate_dependency_report())
