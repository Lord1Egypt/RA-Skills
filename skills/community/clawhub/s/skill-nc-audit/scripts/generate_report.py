#!/usr/bin/env python3
"""
审核结论生成脚本
功能:汇总不符合项统计数据,生成系统性改进建议
"""
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import Counter

DATA_FILE = Path(__file__).parent.parent / "assets" / "nc_data.json"

def load_data():
    """加载数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"non_conformances": [], "audit_ids": []}

def calculate_statistics(data, audit_id=None):
    """计算统计数据"""
    nc_list = data.get('non_conformances', [])
    
    # 按审核ID筛选
    if audit_id:
        nc_list = [nc for nc in nc_list if nc['audit_info']['audit_id'] == audit_id]
    
    if not nc_list:
        return None
    
    stats = {
        "total_nc": len(nc_list),
        "by_category": Counter(nc['category'] for nc in nc_list),
        "by_status": Counter(nc['verification']['status'] for nc in nc_list),
        "by_clause": Counter(nc['clause'] for nc in nc_list),
        "by_auditor": Counter(nc['audit_info']['auditor'] for nc in nc_list if nc['audit_info']['auditor']),
        "clause_distribution": {},
        "closure_rate": 0,
        "major_rate": 0
    }
    
    # 计算条款分布
    for clause, count in stats['by_clause'].items():
        prefix = clause.split('.')[0] if '.' in clause else clause
        stats['clause_distribution'][prefix] = stats['clause_distribution'].get(prefix, 0) + count
    
    # 计算比率
    if stats['total_nc'] > 0:
        stats['closure_rate'] = round(stats['by_status'].get('closed', 0) / stats['total_nc'] * 100, 1)
        stats['major_rate'] = round(stats['by_category'].get('major', 0) / stats['total_nc'] * 100, 1)
    
    return stats

def generate_improvement_suggestions(stats):
    """生成系统性改进建议"""
    suggestions = []
    
    # 基于严重不符合的建议
    if stats.get('major', 0) > 0:
        suggestions.append(f"关注{stats['major']}项严重不符合项,需重点跟踪整改效果")
    
    # 基于条款分布的建议
    if stats['clause_distribution']:
        top_clause = max(stats['clause_distribution'].items(), key=lambda x: x[1])
        suggestions.append(f"条款{top_clause[0]}类问题最多({top_clause[1]}项),建议审查该领域流程")
    
    # 基于关闭率的建议
    if stats['closure_rate'] < 50:
        suggestions.append(f"不符合项关闭率仅{stats['closure_rate']}%,需加快整改进度")
    elif stats['closure_rate'] == 100:
        suggestions.append("所有不符合项已关闭,体系运行良好")
    
    # 基于状态分布的建议
    open_count = stats['by_status'].get('open', 0)
    in_progress = stats['by_status'].get('in_progress', 0)
    if open_count > 0:
        suggestions.append(f"仍有{open_count}项不符合项未启动整改")
    if in_progress > 0:
        suggestions.append(f"{in_progress}项正在进行整改验证")
    
    return suggestions

def generate_report(audit_id, stats_only=False):
    """生成审核结论报告"""
    data = load_data()
    stats = calculate_statistics(data, audit_id)
    
    if not stats:
        return {
            "status": "error",
            "message": f"未找到审核ID为{audit_id}的记录"
        }
    
    result = {
        "status": "success",
        "audit_id": audit_id,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "statistics": {
            "不符合项总数": stats['total_nc'],
            "按类别分布": dict(stats['by_category']),
            "按状态分布": dict(stats['by_status']),
            "按条款分布": dict(stats['by_clause']),
            "条款分布(大类)": stats['clause_distribution'],
            "关闭率": f"{stats['closure_rate']}%",
            "严重不符合占比": f"{stats['major_rate']}%"
        }
    }
    
    if not stats_only:
        suggestions = generate_improvement_suggestions(stats)
        
        # 生成详细报告文本
        report_text = f"""
================================================================================
                          内审不符合项统计分析报告
================================================================================
审核编号: {audit_id}
报告日期: {datetime.now().strftime("%Y-%m-%d")}

【一、总体统计】
不符合项总数: {stats['total_nc']} 项
严重不符合: {stats['by_category'].get('major', 0)} 项
轻微不符合: {stats['by_category'].get('minor', 0)} 项
观察项: {stats['by_category'].get('observation', 0)} 项

【二、验证状态】
待处理(Open): {stats['by_status'].get('open', 0)} 项
处理中(In Progress): {stats['by_status'].get('in_progress', 0)} 项
已验证(Verified): {stats['by_status'].get('verified', 0)} 项
已关闭(Closed): {stats['by_status'].get('closed', 0)} 项
整体关闭率: {stats['closure_rate']}%

【三、条款分布(前10)】
"""
        for clause, count in stats['by_clause'].most_common(10):
            report_text += f"  {clause}: {count} 项\n"
        
        report_text += """
【四、系统性改进建议】
"""
        for i, suggestion in enumerate(suggestions, 1):
            report_text += f"  {i}. {suggestion}\n"
        
        report_text += """
================================================================================
                                  报告结束
================================================================================
"""
        result['report_text'] = report_text
        result['suggestions'] = suggestions
    
    return result

def main():
    parser = argparse.ArgumentParser(description='生成审核结论报告')
    parser.add_argument('--audit-id', required=True, help='审核ID')
    parser.add_argument('--stats-only', action='store_true', help='仅输出统计数据')
    
    args = parser.parse_args()
    result = generate_report(args.audit_id, args.stats_only)
    
    if result['status'] == 'error':
        print(json.dumps(result, ensure_ascii=False))
    elif args.stats_only:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result['report_text'])
        print(json.dumps({
            "statistics": result['statistics'],
            "suggestions": result['suggestions']
        }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
