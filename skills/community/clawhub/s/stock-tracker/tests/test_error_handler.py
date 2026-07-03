"""测试错误处理模块"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from error_handler import (
    StockTrackerError,
    DatabaseError,
    APIError,
    ConfigError,
    CookieError,
    handle_error,
    safe_execute,
)


class TestExceptionClasses:
    """测试异常类"""

    def test_stock_tracker_error_basic(self):
        """测试基础异常类"""
        error = StockTrackerError("test message")
        assert str(error) == "test message"
        assert error.code is None

    def test_stock_tracker_error_with_code(self):
        """测试带错误码的异常类"""
        error = StockTrackerError("test message", code="E001")
        assert str(error) == "test message"
        assert error.code == "E001"

    def test_database_error_inheritance(self):
        """测试数据库异常继承"""
        error = DatabaseError("db error")
        assert isinstance(error, StockTrackerError)
        assert isinstance(error, Exception)

    def test_api_error_inheritance(self):
        """测试API异常继承"""
        error = APIError("api error")
        assert isinstance(error, StockTrackerError)
        assert isinstance(error, Exception)

    def test_config_error_inheritance(self):
        """测试配置异常继承"""
        error = ConfigError("config error")
        assert isinstance(error, StockTrackerError)
        assert isinstance(error, Exception)

    def test_cookie_error_inheritance(self):
        """测试Cookie异常继承"""
        error = CookieError("cookie error")
        assert isinstance(error, StockTrackerError)
        assert isinstance(error, Exception)


class TestHandleError:
    """测试handle_error函数"""

    @patch("error_handler.logger")
    def test_handle_stock_tracker_error(self, mock_logger):
        """测试处理StockTrackerError"""
        error = StockTrackerError("test error", code="E001")
        handle_error(error, context="test_context")
        
        mock_logger.error.assert_called_once_with("test_context: test error (code: E001)")

    @patch("error_handler.logger")
    def test_handle_generic_exception(self, mock_logger):
        """测试处理普通异常"""
        error = ValueError("generic error")
        handle_error(error, context="test_context")
        
        mock_logger.error.assert_called_once_with("test_context: generic error")

    @patch("error_handler.sys.exit")
    @patch("error_handler.logger")
    def test_handle_error_with_exit(self, mock_logger, mock_exit):
        """测试错误处理并退出"""
        error = APIError("api error")
        handle_error(error, context="test_context", exit_on_error=True)
        
        mock_logger.error.assert_called_once()
        mock_exit.assert_called_once_with(1)


class TestSafeExecute:
    """测试safe_execute函数"""

    def test_safe_execute_success(self):
        """测试成功执行函数"""
        def add(a, b):
            return a + b
        
        result = safe_execute(add, 1, 2)
        assert result == 3

    def test_safe_execute_failure(self):
        """测试执行函数失败"""
        def failing_func():
            raise ValueError("test error")
        
        with patch("error_handler.logger"):
            result = safe_execute(failing_func)
            assert result is None

    def test_safe_execute_with_kwargs(self):
        """测试带关键字参数执行函数"""
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"
        
        result = safe_execute(greet, "World", greeting="Hi")
        assert result == "Hi, World!"

    @patch("error_handler.sys.exit")
    def test_safe_execute_exit_on_error(self, mock_exit):
        """测试执行函数失败时退出"""
        def failing_func():
            raise RuntimeError("critical error")
        
        with patch("error_handler.logger"):
            result = safe_execute(failing_func, exit_on_error=True)
            assert result is None
            mock_exit.assert_called_once_with(1)


class TestIntegration:
    """集成测试"""

    def test_exception_hierarchy(self):
        """测试异常层次结构"""
        # 测试所有异常都是Exception的子类
        assert issubclass(StockTrackerError, Exception)
        assert issubclass(DatabaseError, StockTrackerError)
        assert issubclass(APIError, StockTrackerError)
        assert issubclass(ConfigError, StockTrackerError)
        assert issubclass(CookieError, StockTrackerError)

    def test_error_code_preservation(self):
        """测试错误码保留"""
        errors = [
            StockTrackerError("msg", code="E001"),
            DatabaseError("msg", code="DB001"),
            APIError("msg", code="API001"),
            ConfigError("msg", code="CFG001"),
            CookieError("msg", code="CK001"),
        ]
        
        for error in errors:
            assert error.code is not None
            assert len(error.code) > 0
