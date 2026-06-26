#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟用户 Skill - 主入口

功能流程：
1. 用户提问 → 检索场景库
2. 生成 10 个虚拟用户类型 → 用户选择
3. 基于选定的用户进行对话

使用方式：
    python main.py "用户的问题"
"""

import sys
import json
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from encrypt import EncryptManager
from vector_search import VectorSearchEngine
from user_generator import VirtualUserGenerator
from conversation import ConversationManager


class VirtualUserSkill:
    """虚拟用户技能主类"""
    
    def __init__(self, data_dir=None):
        """
        初始化技能
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = data_dir or (Path(__file__).parent.parent / "data")
        self.search_engine = VectorSearchEngine(self.data_dir)
        self.user_generator = VirtualUserGenerator()
        self.conversation_manager = ConversationManager()
        self.initialized = False
    
    def initialize(self):
        """初始化技能（加载模型和数据）"""
        print("🚀 初始化虚拟用户技能...")
        
        # 初始化加密管理器（确保密钥存在）
        encrypt_mgr = EncryptManager()
        encrypt_mgr.load_or_create_key()
        
        # 加载向量化模型
        self.search_engine.load_model()
        
        # 加载场景库数据
        self.search_engine.load_scenarios()
        self.search_engine.load_embeddings()
        
        self.initialized = True
        print("✅ 技能初始化完成")
    
    def run(self, user_question: str, auto_select: bool = False):
        """
        运行技能主流程
        
        Args:
            user_question: 用户问题
            auto_select: 是否自动选择前 3 个用户类型（默认 False，需要用户手动选择）
        
        Returns:
            dict: 执行结果
        """
        if not self.initialized:
            self.initialize()
        
        print(f"\n❓ 用户问题：{user_question}\n")
        
        # 阶段 1：检索场景库，生成虚拟用户类型
        print("=" * 60)
        print("阶段 1: 检索场景库，生成虚拟用户类型")
        print("=" * 60)
        
        scenarios = self.search_engine.search(user_question, top_k=20)
        user_types = self.user_generator.generate_user_types(scenarios, top_n=10)
        
        print(self.user_generator.format_user_list())
        
        if auto_select:
            # 自动选择前 3 个
            self.user_generator.select_all(selected=False)
            for i in range(min(3, len(user_types))):
                self.user_generator.toggle_selection(i + 1, selected=True)
            print("\n✅ 已自动选择前 3 个用户类型")
        else:
            # 等待用户选择
            print("\n⏳ 等待用户选择...")
            print("提示：回复'选择 1,3,5'或'反选 2,4'，或'全选'/'取消全选'")
            # 实际使用时这里会等待用户输入
            # 现在先自动选择前 3 个作为演示
            self.user_generator.select_all(selected=False)
            for i in range(min(3, len(user_types))):
                self.user_generator.toggle_selection(i + 1, selected=True)
            print("（演示模式：已自动选择前 3 个）")
        
        # 获取选中的用户
        selected_users = self.user_generator.get_selected_users()
        print(f"\n✅ 已选择 {len(selected_users)} 个用户类型")
        
        # 阶段 3：开始对话
        print("\n" + "=" * 60)
        print("阶段 3: 虚拟用户对话")
        print("=" * 60)
        
        self.conversation_manager.start_session(selected_users)
        
        # 对每个选中的用户进行对话
        for i, user in enumerate(selected_users):
            print(f"\n🗣️  与 {user['type_name']} 对话：")
            
            self.conversation_manager.set_current_user(i)
            
            # 生成回复
            response = self.conversation_manager.generate_user_response(user_question)
            
            print(f"   回复：{response['response']}")
            print(f"   情绪：{response['emotion']}")
        
        # 生成报告
        print("\n" + "=" * 60)
        print("生成对话报告")
        print("=" * 60)
        
        report = self.conversation_manager.export_report()
        
        return {
            'success': True,
            'user_types': selected_users,
            'conversation_summary': self.conversation_manager.get_conversation_summary(),
            'report': report,
            'conversation_history': self.conversation_manager.conversation_history
        }


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python main.py \"用户的问题\"")
        print("示例：python main.py \"用户预订机票时最关心什么？\"")
        sys.exit(1)
    
    user_question = sys.argv[1]
    auto_select = '--auto' in sys.argv
    
    skill = VirtualUserSkill()
    result = skill.run(user_question, auto_select=auto_select)
    
    if result['success']:
        print("\n✅ 技能执行完成")
    else:
        print("\n❌ 技能执行失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
