# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
可观测性模块

提供调度看板、性能报告和诊断工具
"""

import os
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class SchedulerDashboard:
    """调度看板"""
    
    def __init__(self, history=None, registry=None, environment=None):
        self.history = history
        self.registry = registry
        self.environment = environment
        self.report_dir = os.path.expanduser(
            "~/.openclaw/workspace/skills/skill-pilot/reports"
        )
    
    def generate_report(self, output_format: str = 'text') -> str:
        """
        生成调度报告
        
        Args:
            output_format: text | markdown | json
        
        Returns:
            报告内容
        """
        # 收集数据
        env_data = self._get_env_data()
        stats_data = self._get_stats_data()
        learning_data = self._get_learning_data()
        
        if output_format == 'json':
            return json.dumps({
                'generated_at': datetime.now().isoformat(),
                'environment': env_data,
                'skill_stats': stats_data,
                'learned_patterns': learning_data,
            }, ensure_ascii=False, indent=2)
        
        elif output_format == 'markdown':
            return self._generate_markdown_report(env_data, stats_data, learning_data)
        
        else:
            return self._generate_text_report(env_data, stats_data, learning_data)
    
    def _get_env_data(self) -> Dict:
        """获取环境数据"""
        if not self.environment:
            return {'status': 'not_configured'}
        
        if self.environment.load_cache():
            return {
                'region': self.environment.network_profile.get('region', 'unknown'),
                'proxy': self.environment.network_profile.get('proxy_enabled', False),
                'recommended_profile': self.environment.get_optimal_profile()['name'],
                'last_probe': self.environment.last_probe_time,
            }
        
        return {'status': 'not_probed'}
    
    def _get_stats_data(self) -> Dict:
        """获取统计数据"""
        if not self.history:
            return {'status': 'not_configured'}
        
        return self.history.get_stats_summary()
    
    def _get_learning_data(self) -> Dict:
        """获取学习数据"""
        if not self.history:
            return {'status': 'not_configured'}
        
        patterns = self.history._load_learned_patterns()
        return {
            'patterns_count': len(patterns.get('patterns', {})),
            'last_learned': patterns.get('learned_at', 'N/A'),
            'by_category': patterns.get('patterns', {}),
        }
    
    def _generate_text_report(self, env_data, stats_data, learning_data) -> str:
        """生成文本报告"""
        lines = []
        lines.append("┌" + "─" * 62 + "┐")
        lines.append("│" + " " * 20 + "SkillPilot 调度报告" + " " * 21 + "│")
        lines.append("├" + "─" * 62 + "┤")
        lines.append(f"│ 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{' ' * 33}│")
        lines.append("├" + "─" * 62 + "┤")
        
        # 环境配置
        lines.append("│ 【环境配置】" + " " * 48 + "│")
        if env_data.get('status') == 'not_configured':
            lines.append("│   环境探测模块未配置" + " " * 37 + "│")
        elif env_data.get('status') == 'not_probed':
            lines.append("│   尚未执行环境探测" + " " * 40 + "│")
        else:
            region = env_data.get('region', 'unknown')
            proxy = '是' if env_data.get('proxy') else '否'
            profile = env_data.get('recommended_profile', 'unknown')
            lines.append(f"│   区域：{region}{' ' * 52}│"[:64] + "│")
            lines.append(f"│   代理：{proxy}{' ' * 52}│"[:64] + "│")
            lines.append(f"│   推荐配置：{profile}{' ' * 47}│"[:64] + "│")
        
        lines.append("├" + "─" * 62 + "┤")
        
        # 技能统计
        lines.append("│ 【技能表现】" + " " * 47 + "│")
        total_calls = stats_data.get('total_calls', 0)
        success_rate = stats_data.get('overall_success_rate', 0) * 100
        lines.append(f"│   追踪技能数：{stats_data.get('total_skills_tracked', 0)}{' ' * 44}│"[:64] + "│")
        lines.append(f"│   总调用次数：{total_calls}{' ' * 47}│"[:64] + "│")
        lines.append(f"│   总体成功率：{success_rate:.1f}%{' ' * 46}│"[:64] + "│")
        
        lines.append("├" + "─" * 62 + "┤")
        
        # 学习成果
        lines.append("│ 【学习成果】" + " " * 47 + "│")
        lines.append(f"│   已学习模式：{learning_data.get('patterns_count', 0)} 个{' ' * 46}│"[:64] + "│")
        last_learned = learning_data.get('last_learned', 'N/A')
        if last_learned != 'N/A':
            try:
                dt = datetime.fromisoformat(last_learned)
                last_learned = dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass
        lines.append(f"│   最后学习：{last_learned}{' ' * 47}│"[:64] + "│")
        
        lines.append("├" + "─" * 62 + "┤")
        
        # 优化建议
        lines.append("│ 【优化建议】" + " " * 47 + "│")
        suggestions = self._generate_suggestions(env_data, stats_data, learning_data)
        for i, sug in enumerate(suggestions[:3], 1):
            lines.append(f"│   {i}. {sug}{' ' * (55 - len(sug))}│"[:64] + "│")
        
        if not suggestions:
            lines.append("│   暂无优化建议" + " " * 43 + "│")
        
        lines.append("└" + "─" * 62 + "┘")
        
        return '\n'.join(lines)
    
    def _generate_markdown_report(self, env_data, stats_data, learning_data) -> str:
        """生成 Markdown 报告"""
        lines = []
        lines.append("# SkillPilot 调度报告\n")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 环境配置
        lines.append("## 环境配置\n")
        if env_data.get('status') == 'not_configured':
            lines.append("- 环境探测模块未配置")
        elif env_data.get('status') == 'not_probed':
            lines.append("- 尚未执行环境探测")
        else:
            lines.append(f"- **区域**: {env_data.get('region', 'unknown')}")
            lines.append(f"- **代理**: {'是' if env_data.get('proxy') else '否'}")
            lines.append(f"- **推荐配置**: {env_data.get('recommended_profile', 'unknown')}")
        lines.append("")
        
        # 技能表现
        lines.append("## 技能表现\n")
        lines.append(f"- **追踪技能数**: {stats_data.get('total_skills_tracked', 0)}")
        lines.append(f"- **总调用次数**: {stats_data.get('total_calls', 0)}")
        lines.append(f"- **总体成功率**: {stats_data.get('overall_success_rate', 0) * 100:.1f}%")
        lines.append("")
        
        # 学习成果
        lines.append("## 学习成果\n")
        lines.append(f"- **已学习模式**: {learning_data.get('patterns_count', 0)} 个")
        last_learned = learning_data.get('last_learned', 'N/A')
        lines.append(f"- **最后学习**: {last_learned}")
        lines.append("")
        
        # 优化建议
        lines.append("## 优化建议\n")
        suggestions = self._generate_suggestions(env_data, stats_data, learning_data)
        if suggestions:
            for i, sug in enumerate(suggestions, 1):
                lines.append(f"{i}. {sug}")
        else:
            lines.append("暂无优化建议")
        lines.append("")
        
        # 详细数据
        lines.append("## 详细数据\n")
        lines.append("### 按类别分析\n")
        by_category = learning_data.get('by_category', {})
        if by_category:
            for cat, data in by_category.items():
                lines.append(f"#### {cat}\n")
                lines.append(f"- 最优技能：{data.get('best_skill', 'N/A')}")
                lines.append(f"- 成功率：{data.get('success_rate', 0) * 100:.1f}%")
                lines.append(f"- 平均响应：{data.get('avg_response_time', 0):.0f}ms")
                lines.append(f"- 样本数：{data.get('sample_size', 0)}")
                lines.append("")
        else:
            lines.append("暂无数据\n")
        
        return '\n'.join(lines)
    
    def _generate_suggestions(self, env_data, stats_data, learning_data) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 环境相关
        if env_data.get('status') == 'not_probed':
            suggestions.append("执行环境探测以获取最优配置建议")
        
        if env_data.get('region') == 'cn' and env_data.get('recommended_profile') != 'cn-no-proxy':
            suggestions.append("检测到国内环境，建议使用 cn-no-proxy 配置")
        
        # 统计相关
        total_calls = stats_data.get('total_calls', 0)
        if total_calls < 10:
            suggestions.append("调用样本较少，继续使用以积累学习数据")
        
        success_rate = stats_data.get('overall_success_rate', 0)
        if success_rate < 0.8 and total_calls > 20:
            suggestions.append(f"成功率偏低 ({success_rate*100:.1f}%)，检查技能配置或网络环境")
        
        # 学习相关
        patterns_count = learning_data.get('patterns_count', 0)
        if patterns_count == 0 and total_calls > 50:
            suggestions.append("已积累足够数据，运行学习算法提取优化模式")
        
        return suggestions
    
    def save_report(self, output_format: str = 'markdown') -> str:
        """保存报告到文件"""
        os.makedirs(self.report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"skillpilot_report_{timestamp}"
        
        if output_format == 'markdown':
            filename += '.md'
        elif output_format == 'json':
            filename += '.json'
        else:
            filename += '.txt'
        
        filepath = os.path.join(self.report_dir, filename)
        
        content = self.generate_report(output_format)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def print_skill_health(self) -> str:
        """打印技能健康状态"""
        if not self.history:
            return "历史模块未配置"
        
        stats = self.history._load_stats()
        
        if not stats:
            return "暂无技能数据"
        
        lines = []
        lines.append("技能健康状态")
        lines.append("=" * 50)
        
        # 按调用次数排序
        sorted_skills = sorted(
            stats.items(),
            key=lambda x: x[1]['total_calls'],
            reverse=True
        )
        
        for skill_name, s in sorted_skills[:10]:
            success_rate = s['success_count'] / max(1, s['total_calls'])
            avg_time = s['total_response_time'] / max(1, s['total_calls'])
            
            # 健康分数 (0-100)
            health_score = success_rate * 80 + max(0, 20 - avg_time / 500)
            
            # 进度条
            bar_length = int(health_score / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            
            lines.append(f"{skill_name[:20]:20} {bar} {health_score:.0f}分 (成功率 {success_rate*100:.0f}%, 响应 {avg_time:.0f}ms)")
        
        return '\n'.join(lines)


# 快捷函数
def quick_report() -> str:
    """快速生成报告"""
    from .learning import ExecutionHistory
    from .environment import EnvironmentProbe
    
    history = ExecutionHistory()
    environment = EnvironmentProbe()
    
    dashboard = SchedulerDashboard(history=history, environment=environment)
    return dashboard.generate_report('text')


if __name__ == '__main__':
    # 命令行测试
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from learning import ExecutionHistory
    from environment import EnvironmentProbe
    
    history = ExecutionHistory()
    environment = EnvironmentProbe()
    dashboard = SchedulerDashboard(history=history, environment=environment)
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == 'report':
            fmt = sys.argv[2] if len(sys.argv) > 2 else 'text'
            print(dashboard.generate_report(fmt))
        
        elif action == 'save':
            fmt = sys.argv[2] if len(sys.argv) > 2 else 'markdown'
            filepath = dashboard.save_report(fmt)
            print(f"✓ 报告已保存：{filepath}")
        
        elif action == 'health':
            print(dashboard.print_skill_health())
        
        elif action == 'json':
            print(dashboard.generate_report('json'))
    else:
        # 默认：文本报告
        print(dashboard.generate_report('text'))
