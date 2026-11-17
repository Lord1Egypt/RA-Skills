#!/usr/bin/env python3
"""
甘特图生成脚本
生成交互式HTML甘特图，展示APQP项目进度
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from jinja2 import Template

# 甘特图HTML模板
GANTT_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APQP项目甘特图 - {{ project_name }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .header .meta {
            display: flex;
            gap: 30px;
            font-size: 14px;
            opacity: 0.9;
        }
        
        .progress-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        
        .progress-card h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .progress-bar {
            height: 24px;
            background: #e9ecef;
            border-radius: 12px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-size: 12px;
            font-weight: 600;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .stat-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        
        .gantt-container {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            overflow-x: auto;
        }
        
        .gantt-header {
            display: flex;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        
        .gantt-task-name {
            width: 200px;
            flex-shrink: 0;
            font-weight: 600;
            color: #333;
        }
        
        .gantt-timeline {
            flex: 1;
            display: flex;
            min-width: 800px;
        }
        
        .gantt-day {
            flex: 1;
            text-align: center;
            font-size: 10px;
            color: #999;
            border-left: 1px solid #f0f0f0;
        }
        
        .gantt-day.weekend {
            background: #f8f9fa;
        }
        
        .gantt-day.today {
            background: #fff3cd;
            color: #856404;
            font-weight: 600;
        }
        
        .gantt-row {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            position: relative;
        }
        
        .gantt-task {
            width: 200px;
            flex-shrink: 0;
            font-size: 13px;
            color: #333;
            padding-right: 10px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .gantt-bar-container {
            flex: 1;
            display: flex;
            min-width: 800px;
            position: relative;
            height: 30px;
        }
        
        .gantt-bar {
            position: absolute;
            height: 24px;
            top: 3px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 11px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        .gantt-bar:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        
        .gantt-bar.completed {
            background: linear-gradient(90deg, #28a745, #20c997);
        }
        
        .gantt-bar.in-progress {
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .gantt-bar.pending {
            background: linear-gradient(90deg, #adb5bd, #ced4da);
        }
        
        .gantt-bar.milestone {
            width: 20px !important;
            height: 20px;
            border-radius: 50%;
            background: #ffc107;
            border: 3px solid #fff;
            box-shadow: 0 2px 8px rgba(255,193,7,0.5);
        }
        
        .gantt-marker {
            position: absolute;
            width: 2px;
            height: 100%;
            background: #dc3545;
            z-index: 10;
        }
        
        .gantt-marker::after {
            content: '今日';
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 10px;
            color: #dc3545;
            white-space: nowrap;
        }
        
        .legend {
            display: flex;
            gap: 20px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: #666;
        }
        
        .legend-color {
            width: 20px;
            height: 12px;
            border-radius: 3px;
        }
        
        .legend-color.completed { background: linear-gradient(90deg, #28a745, #20c997); }
        .legend-color.in-progress { background: linear-gradient(90deg, #667eea, #764ba2); }
        .legend-color.pending { background: linear-gradient(90deg, #adb5bd, #ced4da); }
        .legend-color.milestone { 
            width: 12px; 
            height: 12px; 
            border-radius: 50%; 
            background: #ffc107; 
        }
        
        .phase-group {
            margin-bottom: 20px;
        }
        
        .phase-title {
            font-size: 16px;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 10px;
            padding-left: 10px;
            border-left: 4px solid #667eea;
        }
        
        .milestone-marker {
            position: absolute;
            top: 50%;
            transform: translate(-50%, -50%);
            width: 30px;
            height: 30px;
            background: #ffc107;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: #333;
            font-weight: bold;
            box-shadow: 0 2px 8px rgba(255,193,7,0.5);
        }
        
        .tooltip {
            position: absolute;
            background: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            z-index: 100;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
        }
        
        .tooltip.visible {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ project_name }}</h1>
            <div class="meta">
                <span>开始日期: {{ start_date }}</span>
                <span>目标SOP: {{ sop_date }}</span>
                <span>总工期: {{ total_days }}天</span>
            </div>
        </div>
        
        <div class="progress-card">
            <h3>项目整体进度</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{ overall_progress }}%;">{{ overall_progress }}%</div>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{{ completed_tasks }}</div>
                    <div class="stat-label">已完成任务</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ in_progress_tasks }}</div>
                    <div class="stat-label">进行中</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ pending_tasks }}</div>
                    <div class="stat-label">待开始</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ days_remaining }}</div>
                    <div class="stat-label">剩余天数</div>
                </div>
            </div>
        </div>
        
        <div class="gantt-container">
            <div class="gantt-header">
                <div class="gantt-task-name">任务名称</div>
                <div class="gantt-timeline">
                    {% for day in timeline_days %}
                    <div class="gantt-day {% if day.is_weekend %}weekend{% endif %} {% if day.is_today %}today{% endif %}">{{ day.day }}</div>
                    {% endfor %}
                </div>
            </div>
            
            {% for phase in phases %}
            <div class="phase-group">
                <div class="phase-title">{{ phase.name }}</div>
                {% for task in phase.tasks %}
                <div class="gantt-row">
                    <div class="gantt-task" title="{{ task.name }}">{{ task.name }}</div>
                    <div class="gantt-bar-container">
                        {% if task.type == 'milestone' %}
                        <div class="gantt-bar milestone" style="left: {{ task.start_percent }}%;" title="{{ task.name }}"></div>
                        {% else %}
                        <div class="gantt-bar {{ task.status }}" 
                             style="left: {{ task.start_percent }}%; width: {{ task.width_percent }}%;" 
                             title="{{ task.name }}&#10;开始: {{ task.start }}&#10;结束: {{ task.end }}&#10;进度: {{ task.progress }}%">
                            {% if task.width_percent > 15 %}{{ task.progress }}%{% endif %}
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
            
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color completed"></div>
                    <span>已完成</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color in-progress"></div>
                    <span>进行中</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color pending"></div>
                    <span>待开始</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color milestone"></div>
                    <span>里程碑</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="tooltip" id="tooltip"></div>
</body>
</html>
"""


