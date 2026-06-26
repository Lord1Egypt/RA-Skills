#!/usr/bin/env python3
"""
达梦数据库转换器单元测试
测试 SQL Server -> 达梦数据库 的语法转换
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dm_converter import (
    DMConverter, ConversionType, ConversionResult,
    convert_sqlserver_to_dm, convert_sqlserver_to_dm_with_result,
    get_converter, get_conversion_summary,
)


class TestDMConverterBasic(unittest.TestCase):
    """基础转换测试"""

    def setUp(self):
        self.converter = DMConverter()

    def test_empty_content(self):
        """空内容不转换"""
        result = convert_sqlserver_to_dm_with_result('', 'generic')
        self.assertEqual(result.converted, '')
        self.assertEqual(result.change_count, 0)

    def test_whitespace_only(self):
        """纯空白不转换"""
        result = convert_sqlserver_to_dm_with_result('   \n  ', 'generic')
        self.assertEqual(result.converted.strip(), '')

    def test_getdate(self):
        """GETDATE() -> CURRENT_TIMESTAMP"""
        result = convert_sqlserver_to_dm_with_result('SELECT GETDATE()', 'generic')
        self.assertIn('CURRENT_TIMESTAMP', result.converted)
        self.assertNotIn('GETDATE', result.converted)

    def test_isnull(self):
        """ISNULL() -> NVL()"""
        result = convert_sqlserver_to_dm_with_result("SELECT ISNULL(name, 'N/A')", 'generic')
        self.assertIn('NVL(', result.converted)
        self.assertNotIn('ISNULL', result.converted)

    def test_string_not_modified(self):
        """字符串内容不被误改"""
        result = convert_sqlserver_to_dm_with_result("SELECT 'GETDATE is cool'", 'generic')
        # 字符串内的GETDATE不应被替换
        self.assertIn('GETDATE is cool', result.converted)

    def test_multiple_conversions(self):
        """多个转换同时执行"""
        sql = "SELECT ISNULL(name, 'N/A'), GETDATE()"
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn('NVL(', result.converted)
        self.assertIn('CURRENT_TIMESTAMP', result.converted)


class TestProcedureConversion(unittest.TestCase):
    """存储过程转换测试"""

    def test_procedure_with_params(self):
        """带参数的存储过程"""
        sql = """CREATE PROCEDURE sp_test(@p1 INT, @p2 VARCHAR(100))
AS
BEGIN
    SELECT @p1
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'procedure')
        self.assertIn('CREATE OR REPLACE PROCEDURE', result.converted)
        self.assertIn('AS', result.converted)
        self.assertNotIn(' IS', result.converted)  # 达梦存储过程用AS而非IS
        self.assertIn('p1 INTEGER', result.converted)
        self.assertIn('p2 VARCHAR(100 CHAR)', result.converted)
        self.assertNotIn('@p1', result.converted)
        self.assertNotIn('@p2', result.converted)

    def test_procedure_without_params(self):
        """无参数的存储过程"""
        sql = """CREATE PROCEDURE sp_simple
AS
BEGIN
    SELECT 1
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'procedure')
        self.assertIn('CREATE OR REPLACE PROCEDURE "sp_simple" AS', result.converted)

    def test_procedure_terminator(self):
        """存储过程添加终止符 /"""
        sql = """CREATE PROCEDURE sp_test(@p1 INT)
AS
BEGIN
    RETURN @p1
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'procedure')
        self.assertTrue(result.converted.strip().endswith('/'))

    def test_procedure_variables(self):
        """变量声明和赋值"""
        sql = """CREATE PROCEDURE sp_vars(@p1 INT)
AS
BEGIN
    DECLARE @v_count INT
    SET @v_count = 0
    SELECT @v_count = COUNT(*) FROM users
    RETURN @v_count
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'procedure')
        self.assertNotIn('DECLARE', result.converted)
        self.assertIn(':=', result.converted)
        self.assertNotIn('@v_count', result.converted)
        self.assertNotIn('@p1', result.converted)


class TestFunctionConversion(unittest.TestCase):
    """函数转换测试"""

    def test_scalar_function(self):
        """标量函数"""
        sql = """CREATE FUNCTION fn_test(@val INT)
