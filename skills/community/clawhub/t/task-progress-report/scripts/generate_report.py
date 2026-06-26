#!/usr/bin/env python3
"""
任务进展报告生成脚本
用于生成格式化的任务进展报告
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

REPORT_DIR = Path("/root/.openclaw/workspace/reports/progress")
REPORT_FILE = REPORT_DIR / "task_progress_report.md"

def ensure_report_dir():
    """确保报告目录存在"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

def format_short_message(task_name: str, progress: str, completed: str, 
                        current: str, estimate: str, advice: str = "") -> str:
    """生成简短汇报消息"""
    lines = [
        f"【任务进展 {progress}】",
        f"✅ 已完成：{completed}",
        f"🔄 正在：{current}",
        f"⏱️ 预计：{estimate}",
    ]
    if advice:
        lines.append(f"💡 建议：{advice}")
    
    lines.append(f"\n📄 详细报告：{REPORT_FILE}")
    return "\n".join(lines)

def update_detailed_report(task_name: str, data: dict):
    """更新详细报告文件（追加模式）"""
    ensure_report_dir()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""
---
更新时间: {timestamp}

## 任务: {task_name}

### 当前状态
- 进度: {data.get('progress', 'N/A')}
- 状态: {data.get('status', '正常')}
- 已用时间: {data.get('elapsed', 'N/A')}
- 预计剩余: {data.get('remaining', 'N/A')}

### 已完成
{data.get('completed', '- 无')}

### 正在进行
{data.get('current', '- 无')}

### 关键指标
"""
    
    # 添加指标
    metrics = data.get('metrics', {})
    if metrics:
        for key, value in metrics.items():
            content += f"- {key}: {value}\n"
    else:
        content += "- 暂无指标记录\n"
    
    # 添加问题和建议
    if data.get('issues'):
        content += "\n### 问题与建议\n"
        for issue in data['issues']:
            content += f"- ⚠️ {issue}\n"
    
    if data.get('advice'):
        content += f"\n### 行动建议\n{data['advice']}\n"
    
    content += "\n---\n"
    
    # 追加到文件
    with open(REPORT_FILE, 'a', encoding='utf-8') as f:
        f.write(content)
    
    return REPORT_FILE

def generate_summary_report():
    """生成最终总结报告"""
    ensure_report_dir()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    summary = f"""# 任务执行总结报告

生成时间: {timestamp}

## 执行概况
本报告汇总了任务执行的完整进展记录。

## 查看详细进展
请查看本目录下的历史记录或上文的详细日志。

## 报告文件位置
{REPORT_FILE}

---
*由 task-progress-report 技能自动生成*
"""
    
    summary_file = REPORT_DIR / "task_summary.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    return summary_file

def main():
    parser = argparse.ArgumentParser(description='生成任务进展报告')
    parser.add_argument('--task-name', required=True, help='任务名称')
    parser.add_argument('--progress', required=True, help='当前进度 (如: 3/10 或 50%)')
    parser.add_argument('--status', default='正常', help='任务状态')
    parser.add_argument('--completed', default='', help='已完成工作简述')
    parser.add_argument('--current', default='', help='当前进行的工作')
    parser.add_argument('--elapsed', default='', help='已用时间')
    parser.add_argument('--remaining', default='', help='预计剩余时间')
    parser.add_argument('--advice', default='', help='建议')
    parser.add_argument('--summary', action='store_true', help='生成总结报告')
    
    args = parser.parse_args()
    
    if args.summary:
        summary_file = generate_summary_report()
        print(f"总结报告已生成: {summary_file}")
        return
    
    # 构建数据
    data = {
        'progress': args.progress,
        'status': args.status,
        'completed': args.completed,
        'current': args.current,
        'elapsed': args.elapsed,
        'remaining': args.remaining,
        'advice': args.advice,
    }
    
    # 更新详细报告
    report_path = update_detailed_report(args.task_name, data)
    
    # 输出简短消息（用于发送给用户）
    short_msg = format_short_message(
        task_name=args.task_name,
        progress=args.progress,
        completed=args.completed or "阶段性工作",
        current=args.current or "执行中",
        estimate=args.remaining or "计算中...",
        advice=args.advice
    )
    
    print(short_msg)
    print(f"\n详细报告已更新: {report_path}")

if __name__ == '__main__':
    main()
