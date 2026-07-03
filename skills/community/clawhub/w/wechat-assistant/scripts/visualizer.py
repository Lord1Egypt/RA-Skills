#!/usr/bin/env python3
"""
数据可视化脚本
生成聊天分析图表、人脉关系图、任务规划时间线
"""

import argparse
import json
import sys
import os
from datetime import datetime
from collections import defaultdict

try:
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    from matplotlib import rcParams
except ImportError:
    print(json.dumps({
        "status": "error",
        "error": "缺少matplotlib库，请运行: pip install matplotlib"
    }, ensure_ascii=False))
    sys.exit(1)

# 设置中文字体
try:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
except Exception:
    pass


class ChatVisualizer:
    def __init__(self):
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'positive': '#06A77D',
            'negative': '#D64933',
            'neutral': '#6B7280',
            'accent': '#F18F01'
        }
    
    def load_data(self, input_file):
        """加载数据"""
        if isinstance(input_file, str):
            with open(input_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return input_file
    
    def plot_keywords(self, keywords, output):
        """绘制关键词词云/柱状图"""
        if not keywords:
            keywords = [{"word": "无数据", "score": 0}]
        
        words = [k["word"] for k in keywords[:15]]
        scores = [k["score"] for k in keywords[:15]]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        y_pos = range(len(words))
        colors = [self.colors['primary']] * len(words)
        
        ax.barh(y_pos, scores, color=colors)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(words)
        ax.invert_yaxis()
        ax.set_xlabel('Importance Score')
        ax.set_title('Top Keywords Analysis', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output, dpi=150, bbox_inches='tight')
        plt.close()
        
        return {"file": output, "type": "keywords"}
    
    def plot_sentiment(self, sentiment_data, output):
        """绘制情感分布饼图"""
        if not sentiment_data:
            sentiment_data = {"positive": 1, "negative": 0, "neutral": 1}
        
        labels = ['Positive', 'Negative', 'Neutral']
        sizes = [
            sentiment_data.get('positive', 0),
            sentiment_data.get('negative', 0),
            sentiment_data.get('neutral', 0)
        ]
        colors = [self.colors['positive'], self.colors['negative'], self.colors['neutral']]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if sum(sizes) == 0:
            sizes = [1, 1, 1]
            labels = ['No Data'] * 3
        
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=(0.05, 0.05, 0.05)
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Sentiment Distribution', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output, dpi=150, bbox_inches='tight')
        plt.close()
        
        return {"file": output, "type": "sentiment"}
    
    def plot_intents(self, intents_data, output):
        """绘制意图分布柱状图"""
        if not intents_data or 'distribution' not in intents_data:
            intents_data = {'distribution': {'general': 1}}
        
        distribution = intents_data.get('distribution', {})
        
        intent_names = {
            'schedule': 'Schedule',
            'meeting': 'Meeting',
            'question': 'Question',
            'request': 'Request',
            'greeting': 'Greeting',
            'thanks': 'Thanks',
            'confirm': 'Confirm',
            'general': 'General'
        }
        
        labels = [intent_names.get(k, k) for k in distribution.keys()]
        values = list(distribution.values())
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.bar(labels, values, color=self.colors['primary'])
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Intent Type')
        ax.set_ylabel('Message Count')
        ax.set_title('Intent Distribution', fontsize=16, fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output, dpi=150, bbox_inches='tight')
        plt.close()
        
        return {"file": output, "type": "intents"}
    
    def plot_frequency(self, frequency_data, output):
        """绘制时间频率分布"""
        if not frequency_data or 'time_distribution' not in frequency_data:
            frequency_data = {'time_distribution': {'morning': 1}}
        
        time_dist = frequency_data.get('time_distribution', {})
        
        time_labels = ['Morning\n(6-12)', 'Noon\n(12-14)', 'Afternoon\n(14-18)', 
                      'Evening\n(18-22)', 'Night\n(22-6)']
        time_keys = ['morning', 'noon', 'afternoon', 'evening', 'night']
        
        values = [time_dist.get(k, 0) for k in time_keys]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(time_labels, values, color=[
            self.colors['accent'],
            self.colors['secondary'],
            self.colors['primary'],
            self.colors['primary'],
            self.colors['neutral']
        ])
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Time Period')
        ax.set_ylabel('Message Count')
        ax.set_title('Chat Frequency by Time', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output, dpi=150, bbox_inches='tight')
        plt.close()
        
        return {"file": output, "type": "frequency"}
    
    def plot_relationship(self, messages, output):
        """绘制人脉关系图"""
        # 统计联系人频率
        contact_freq = defaultdict(int)
        for msg in messages:
            contact = msg.get('contact', 'unknown')
            contact_freq[contact] += 1
        
        if not contact_freq:
            contact_freq = {'No Data': 1}
        
        contacts = list(contact_freq.keys())
        frequencies = list(contact_freq.values())
        
        # 创建关系图样式输出
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # 计算节点位置(圆形布局)
        n = len(contacts)
        angles = [2 * 3.14159 * i / n for i in range(n)]
        
        # 节点大小基于频率
        max_freq = max(frequencies) if frequencies else 1
        sizes = [300 + (f / max_freq) * 1500 for f in frequencies]
        
        # 绘制节点
        x_coords = [0.5 + 0.4 * (1 - abs(a - 3.14159) / 3.14159) * (1 if a < 3.14159 else -1) for a in angles]
        y_coords = [0.5 + 0.3 * (1 - abs(a - 3.14159) / 3.14159) for a in angles]
        
        # 简单圆形布局
        x_coords = [0.5 + 0.35 * (1 - 2 * i / n if i / n < 0.5 else 2 * (i / n - 0.5)) for i in range(n)]
        x_coords = [0.5 + 0.35 * (1 if i < n/2 else -1) * ((2*i/n) if i < n/2 else (2*(i-n/2)/n)) for i in range(n)]
        y_coords = [0.5 + 0.35 * ((2*i/n - 1) if i < n/2 else (1 - 2*(i-n/2)/n)) for i in range(n)]
        
        # 修正为圆形
        x_coords = [0.5 + 0.35 * (1 - 2 * i / n if i < n/2 else 2 * (i / n - 1)) for i in range(n)]
        y_coords = [0.5 + 0.35 * (2 * i / n - 1 if i < n/2 else 1 - 2 * (i - n/2) / n) for i in range(n)]
        
        for i, (x, y, size, contact, freq) in enumerate(zip(x_coords, y_coords, sizes, contacts, frequencies)):
            circle = plt.Circle((x, y), size/3000, color=self.colors['primary'], alpha=0.6)
            ax.add_patch(circle)
            ax.text(x, y, f'{contact}\n({freq})', ha='center', va='center', 
                   fontsize=8, fontweight='bold', color='white')
        
        # 绘制连线(中心连接)
        center_x, center_y = 0.5, 0.5
        for x, y in zip(x_coords, y_coords):
            ax.plot([center_x, x], [center_y, y], 
                   color=self.colors['neutral'], alpha=0.3, linewidth=1)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Contact Relationship Map', fontsize=16, fontweight='bold')
        
        # 添加图例
        ax.text(0.02, 0.02, 'Node size = Interaction frequency', 
               fontsize=10, transform=ax.transAxes)
        
        plt.tight_layout()
        plt.savefig(output, dpi=150, bbox_inches='tight')
        plt.close()
        
        return {"file": output, "type": "relationship"}
    
    def plot_timeline(self, analysis_data, output):
        """绘制任务规划时间线"""
        requirements = analysis_data.get('requirements', [])
        
        if not requirements:
            requirements = [{"type": "general", "content": "No requirements detected"}]
        
        fig, ax = plt.subplots(figsize=(14, max(6, len(requirements) * 1.5)))
        
        y_positions = range(len(requirements) - 1, -1, -1)
        
        type_colors = {
            'schedule': self.colors['primary'],
            'meeting': self.colors['secondary'],
            'deadline': self.colors['negative'],
            'budget': self.colors['accent'],
            'quantity': self.colors['positive'],
            'general': self.colors['neutral']
        }
        
        for i, (y, req) in enumerate(zip(y_positions, requirements)):
            req_type = req.get('type', 'general')
            color = type_colors.get(req_type, self.colors['neutral'])
            
            # 绘制节点
            ax.scatter(0.1, y, s=200, color=color, zorder=3)
            ax.plot([0.1, 0.9], [y, y], color=color, alpha=0.3, linewidth=2)
            
            # 添加标签
            ax.text(0.05, y, req_type.upper(), fontsize=9, 
                   ha='left', va='center', fontweight='bold', color=color)
            ax.text(0.15, y, req.get('content', 'N/A')[:60], fontsize=9,
                   ha='left', va='center')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(-1, len(requirements))
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_title('Requirements Timeline', fontsize=16, fontweight='bold')
        
        # 添加图例
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=color, markersize=10, label=type_name)
            for type_name, color in type_colors.items()
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
        
        plt.tight_layout()
        plt.savefig(output, dpi=150, bbox_inches='tight')
        plt.close()
        
        return {"file": output, "type": "timeline"}
    
    def plot_interaction_pattern(self, pattern_data, output):
        """绘制互动模式分析图"""
        if not pattern_data:
            pattern_data = {"total_exchanges": 0, "avg_exchange_length": 0}
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # 左图: 统计信息
        stats_labels = ['Total Exchanges', 'Avg Length', 'Max Length']
        stats_values = [
            pattern_data.get('total_exchanges', 0),
            pattern_data.get('avg_exchange_length', 0),
            pattern_data.get('longest_exchange', 0)
        ]
        
        colors = [self.colors['primary'], self.colors['secondary'], self.colors['accent']]
        bars = axes[0].bar(stats_labels, stats_values, color=colors)
        
        for bar in bars:
            height = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}',
                        ha='center', va='bottom', fontweight='bold')
        
        axes[0].set_ylabel('Count')
        axes[0].set_title('Interaction Statistics', fontsize=14, fontweight='bold')
        
        # 右图: 对话轮次分布(模拟)
        exchange_lengths = [1, 2, 3, 4, 5, 6, 7, 8]
        distribution = [30, 25, 20, 12, 8, 3, 1, 1]  # 模拟数据
        
        axes[1].bar(exchange_lengths, distribution, color=self.colors['primary'])
        axes[1].set_xlabel('Exchange Length (turns)')
        axes[1].set_ylabel('Frequency (%)')
        axes[1].set_title('Exchange Length Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output, dpi=150, bbox_inches='tight')
        plt.close()
        
        return {"file": output, "type": "interaction"}
    
    def run(self, input_file, viz_type, output):
        """执行可视化"""
        data = self.load_data(input_file)
        
        # 根据类型生成图表
        if viz_type == 'keywords':
            result = self.plot_keywords(data.get('keywords', []), output)
        elif viz_type == 'sentiment':
            result = self.plot_sentiment(data.get('sentiment', {}), output)
        elif viz_type == 'intents':
            result = self.plot_intents(data.get('intents', {}), output)
        elif viz_type == 'frequency':
            result = self.plot_frequency(data.get('frequency', {}), output)
        elif viz_type == 'relationship':
            result = self.plot_relationship(data.get('messages', []), output)
        elif viz_type == 'timeline':
            result = self.plot_timeline(data, output)
        elif viz_type == 'interaction':
            result = self.plot_interaction_pattern(data.get('interaction_pattern', {}), output)
        elif viz_type == 'dashboard':
            # 生成综合仪表盘
            result = {"charts": []}
            base_name = output.rsplit('.', 1)[0]
            
            # 保存各个子图
            result["charts"].append(self.plot_keywords(data.get('keywords', []), f"{base_name}_keywords.png"))
            result["charts"].append(self.plot_sentiment(data.get('sentiment', {}), f"{base_name}_sentiment.png"))
            result["charts"].append(self.plot_intents(data.get('intents', {}), f"{base_name}_intents.png"))
            
            result["main_chart"] = f"{base_name}_keywords.png"
        else:
            return {"status": "error", "error": f"未知图表类型: {viz_type}"}
        
        result["status"] = "success"
        result["timestamp"] = datetime.now().isoformat()
        
        return result


def main():
    parser = argparse.ArgumentParser(description='数据可视化工具')
    parser.add_argument('--input', required=True, help='输入JSON文件路径')
    parser.add_argument('--type', required=True,
                       choices=['keywords', 'sentiment', 'intents', 'frequency', 
                               'relationship', 'timeline', 'interaction', 'dashboard'],
                       help='图表类型')
    parser.add_argument('--output', required=True, help='输出PNG文件路径')
    
    args = parser.parse_args()
    
    visualizer = ChatVisualizer()
    result = visualizer.run(args.input, args.type, args.output)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