RETURNS VARCHAR(50)
AS
BEGIN
    RETURN 'ok'
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'function')
        self.assertIn('CREATE OR REPLACE FUNCTION', result.converted)
        self.assertIn('RETURN VARCHAR(50 CHAR)', result.converted)
        self.assertIn('IS', result.converted)


class TestViewConversion(unittest.TestCase):
    """视图转换测试"""

    def test_view_with_functions(self):
        """带函数的视图"""
        sql = """CREATE VIEW v_users AS
SELECT id, ISNULL(name, 'N/A') AS display_name
FROM users
WHERE created > GETDATE() - 30"""
        result = convert_sqlserver_to_dm_with_result(sql, 'view')
        self.assertIn('CREATE OR REPLACE VIEW', result.converted)
        self.assertIn('NVL(', result.converted)
        self.assertIn('CURRENT_TIMESTAMP', result.converted)
        self.assertIn("'N/A'", result.converted)


class TestTableConversion(unittest.TestCase):
    """表结构转换测试"""

    def test_data_types(self):
        """数据类型映射"""
        sql = """CREATE TABLE users (
    id INT NOT NULL,
    name NVARCHAR(100),
    flag BIT,
    created DATETIME DEFAULT GETDATE()
)"""
        result = convert_sqlserver_to_dm_with_result(sql, 'table')
        self.assertIn('id INTEGER', result.converted)
        self.assertIn('name VARCHAR(100 CHAR)', result.converted)
        self.assertIn('flag BOOLEAN', result.converted)
        self.assertIn('created TIMESTAMP', result.converted)
        self.assertIn('CURRENT_TIMESTAMP', result.converted)

    def test_identity(self):
        """IDENTITY保留"""
        sql = "CREATE TABLE t (id INT IDENTITY(1,1) NOT NULL)"
        result = convert_sqlserver_to_dm_with_result(sql, 'table')
        self.assertIn('IDENTITY("id", 1, 1)', result.converted)
        self.assertIn('INTEGER', result.converted)

    def test_insert_into_not_modified(self):
        """INSERT INTO不被误匹配为数据类型"""
        sql = """CREATE TABLE t (id INT)
INSERT INTO t VALUES(1)"""
        result = convert_sqlserver_to_dm_with_result(sql, 'table')
        self.assertIn('INSERT INTO', result.converted)
        self.assertNotIn('INTEGERO', result.converted)


class TestTriggerConversion(unittest.TestCase):
    """触发器转换测试"""

    def test_after_trigger(self):
        """AFTER触发器"""
        sql = """CREATE TRIGGER tr_users ON users AFTER INSERT, UPDATE
AS
BEGIN
    INSERT INTO log_table(action) VALUES('changed')
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'trigger')
        self.assertIn('CREATE OR REPLACE TRIGGER', result.converted)
        self.assertIn('AFTER INSERT', result.converted)
        self.assertIn('INSERT INTO', result.converted)
        self.assertNotIn('INTEGERO', result.converted)


class TestTryCatchConversion(unittest.TestCase):
    """TRY-CATCH转换测试"""

    def test_try_catch(self):
        """TRY-CATCH -> EXCEPTION"""
        sql = """BEGIN TRY
    INSERT INTO t VALUES(1)
END TRY
BEGIN CATCH
    PRINT 'error'
