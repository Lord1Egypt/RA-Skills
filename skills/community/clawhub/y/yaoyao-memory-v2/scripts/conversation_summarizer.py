#!/usr/bin/env python3
"""
对话摘要模块 - 快速总结对话内容

功能：
- 实时对话摘要
- 关键信息提取
- 行动项识别
- 对话主题分类
- 情绪分析（简化版）
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))


class ConversationSummarizer:
    """对话摘要器"""
    
    def __init__(self):
        self.max_messages = 100
    
    def extract_key_points(self, messages: List[str]) -> List[str]:
        """提取关键点"""
        if not messages:
            return []
        
        key_points = []
        
        # 提取包含数字的陈述
        for msg in messages:
            numbers = re.findall(r'\d+', msg)
            if numbers and len(msg) > 20:
                key_points.append(f"提及数字：{', '.join(numbers[:5])}")
        
        # 提取动作指令
        action_patterns = [
            (r'记住(.+)', '记住'),
            (r'帮我(.+)', '帮做'),
            (r'设置(.+)', '设置'),
            (r'创建(.+)', '创建'),
            (r'删除(.+)', '删除'),
            (r'更新(.+)', '更新'),
        ]
        
        actions = []
        for msg in messages:
            for pattern, action in action_patterns:
                match = re.search(pattern, msg)
                if match:
                    actions.append(f"{action}: {match.group(1)[:30]}")
        
        if actions:
            key_points.extend(actions[:5])
        
        return list(set(key_points))[:10]
    
    def extract_decisions(self, messages: List[str]) -> List[str]:
        """提取决策"""
        decisions = []
        
        decision_keywords = ['决定', '选择', '采用', '确定', '就这样']
        
        for msg in messages:
            for kw in decision_keywords:
                if kw in msg:
                    # 提取包含关键词的完整句子
                    sentences = re.split(r'[。！？]', msg)
                    for s in sentences:
                        if kw in s and len(s) > 5:
                            decisions.append(s.strip())
        
        return decisions[:5]
    
    def extract_action_items(self, messages: List[str]) -> List[Dict]:
        """提取行动项"""
        action_items = []
        
        action_patterns = [
            (r'帮我(.+?)[。！]', '待做'),
            (r'需要(.+?)[。！]', '需做'),
            (r'应该(.+?)[。！]', '应做'),
            (r'记得(.+?)[。！]', '提醒'),
            (r'TODO[:：]?\s*(.+)', 'TODO'),
        ]
        
        for msg in messages:
            for pattern, item_type in action_patterns:
                match = re.search(pattern, msg)
                if match:
                    action_items.append({
                        'type': item_type,
                        'content': match.group(1).strip()[:50],
                        'source': msg[:50]
                    })
        
        return action_items[:10]
    
    def classify_topics(self, messages: List[str]) -> List[Tuple[str, int]]:
        """分类对话主题"""
        topic_keywords = {
            '技术': ['代码', '编程', '开发', 'API', '系统', '配置', '安装', '部署'],
            '项目': ['项目', '任务', '计划', '开发', '设计', '架构'],
            '生活': ['吃饭', '睡觉', '运动', '休息', '朋友', '家人'],
            '工作': ['工作', '会议', '报告', '客户', '同事', '上班'],
            '学习': ['学习', '研究', '课程', '读书', '考试', '练习'],
            '财务': ['钱', '价格', '成本', '预算', '支付', '购买'],
            '健康': ['健康', '医生', '医院', '药', '身体', '锻炼'],
        }
        
        topic_counts = Counter()
        
        for msg in messages:
            msg_lower = msg.lower()
            for topic, keywords in topic_keywords.items():
                if any(kw in msg for kw in keywords):
                    topic_counts[topic] += 1
        
        return topic_counts.most_common(5)
    
    def analyze_sentiment(self, messages: List[str]) -> Dict:
        """情绪分析（简化版）"""
        positive_words = ['好', '棒', '赞', '优秀', '完美', '喜欢', '谢谢', '好的', 'OK', '同意', '成功', '不错', '厉害']
        negative_words = ['不好', '糟糕', '差', '烂', '讨厌', '麻烦', '问题', '错误', '失败', '不对', '别', '不要']
        neutral_words = ['了解', '知道', '明白', '理解', '可能', '大概']
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for msg in messages:
            has_positive = any(w in msg for w in positive_words)
            has_negative = any(w in msg for w in negative_words)
            
            if has_positive and not has_negative:
                positive_count += 1
            elif has_negative:
                negative_count += 1
            else:
                neutral_count += 1
        
        total = len(messages)
        if total == 0:
            return {'sentiment': 'neutral', 'positive': 0, 'negative': 0, 'neutral': 0}
        
        # 判断主要情绪
        if positive_count > negative_count and positive_count > neutral_count:
            sentiment = 'positive'
        elif negative_count > neutral_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'positive': round(positive_count / total * 100),
            'negative': round(negative_count / total * 100),
            'neutral': round(neutral_count / total * 100)
        }
    
    def generate_summary(self, messages: List[str], title: str = "对话摘要") -> str:
        """生成完整摘要"""
        if not messages:
            return "# 对话摘要\n\n（无消息内容）"
        
        lines = [f"# 📝 {title}", ""]
        lines.append(f"**消息数**：{len(messages)} 条")
        lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        
        # 情绪分析
        sentiment = self.analyze_sentiment(messages)
        sentiment_emoji = {'positive': '😊', 'negative': '😔', 'neutral': '😐'}
        lines.append(f"## {sentiment_emoji.get(sentiment['sentiment'], '😐')} 整体情绪")
        lines.append(f"- 积极：{sentiment['positive']}%")
        lines.append(f"- 消极：{sentiment['negative']}%")
        lines.append(f"- 中性：{sentiment['neutral']}%")
        lines.append("")
        
        # 主题分类
        topics = self.classify_topics(messages)
        if topics:
            lines.append("## 📊 话题分布")
            for topic, count in topics:
                lines.append(f"- {topic}：{count} 条消息")
            lines.append("")
        
        # 关键点
        key_points = self.extract_key_points(messages)
        if key_points:
            lines.append("## 🔑 关键信息")
            for point in key_points[:5]:
                lines.append(f"- {point}")
            lines.append("")
        
        # 决策
        decisions = self.extract_decisions(messages)
        if decisions:
            lines.append("## ✅ 决策记录")
            for d in decisions:
                lines.append(f"- {d}")
            lines.append("")
        
        # 行动项
        action_items = self.extract_action_items(messages)
        if action_items:
            lines.append("## 📋 行动项")
            for item in action_items:
                lines.append(f"- [{item['type']}] {item['content']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def quick_summary(self, messages: List[str]) -> str:
        """快速摘要（一句话）"""
        if not messages:
            return "无消息"
        
        # 提取第一个和最后一个有意义的消息
        first = next((m for m in messages if len(m) > 10), messages[0])
        last = next((m for m in reversed(messages) if len(m) > 10), messages[-1])
        
        # 提取主题
        topics = self.classify_topics(messages)
        main_topic = topics[0][0] if topics else "对话"
        
        return f"围绕「{main_topic}」的{len(messages)}条对话，从【{first[:20]}...】到【{last[:20]}...】"


def summarize_conversation(messages: List[str], format: str = "full") -> str:
    """便捷函数"""
    summarizer = ConversationSummarizer()
    
    if format == "quick":
        return summarizer.quick_summary(messages)
    else:
        return summarizer.generate_summary(messages)


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='对话摘要')
    parser.add_argument('--messages', '-m', nargs='+', help='输入消息列表')
    parser.add_argument('--quick', '-q', action='store_true', help='快速摘要')
    parser.add_argument('--topics', '-t', action='store_true', help='只显示主题')
    parser.add_argument('--actions', '-a', action='store_true', help='只显示行动项')
    args = parser.parse_args()
    
    # 默认测试数据
    test_messages = [
        "帮我记住我的密码是 abc123",
        "好的，已记住",
        "今天天气不错",
        "我决定用 Python 来开发这个项目",
        "需要配置 API Key",
        "帮我创建一个备份脚本",
    ]
    
    messages = args.messages if args.messages else test_messages
    
    summarizer = ConversationSummarizer()
    
    if args.quick:
        print(summarizer.quick_summary(messages))
    elif args.topics:
        topics = summarizer.classify_topics(messages)
        print("# 📊 话题分布")
        for t, c in topics:
            print(f"- {t}: {c}")
    elif args.actions:
        actions = summarizer.extract_action_items(messages)
        print("# 📋 行动项")
        for a in actions:
            print(f"- [{a['type']}] {a['content']}")
    else:
        print(summarizer.generate_summary(messages))
    
    summarizer.close()


if __name__ == '__main__':
    main()
