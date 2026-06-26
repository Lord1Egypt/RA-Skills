#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟用户生成模块 - 基于场景库生成虚拟用户类型

功能：
1. 根据搜索结果生成 10 个虚拟用户类型
2. 支持用户选择/反选
3. 生成虚拟用户画像
"""

import json
from typing import List, Dict


class VirtualUserGenerator:
    """虚拟用户生成器"""
    
    def __init__(self):
        self.user_types = []
        self.selected_types = []
    
    def generate_user_types(self, scenarios: List[Dict], top_n=10) -> List[Dict]:
        """
        基于场景生成虚拟用户类型
        
        Args:
            scenarios: 场景库搜索结果
            top_n: 生成的用户类型数量
        
        Returns:
            list: 虚拟用户类型列表
        """
        # 从场景中提取用户特征
        user_profiles = []
        
        for scenario in scenarios:
            profile = self._extract_user_profile(scenario)
            if profile and profile not in user_profiles:
                user_profiles.append(profile)
        
        # 如果场景数量不足，进行组合生成
        while len(user_profiles) < top_n and len(user_profiles) > 0:
            # 随机组合现有特征生成新用户
            base_profile = user_profiles[len(user_profiles) % len(user_profiles)].copy()
            # 微调某些特征
            base_profile['variation_id'] = len(user_profiles) + 1
            user_profiles.append(base_profile)
        
        # 格式化输出
        user_types = []
        for i, profile in enumerate(user_profiles[:top_n], 1):
            user_type = {
                'id': i,
                'type_name': f"类型{i}: {profile.get('人群类型', '普通用户')}",
                'profile': profile,
                'scenario_summary': self._summarize_scenario(profile),
                'selected': True  # 默认全选
            }
            user_types.append(user_type)
        
        self.user_types = user_types
        return user_types
    
    def _extract_user_profile(self, scenario: Dict) -> Dict:
        """从场景中提取用户画像"""
        # 解析用户姓名和背景信息字段
        background = scenario.get('用户姓名和背景信息', '')
        
        profile = {
            '姓名': '',
            '人群类型': '',
            '年龄': '',
            '消费力': '',
            '职业': '',
            '婚姻状况': '',
            '旅行特征': '',
            '场景': scenario.get('用户具体场景', ''),
            '任务': scenario.get('任务', ''),
            '痛点': scenario.get('痛点', ''),
            '爽点': scenario.get('爽点', ''),
            '底层需求': scenario.get('底层需求', '')
        }
        
        # 简单解析背景信息（实际使用时需要根据数据格式优化）
        if '姓名' in background:
            # 示例格式：姓名 [廖慧] 所属八大人群 [新锐白领] 年龄 [28]...
            import re
            name_match = re.search(r'姓名\[([^\]]+)\]', background)
            if name_match:
                profile['姓名'] = name_match.group(1)
            
            crowd_match = re.search(r'所属八大人群\[([^\]]+)\]', background)
            if crowd_match:
                profile['人群类型'] = crowd_match.group(1)
            
            age_match = re.search(r'年龄\[([^\]]+)\]', background)
            if age_match:
                profile['年龄'] = age_match.group(1)
        
        return profile
    
    def _summarize_scenario(self, profile: Dict) -> str:
        """生成场景摘要"""
        summary_parts = []
        
        if profile.get('场景'):
            summary_parts.append(f"场景：{profile['场景']}")
        if profile.get('痛点'):
            summary_parts.append(f"痛点：{profile['痛点'][:50]}...")
        if profile.get('底层需求'):
            summary_parts.append(f"需求：{profile['底层需求'][:50]}...")
        
        return " | ".join(summary_parts) if summary_parts else "暂无场景信息"
    
    def toggle_selection(self, user_type_id: int, selected: bool):
        """
        切换用户类型选择状态
        
        Args:
            user_type_id: 用户类型 ID
            selected: 是否选中
        """
        for user_type in self.user_types:
            if user_type['id'] == user_type_id:
                user_type['selected'] = selected
                break
    
    def get_selected_users(self) -> List[Dict]:
        """获取已选中的用户类型"""
        return [ut for ut in self.user_types if ut['selected']]
    
    def select_all(self, selected=True):
        """全选/取消全选"""
        for user_type in self.user_types:
            user_type['selected'] = selected
    
    def format_user_list(self) -> str:
        """格式化输出用户类型列表"""
        output = []
        output.append("📋 生成的虚拟用户类型：\n")
        
        for user_type in self.user_types:
            status = "✅" if user_type['selected'] else "❌"
            output.append(f"{status} {user_type['type_name']}")
            output.append(f"   {user_type['scenario_summary']}")
            output.append("")
        
        output.append("\n💡 提示：回复'选择 1,3,5'选中特定类型，或'反选 2,4'取消选中")
        
        return "\n".join(output)
    
    def parse_selection_command(self, command: str) -> Dict:
        """
        解析用户的选择命令
        
        Args:
            command: 用户命令，如"选择 1,3,5"或"反选 2,4"
        
        Returns:
            dict: 解析结果
        """
        import re
        
        # 匹配"选择 X,Y,Z"或"反选 X,Y,Z"
        match = re.search(r'(选择 | 反选)\s*([\d,\s]+)', command)
        
        if not match:
            return {'success': False, 'message': '未识别选择命令'}
        
        action = match.group(1)
        ids = [int(x.strip()) for x in match.group(2).split(',') if x.strip().isdigit()]
        
        if not ids:
            return {'success': False, 'message': '未指定用户类型 ID'}
        
        # 执行选择
        selected = (action == '选择')
        for user_type_id in ids:
            self.toggle_selection(user_type_id, selected)
        
        return {
            'success': True,
            'action': action,
            'ids': ids,
            'message': f"已{action}用户类型：{', '.join(map(str, ids))}"
        }


# 测试代码
if __name__ == "__main__":
    # 模拟测试数据
    test_scenarios = [
        {
            '用户姓名和背景信息': '姓名 [廖慧] 所属八大人群 [新锐白领] 年龄 [28]',
            '用户具体场景': '行程规划和攻略制定',
            '任务': '为亚洲短途旅行确定合适的预订启动时间',
            '痛点': '无明显痛点，但如果遇到热门假期，一个月可能偏晚',
            '爽点': '对行程准备时间有清晰的预期',
            '底层需求': '对旅行规划有掌控感和确定性'
        }
    ]
    
    generator = VirtualUserGenerator()
    user_types = generator.generate_user_types(test_scenarios, top_n=3)
    
    print("生成的虚拟用户类型：")
    for ut in user_types:
        print(f"- {ut['type_name']}")