END CATCH"""
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn('EXCEPTION WHEN OTHERS THEN', result.converted)
        self.assertNotIn('BEGIN TRY', result.converted)
        self.assertNotIn('END TRY', result.converted)


class TestTransactionConversion(unittest.TestCase):
    """事务语句转换测试"""

    def test_commit_transaction(self):
        """COMMIT TRANSACTION -> COMMIT"""
        result = convert_sqlserver_to_dm_with_result('COMMIT TRANSACTION', 'generic')
        self.assertIn('COMMIT', result.converted)

    def test_rollback_transaction(self):
        """ROLLBACK TRANSACTION -> ROLLBACK"""
        result = convert_sqlserver_to_dm_with_result('ROLLBACK TRANSACTION', 'generic')
        self.assertIn('ROLLBACK', result.converted)


class TestGlobalVarsConversion(unittest.TestCase):
    """全局变量转换测试"""

    def test_rowcount(self):
        """@@ROWCOUNT -> SQL%ROWCOUNT"""
        result = convert_sqlserver_to_dm_with_result('SELECT @@ROWCOUNT', 'generic')
        self.assertIn('SQL%ROWCOUNT', result.converted)

    def test_error(self):
        """@@ERROR -> SQL%ERROR_CODE"""
        result = convert_sqlserver_to_dm_with_result('IF @@ERROR <> 0', 'generic')
        self.assertIn('SQL%ERROR_CODE', result.converted)


class TestSetStatements(unittest.TestCase):
    """SET语句转换测试"""

    def test_set_nocount_on(self):
        """SET NOCOUNT ON -> 删除(达梦不需要)"""
        result = convert_sqlserver_to_dm_with_result('SET NOCOUNT ON', 'generic')
        self.assertNotIn('SET NOCOUNT', result.converted)


class TestConversionResult(unittest.TestCase):
    """ConversionResult对象测试"""

    def test_no_changes(self):
        """无需转换"""
        result = ConversionResult('abc', 'abc', [])
        self.assertFalse(result.has_changes)
        self.assertEqual(result.change_count, 0)
        self.assertEqual(result.summary(), '无需转换')

    def test_with_changes(self):
        """有转换"""
        changes = [{'type': 'test', 'line': 1, 'old': 'a', 'new': 'b'}]
        result = ConversionResult('a', 'b', changes)
        self.assertTrue(result.has_changes)
        self.assertEqual(result.change_count, 1)

    def test_summary(self):
        """转换摘要"""
        changes = [{'type': 'data_type', 'line': 1, 'old': 'INT', 'new': 'INTEGER', 'desc': '类型映射'}]
        result = ConversionResult('a', 'b', changes)
        summary = result.summary()
        self.assertIn('1 处转换', summary)
        self.assertIn('INT', summary)
        self.assertIn('INTEGER', summary)


class TestConverterAPI(unittest.TestCase):
    """便捷函数API测试"""

    def test_convert_sqlserver_to_dm(self):
        """便捷函数返回字符串"""
        result = convert_sqlserver_to_dm('SELECT GETDATE()', 'generic')
        self.assertIsInstance(result, str)
        self.assertIn('CURRENT_TIMESTAMP', result)

    def test_get_converter_singleton(self):
        """转换器单例"""
        c1 = get_converter()
        c2 = get_converter()
        self.assertIs(c1, c2)

    def test_get_conversion_summary(self):
        """转换摘要"""
        summary = get_conversion_summary()
        self.assertIn('supported_conversions', summary)
        self.assertIn('supported_objects', summary)
        self.assertIn('limitations', summary)


class TestIntegrationWithSplit(unittest.TestCase):
    """与拆分流程集成测试"""

    def test_split_and_convert(self):
        """拆分+转换端到端测试"""
        from split_sql_v21 import split_sql_file, SQLDialect

        # 创建临时SQL文件
        tmpdir = tempfile.mkdtemp()
        try:
            sql_file = os.path.join(tmpdir, 'test.sql')
            with open(sql_file, 'w') as f:
                f.write("""CREATE PROCEDURE sp_demo(@id INT, @name VARCHAR(50))
AS
BEGIN
    DECLARE @cnt INT
    SET @cnt = 0
    SELECT ISNULL(@name, 'unknown')
END
GO

CREATE TABLE demo_table (
    id INT IDENTITY(1,1) NOT NULL,
    name NVARCHAR(100),
    created DATETIME DEFAULT GETDATE()
)

