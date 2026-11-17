#!/usr/bin/env python3
"""
精益六西格玛项目规划生成器

根据用户输入的项目参数，生成标准化的DMAIC或DMADV项目规划文档。

使用方法:
    python scripts/generate_plan.py --methodology dmaic --industry manufacturing --scope "降低产品不良率"
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

def generate_dmaic_plan(industry, scope):
    """生成DMAIC项目规划"""
    
    start_date = datetime.now()
    
    # 各阶段时长(周)
    phase_durations = {
        'D': 3,
        'M': 6,
        'A': 6,
        'I': 8,
        'C': 4
    }
    
    current_date = start_date
    
    phases = []
    for phase in ['D', 'M', 'A', 'I', 'C']:
        phase_end = current_date + timedelta(weeks=phase_durations[phase])
        phases.append({
            'phase': phase,
            'name': get_phase_name(phase),
            'start': current_date.strftime('%Y-%m-%d'),
            'end': phase_end.strftime('%Y-%m-%d'),
            'duration_weeks': phase_durations[phase],
            'tasks': get_phase_tasks(phase, industry),
            'tools': get_phase_tools(phase),
            'deliverables': get_phase_deliverables(phase)
        })
        current_date = phase_end + timedelta(days=1)
    
    team_roles = [
        {'role': 'Champion', 'responsibility': '战略支持与资源协调', 'time_commitment': '2-4小时/周'},
        {'role': 'Sponsor', 'responsibility': '业务支持与项目推进', 'time_commitment': '4-6小时/周'},
        {'role': 'Black Belt', 'responsibility': '方法论指导与项目执行', 'time_commitment': '50%时间'},
        {'role': 'Green Belt', 'responsibility': '项目负责人与团队协调', 'time_commitment': '30%时间'},
        {'role': 'Team Member', 'responsibility': '数据分析与方案实施', 'time_commitment': '20%时间'}
    ]
    
    total_weeks = sum(d['duration_weeks'] for d in phases)
    
    return {
        'project_type': 'DMAIC改进项目',
        'industry': industry,
        'scope': scope,
        'total_duration_weeks': total_weeks,
        'phases': phases,
        'team_roles': team_roles,
        'success_criteria': get_success_criteria(industry),
        'key_metrics': get_key_metrics(industry),
        'recommendations': get_industry_recommendations(industry)
    }

def generate_dmadv_plan(industry, scope):
    """生成DMADV项目规划"""
    
    start_date = datetime.now()
    
    # DMADV各阶段时长(周)
    phase_durations = {
        'D': 4,
        'M': 6,
        'A': 8,
        'D_design': 10,
        'V': 6
    }
    
    current_date = start_date
    
    phases = []
    for phase in ['D', 'M', 'A', 'D_design', 'V']:
        phase_end = current_date + timedelta(weeks=phase_durations[phase])
        phase_name = 'D(设计)' if phase == 'D_design' else get_phase_name(phase)
        phases.append({
            'phase': phase if phase != 'D_design' else 'D',
            'phase_full': phase_name,
            'start': current_date.strftime('%Y-%m-%d'),
            'end': phase_end.strftime('%Y-%m-%d'),
            'duration_weeks': phase_durations[phase],
            'tasks': get_dmadv_phase_tasks(phase, industry),
            'tools': get_dmadv_phase_tools(phase),
            'deliverables': get_dmadv_phase_deliverables(phase)
        })
        current_date = phase_end + timedelta(days=1)
    
    team_roles = [
        {'role': 'Champion', 'responsibility': '战略支持与资源协调', 'time_commitment': '2-4小时/周'},
        {'role': 'Design Sponsor', 'responsibility': '设计决策与业务对齐', 'time_commitment': '6-8小时/周'},
        {'role': 'Black Belt', 'responsibility': 'DFSS方法论指导', 'time_commitment': '80%时间'},
        {'role': 'Green Belt', 'responsibility': '项目协调与执行', 'time_commitment': '50%时间'},
        {'role': 'Technical Lead', 'responsibility': '技术方案设计', 'time_commitment': '60%时间'},
        {'role': 'Team Member', 'responsibility': '需求分析与验证', 'time_commitment': '30%时间'}
    ]
    
    total_weeks = sum(d['duration_weeks'] for d in phases)
    
    return {
        'project_type': 'DMADV设计项目',
        'industry': industry,
        'scope': scope,
        'total_duration_weeks': total_weeks,
        'phases': phases,
        'team_roles': team_roles,
        'success_criteria': get_dmadv_success_criteria(industry),
        'key_metrics': get_key_metrics(industry),
        'recommendations': get_industry_recommendations(industry)
    }

def get_phase_name(phase):
    names = {
        'D': 'Define(定义)',
        'M': 'Measure(测量)',
        'A': 'Analyze(分析)',
        'I': 'Improve(改进)',
        'C': 'Control(控制)'
    }
    return names.get(phase, phase)

def get_phase_tasks(phase, industry):
    tasks_by_phase = {
        'D': [
            '问题陈述编写',
            '项目章程制定',
            'SIPOC图绘制',
            '团队组建与职责分工',
            'VOC/VOB分析',
            '项目启动会议'
        ],
        'M': [
            '数据收集计划制定',
            '测量系统分析(MSA)',
            '数据收集执行',
            '过程能力分析',
            '基线建立',
            'Y-X映射'
        ],
        'A': [
            '鱼骨图分析',
            '5Why分析',
            'Pareto分析',
            '假设检验',
            '相关性分析',
            '根本原因确定'
        ],
        'I': [
            '方案生成(头脑风暴)',
            '方案评估与筛选',
            'FMEA风险分析',
            '试点方案设计',
            '试点实施与验证',
            '全面实施方案'
        ],
        'C': [
            '控制计划制定',
            'SPC控制图建立',
            'SOP标准化',
            '团队培训',
            '项目验收',
            '经验总结与分享'
        ]
    }
    return tasks_by_phase.get(phase, [])

def get_phase_tools(phase):
    tools_by_phase = {
        'D': ['问题陈述模板', 'SIPOC图', '项目章程模板', 'VOC分析'],
        'M': ['数据收集表', 'MSA模板', '直方图', '箱线图', '过程能力报告'],
        'A': ['鱼骨图', '5Why分析表', 'Pareto图', '散点图', '假设检验'],
        'I': ['FMEA模板', '决策矩阵', 'PDCA模板', 'DOE设计'],
        'C': ['控制图模板', '控制计划表', 'SPC系统', '检查清单']
    }
    return tools_by_phase.get(phase, [])

def get_phase_deliverables(phase):
    deliverables_by_phase = {
        'D': ['问题陈述文档', '项目章程', 'SIPOC图', '团队名单'],
        'M': ['数据收集计划', 'MSA报告', '基线数据报告', '过程能力报告'],
        'A': ['因果分析图', '根因分析报告', '关键因子清单', '统计验证报告'],
        'I': ['改进方案', 'FMEA报告', '试点结果', '实施计划'],
        'C': ['控制计划', '控制限文档', 'SOP文件', '项目总结报告']
    }
    return deliverables_by_phase.get(phase, [])

def get_dmadv_phase_tasks(phase, industry):
    tasks_by_phase = {
        'D': [
            'VOC/VOB收集',
            '设计需求文档(DRD)',
            'CTQ树构建',
            '项目章程制定',
            '团队组建'
        ],
        'M': [
            '技术能力评估',
            '风险初步分析',
            'Benchmark分析',
            '差距分析',
            '能力基线建立'
        ],
        'A': [
            '功能分解',
            '概念方案生成',
            '概念评估筛选',
            '概念选择决策',
            'Pugh矩阵分析'
        ],
        'D_design': [
            '详细技术设计',
            'DFMEA分析',
            'CAD/工艺设计',
            '原型设计',
            '设计评审'
        ],
        'V': [
            '原型测试',
            '设计验证',
            '试点实施',
            '客户验收',
            '项目收尾'
        ]
    }
    return tasks_by_phase.get(phase, [])

def get_dmadv_phase_tools(phase):
    tools_by_phase = {
        'D': ['VOC分析', 'QFD(质量屋)', 'CTQ树', '项目章程'],
        'M': ['能力矩阵', 'FMEA', 'Benchmark分析'],
        'A': ['TRIZ', 'Pugh矩阵', '功能分析', '概念草图'],
        'D_design': ['DFMEA', 'CAD软件', '仿真工具', '设计规范'],
        'V': ['测试计划', '验收标准', '控制计划']
    }
    return tools_by_phase.get(phase, [])

def get_dmadv_phase_deliverables(phase):
    deliverables_by_phase = {
        'D': ['设计需求文档', 'CTQ分解', '项目章程'],
        'M': ['能力评估报告', '风险清单', 'Benchmark报告'],
        'A': ['概念方案(3个+)', '评估报告', '概念选择报告'],
        'D_design': ['详细设计文档', 'DFMEA报告', '原型样件'],
        'V': ['验证报告', '设计释放文档', '控制计划']
    }
    return deliverables_by_phase.get(phase, [])

def get_success_criteria(industry):
    criteria = {
        'manufacturing': [
            '过程能力Cpk >= 1.33',
            '不良率降低50%以上',
            '返工成本降低30%以上',
            '改善成果维持6个月以上'
        ],
        'service': [
            '处理时间缩短30%以上',
            '客户满意度提升15%以上',
            '错误率降低50%以上',
            '流程效率提升25%以上'
        ],
        'healthcare': [
            '患者等待时间缩短30%以上',
            '医疗错误率降低50%以上',
            '床位周转率提升20%以上',
            '患者满意度提升15%以上'
        ],
        'finance': [
            '处理时间缩短40%以上',
            '错误率降低60%以上',
            '客户投诉率降低50%以上',
            '合规达标率100%'
        ]
    }
    return criteria.get(industry, criteria['manufacturing'])

def get_dmadv_success_criteria(industry):
    criteria = {
        'manufacturing': [
            '设计能力Cpk >= 1.67',
            '初期不良率<1%',
            '一次通过率>90%',
            '成本降低20%以上'
        ],
        'service': [
            '新服务客户满意度>90%',
            '处理效率提升40%以上',
            '设计可扩展性达标',
            '运营成本优化20%以上'
        ],
        'healthcare': [
            '患者安全指标100%达标',
            '治疗效果提升20%以上',
            '流程合规性100%',
            '患者体验评分>90%'
        ],
        'finance': [
            '新系统错误率<0.1%',
            '处理能力提升50%以上',
            '合规性100%',
            '成本效益达标'
        ]
    }
    return criteria.get(industry, criteria['manufacturing'])

def get_key_metrics(industry):
    metrics = {
        'manufacturing': ['不良率(DPU)', '过程能力(Cpk)', '设备综合效率(OEE)', '返工成本'],
        'service': ['处理时间', '首次解决率', '客户满意度', '错误率'],
        'healthcare': ['等待时间', '诊断准确率', '感染率', '患者满意度'],
        'finance': ['处理时间', '准确率', '客户满意度', '合规率']
    }
    return metrics.get(industry, metrics['manufacturing'])

def get_industry_recommendations(industry):
    recommendations = {
        'manufacturing': [
            '充分利用设备数据采集系统',
            '重视测量系统分析(MSA)',
            '关注防错设计(Poka-Yoke)',
            '建立标准化的SPC控制机制'
        ],
        'service': [
            '重视客户声音(VOC)收集',
            '消除等待时间是关键',
            '关注员工培训与激励',
            '建立服务标准(SLA)'
        ],
        'healthcare': [
            '患者安全永远是第一位',
            '建立跨部门协作机制',
            '注重流程标准化与合规',
            '平衡效率与质量'
        ],
        'finance': [
            '严格遵守监管合规要求',
            '重视数据安全与隐私',
            '确保系统稳定性',
            '建立审计追踪机制'
        ]
    }
    return recommendations.get(industry, recommendations['manufacturing'])

def main():
    parser = argparse.ArgumentParser(description='精益六西格玛项目规划生成器')
    parser.add_argument('--methodology', choices=['dmaic', 'dmadv'], required=True,
                        help='选择方法论: dmaic(改进) 或 dmadv(设计)')
    parser.add_argument('--industry', choices=['manufacturing', 'service', 'healthcare', 'finance'],
                        required=True, help='行业类型')
    parser.add_argument('--scope', required=True, help='项目范围/目标描述')
    
    args = parser.parse_args()
    
    if args.methodology == 'dmaic':
        result = generate_dmaic_plan(args.industry, args.scope)
    else:
        result = generate_dmadv_plan(args.industry, args.scope)
    
    # 输出JSON格式结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 输出可读格式摘要
    print("\n" + "="*60)
    print("项目规划摘要")
    print("="*60)
    print(f"项目类型: {result['project_type']}")
    print(f"项目范围: {result['scope']}")
    print(f"行业类型: {result['industry']}")
    print(f"预计周期: {result['total_duration_weeks']} 周")
    print("\n阶段计划:")
    for phase in result['phases']:
        full_name = phase.get('phase_full', get_phase_name(phase['phase']))
        print(f"  {full_name}: {phase['start']} ~ {phase['end']} ({phase['duration_weeks']}周)")
    print("\n关键指标:")
    for metric in result['key_metrics']:
        print(f"  - {metric}")
    print("\n成功标准:")
    for criterion in result['success_criteria']:
        print(f"  - {criterion}")

if __name__ == "__main__":
    main()
