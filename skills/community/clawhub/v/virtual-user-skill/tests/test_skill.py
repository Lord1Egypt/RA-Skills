#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟用户 Skill 单元测试
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from encrypt import EncryptManager
from user_generator import VirtualUserGenerator
from conversation import ConversationManager


class TestEncryptManager:
    """测试加密管理器"""
    
    def test_key_generation(self):
        """测试密钥生成"""
        manager = EncryptManager()
        key = manager.generate_key()
        
        assert key is not None
        assert len(key) == 44  # Fernet 密钥长度
    
    def test_encrypt_decrypt(self):
        """测试加密解密"""
        manager = EncryptManager()
        manager.load_or_create_key()
        
        # 测试数据
        test_data = b"这是测试数据"
        
        # 加密
        encrypted = manager.encrypt_data(test_data)
        assert encrypted is not None
        
        # 解密
        decrypted = manager.decrypt_data(encrypted)
        assert decrypted == test_data
    
    def test_key_persistence(self):
        """测试密钥持久化"""
        manager = EncryptManager()
        
        # 第一次加载（创建）
        key1 = manager.load_or_create_key()
        
        # 第二次加载（读取）
        key2 = manager.load_or_create_key()
        
        # 密钥应该相同
        assert key1 == key2


class TestUserGenerator:
    """测试用户生成器"""
    
    def test_generate_user_types(self):
        """测试用户类型生成"""
        generator = VirtualUserGenerator()
        
        # 模拟场景数据
        scenarios = [
            {
                '用户姓名和背景信息': '姓名 [测试用户] 所属八大人群 [新锐白领]',
                '用户具体场景': '行程规划',
                '任务': '确定预订时间',
                '痛点': '时间紧张',
                '爽点': '流程简单',
                '底层需求': '高效便捷'
            }
        ]
        
        # 生成用户类型
        user_types = generator.generate_user_types(scenarios, top_n=3)
        
        assert len(user_types) == 3
        assert all('type_name' in ut for ut in user_types)
        assert all('profile' in ut for ut in user_types)
    
    def test_toggle_selection(self):
        """测试选择切换"""
        generator = VirtualUserGenerator()
        
        scenarios = [{'用户姓名和背景信息': '测试'}]
        user_types = generator.generate_user_types(scenarios, top_n=3)
        
        # 默认全选
        assert all(ut['selected'] for ut in user_types)
        
        # 取消选择类型 1
        generator.toggle_selection(1, False)
        assert user_types[0]['selected'] == False
        assert user_types[1]['selected'] == True
    
    def test_get_selected_users(self):
        """测试获取已选用户"""
        generator = VirtualUserGenerator()
        
        scenarios = [{'用户姓名和背景信息': '测试'}]
        user_types = generator.generate_user_types(scenarios, top_n=3)
        
        # 只选择类型 1 和 3
        generator.select_all(selected=False)
        generator.toggle_selection(1, True)
        generator.toggle_selection(3, True)
        
        selected = generator.get_selected_users()
        assert len(selected) == 2


class TestConversationManager:
    """测试对话管理器"""
    
    def test_start_session(self):
        """测试开始会话"""
        manager = ConversationManager()
        
        users = [
            {
                'type_name': '测试用户 1',
                'profile': {'场景': '测试场景'}
            }
        ]
        
        manager.start_session(users, session_id='test_001')
        
        assert manager.session_id == 'test_001'
        assert len(manager.selected_users) == 1
    
    def test_generate_response(self):
        """测试生成回复"""
        manager = ConversationManager()
        
        users = [
            {
                'type_name': '测试用户',
                'profile': {
                    '场景': '行程规划',
                    '痛点': '时间紧张',
                    '底层需求': '高效便捷'
                }
            }
        ]
        
        manager.start_session(users)
        manager.set_current_user(0)
        
        response = manager.generate_user_response("你觉得这个产品怎么样？")
        
        assert response['success'] != False
        assert 'response' in response
        assert 'emotion' in response
    
    def test_export_report(self):
        """测试导出报告"""
        manager = ConversationManager()
        
        users = [{'type_name': '测试用户', 'profile': {}}]
        manager.start_session(users)
        manager.set_current_user(0)
        manager.generate_user_response("测试问题")
        
        report = manager.export_report()
        
        assert '# 虚拟用户对话报告' in report
        assert '测试用户' in report


def run_tests():
    """运行所有测试"""
    pytest.main([__file__, '-v'])


if __name__ == "__main__":
    run_tests()