CREATE VIEW v_demo AS
SELECT id, ISNULL(name, 'N/A') FROM demo_table
""")
            output_dir = os.path.join(tmpdir, 'output')
            result = split_sql_file(
                sql_file,
                output_dir,
                dialect=SQLDialect.SQLSERVER,
                verbose=False,
                convert_to='dm',
            )
            self.assertTrue(result.success)

            # 检查原始拆分目录存在
            self.assertTrue(os.path.isdir(output_dir))

            # 检查达梦转换目录存在
            dm_dir = output_dir + '_dm'
            self.assertTrue(os.path.isdir(dm_dir), f"DM dir {dm_dir} should exist")

            # 检查转换后的文件
            dm_files = os.listdir(dm_dir)
            self.assertTrue(len(dm_files) > 0, "DM dir should have files")

            # 检查转换内容
            for fname in dm_files:
                if fname.endswith('.sql') and fname != 'merge_all.sql':
                    fpath = os.path.join(dm_dir, fname)
                    with open(fpath, 'r') as f:
                        content = f.read()
                    # 不应包含SQL Server特有语法
                    self.assertNotIn('GETDATE', content, f"{fname}: GETDATE should be converted")
        finally:
            shutil.rmtree(tmpdir)


class TestComplexProcedureConversion(unittest.TestCase):
    """复杂存储过程转换测试"""

    def test_complex_procedure(self):
        """复杂存储过程: IF+TRY-CATCH+SELECT INTO+多变量"""
        sql = """CREATE PROCEDURE sp_order_stats(@p_date DATETIME, @p_type VARCHAR(20))
AS
BEGIN
    SET NOCOUNT ON
    DECLARE @v_count INT
    DECLARE @v_total DECIMAL(18,2)
    DECLARE @v_name NVARCHAR(100)
    
    SET @v_count = 0
    SELECT @v_count = COUNT(*), @v_total = SUM(amount) FROM orders WHERE create_date > @p_date
    
    IF @v_count > 0
    BEGIN
        SELECT @v_name = name FROM #temp_orders WHERE type = @p_type
        PRINT 'Total: ' + CONVERT(VARCHAR, @v_total)
    END
    
    BEGIN TRY
        INSERT INTO log_table(action, cnt) VALUES('count', @v_count)
    END TRY
    BEGIN CATCH
        PRINT 'Error: ' + CONVERT(VARCHAR, @@ERROR)
    END CATCH
    
    RETURN @v_count
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'procedure')
        # 不应包含SQL Server特有语法
        self.assertNotIn('END IF; THEN', result.converted, "不应出现END IF; THEN重复")
        self.assertNotIn('BEGIN TRY', result.converted)
        self.assertNotIn('END TRY', result.converted)
        self.assertNotIn('BEGIN CATCH', result.converted)
        self.assertNotIn('@v_count', result.converted, "@前缀应去掉")
        self.assertNotIn('@p_date', result.converted)
        # SET NOCOUNT ON被注释为 "-- SET NOCOUNT ON (达梦不需要)"，不算原始语句
        self.assertNotRegex(result.converted, r'^\s*SET\s+NOCOUNT\s+ON\b', "SET NOCOUNT ON应被注释掉")
        self.assertNotIn('CONVERT(', result.converted)
        # 应包含达梦语法
        self.assertIn('CREATE OR REPLACE PROCEDURE', result.converted)
        self.assertIn('EXCEPTION WHEN OTHERS THEN', result.converted)
        self.assertIn('END IF;', result.converted)
        self.assertIn('DBMS_OUTPUT.PUT_LINE', result.converted)
        self.assertIn('CAST(', result.converted)

    def test_select_into_with_from(self):
        """SELECT @var = expr FROM table -> SELECT expr INTO var FROM table"""
        sql = "SELECT @v_count = COUNT(*) FROM users WHERE active = 1"
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn('INTO', result.converted)
        self.assertIn('FROM', result.converted)
        self.assertNotIn('@v_count', result.converted)

    def test_select_multi_assign(self):
        """SELECT多变量赋值"""
        sql = "SELECT @a = col1, @b = col2 FROM users"
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn('INTO', result.converted)
        self.assertIn('col1', result.converted)
        self.assertIn('col2', result.converted)

    def test_select_assign_no_from(self):
        """SELECT @var = expr (无FROM) -> var := expr"""
        sql = "SELECT @v_count = 0"
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn(':=', result.converted)
        self.assertNotIn('INTO', result.converted)

    def test_if_with_try_catch(self):
        """IF和TRY-CATCH共存时不冲突"""
        sql = """IF @x > 0
BEGIN
    SELECT 1
END

BEGIN TRY
    INSERT INTO t VALUES(1)
END TRY
BEGIN CATCH
    SELECT 2
END CATCH"""
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn('END IF;', result.converted)
        self.assertIn('EXCEPTION WHEN OTHERS THEN', result.converted)
        self.assertNotIn('END IF; THEN', result.converted)

    def test_if_else(self):
        """IF...ELSE...转换"""
        sql = """IF @x > 0
BEGIN
    SELECT 1
END
ELSE
BEGIN
    SELECT 2
END"""
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn('IF', result.converted)
        self.assertIn('THEN', result.converted)
        self.assertIn('ELSE', result.converted)
        self.assertIn('END IF;', result.converted)

    def test_while_loop(self):
        """WHILE...BEGIN...END -> WHILE...LOOP...END LOOP"""
        sql = """WHILE @x > 0
BEGIN
    SET @x = @x - 1
END"""
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn('LOOP', result.converted)
        self.assertIn('END LOOP;', result.converted)

    def test_nested_if(self):
        """嵌套IF"""
        sql = """IF @x > 0
BEGIN
    IF @y > 0
    BEGIN
        SELECT 1
    END
END"""
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        # 应有两个END IF
        self.assertEqual(result.converted.count('END IF;'), 2)

    def test_dateadd_conversion(self):
        """DATEADD函数转换"""
        sql = "SELECT DATEADD(day, 7, GETDATE())"
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn('INTERVAL', result.converted)
        self.assertIn('DAY', result.converted)
        self.assertNotIn('DATEADD', result.converted)

    def test_datediff_conversion(self):
        """DATEDIFF函数转换"""
        sql = "SELECT DATEDIFF(day, @start, @end)"
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertNotIn('DATEDIFF', result.converted)

    def test_string_agg_conversion(self):
        """STRING_AGG -> LISTAGG"""
        sql = "SELECT STRING_AGG(name, ',')"
        result = convert_sqlserver_to_dm_with_result(sql, 'generic')
        self.assertIn('LISTAGG', result.converted)
        self.assertNotIn('STRING_AGG', result.converted)


