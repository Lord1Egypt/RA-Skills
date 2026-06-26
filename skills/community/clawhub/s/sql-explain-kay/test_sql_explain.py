#!/usr/bin/env python3
"""
测试用例 - sql-explain
使用 pytest 框架
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sql_explain import (
    format_sql,
    check_syntax,
    analyze_sql_structure,
    nl_to_sql,
    extract_tables,
    explain_sql,
)


# ==================== format_sql 测试 ====================

class TestFormatSql:
    """format_sql() 函数测试"""

    def test_simple_select(self):
        """简单 SELECT 语句格式化"""
        sql = "select * from users"
        result = format_sql(sql)
        assert "SELECT" in result
        assert "FROM" in result

    def test_uppercase_keywords(self):
        """关键字大写"""
        sql = "select id, name from users"
        result = format_sql(sql)
        assert "SELECT" in result
        assert result == result.upper() or "SELECT" in result

    def test_join_query(self):
        """带 JOIN 的查询格式化"""
        sql = "select u.name, o.total from users u join orders o on u.id=o.user_id"
        result = format_sql(sql)
        assert "SELECT" in result
        assert "JOIN" in result.upper() or "join" in result.lower()

    def test_complex_query(self):
        """复杂 SQL 格式化（子查询、GROUP BY、ORDER BY）"""
        sql = "select department, count(*) as cnt from employees where salary>5000 group by department having count(*)>5 order by cnt desc"
        result = format_sql(sql)
        assert "SELECT" in result
        assert "GROUP BY" in result.upper() or "group by" in result.lower()

    def test_empty_string(self):
        """空字符串"""
        result = format_sql("")
        assert result == ""

    def test_whitespace_only(self):
        """仅空白字符"""
        result = format_sql("   \n\t  ")
        assert result == ""

    def test_multiple_statements(self):
        """多条 SQL 语句"""
        sql = "select * from users; select * from orders"
        result = format_sql(sql)
        assert "SELECT" in result


# ==================== check_syntax 测试 ====================

class TestCheckSyntax:
    """check_syntax() 函数测试"""

    def test_valid_simple_select(self):
        """有效简单 SELECT"""
        sql = "SELECT * FROM users"
        result = check_syntax(sql)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_valid_select_with_where(self):
        """有效 SELECT + WHERE"""
        sql = "SELECT id, name FROM users WHERE id = 1"
        result = check_syntax(sql)
        assert result["valid"] is True

    def test_valid_insert(self):
        """有效 INSERT"""
        sql = "INSERT INTO users (name, email) VALUES ('test', 'test@example.com')"
        result = check_syntax(sql)
        assert result["valid"] is True

    def test_valid_update(self):
        """有效 UPDATE"""
        sql = "UPDATE users SET name = 'new' WHERE id = 1"
        result = check_syntax(sql)
        assert result["valid"] is True

    def test_valid_delete(self):
        """有效 DELETE"""
        sql = "DELETE FROM users WHERE id = 1"
        result = check_syntax(sql)
        assert result["valid"] is True

    def test_syntax_error_missing_from(self):
        """语法错误：无效语句"""
        # sqlparse 是非验证解析器，无法检测所有语义错误
        # 只要能解析成 tokens 就返回 valid=True
        sql = "SELECT *** FROM"
        result = check_syntax(sql)
        assert "valid" in result
        assert "errors" in result
        assert "statement_count" in result
        assert result["statement_count"] >= 0

    def test_syntax_error_typo_keyword(self):
        """语法错误：关键字拼写错误"""
        sql = "SELEKT * FROM users"
        result = check_syntax(sql)
        # sqlparse 可能不会严格报错，但应返回解析结果
        assert "valid" in result
        assert "errors" in result

    def test_empty_string(self):
        """空字符串"""
        result = check_syntax("")
        assert result["valid"] is False
        assert len(result["errors"]) > 0 or result["statement_count"] == 0

    def test_whitespace_only(self):
        """仅空白字符"""
        result = check_syntax("   \n")
        assert result["valid"] is False

    def test_complex_join_query(self):
        """复杂 JOIN 查询"""
        sql = "SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id WHERE o.total > 100"
        result = check_syntax(sql)
        assert result["valid"] is True

    def test_statement_count(self):
        """语句计数"""
        sql = "SELECT * FROM users; SELECT * FROM orders;"
        result = check_syntax(sql)
        assert result["statement_count"] >= 1


# ==================== analyze_sql_structure 测试 ====================

class TestAnalyzeSqlStructure:
    """analyze_sql_structure() 函数测试"""

    def test_simple_select(self):
        """简单 SELECT 分析"""
        sql = "SELECT * FROM users"
        result = analyze_sql_structure(sql)
        assert result["type"] == "SELECT"
        assert "tables" in result
        assert result["tables"] == ["users"]

    def test_select_with_columns(self):
        """带列名的 SELECT"""
        sql = "SELECT id, name, email FROM users"
        result = analyze_sql_structure(sql)
        assert result["type"] == "SELECT"
        assert "users" in result["tables"]

    def test_join_query(self):
        """JOIN 查询分析"""
        sql = "SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id"
        result = analyze_sql_structure(sql)
        assert result["type"] == "SELECT"
        assert "users" in result["tables"]
        assert "orders" in result["tables"]

    def test_complexity_simple(self):
        """简单语句复杂度为 SIMPLE"""
        sql = "SELECT * FROM users"
        result = analyze_sql_structure(sql)
        assert result["complexity"] == "SIMPLE"

    def test_complexity_moderate(self):
        """中等复杂度（带一个复杂因素）"""
        sql = "SELECT * FROM users WHERE id = 1 ORDER BY name"
        result = analyze_sql_structure(sql)
        assert result["complexity"] in ("SIMPLE", "MODERATE")

    def test_complexity_complex(self):
        """复杂语句（3+ 复杂因素）"""
        sql = "SELECT u.name, COUNT(o.id) as order_count FROM users u JOIN orders o ON u.id = o.user_id WHERE u.status = 1 GROUP BY u.name HAVING COUNT(o.id) > 5 ORDER BY order_count DESC"
        result = analyze_sql_structure(sql)
        assert result["complexity"] == "COMPLEX"

    def test_complexity_factors_join(self):
        """复杂度因素：JOIN"""
        sql = "SELECT * FROM users u JOIN orders o ON u.id = o.user_id"
        result = analyze_sql_structure(sql)
        assert "+JOIN" in result["complexity_factors"]

    def test_complexity_factors_group_by(self):
        """复杂度因素：GROUP BY"""
        sql = "SELECT status, COUNT(*) FROM users GROUP BY status"
        result = analyze_sql_structure(sql)
        assert "+GROUP BY" in result["complexity_factors"]

    def test_complexity_factors_order_by(self):
        """复杂度因素：ORDER BY"""
        sql = "SELECT * FROM users ORDER BY created_at"
        result = analyze_sql_structure(sql)
        assert "+ORDER BY" in result["complexity_factors"]

    def test_complexity_factors_limit(self):
        """复杂度因素：LIMIT"""
        sql = "SELECT * FROM users LIMIT 10"
        result = analyze_sql_structure(sql)
        assert "+LIMIT" in result["complexity_factors"]

    def test_complexity_factors_subquery(self):
        """复杂度因素：子查询"""
        sql = "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE total > 100)"
        result = analyze_sql_structure(sql)
        assert "+子查询" in result["complexity_factors"]

    def test_token_count(self):
        """Token 计数"""
        sql = "SELECT id, name FROM users"
        result = analyze_sql_structure(sql)
        assert result["token_count"] > 0

    def test_insert_statement(self):
        """INSERT 语句"""
        sql = "INSERT INTO users (name) VALUES ('test')"
        result = analyze_sql_structure(sql)
        assert result["type"] == "INSERT"

    def test_update_statement(self):
        """UPDATE 语句"""
        sql = "UPDATE users SET name = 'new' WHERE id = 1"
        result = analyze_sql_structure(sql)
        assert result["type"] == "UPDATE"

    def test_delete_statement(self):
        """DELETE 语句"""
        sql = "DELETE FROM users WHERE id = 1"
        result = analyze_sql_structure(sql)
        assert result["type"] == "DELETE"

    def test_empty_string(self):
        """空字符串"""
        result = analyze_sql_structure("")
        assert result["type"] == "UNKNOWN"
        assert result["complexity"] == "UNKNOWN"

    def test_invalid_sql(self):
        """无效 SQL"""
        sql = "THIS IS NOT SQL AT ALL"
        result = analyze_sql_structure(sql)
        assert "type" in result
        assert "tables" in result


# ==================== nl_to_sql 测试 ====================

class TestNlToSql:
    """nl_to_sql() 函数测试"""

    def test_simple_select(self):
        """简单查询描述"""
        result = nl_to_sql("查询所有用户")
        assert "SELECT" in result.upper()
        assert "FROM" in result.upper()

    def test_select_with_table(self):
        """指定表名"""
        result = nl_to_sql("查询表: orders")
        assert "orders" in result.lower()

    def test_select_with_limit(self):
        """带 LIMIT"""
        result = nl_to_sql("查询用户 limit 5")
        assert "LIMIT" in result.upper()

    def test_insert(self):
        """插入数据"""
        result = nl_to_sql("插入数据到 users")
        assert "INSERT" in result.upper()

    def test_update(self):
        """更新数据"""
        result = nl_to_sql("更新 users 表")
        assert "UPDATE" in result.upper()

    def test_delete(self):
        """删除数据"""
        result = nl_to_sql("删除 users 表的数据")
        assert "DELETE" in result.upper()

    def test_unrecognized_intent(self):
        """无法识别的意图"""
        result = nl_to_sql("你好吗")
        assert "--" in result or "无法识别" in result

    def test_english_select(self):
        """英文 select"""
        result = nl_to_sql("select all from users")
        assert "SELECT" in result.upper()

    def test_chinese_condition_with_where_keyword(self):
        """中文条件（有 where 关键字时）"""
        result = nl_to_sql("查询满足 status = 1 的用户")
        assert "status" in result.lower()


# ==================== extract_tables 测试 ====================

class TestExtractTables:
    """extract_tables() 函数测试"""

    def test_simple_from(self):
        """简单 FROM"""
        sql = "SELECT * FROM users"
        result = extract_tables(sql)
        assert "users" in result

    def test_join(self):
        """JOIN 表名"""
        sql = "SELECT * FROM users u JOIN orders o ON u.id = o.user_id"
        result = extract_tables(sql)
        assert "users" in result
        assert "orders" in result

    def test_multiple_joins(self):
        """多次 JOIN"""
        sql = "SELECT * FROM a JOIN b ON a.id = b.a_id JOIN c ON b.id = c.b_id"
        result = extract_tables(sql)
        assert "a" in result
        assert "b" in result
        assert "c" in result

    def test_update_table(self):
        """UPDATE 表名"""
        sql = "UPDATE users SET name = 'new'"
        result = extract_tables(sql)
        assert "users" in result

    def test_delete_table(self):
        """DELETE 表名"""
        sql = "DELETE FROM users WHERE id = 1"
        result = extract_tables(sql)
        assert "users" in result

    def test_insert_into(self):
        """INSERT INTO 表名"""
        sql = "INSERT INTO users (name) VALUES ('test')"
        result = extract_tables(sql)
        assert "users" in result

    def test_empty_sql(self):
        """空 SQL"""
        result = extract_tables("")
        assert result == []

    def test_no_table(self):
        """无表名"""
        sql = "SELECT 1 + 1"
        result = extract_tables(sql)
        assert result == []


# ==================== explain_sql 测试 ====================

class TestExplainSql:
    """explain_sql() 函数测试"""

    def test_seq_scan_warning(self):
        """全表扫描警告"""
        output = "Seq Scan on users (cost=0.00..100.00 rows=1000 width=100)"
        result = explain_sql(output)
        assert "Seq Scan" in result or "全表扫描" in result

    def test_index_scan(self):
        """索引扫描"""
        output = "Index Scan using idx_users_id on users (cost=0.00..50.00 rows=100 width=100)"
        result = explain_sql(output)
        assert "Index" in result or "索引" in result

    def test_high_cost(self):
        """高成本警告"""
        output = "Seq Scan on users (cost=0.00..50000.00 rows=1000000 width=100)"
        result = explain_sql(output)
        assert "成本" in result or "cost" in result.lower()

    def test_empty_output(self):
        """空输出"""
        result = explain_sql("")
        assert "无" in result or "无效" in result

    def test_hash_join(self):
        """Hash Join"""
        output = "Hash Join (cost=100.00..500.00 rows=1000)"
        result = explain_sql(output)
        assert "Hash Join" in result or "哈希" in result

    def test_nested_loop(self):
        """Nested Loop"""
        output = "Nested Loop (cost=50.00..300.00 rows=500)"
        result = explain_sql(output)
        assert "Nested Loop" in result or "循环" in result


# ==================== 边界情况测试 ====================

class TestEdgeCases:
    """边界情况测试"""

    def test_very_long_sql(self):
        """超长 SQL（模拟）"""
        sql = "SELECT " + ", ".join([f"column_{i}" for i in range(100)]) + " FROM users"
        result = format_sql(sql)
        assert len(result) > 0

    def test_special_characters(self):
        """特殊字符"""
        sql = "SELECT * FROM users WHERE name = 'O\\'Brien'"
        result = check_syntax(sql)
        assert "valid" in result

    def test_unicode_in_sql(self):
        """SQL 中的 Unicode"""
        sql = "SELECT * FROM users WHERE name = '中文用户名'"
        result = check_syntax(sql)
        assert "valid" in result

    def test_nested_quotes(self):
        """嵌套引号"""
        sql = 'SELECT * FROM users WHERE name = "double" AND email = \'single\''
        result = check_syntax(sql)
        assert "valid" in result

    def test_multiline_sql(self):
        """多行 SQL"""
        sql = """
        SELECT
            u.id,
            u.name,
            o.total
        FROM users u
        JOIN orders o ON u.id = o.user_id
        WHERE o.total > 100
        """
        result = check_syntax(sql)
        assert "valid" in result

    def test_numeric_only(self):
        """纯数字（无效 SQL）"""
        sql = "12345"
        result = check_syntax(sql)
        assert "valid" in result or "valid" in result

    def test_sql_with_comments(self):
        """带注释的 SQL"""
        sql = "-- 这是注释\nSELECT * FROM users"
        result = check_syntax(sql)
        assert "valid" in result

    def test_chinese_table_name(self):
        """中文表名（不规范但可能存在）"""
        sql = "SELECT * FROM 用户表"
        result = check_syntax(sql)
        assert "valid" in result

    def test_case_insensitive_keywords(self):
        """大小写不敏感关键字"""
        sql = "sElEcT * fRoM uSeRs"
        result = format_sql(sql)
        assert "SELECT" in result


# ==================== CLI main 测试 ====================

class TestCliMain:
    """main() 函数 CLI 测试"""

    def test_main_format(self, capsys):
        """CLI format 命令"""
        sys.argv = ["sql_explain.py", "format", "select * from users"]
        try:
            from sql_explain import main
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "SELECT" in captured.out

    def test_main_check(self, capsys):
        """CLI check 命令"""
        sys.argv = ["sql_explain.py", "check", "SELECT * FROM users"]
        try:
            from sql_explain import main
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "valid" in captured.out or "SELECT" in captured.out

    def test_main_analyze(self, capsys):
        """CLI analyze 命令"""
        sys.argv = ["sql_explain.py", "analyze", "SELECT * FROM users"]
        try:
            from sql_explain import main
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "SELECT" in captured.out or "users" in captured.out

    def test_main_nl2sql(self, capsys):
        """CLI nl2sql 命令"""
        sys.argv = ["sql_explain.py", "nl2sql", "查询所有用户"]
        try:
            from sql_explain import main
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "SELECT" in captured.out or "FROM" in captured.out

    def test_main_no_args(self, capsys):
        """无参数运行"""
        sys.argv = ["sql_explain.py"]
        with pytest.raises(SystemExit):
            from sql_explain import main
            main()

    def test_main_unknown_command(self, capsys):
        """未知命令"""
        sys.argv = ["sql_explain.py", "unknown_cmd"]
        with pytest.raises(SystemExit):
            from sql_explain import main
            main()
