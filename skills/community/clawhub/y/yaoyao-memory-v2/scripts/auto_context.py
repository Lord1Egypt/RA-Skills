#!/usr/bin/env python3
"""
自动上下文追踪模块 - 自动追踪对话上下文并提取关键信息

功能：
- 自动检测对话主题
- 追踪当前项目/任务
- 提取关键实体（人名、地名、时间）
- 生成上下文摘要
- 上下文切换检测
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_memory_base


class ContextTracker:
    """上下文追踪器"""
    
    def __init__(self):
        self.current_topic = None
        self.current_project = None
        self.entities: Dict[str, Set[str]] = defaultdict(set)
        self.conversation_history: List[Dict] = []
        self.topic_history: List[Dict] = []
        self.max_history = 50
        
        # 模式定义
        self.entity_patterns = {
            'person': re.compile(r'([A-Z][a-z]+ [A-Z][a-z]+)|([\u4e00-\u9fff]{2,3}(?:先生|女士|老师|同学|老板))'),
            'time': re.compile(r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?|\d{1,2}[时点]\d{0,2}分?|下[周个星期天月年]|今明后[天日周])'),
            'place': re.compile(r'在([A-Z][a-z]+)|在([\u4e00-\u9fff]{2,4}(?:公司|医院|学校|店|餐厅|酒店|机场|车站|图书馆))'),
            'project': re.compile(r'(?:项目|任务|案子)[:：]?\s*([^\s，。！？]+)'),
        }
        
        # 主题关键词
        self.topic_keywords = {
            '技术': ['代码', '编程', '开发', 'API', '系统', '配置', '安装', '部署', 'Git', 'Python', 'JavaScript'],
            '工作': ['工作', '会议', '报告', '客户', '同事', '上班', '下班', '加班', '项目'],
            '生活': ['吃饭', '睡觉', '运动', '休息', '朋友', '家人', '购物', '旅行'],
            '学习': ['学习', '研究', '课程', '读书', '考试', '练习', '作业'],
            '财务': ['钱', '价格', '成本', '预算', '支付', '购买', '工资', '报销'],
            '健康': ['健康', '医生', '医院', '药', '身体', '锻炼', '运动', '减肥'],
        }
    
    def process_message(self, text: str, is_user: bool = True) -> Dict:
        """处理消息并提取上下文"""
        result = {
            'entities': {},
            'topic': None,
            'is_topic_change': False,
            'summary': None
        }
        
        # 提取实体
        entities = self._extract_entities(text)
        for entity_type, values in entities.items():
            self.entities[entity_type].update(values)
        result['entities'] = entities
        
        # 检测主题
        new_topic = self._detect_topic(text)
        if new_topic != self.current_topic:
            if self.current_topic is not None:
                result['is_topic_change'] = True
            self.current_topic = new_topic
            self.topic_history.append({
                'topic': new_topic,
                'timestamp': datetime.now().isoformat(),
                'preview': text[:50]
            })
        result['topic'] = self.current_topic
        
        # 检测项目
        project_match = self.entity_patterns['project'].search(text)
        if project_match:
            self.current_project = project_match.group(1)
            result['project'] = self.current_project
        
        # 添加到历史
        self.conversation_history.append({
            'text': text,
            'is_user': is_user,
            'topic': self.current_topic,
            'timestamp': datetime.now().isoformat()
        })
        
        # 限制历史长度
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        # 生成摘要
        result['summary'] = self._generate_summary()
        
        return result
    
    def _extract_entities(self, text: str) -> Dict[str, Set[str]]:
        """提取实体"""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = pattern.findall(text)
            if matches:
                # 展平元组
                values = set()
                for m in matches:
                    if isinstance(m, tuple):
                        values.update(v for v in m if v)
                    else:
                        values.add(m)
                if values:
                    entities[entity_type] = values
        
        return entities
    
    def _detect_topic(self, text: str) -> Optional[str]:
        """检测主题"""
        topic_scores = defaultdict(int)
        
        for topic, keywords in self.topic_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    topic_scores[topic] += 1
        
        if topic_scores:
            return max(topic_scores.items(), key=lambda x: x[1])[0]
        
        return None
    
    def _generate_summary(self) -> str:
        """生成上下文摘要"""
        lines = ["当前上下文摘要", ""]
        
        if self.current_topic:
            lines.append(f"📌 主题：{self.current_topic}")
        
        if self.current_project:
            lines.append(f"📋 项目：{self.current_project}")
        
        if self.entities:
            lines.append("")
            for entity_type, values in self.entities.items():
                if values:
                    top_values = list(values)[:3]
                    lines.append(f"{entity_type}：{', '.join(top_values)}")
        
        if len(self.conversation_history) > 0:
            recent = self.conversation_history[-5:]
            user_msgs = [m['text'] for m in recent if m['is_user']]
            if user_msgs:
                lines.append("")
                lines.append(f"最近 {len(user_msgs)} 条用户消息")
        
        return "\n".join(lines)
    
    def detect_context_switch(self, new_text: str) -> bool:
        """检测上下文是否切换"""
        # 检查主题变化
        new_topic = self._detect_topic(new_text)
        if new_topic and self.current_topic and new_topic != self.current_topic:
            return True
        
        # 检查项目变化
        project_match = self.entity_patterns['project'].search(new_text)
        if project_match and self.current_project:
            if project_match.group(1) != self.current_project:
                return True
        
        return False
    
    def get_current_context(self) -> Dict:
        """获取当前上下文"""
        return {
            'topic': self.current_topic,
            'project': self.current_project,
            'entities': dict(self.entities),
            'message_count': len(self.conversation_history),
            'recent_preview': self.conversation_history[-3:] if self.conversation_history else []
        }
    
    def reset_context(self):
        """重置上下文"""
        self.current_topic = None
        self.current_project = None
        self.entities.clear()
        self.conversation_history.clear()


class ContextManager:
    """上下文管理器 - 长期上下文追踪"""
    
    def __init__(self):
        self.tracker = ContextTracker()
        self.contexts: Dict[str, ContextTracker] = {}
        self.active_context_key = "default"
    
    def switch_context(self, key: str):
        """切换上下文"""
        if key not in self.contexts:
            self.contexts[key] = ContextTracker()
        self.active_context_key = key
    
    def process(self, text: str, is_user: bool = True) -> Dict:
        """处理消息"""
        tracker = self.contexts.get(self.active_context_key, self.tracker)
        return tracker.process_message(text, is_user)
    
    def get_active_context(self) -> Dict:
        """获取当前活动上下文"""
        tracker = self.contexts.get(self.active_context_key, self.tracker)
        return tracker.get_current_context()


def main():
    """CLI 测试"""
    tracker = ContextTracker()
    
    # 模拟对话
    messages = [
        "帮我记住这个项目叫 AI-Helper",
        "今天天气不错",
        "项目的代码已经提交到 Git 了",
        "明天要和客户开会讨论进度",
    ]
    
    for msg in messages:
        result = tracker.process_message(msg)
        print(f"\n📝 消息: {msg}")
        print(f"   主题: {result['topic']}")
        print(f"   实体: {result['entities']}")
        print(f"   切换: {result['is_topic_change']}")
    
    print("\n" + "="*50)
    print(tracker.get_current_context())


if __name__ == '__main__':
    main()