class TestProcedureTypeMapping(unittest.TestCase):
    """存储过程类型映射增强测试: VARCHAR(n CHAR) + CAST中nvarchar映射"""

    def test_procedure_varchar_char_semantic(self):
        """存储过程中DECLARE变量VARCHAR(n)应加CHAR语义"""
        sql = """CREATE PROCEDURE sp_varchar_test(@p1 INT)
AS
BEGIN
    DECLARE @v_sql VARCHAR(4000)
    SET @v_sql = 'test'
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'procedure')
        self.assertIn('v_sql VARCHAR(4000 CHAR)', result.converted)
        self.assertNotIn('v_sql VARCHAR(4000);', result.converted)

    def test_procedure_cast_nvarchar(self):
        """存储过程中CAST(xxx AS nvarchar(50))应映射为VARCHAR(50 CHAR)"""
        sql = """CREATE PROCEDURE sp_cast_test(@TX_DATE INT)
AS
BEGIN
    DECLARE @v_month VARCHAR(6)
    SET @v_month = CAST(@TX_DATE AS nvarchar(6))
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'procedure')
        self.assertIn('VARCHAR(6 CHAR)', result.converted)
        # nvarchar应被映射为VARCHAR
        self.assertNotIn('nvarchar', result.converted)

    def test_procedure_parameter_varchar_char(self):
        """存储过程参数中的VARCHAR(n)也应加CHAR语义"""
        sql = """CREATE PROCEDURE sp_param_test(@name VARCHAR(100), @id INT)
AS
BEGIN
    SELECT @id
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'procedure')
        self.assertIn('name VARCHAR(100 CHAR)', result.converted)

    def test_function_returns_varchar_char(self):
        """函数RETURNS VARCHAR(n)也应加CHAR语义"""
        sql = """CREATE FUNCTION fn_test(@val INT)
