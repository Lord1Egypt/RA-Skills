#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkillPilot v0.2.0 - 综合演示脚本

展示自适应技能调度引擎的核心功能
"""

import os
import sys

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, 'scripts'))

from environment import EnvironmentProbe
from preference import UserPreference
from learning import ExecutionHistory
from observability import SchedulerDashboard


def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    print_section("SkillPilot v0.2.0 - 自适应技能调度引擎")
    
    # 1. 环境探测
    print_section("1. 环境探测")
    
    probe = EnvironmentProbe()
    if probe.load_cache():
        print("✓ 使用缓存的环境数据")
        print(f"  区域：{probe.network_profile.get('region', 'unknown')}")
        print(f"  代理：{'是' if probe.network_profile.get('proxy_enabled') else '否'}")
        print(f"  推荐配置：{probe.get_optimal_profile()['name']}")
    else:
        print("⚠ 尚未执行环境探测")
        print("  运行：python scripts/environment.py")
    
    # 2. 用户偏好
    print_section("2. 用户偏好")
    
    pref = UserPreference()
    print(f"优化目标：{pref.optimization_goal}")
    print(f"预算限制：{pref.budget_limit}")
    print(f"权重配置：{pref.to_weights()}")
    
    # 显示预设模板
    print("\n可用预设模板:")
    templates = ['speed', 'cost', 'quality', 'balanced', 'cn-optimized', 'global-optimized']
    for t in templates:
        template = pref.create_template(t)
        print(f"  - {t}: {template['description']}")
    
    # 3. 历史学习
    print_section("3. 历史学习")
    
    history = ExecutionHistory()
    stats = history.get_stats_summary()
    print(f"追踪技能数：{stats['total_skills_tracked']}")
    print(f"总调用次数：{stats['total_calls']}")
    print(f"总体成功率：{stats['overall_success_rate']*100:.1f}%")
    print(f"已学习模式：{stats['patterns_learned']} 个")
    
    # 4. 可观测性
    print_section("4. 可观测性")
    
    dashboard = SchedulerDashboard(history=history, environment=probe)
    print(dashboard.generate_report('text'))
    
    # 5. 使用建议
    print_section("5. 使用建议")
    
    print("""
快速开始:
  1. 环境探测：python scripts/environment.py
  2. 设置偏好：python scripts/preference.py init balanced
  3. 查看报告：python scripts/observability.py report
  4. 分析表现：python scripts/learning.py analyze search

进阶使用:
  - 自定义配置：编辑 config/preference.yaml
  - 添加策略：在 strategies/ 目录创建 YAML 文件
  - 查看健康：python scripts/observability.py health
  - 学习模式：python scripts/learning.py learn
""")
    
    print_section("演示完成")


if __name__ == '__main__':
    main()
