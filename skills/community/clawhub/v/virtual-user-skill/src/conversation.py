#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话管理模块 - 虚拟用户对话引擎

功能：
1. 基于选定的虚拟用户类型进行多轮对话
2. 支持产品方案测评
3. 生成对话报告
"""

import json
from typing import List, Dict
from datetime import datetime


class ConversationManager:
    """对话管理器"""
    
    def __init__(self):
        self.selected_users = []
        self.conversation_history = []
        self.current_user = None
        self.session_id = None
    
    def start_session(self, selected_users: List[Dict], session_id: str = None):
        """
        开始对话会话
        
        Args:
            selected_users: 已选中的虚拟用户列表
            session_id: 会话 ID
        """
        self.selected_users = selected_users
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.conversation_history = []
        
        print(f"🎭 开始虚拟用户对话会话：{self.session_id}")
        print(f"👥 参与用户：{len(selected_users)} 个类型")
    
    def set_current_user(self, user_index: int):
        """
        设置当前对话的虚拟用户
        
        Args:
            user_index: 用户索引（从 0 开始）
        """
        if 0 <= user_index < len(self.selected_users):
            self.current_user = self.selected_users[user_index]
            print(f"🗣️  当前对话用户：{self.current_user.get('type_name', '未知')}")
        else:
            print(f"❌ 无效的用户索引：{user_index}")
    
    def generate_user_response(self, user_question: str, product_info: str = None) -> Dict:
        """
        生成虚拟用户的回复
        
        Args:
            user_question: 用户（研究者）的问题
            product_info: 产品信息（可选）
        
        Returns:
            dict: 虚拟用户的回复
        """
        if not self.current_user:
            return {
                'success': False,
                'message': '请先设置当前对话的虚拟用户'
            }
        
        profile = self.current_user.get('profile', {})
        
        # 构建虚拟用户的回复
        response = {
            'user_type': self.current_user.get('type_name'),
            'user_profile': profile,
            'question': user_question,
            'response': self._simulate_response(user_question, profile, product_info),
            'emotion': self._infer_emotion(user_question, profile),
            'timestamp': datetime.now().isoformat()
        }
        
        # 记录对话历史
        self.conversation_history.append(response)
        
        return response
    
    def _simulate_response(self, question: str, profile: Dict, product_info: str = None) -> str:
        """
        模拟虚拟用户的回复
        
        根据用户画像和场景，生成符合该用户特征的回复
        """
        # 提取用户特征
        pain_point = profile.get('痛点', '')
        scenario = profile.get('场景', '')
        demand = profile.get('底层需求', '')
        user_type = profile.get('人群类型', '')
        
        # 将场景转换为第一人称
        scenario = scenario.replace('用户', '我')
        
        # 构建更自然的回复
        response_parts = []
        
        # 1. 开场白 - 表明身份
        if user_type and user_type.strip():
            response_parts.append(f"作为{user_type}，")
        else:
            response_parts.append("在我的旅行经历中，")
        
        # 2. 结合场景
        if scenario:
            response_parts.append(f"{scenario}。")
        
        # 3. 表达痛点
        if pain_point:
            response_parts.append(f"这让我感到{pain_point}。")
        
        # 4. 表达需求
        if demand:
            response_parts.append(f"所以我真正需要的是{demand}。")
        
        # 5. 针对问题的回答
        response_parts.append(f"对于这个问题，我会从我的实际体验出发来判断。")
        
        return "".join(response_parts)
    
    def _generate_price_response(self, profile: Dict, question: str) -> str:
        """生成价格相关的回复"""
        consumption = profile.get('消费力', '中等')
        pain_point = profile.get('痛点', '')
        
        if '高' in consumption or '白领' in profile.get('人群类型', ''):
            return f"价格对我来说不是首要考虑因素，我更关注{pain_point if pain_point else '体验和服务质量'}。只要能解决我的问题，合理的溢价是可以接受的。"
        else:
            return f"我会比较在意性价比，{pain_point if pain_point else '希望能有明确的价格说明和透明的收费'}。如果有优惠活动会更有吸引力。"
    
    def _generate_experience_response(self, profile: Dict, question: str) -> str:
        """生成体验相关的回复"""
        scenario = profile.get('场景', '')
        pain_point = profile.get('痛点', '')
        demand = profile.get('底层需求', '')
        
        return f"在我的{scenario}场景下，我最在意的是{demand if demand else '流程是否顺畅'}。{pain_point if pain_point else '目前整体体验还可以'}。"
    
    def _generate_suggestion_response(self, profile: Dict, question: str) -> str:
        """生成建议相关的回复"""
        pain_point = profile.get('痛点', '')
        demand = profile.get('底层需求', '')
        
        suggestions = []
        if pain_point:
            suggestions.append(f"希望能解决'{pain_point}'这个问题")
        if demand:
            suggestions.append(f"满足'{demand}'这个需求")
        
        if suggestions:
            return "我的建议是：" + "；".join(suggestions) + "。"
        else:
            return "目前没有想到特别的改进建议，整体使用下来还不错。"
    
    def _generate_general_response(self, profile: Dict, question: str) -> str:
        """生成通用回复"""
        scenario = profile.get('场景', '')
        profile_type = profile.get('人群类型', '普通用户')
        
        return f"作为一个{profile_type}，在{scenario}场景下，我会根据自己的实际需求来做判断。具体来说，我会关注产品是否能真正解决我的问题。"
    
    def _infer_emotion(self, question: str, profile: Dict) -> str:
        """推断虚拟用户的情绪"""
        pain_point = profile.get('痛点', '')
        
        if '不满' in pain_point or '痛点' in pain_point or '问题' in pain_point:
            return "略带焦虑，希望问题得到解决"
        elif '满意' in profile.get('爽点', ''):
            return "满意，愿意继续使用"
        else:
            return "平静，理性评估"
    
    def get_conversation_summary(self) -> Dict:
        """获取对话摘要"""
        return {
            'session_id': self.session_id,
            'total_users': len(self.selected_users),
            'conversation_count': len(self.conversation_history),
            'history': self.conversation_history
        }
    
    def export_report(self, output_file: str = None) -> str:
        """
        导出对话报告
        
        Args:
            output_file: 输出文件路径
        
        Returns:
            str: 报告内容
        """
        if not self.conversation_history:
            return "暂无对话记录"
        
        report_lines = [
            "# 虚拟用户对话报告",
            f"\n**会话 ID**: {self.session_id}",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**参与用户类型**: {len(self.selected_users)} 个",
            f"**对话轮数**: {len(self.conversation_history)} 轮",
            "\n---\n"
        ]
        
        # 用户类型概览
        report_lines.append("## 参与用户类型\n")
        for i, user in enumerate(self.selected_users, 1):
            profile = user.get('profile', {})
            report_lines.append(f"### {i}. {user.get('type_name', '未知')}")
            report_lines.append(f"- 场景：{profile.get('场景', 'N/A')}")
            report_lines.append(f"- 痛点：{profile.get('痛点', 'N/A')}")
            report_lines.append(f"- 底层需求：{profile.get('底层需求', 'N/A')}")
            report_lines.append("")
        
        # 对话记录
        report_lines.append("\n## 对话记录\n")
        for i, conv in enumerate(self.conversation_history, 1):
            report_lines.append(f"### 第{i}轮对话")
            report_lines.append(f"**用户类型**: {conv['user_type']}")
            report_lines.append(f"**问题**: {conv['question']}")
            report_lines.append(f"**回复**: {conv['response']}")
            report_lines.append(f"**情绪**: {conv['emotion']}")
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"📄 报告已保存：{output_file}")
        
        return report_content


# 测试代码
if __name__ == "__main__":
    # 模拟测试
    manager = ConversationManager()
    
    test_users = [
        {
            'type_name': '类型 1: 新锐白领',
            'profile': {
                '场景': '行程规划',
                '痛点': '时间紧张',
                '底层需求': '高效便捷'
            }
        }
    ]
    
    manager.start_session(test_users)
    manager.set_current_user(0)
    
    response = manager.generate_user_response("你觉得这个产品怎么样？")
    print(f"虚拟用户回复：{response['response']}")