RETURNS VARCHAR(50)
AS
BEGIN
    RETURN 'ok'
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'function')
        self.assertIn('VARCHAR(50 CHAR)', result.converted)


class TestTruncateConversion(unittest.TestCase):
    """TRUNCATE TABLE -> DELETE FROM 转换测试"""

    def test_truncate_table_in_procedure(self):
        """存储过程内 TRUNCATE TABLE -> DELETE FROM"""
        sql = """CREATE PROCEDURE sp_clear_data
AS
BEGIN
    TRUNCATE TABLE temp_data
    SELECT * FROM users
END
GO"""
        result = convert_sqlserver_to_dm_with_result(sql, 'procedure')
        self.assertIn('DELETE FROM', result.converted)
        self.assertNotIn('TRUNCATE', result.converted)

    def test_truncate_table_generic(self):
        """通用上下文中 TRUNCATE TABLE -> DELETE FROM"""
        result = convert_sqlserver_to_dm('TRUNCATE TABLE log_table', 'generic')
        self.assertIn('DELETE FROM', result)
        self.assertNotIn('TRUNCATE', result)

    def test_truncate_table_case_insensitive(self):
        """大小写不敏感匹配"""
        result = convert_sqlserver_to_dm('truncate table MyTable', 'generic')
        self.assertIn('DELETE FROM', result)
        self.assertNotIn('TRUNCATE', result)
        self.assertIn('MyTable', result)

    def test_truncate_preserves_table_name(self):
        """TRUNCATE转换保留表名"""
        result = convert_sqlserver_to_dm('TRUNCATE TABLE dbo.transaction_log', 'generic')
        self.assertIn('DELETE FROM', result)
        self.assertIn('dbo.transaction_log', result)


class TestEndingSemicolon(unittest.TestCase):
    """TABLE/VIEW结尾分号测试"""

    def test_table_ending_semicolon(self):
        """表转换后结尾有分号"""
        sql = """CREATE TABLE users (
    id INTEGER,
    name VARCHAR(100)
)"""
        result = convert_sqlserver_to_dm(sql, 'table')
        self.assertTrue(result.rstrip().endswith(';'),
            f"Table should end with semicolon, got: ...{result[-30:]}")

    def test_view_ending_semicolon(self):
        """视图转换后结尾有分号"""
        sql = "CREATE VIEW v_users AS SELECT id, name FROM users"
        result = convert_sqlserver_to_dm(sql, 'view')
        self.assertTrue(result.rstrip().endswith(';'),
            f"View should end with semicolon, got: ...{result[-30:]}")

    def test_index_ending_semicolon(self):
        """索引转换后结尾有分号"""
        sql = "CREATE INDEX idx_name ON users(name)"
        result = convert_sqlserver_to_dm(sql, 'index')
        self.assertTrue(result.rstrip().endswith(';'),
            f"Index should end with semicolon, got: ...{result[-30:]}")

    def test_constraint_ending_semicolon(self):
        """约束转换后结尾有分号"""
        sql = "ALTER TABLE users ADD CONSTRAINT pk_users PRIMARY KEY (id)"
        result = convert_sqlserver_to_dm(sql, 'constraint')
        self.assertTrue(result.rstrip().endswith(';'),
            f"Constraint should end with semicolon, got: ...{result[-30:]}")

    def test_table_already_has_semicolon_no_duplicate(self):
        """表已有分号不重复加"""
        sql = """CREATE TABLE users (
    id INTEGER,
    name VARCHAR(100)
);"""
        result = convert_sqlserver_to_dm(sql, 'table')
        # 结尾应该只有一个分号
        self.assertTrue(result.rstrip().endswith(';'))
        self.assertNotIn(';;', result)


if __name__ == '__main__':
    unittest.main()
