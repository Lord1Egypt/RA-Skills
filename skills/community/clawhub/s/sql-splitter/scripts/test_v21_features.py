#!/usr/bin/env python3
"""
SQL 拆分工具 v2.1 功能测试
测试：进度条、错误处理、dry-run 模式
"""

import os
import sys
import tempfile
import unittest

# 让 import 能找到 scripts 目录
sys.path.insert(0, os.path.dirname(__file__))

from split_sql_v21 import split_sql_file, SQLDialect
from error_handler import ErrorHandler, SplitError, SplitWarning, ErrorType


class TestV21Features(unittest.TestCase):
    """测试 v2.1 新功能"""
    
    def setUp(self):
        """创建测试用的 SQL 文件"""
        self.test_dir = tempfile.mkdtemp()
        self.test_sql = os.path.join(self.test_dir, 'test.sql')
        
        # 创建测试 SQL 文件
        with open(self.test_sql, 'w', encoding='utf-8') as f:
            f.write("""
-- 测试存储过程
CREATE OR REPLACE PROCEDURE test_proc1
IS
BEGIN
    NULL;
END;
/

-- 测试函数
CREATE OR REPLACE FUNCTION test_func1
RETURN NUMBER
IS
BEGIN
    RETURN 1;
END;
/

-- 测试视图
CREATE OR REPLACE VIEW test_view1 AS
SELECT 1 FROM dual;
""")
    
    def tearDown(self):
        """清理测试文件"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_dry_run_mode(self):
        """测试 dry-run 模式"""
        print("\n=== 测试 dry-run 模式 ===")
        
        # 执行 dry-run
        result = split_sql_file(
            self.test_sql,
            output_dir=os.path.join(self.test_dir, 'output'),
            dialect=SQLDialect.ORACLE,
            verbose=True,
            dry_run=True,
            show_progress=False,
        )
        
        # 验证结果
        self.assertTrue(result.success)
        self.assertTrue(result.dry_run)
        self.assertEqual(result.total, 3)  # 应该找到3个对象
        self.assertEqual(len(result.files_created), 3)  # 应该有3个文件路径
        
        # 验证文件没有被实际创建
        for file_path in result.files_created:
            self.assertFalse(os.path.exists(file_path), 
                           f"dry-run 模式下不应创建文件: {file_path}")
        
        print(f"✓ dry-run 模式测试通过，找到 {result.total} 个对象，未实际创建文件")
    
    def test_error_handling(self):
        """测试错误处理"""
        print("\n=== 测试错误处理 ===")
        
        # 测试不存在的文件
        result = split_sql_file(
            '/nonexistent/file.sql',
            output_dir=os.path.join(self.test_dir, 'output'),
            verbose=True,
            dry_run=True,
            show_progress=False,
        )
        
        # 验证错误处理
        self.assertFalse(result.success)
        self.assertGreater(len(result.errors), 0)
        
        # 验证错误是 SplitError 类型
        for error in result.errors:
            self.assertIsInstance(error, SplitError)
            self.assertIsNotNone(error.message)
            self.assertIsNotNone(error.error_type)
            print(f"✓ 错误处理测试通过: {error.error_type.value} - {error.message}")
    
    def test_progress_bar(self):
        """测试进度条功能"""
        print("\n=== 测试进度条功能 ===")
        
        # 测试启用进度条
        result = split_sql_file(
            self.test_sql,
            output_dir=os.path.join(self.test_dir, 'output'),
            dialect=SQLDialect.ORACLE,
            verbose=True,
            dry_run=True,
            show_progress=True,
        )
        
        self.assertTrue(result.success)
        print(f"✓ 进度条测试通过，找到 {result.total} 个对象")
        
        # 测试禁用进度条
        result2 = split_sql_file(
            self.test_sql,
            output_dir=os.path.join(self.test_dir, 'output2'),
            dialect=SQLDialect.ORACLE,
            verbose=True,
            dry_run=True,
            show_progress=False,
        )
        
        self.assertTrue(result2.success)
        print(f"✓ 禁用进度条测试通过")
    
    def test_statistics(self):
        """测试统计信息"""
        print("\n=== 测试统计信息 ===")
        
        result = split_sql_file(
            self.test_sql,
            output_dir=os.path.join(self.test_dir, 'output'),
            dialect=SQLDialect.ORACLE,
            verbose=True,
            dry_run=True,
            show_progress=False,
        )
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.stats)
        self.assertGreater(len(result.stats), 0)
        
        print(f"✓ 统计信息测试通过:")
        for obj_type, count in result.stats.items():
            print(f"  {obj_type}: {count}")
    
    def test_warnings(self):
        """测试警告信息"""
        print("\n=== 测试警告信息 ===")
        
        # 创建一个可能有问题的 SQL 文件
        test_sql2 = os.path.join(self.test_dir, 'test2.sql')
        with open(test_sql2, 'w', encoding='utf-8') as f:
            f.write("""
-- 简单的存储过程
CREATE OR REPLACE PROCEDURE simple_proc
IS
BEGIN
    NULL;
END;
/
""")
        
        result = split_sql_file(
            test_sql2,
            output_dir=os.path.join(self.test_dir, 'output'),
            dialect=SQLDialect.ORACLE,
            verbose=True,
            dry_run=True,
            show_progress=False,
        )
        
        self.assertTrue(result.success)
        # 警告列表可能为空，这是正常的
        print(f"✓ 警告信息测试通过，警告数量: {len(result.warnings)}")


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("SQL 拆分工具 v2.1 功能测试")
    print("=" * 60)
    
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestV21Features)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出总结
    print("\n" + "=" * 60)
    print(f"测试完成: 运行 {result.testsRun} 个测试")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)