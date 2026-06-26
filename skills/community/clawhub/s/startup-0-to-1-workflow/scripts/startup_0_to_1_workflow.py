#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Startup 0 to 1 Workflow - 从 0 到 1 创业工作流
"""

import os
import sys
import io
import json
from datetime import datetime

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WORKFLOW_STAGES = [
    {'name': '创意验证', 'duration': '2-4 周', 'skills': ['founder', 'business-model-canvas']},
    {'name': '市场调研', 'duration': '2-3 周', 'skills': ['market-research-reports', 'competitive-analysis']},
    {'name': '商业规划', 'duration': '2-3 周', 'skills': ['business-plan', 'business-model-canvas']},
    {'name': '产品开发', 'duration': '4-8 周', 'skills': ['startup']},
    {'name': '产品市场匹配', 'duration': '4-12 周', 'skills': ['founder', 'founder-coach']},
    {'name': '融资路演', 'duration': '4-8 周', 'skills': ['pitch-deck-visuals', 'business-plan']}
]

STARTUP_STAGES = {
    'idea': {
        'name': '创意阶段',
        'focus': '问题验证',
        'metrics': ['用户访谈数', '问题验证度'],
        'duration': '2-4 周',
        'priority': '学习速度'
    },
    'pre-pmf': {
        'name': '产品市场匹配前',
        'focus': 'PMF 验证',
        'metrics': ['留存率', '40% 阈值', '用户反馈'],
        'duration': '3-6 个月',
        'priority': '学习速度'
    },
    'pmf': {
        'name': '产品市场匹配',
        'focus': '增长验证',
        'metrics': ['月增长率', 'LTV/CAC', '推荐率'],
        'duration': '2-3 个月',
        'priority': '增长效率'
    },
    'post-pmf': {
        'name': '产品市场匹配后',
        'focus': '规模化',
        'metrics': ['收入增长', '市场份额', '团队效率'],
        'duration': '6-12 个月',
        'priority': '规模化效率'
    },
    'scaling': {
        'name': '规模化阶段',
        'focus': '市场扩张',
        'metrics': ['市场份额', '利润率', '组织效率'],
        'duration': '12+ 个月',
        'priority': '可持续增长'
    }
}

CORE_FRAMEWORKS = [
    {'name': '精益创业', 'core': '构建 - 测量 - 学习', 'concept': 'MVP + 快速迭代'},
    {'name': '商业模式画布', 'core': '9+1 模块', 'concept': '价值创造 + 价值捕获'},
    {'name': '4Ps 框架', 'core': 'Persona/Problem/Promise/Product', 'concept': '摆脱困境'},
    {'name': 'PMF 测量', 'core': '40% 用户非常失望', 'concept': 'Sean Ellis Test'}
]

COMMON_TRAPS = {
    'pre-pmf': [
        '留存率有问题时还在构建功能',
        '在创始人不堪重负前就招聘',
        '在产品市场匹配前优化收入',
        '在销售流程可重复前规模化销售',
        '在分销有效前在品牌上花钱'
    ],
    'post-pmf': [
        '增长过快导致质量下降',
        '忽视单位经济',
        '团队建设跟不上业务增长',
        '忽视现金流管理',
        '过早多元化'
    ]
}

def print_stage(stage_num, stage_info):
    """打印阶段信息"""
    print(f"\n阶段 {stage_num}: {stage_info['name']} ({stage_info['duration']})")
    print(f"  使用技能：{', '.join(stage_info['skills'])}")

def print_startup_stage(stage_key, stage_info):
    """打印创业阶段信息"""
    print(f"\n{stage_info['name']} ({stage_key})")
    print(f"  焦点：{stage_info['focus']}")
    print(f"  关键指标：{', '.join(stage_info['metrics'])}")
    print(f"  持续时间：{stage_info['duration']}")
    print(f"  优先级：{stage_info['priority']}")

def startup_0_to_1_workflow(stage=None, action='overview'):
    """从 0 到 1 创业工作流"""
    print("="*70)
    print("从 0 到 1 创业工作流")
    print("="*70)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if action == 'overview':
        # 显示 6 个工作流阶段
        print("\n" + "="*70)
        print("创业工作流 - 6 个阶段")
        print("="*70)
        for i, stage_info in enumerate(WORKFLOW_STAGES, 1):
            print_stage(i, stage_info)
        
        # 显示 5 个创业阶段
        print("\n" + "="*70)
        print("创业阶段 - 5 个阶段")
        print("="*70)
        for key, info in STARTUP_STAGES.items():
            print_startup_stage(key, info)
        
        # 显示核心框架
        print("\n" + "="*70)
        print("核心框架")
        print("="*70)
        for framework in CORE_FRAMEWORKS:
            print(f"\n{framework['name']}")
            print(f"  核心：{framework['core']}")
            print(f"  概念：{framework['concept']}")
        
        # 显示常见陷阱
        print("\n" + "="*70)
        print("常见陷阱")
        print("="*70)
        for stage_key, traps in COMMON_TRAPS.items():
            print(f"\n{STARTUP_STAGES[stage_key]['name']}:")
            for trap in traps:
                print(f"  ⚠️  {trap}")
        
        print("\n" + "="*70)
        print(f"完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
    
    elif action == 'assess':
        # 阶段评估
        if stage and stage in STARTUP_STAGES:
            stage_info = STARTUP_STAGES[stage]
            print(f"\n当前阶段：{stage_info['name']}")
            print(f"焦点：{stage_info['focus']}")
            print(f"优先级：{stage_info['priority']}")
            print(f"\n关键指标:")
            for metric in stage_info['metrics']:
                print(f"  - {metric}")
        else:
            print("请指定有效阶段：idea, pre-pmf, pmf, post-pmf, scaling")
    
    elif action == 'tasks':
        # 任务清单
        if stage and stage in STARTUP_STAGES:
            stage_info = STARTUP_STAGES[stage]
            print(f"\n{stage_info['name']} - 核心任务")
            print("-"*70)
            
            tasks = {
                'idea': [
                    '完成 20+ 用户访谈',
                    '验证问题真实性',
                    '完成商业模式画布',
                    '设计 MVP 方案'
                ],
                'pre-pmf': [
                    '开发 MVP',
                    '获取前 100 个用户',
                    '每周用户访谈',
                    '快速迭代产品'
                ],
                'pmf': [
                    '验证 PMF (Sean Ellis Test)',
                    '优化获客渠道',
                    '建立增长模型',
                    '准备融资材料'
                ],
                'post-pmf': [
                    '规模化获客',
                    '团队建设',
                    '流程优化',
                    'A/B 轮融资'
                ],
                'scaling': [
                    '市场扩张',
                    '产品线扩展',
                    '组织建设',
                    'C 轮 + 融资'
                ]
            }
            
            for i, task in enumerate(tasks.get(stage, []), 1):
                print(f"  [ ] {i}. {task}")
        else:
            print("请指定有效阶段：idea, pre-pmf, pmf, post-pmf, scaling")
    
    print("\n✅ 创业工作流分析完成！")
    print("\n建议执行步骤：")
    print("1. 阶段 1: 使用 founder 进行问题验证")
    print("2. 阶段 2: 使用 market-research-reports 进行市场调研")
    print("3. 阶段 3: 使用 business-plan 制定商业计划")
    print("4. 阶段 4: 使用 startup 编排产品开发")
    print("5. 阶段 5: 使用 founder-coach 进行 PMF 验证")
    print("6. 阶段 6: 使用 pitch-deck-visuals 准备融资路演")

if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else None
    action = sys.argv[2] if len(sys.argv) > 2 else 'overview'
    
    startup_0_to_1_workflow(stage, action)