def calculate_gantt_data(start_date, sop_date, phases):
    """计算甘特图数据"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(sop_date, "%Y-%m-%d")
    total_days = (end - start).days
    
    today = datetime.now()
    
    # 生成时间轴
    timeline_days = []
    for i in range(total_days + 1):
        current = start + timedelta(days=i)
        timeline_days.append({
            "day": current.day if i % 7 == 0 else "",
            "is_weekend": current.weekday() >= 5,
            "is_today": current.date() == today.date()
        })
    
    # 处理每个阶段的任务
    processed_phases = []
    completed_tasks = 0
    in_progress_tasks = 0
    pending_tasks = 0
    total_tasks = 0
    
    for phase in phases:
        processed_tasks = []
        for task in phase.get("tasks", []):
            task_start = datetime.strptime(task["start"], "%Y-%m-%d")
            task_end = datetime.strptime(task["end"], "%Y-%m-%d")
            
            start_percent = (task_start - start).days / total_days * 100
            duration_days = (task_end - task_start).days + 1
            width_percent = duration_days / total_days * 100
            
            # 计算进度
            if task_end < today:
                status = "completed"
                progress = 100
                completed_tasks += 1
            elif task_start > today:
                status = "pending"
                progress = 0
                pending_tasks += 1
            else:
                status = "in-progress"
                elapsed = (today - task_start).days
                progress = min(100, int(elapsed / duration_days * 100))
                in_progress_tasks += 1
            
            total_tasks += 1
            
            processed_tasks.append({
                "name": task["name"],
                "start": task["start"],
                "end": task["end"],
                "start_percent": max(0, start_percent),
                "width_percent": max(2, width_percent),
                "progress": progress,
                "status": status,
                "type": task.get("type", "task")
            })
        
        processed_phases.append({
            "name": phase["name"],
            "tasks": processed_tasks
        })
    
    # 计算剩余天数
    days_remaining = max(0, (end - today).days)
    
    # 计算整体进度
    overall_progress = int((completed_tasks + in_progress_tasks * 0.5) / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        "timeline_days": timeline_days,
        "phases": processed_phases,
        "total_days": total_days,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "pending_tasks": pending_tasks,
        "days_remaining": days_remaining,
        "overall_progress": overall_progress
    }


def generate_gantt(args):
    """生成甘特图HTML"""
    
    # 解析日期
    start_date = args.start_date
    sop_date = args.sop_date
    
    # 如果没有提供阶段数据，生成默认APQP五阶段
    if not args.phases:
        default_phases = [
            {
                "name": "阶段1: 策划与定义",
                "tasks": [
                    {"name": "项目立项与章程", "start": start_date, "end": _date_add(start_date, 14)},
                    {"name": "多方论证会议", "start": _date_add(start_date, 7), "end": _date_add(start_date, 21)},
                    {"name": "QFD质量功能展开", "start": _date_add(start_date, 14), "end": _date_add(start_date, 35)},
                    {"name": "初始BOM建立", "start": _date_add(start_date, 28), "end": _date_add(start_date, 42)},
                    {"name": "阶段1评审", "start": _date_add(start_date, 42), "end": _date_add(start_date, 42), "type": "milestone"}
                ]
            },
            {
                "name": "阶段2: 产品设计开发",
                "tasks": [
                    {"name": "概念设计", "start": _date_add(start_date, 42), "end": _date_add(start_date, 70)},
                    {"name": "DFMEA编制", "start": _date_add(start_date, 56), "end": _date_add(start_date, 98)},
                    {"name": "设计验证DVP&R", "start": _date_add(start_date, 84), "end": _date_add(start_date, 112)},
                    {"name": "样件制作", "start": _date_add(start_date, 98), "end": _date_add(start_date, 140)},
                    {"name": "阶段2评审(DR)", "start": _date_add(start_date, 112), "end": _date_add(start_date, 112), "type": "milestone"}
                ]
            },
            {
                "name": "阶段3: 过程设计开发",
                "tasks": [
                    {"name": "工艺流程设计", "start": _date_add(start_date, 112), "end": _date_add(start_date, 140)},
                    {"name": "PFMEA编制", "start": _date_add(start_date, 126), "end": _date_add(start_date, 168)},
                    {"name": "控制计划编制", "start": _date_add(start_date, 154), "end": _date_add(start_date, 182)},
                    {"name": "工装夹具开发", "start": _date_add(start_date, 140), "end": _date_add(start_date, 196)},
                    {"name": "阶段3评审", "start": _date_add(start_date, 182), "end": _date_add(start_date, 182), "type": "milestone"}
                ]
            },
            {
                "name": "阶段4: 产品与过程验证",
                "tasks": [
                    {"name": "试生产准备", "start": _date_add(start_date, 182), "end": _date_add(start_date, 196)},
                    {"name": "试生产Run at Rate", "start": _date_add(start_date, 196), "end": _date_add(start_date, 224)},
                    {"name": "PPAP文件准备", "start": _date_add(start_date, 210), "end": _date_add(start_date, 238)},
                    {"name": "PPAP提交", "start": _date_add(start_date, 238), "end": _date_add(start_date, 238), "type": "milestone"}
                ]
            },
            {
                "name": "阶段5: 反馈与改进",
                "tasks": [
                    {"name": "项目总结", "start": _date_add(start_date, 238), "end": _date_add(start_date, 252)},
                    {"name": "经验教训归档", "start": _date_add(start_date, 245), "end": _date_add(start_date, 259)},
                    {"name": "量产移交", "start": _date_add(start_date, 252), "end": _date_add(start_date, 266)},
                    {"name": "SOP达成", "start": sop_date, "end": sop_date, "type": "milestone"}
                ]
            }
        ]
        phases = default_phases
    else:
        # 从文件加载阶段数据
        try:
            with open(args.phases, 'r', encoding='utf-8') as f:
                content = f.read()
                phases = json.loads(content)
        except:
            phases = []
    
    # 计算甘特图数据
    gantt_data = calculate_gantt_data(start_date, sop_date, phases)
    
    # 准备模板数据
    template_data = {
        "project_name": args.project,
        "start_date": start_date,
        "sop_date": sop_date,
        **gantt_data
    }
    
    # 渲染模板
    template = Template(GANTT_HTML_TEMPLATE)
    html_content = template.render(**template_data)
    
    # 写入文件
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 返回JSON结果
    result = {
        "status": "success",
        "output": args.output,
        "project": args.project,
        "start_date": start_date,
        "sop_date": sop_date,
        "overall_progress": gantt_data["overall_progress"],
        "completed_tasks": gantt_data["completed_tasks"],
        "in_progress_tasks": gantt_data["in_progress_tasks"],
        "pending_tasks": gantt_data["pending_tasks"],
        "days_remaining": gantt_data["days_remaining"]
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def _date_add(date_str, days):
    """日期加天数"""
    from datetime import datetime, timedelta
    date = datetime.strptime(date_str, "%Y-%m-%d")
    new_date = date + timedelta(days=days)
    return new_date.strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(description='生成APQP项目甘特图')
    parser.add_argument('--project', required=True, help='项目名称')
    parser.add_argument('--phases', help='阶段定义JSON文件(可选)')
    parser.add_argument('--start-date', dest='start_date', required=True, help='项目开始日期(YYYY-MM-DD)')
    parser.add_argument('--sop-date', dest='sop_date', required=True, help='目标SOP日期(YYYY-MM-DD)')
    parser.add_argument('--output', required=True, help='输出HTML文件路径')
    
    args = parser.parse_args()
    generate_gantt(args)


if __name__ == "__main__":
    main()
