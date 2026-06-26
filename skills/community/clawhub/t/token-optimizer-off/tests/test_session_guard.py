#!/usr/bin/env python3
"""测试 session_guard 模块"""
import unittest
import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from session_guard import detect_task_type, check, load_state, reset_state


class TestSessionGuard(unittest.TestCase):
    """session_guard 测试类"""
    
    def setUp(self):
        """每个测试前重置状态"""
        reset_state()
    
    def test_detect_task_type_stock(self):
        """测试股票任务识别"""
        self.assertEqual(detect_task_type('今天股票行情怎么样'), 'STOCK')
        self.assertEqual(detect_task_type('我想买入股票'), 'STOCK')
        self.assertEqual(detect_task_type('止损怎么设置'), 'STOCK')
    
    def test_detect_task_type_deploy(self):
        """测试部署任务识别"""
        self.assertEqual(detect_task_type('部署一个服务'), 'DEPLOY')
        self.assertEqual(detect_task_type('安装依赖报错'), 'DEPLOY')
        self.assertEqual(detect_task_type('systemd服务启动失败'), 'DEPLOY')
    
    def test_detect_task_type_query(self):
        """测试查询任务识别"""
        self.assertEqual(detect_task_type('今天天气怎么样'), 'QUERY')
        self.assertEqual(detect_task_type('搜索一下'), 'QUERY')
        self.assertEqual(detect_task_type('现在几点'), 'QUERY')
    
    def test_detect_task_type_code(self):
        """测试代码任务识别"""
        self.assertEqual(detect_task_type('帮我写个函数'), 'CODE')
        self.assertEqual(detect_task_type('这个bug怎么修'), 'CODE')
        self.assertEqual(detect_task_type('实现一个类'), 'CODE')
    
    def test_detect_task_type_default(self):
        """测试默认任务类型"""
        result = detect_task_type('你好啊')
        self.assertEqual(result, 'QUERY')  # 无关键词时返回得分最高的
    
    def test_check_normal(self):
        """测试正常会话"""
        result = check(task_type='STOCK', rounds=5, context_size=30000)
        self.assertEqual(result['action'], 'continue')
        self.assertEqual(result['task_type'], 'STOCK')
    
    def test_check_compress(self):
        """测试需要压缩的情况"""
        result = check(task_type='STOCK', rounds=10, context_size=50000)
        self.assertEqual(result['action'], 'compress')
    
    def test_check_new_session_rounds(self):
        """测试轮数超限需要新开会话"""
        result = check(task_type='STOCK', rounds=30, context_size=40000)
        self.assertEqual(result['action'], 'new_session')
        # 检查 reason 包含轮数或阈值相关信息
        self.assertTrue('轮数' in result['reason'] or '阈值' in result['reason'])
    
    def test_check_new_session_tokens(self):
        """测试 token 超限需要新开会话"""
        result = check(task_type='STOCK', rounds=10, context_size=80000)
        self.assertEqual(result['action'], 'new_session')
        self.assertIn('tokens', result['reason'])
    
    def test_task_switch_detection(self):
        """测试任务切换检测"""
        # 先执行一个 STOCK 任务
        check(task_type='STOCK', rounds=1, context_size=10000, message='股票行情')
        # 切换到 DEPLOY 任务
        result = check(task_type='DEPLOY', rounds=2, context_size=10000, message='部署服务')
        
        # 应该检测到任务切换
        self.assertEqual(result['task_switches'], 1)
    
    def test_load_state(self):
        """测试状态加载"""
        state = load_state()
        self.assertIn('session_start', state)
        self.assertIn('rounds', state)
        self.assertIn('task_history', state)
        self.assertEqual(state['rounds'], 0)
    
    def test_reset_state(self):
        """测试状态重置"""
        # 先设置一些状态
        check(task_type='STOCK', rounds=10, context_size=50000)
        
        # 重置
        state = reset_state()
        
        # 验证状态已重置
        self.assertEqual(state['rounds'], 0)
        self.assertEqual(state['task_switches'], 0)


class TestSessionGuardIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """每个测试前重置状态"""
        reset_state()
    
    def test_full_session_lifecycle(self):
        """测试完整会话生命周期"""
        # 1. 开始新会话
        result = check(task_type='STOCK', rounds=1, context_size=5000, message='股票行情')
        self.assertEqual(result['action'], 'continue')
        
        # 2. 多轮对话
        for i in range(5):
            result = check(task_type='STOCK', context_size=10000)
            self.assertEqual(result['action'], 'continue')
        
        # 3. 检查状态
        state = load_state()
        self.assertEqual(state['rounds'], 6)
    
    def test_auto_task_detection(self):
        """测试自动任务识别"""
        result = check(message='我想查看今天的股票持仓')
        self.assertEqual(result['task_type'], 'STOCK')


if __name__ == '__main__':
    unittest.main()