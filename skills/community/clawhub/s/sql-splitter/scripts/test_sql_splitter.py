#!/usr/bin/env python3
"""
SQL 拆分工具单元测试
覆盖：方言检测、对象边界检测、BEGIN/END 深度匹配、依赖分析、合并脚本生成
"""

import os
import sys
import tempfile
import unittest

# 让 import 能找到 scripts 目录
sys.path.insert(0, os.path.dirname(__file__))

from common import (
    SQLDialect, OBJECT_PREFIXES, clean_object_name,
    strip_sql_comments, find_matching_end, _is_keyword_at,
)
from split_sql import (
    detect_dialect, find_object_end, find_block_end,
    find_semicolon_end, find_paren_end, split_sql_file,
    DIALECT_PATTERNS,
)
from dependency_analyzer import DependencyAnalyzer


# ============================================================
# common.py 测试
# ============================================================

class TestCleanObjectName(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(clean_object_name('my_proc'), 'my_proc')

    def test_quoted(self):
        self.assertEqual(clean_object_name('"MY_PROC"'), 'MY_PROC')
        self.assertEqual(clean_object_name('`my_proc`'), 'my_proc')
        self.assertEqual(clean_object_name('[my_proc]'), 'my_proc')

    def test_schema_name(self):
        self.assertEqual(clean_object_name('schema.my_proc'), 'my_proc')
        self.assertEqual(clean_object_name('"SCHEMA"."MY_PROC"'), 'MY_PROC')


class TestStripSqlComments(unittest.TestCase):
    def test_single_line(self):
        sql = "SELECT a -- comment\nFROM t"
        self.assertEqual(strip_sql_comments(sql), "SELECT a \nFROM t")

    def test_multi_line(self):
        sql = "SELECT a /* block */ FROM t"
        self.assertEqual(strip_sql_comments(sql), "SELECT a  FROM t")

    def test_string_not_stripped(self):
        sql = "SELECT 'not -- a comment' FROM t"
        self.assertEqual(strip_sql_comments(sql), sql)


class TestFindMatchingEnd(unittest.TestCase):
    def test_simple_begin_end(self):
        sql = "BEGIN INSERT INTO t VALUES(1); END;"
        end = find_matching_end(sql, 0, len(sql))
        self.assertEqual(end, len(sql))

    def test_nested_begin_end(self):
        sql = "BEGIN BEGIN INSERT INTO t VALUES(1); END; END;"
        end = find_matching_end(sql, 0, len(sql))
        self.assertEqual(end, len(sql))

    def test_triple_nested(self):
        sql = "BEGIN BEGIN BEGIN x:=1; END; END; END;"
        end = find_matching_end(sql, 0, len(sql))
        self.assertEqual(end, len(sql))

    def test_end_if(self):
        sql = "BEGIN IF x > 0 THEN y := 1; END IF; END;"
        end = find_matching_end(sql, 0, len(sql))
        self.assertEqual(end, len(sql))


class TestIsKeywordAt(unittest.TestCase):
    def test_begin(self):
        self.assertTrue(_is_keyword_at("BEGIN", 0, 5, "BEGIN"))

    def test_not_keyword(self):
        self.assertFalse(_is_keyword_at("BEGINS", 0, 6, "BEGIN"))

    def test_mid_word(self):
        self.assertFalse(_is_keyword_at("XBEGINS", 1, 7, "BEGIN"))


# ============================================================
# split_sql.py 测试
# ============================================================

class TestDetectDialect(unittest.TestCase):
    def test_oracle_slash(self):
        sql = "CREATE PROCEDURE foo IS BEGIN NULL; END;\n/"
        self.assertEqual(detect_dialect(sql), SQLDialect.ORACLE)

    def test_sqlserver_go(self):
        sql = "CREATE PROC foo AS BEGIN SELECT 1 END\nGO"
        self.assertEqual(detect_dialect(sql), SQLDialect.SQLSERVER)

    def test_postgresql_dollar(self):
        sql = "CREATE FUNCTION f() RETURNS void AS $$ BEGIN END; $$ LANGUAGE plpgsql;"
        self.assertEqual(detect_dialect(sql), SQLDialect.POSTGRESQL)

    def test_mysql_backtick(self):
        sql = "CREATE TABLE `users` (id INT) ENGINE=InnoDB;"
        self.assertEqual(detect_dialect(sql), SQLDialect.MYSQL)

    def test_generic(self):
        sql = "CREATE TABLE users (id INT);"
        self.assertEqual(detect_dialect(sql), SQLDialect.GENERIC)


class TestFindObjectEnd(unittest.TestCase):
    def test_procedure_with_nested_begin(self):
        """存储过程内部有嵌套 BEGIN...END，不应提前截断"""
        sql = """CREATE PROCEDURE my_proc
IS
BEGIN
  IF x > 0 THEN
    BEGIN
      INSERT INTO t VALUES(1);
    END;
  END IF;
END;
/
"""
        end = find_object_end(sql, SQLDialect.ORACLE, 'procedure', 0)
        # 应该包含完整的存储过程，直到 / 结束
        self.assertIn('END;', sql[:end])

    def test_procedure_with_inner_create(self):
        """存储过程体内含 CREATE 语句，不应在内部 CREATE 处截断"""
        sql = """CREATE PROCEDURE my_proc
IS
  v_sql VARCHAR2(200);
BEGIN
  v_sql := 'CREATE TABLE temp_x (id INT)';
  EXECUTE IMMEDIATE v_sql;
  INSERT INTO log VALUES('done');
END;
/
"""
        end = find_object_end(sql, SQLDialect.ORACLE, 'procedure', 0)
        self.assertIn('EXECUTE IMMEDIATE', sql[:end])
        self.assertIn("log VALUES", sql[:end])

    def test_table_paren_matching(self):
        """表定义含嵌套括号"""
        sql = "CREATE TABLE orders (id INT, data VARCHAR(200), PRIMARY KEY (id));\nCREATE TABLE items..."
        end = find_object_end(sql, SQLDialect.GENERIC, 'table', 0)
        self.assertIn('PRIMARY KEY', sql[:end])
        self.assertNotIn('items', sql[:end])

    def test_index_semicolon(self):
        """索引以分号结束"""
        sql = "CREATE INDEX idx_name ON users(name);\nCREATE TABLE next..."
        end = find_object_end(sql, SQLDialect.GENERIC, 'index', 0)
        self.assertTrue(sql[:end].strip().endswith(';'))

    def test_dm_procedure_with_dynamic_sql(self):
        """达梦存储过程含动态SQL中嵌入的分号"""
        sql = '''CREATE PROCEDURE "SP_IMPORT_DATA"
AS
BEGIN
  EXECUTE IMMEDIATE 'INSERT INTO t VALUES(1);';
  EXECUTE IMMEDIATE 'INSERT INTO t VALUES(2);';
  COMMIT;
END;
/'''
        end = find_object_end(sql, SQLDialect.DM, 'procedure', 0)
        self.assertIn('COMMIT', sql[:end])

    def test_sqlserver_procedure(self):
        """SQL Server 存储过程以 GO 结束"""
        sql = "CREATE PROCEDURE my_proc @p INT AS BEGIN SELECT @p END\nGO\nCREATE TABLE..."
        end = find_object_end(sql, SQLDialect.SQLSERVER, 'procedure', 0)
        self.assertIn('SELECT @p', sql[:end])


class TestSplitSQLFile(unittest.TestCase):
    """端到端拆分测试"""

    def _split(self, sql_content, dialect=None, suffix='test'):
        """辅助：写临时文件 → 拆分 → 返回结果"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, f'{suffix}.sql')
            output_dir = os.path.join(tmpdir, f'{suffix}_split')
            with open(input_path, 'w') as f:
                f.write(sql_content)
            result = split_sql_file(input_path, output_dir, dialect, verbose=False)
            # 读取所有生成的文件内容
            files = {}
            for fp in result['created_files']:
                fname = os.path.basename(fp)
                with open(fp, 'r') as f:
                    files[fname] = f.read()
            return result, files

    def test_oracle_procedure_and_function(self):
        sql = """CREATE OR REPLACE PROCEDURE sp_calc
IS
  v_result NUMBER;
BEGIN
  v_result := fn_multiply(3, 4);
  DBMS_OUTPUT.PUT_LINE(v_result);
END;
/

CREATE OR REPLACE FUNCTION fn_multiply
  (a IN NUMBER, b IN NUMBER)
  RETURN NUMBER
IS
BEGIN
  RETURN a * b;
END;
/
"""
        result, files = self._split(sql, SQLDialect.ORACLE)
        self.assertEqual(result['total'], 2)
        self.assertIn('proc_sp_calc.sql', files)
        self.assertIn('func_fn_multiply.sql', files)
        # 确认过程体完整
        self.assertIn('fn_multiply', files['proc_sp_calc.sql'])
        self.assertIn('RETURN a * b', files['func_fn_multiply.sql'])

    def test_dm_procedure_with_semicolons_in_string(self):
        sql = '''CREATE OR REPLACE PROCEDURE "SP_BATCH"
AS
BEGIN
  EXECUTE IMMEDIATE 'DELETE FROM temp_data WHERE id > 100;';
  INSERT INTO log VALUES('batch done');
  COMMIT;
END;
/
'''
        result, files = self._split(sql, SQLDialect.DM)
        self.assertEqual(result['total'], 1)
        self.assertIn('COMMIT', files.get('proc_SP_BATCH.sql', ''))

    def test_mysql_table_and_index(self):
        sql = """CREATE TABLE `users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(100),
  `email` VARCHAR(200)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX `idx_users_email` ON `users`(`email`);
"""
        result, files = self._split(sql, SQLDialect.MYSQL)
        self.assertEqual(result['total'], 2)
        self.assertIn('table_users.sql', files)
        self.assertIn('idx_idx_users_email.sql', files)

    def test_sqlserver_procedure_with_go(self):
        sql = """CREATE PROCEDURE usp_GetUser
  @UserId INT
AS
BEGIN
  SELECT * FROM Users WHERE Id = @UserId;
END
GO

CREATE TABLE Users (
  Id INT PRIMARY KEY,
  Name NVARCHAR(100)
);
GO
"""
        result, files = self._split(sql, SQLDialect.SQLSERVER)
        self.assertGreaterEqual(result['total'], 2)

    def test_postgresql_function_dollar_quote(self):
        sql = """CREATE OR REPLACE FUNCTION calculate_tax(subtotal NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
  RETURN subtotal * 0.1;
END;
$$ LANGUAGE plpgsql;
"""
        result, files = self._split(sql, SQLDialect.POSTGRESQL)
        self.assertEqual(result['total'], 1)
        content = list(files.values())[0]
        self.assertIn('0.1', content)

    def test_multiple_objects_no_boundary_issue(self):
        """过程1 的体不能渗透到过程2"""
        sql = """CREATE PROCEDURE proc_a
IS
BEGIN
  INSERT INTO log VALUES('a');
  UPDATE stats SET count = count + 1;
END;
/

CREATE PROCEDURE proc_b
IS
BEGIN
  DELETE FROM temp;
END;
/
"""
        result, files = self._split(sql, SQLDialect.ORACLE)
        self.assertEqual(result['total'], 2)
        a_content = files.get('proc_proc_a.sql', '')
        b_content = files.get('proc_proc_b.sql', '')
        self.assertIn("log VALUES('a')", a_content)
        self.assertNotIn('DELETE FROM temp', a_content)
        self.assertIn('DELETE FROM temp', b_content)


# ============================================================
# dependency_analyzer.py 测试
# ============================================================

class TestDependencyAnalyzer(unittest.TestCase):
    def test_simple_dependencies(self):
        analyzer = DependencyAnalyzer()
        analyzer.add_object('table', 'users', 'CREATE TABLE users (id INT);')
        analyzer.add_object('view', 'v_users', 'SELECT * FROM users;')
        analyzer.add_object('procedure', 'sp_update', 'UPDATE users SET name = ? WHERE id = ?;')

        analyzer.analyze_all()
        order = analyzer.topological_sort()

        # users 必须在 v_users 和 sp_update 之前
        users_idx = next(i for i, k in enumerate(order) if 'users' in k and 'table' in k)
        vusers_idx = next(i for i, k in enumerate(order) if 'v_users' in k)
        sp_idx = next(i for i, k in enumerate(order) if 'sp_update' in k)

        self.assertLess(users_idx, vusers_idx)
        self.assertLess(users_idx, sp_idx)

    def test_no_self_reference(self):
        analyzer = DependencyAnalyzer()
        analyzer.add_object('function', 'fn_calc', 'SELECT fn_calc(x) FROM dual;')
        analyzer.analyze_all()
        obj = analyzer.objects['function:fn_calc']
        # 自引用不应成为依赖
        self.assertNotIn('function:fn_calc', obj['dependencies'])

    def test_circular_dependency_graceful(self):
        """循环依赖不应报错，而是按类型优先级追加"""
        analyzer = DependencyAnalyzer()
        analyzer.add_object('procedure', 'sp_a', 'CALL sp_b;')
        analyzer.add_object('procedure', 'sp_b', 'CALL sp_a;')
        analyzer.analyze_all()
        order = analyzer.topological_sort()
        self.assertEqual(len(order), 2)

    def test_merge_script_oracle(self):
        analyzer = DependencyAnalyzer(SQLDialect.ORACLE)
        analyzer.add_object('table', 'users', 'CREATE TABLE users (id INT);')
        analyzer.add_object('procedure', 'sp_test', 'SELECT * FROM users;')
        analyzer.analyze_all()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'merge_all.sql')
            content = analyzer.generate_merge_script(path, tmpdir, SQLDialect.ORACLE)
            self.assertIn('@@', content)
            self.assertIn('SET DEFINE OFF', content)

    def test_merge_script_sqlserver(self):
        analyzer = DependencyAnalyzer(SQLDialect.SQLSERVER)
        analyzer.add_object('table', 'users', 'CREATE TABLE users (id INT);')
        analyzer.analyze_all()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'merge_all.sql')
            content = analyzer.generate_merge_script(path, tmpdir, SQLDialect.SQLSERVER)
            self.assertIn(':r ', content)
            self.assertIn('SET NOCOUNT ON', content)

    def test_merge_script_postgresql(self):
        analyzer = DependencyAnalyzer(SQLDialect.POSTGRESQL)
        analyzer.add_object('table', 'users', 'CREATE TABLE users (id INT);')
        analyzer.analyze_all()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'merge_all.sql')
            content = analyzer.generate_merge_script(path, tmpdir, SQLDialect.POSTGRESQL)
            self.assertIn('\\i ', content)
            self.assertIn('ON_ERROR_STOP', content)

    def test_filter_sql_keywords(self):
        """SQL 关键字不应被识别为依赖"""
        analyzer = DependencyAnalyzer()
        analyzer.add_object('procedure', 'sp_test', 'SELECT COUNT(*) FROM users WHERE name IS NOT NULL;')
        analyzer.add_object('table', 'users', 'CREATE TABLE users (id INT);')
        analyzer.analyze_all()

        obj = analyzer.objects['procedure:sp_test']
        # COUNT, IS, NOT, NULL 不应出现为依赖
        dep_names = [analyzer.objects[d]['name'] for d in obj['dependencies']]
        self.assertNotIn('COUNT', dep_names)
        self.assertNotIn('NULL', dep_names)
        self.assertIn('users', dep_names)


# ============================================================
# 运行
# ============================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
