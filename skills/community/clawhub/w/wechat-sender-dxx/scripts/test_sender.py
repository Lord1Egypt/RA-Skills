#!/usr/bin/env python3
"""
微信发送器测试
"""

import sys
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))


class TestRateLimit:
    """测试频率限制"""
    
    def test_rate_limit_config(self):
        """测试频率限制配置"""
        from send_message import RATE_LIMIT
        assert RATE_LIMIT["max_per_minute"] == 20
        assert RATE_LIMIT["cooldown_seconds"] == 3
    
    def test_rate_limit_check(self):
        """测试频率限制检查"""
        import send_message
        send_message._last_send_time = 0  # 重置
        
        # 首次调用应该直接通过
        with patch('time.sleep') as mock_sleep:
            send_message.check_rate_limit()
            assert not mock_sleep.called


class TestSendMessage:
    """测试发送消息功能"""
    
    @patch('send_message.urllib.request.urlopen')
    def test_send_text_message_success(self, mock_urlopen):
        """测试发送文字消息成功"""
        # 模拟成功响应
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "success": True,
            "messageId": "msg-12345",
            "timestamp": 1701234567890
        }).encode()
        mock_urlopen.return_value.__enter__ = Mock(return_value=mock_response)
        mock_urlopen.return_value.__exit__ = Mock(return_value=False)
        
        from send_message import send_message
        result = send_message("测试用户", "你好")
        
        assert result["success"] == True
        assert "messageId" in result
    
    @patch('send_message.urllib.request.urlopen')
    def test_send_text_message_failure(self, mock_urlopen):
        """测试发送消息失败"""
        import urllib.error
        
        # 模拟 HTTP 错误
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "success": False,
            "code": "E001",
            "message": "未登录微信"
        }).encode()
        
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=StringIO('{"success": false, "code": "E001"}')
        )
        
        from send_message import send_message
        result = send_message("测试用户", "你好")
        
        assert result["success"] == False
        assert "error_code" in result
    
    def test_send_image_file_not_exists(self):
        """测试图片文件不存在"""
        from send_message import send_message
        result = send_message("测试用户", "/nonexistent/path/image.jpg", "image")
        
        assert result["success"] == False
        assert result["error_code"] == "E005"
    
    def test_send_message_build_payload(self):
        """测试构建请求payload"""
        from send_message import send_message
        import send_message as sm
        
        # 检查payload构建
        with patch('send_message.check_rate_limit'):
            with patch('send_message.urllib.request.urlopen') as mock_urlopen:
                mock_response = MagicMock()
                mock_response.read.return_value = json.dumps({"success": True}).encode()
                mock_urlopen.return_value.__enter__ = Mock(return_value=mock_response)
                mock_urlopen.return_value.__exit__ = Mock(return_value=False)
                
                sm._last_send_time = 0  # 重置
                send_message("测试用户", "你好", "text")
                
                # 检查调用参数
                call_args = mock_urlopen.call_args
                assert call_args is not None


class TestMain:
    """测试主程序"""
    
    def test_main_help(self):
        """测试帮助信息"""
        import send_message
        with patch('sys.argv', ['send_message.py', '--help']):
            try:
                send_message.main()
            except SystemExit:
                pass  # --help 会触发 sys.exit(0)
    
    def test_main_missing_to(self):
        """测试缺少收件人参数"""
        import send_message
        with patch('sys.argv', ['send_message.py', '--text', '你好']):
            try:
                send_message.main()
            except SystemExit:
                pass  # required 参数会触发退出
    
    def test_main_missing_content(self):
        """测试缺少消息内容"""
        import send_message
        with patch('sys.argv', ['send_message.py', '--to', '测试']):
            try:
                send_message.main()
            except SystemExit:
                pass  # 会打印错误并退出
    
    def test_main_dry_run(self):
        """测试模拟发送"""
        import send_message
        with patch('sys.argv', ['send_message.py', '--to', '测试', '--text', '你好', '--dry-run']):
            with patch('builtins.print') as mock_print:
                send_message.main()
                # 检查是否输出了模拟发送的信息
                assert any("模拟发送" in str(c) for c in mock_print.call_args_list)


class TestIntegration:
    """集成测试"""
    
    def test_import_module(self):
        """测试模块导入"""
        import send_message
        assert hasattr(send_message, 'send_message')
        assert hasattr(send_message, 'check_rate_limit')
        assert hasattr(send_message, 'API_ENDPOINT')
    
    def test_gateway_config(self):
        """测试Gateway配置"""
        from send_message import GATEWAY_HOST, GATEWAY_PORT, API_ENDPOINT
        assert GATEWAY_HOST == "127.0.0.1"
        assert GATEWAY_PORT == 18789
        assert "127.0.0.1:18789" in API_ENDPOINT


def run_tests():
    """运行所有测试"""
    print("🧪 运行 WeChat Sender 测试...\n")
    
    test_classes = [
        TestRateLimit,
        TestSendMessage,
        TestMain,
        TestIntegration,
    ]
    
    total = 0
    passed = 0
    failed = []
    
    for test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total += 1
                try:
                    getattr(instance, method_name)()
                    passed += 1
                    print(f"  ✅ {method_name}")
                except Exception as e:
                    failed.append((method_name, str(e)))
                    print(f"  ❌ {method_name}: {e}")
    
    print(f"\n📊 测试结果: {passed} 通过, {len(failed)} 失败, 共 {total} 个")
    
    if failed:
        print("\n❌ 失败详情:")
        for name, err in failed:
            print(f"  - {name}: {err}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(run_tests())