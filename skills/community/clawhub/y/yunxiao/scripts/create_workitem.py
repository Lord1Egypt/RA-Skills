#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创建工作项"""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yunxiao_api import load_config, create_workitem, search_projects, list_workitem_types


def find_project_by_name(name: str):
    """根据名称查找项目"""
    projects = search_projects(name=name)
    if projects:
        # 精确匹配
        for p in projects:
            if p['name'] == name:
                return p
        # 模糊匹配返回第一个
        return projects[0]
    return None


def find_workitem_type_id(space_id: str, type_name: str):
    """根据类型名称查找工作项类型 ID"""
    types = list_workitem_types(space_id)
    for t in types:
        if t['name'] == type_name:
            return t['id']
    # 默认查找"任务"类型
    for t in types:
        if t['name'] == '任务' or t.get('categoryId') == 'Task':
            return t['id']
    return None


def main():
    parser = argparse.ArgumentParser(description='创建云效工作项')
    parser.add_argument('--subject', '-s', type=str, required=True, help='工作项标题')
    parser.add_argument('--project', '-p', type=str, help='项目名称或 ID')
    parser.add_argument('--type', '-t', type=str, default='任务', help='工作项类型（默认：任务）')
    parser.add_argument('--desc', '-d', type=str, help='工作项描述')
    parser.add_argument('--assignee', '-a', type=str, help='负责人 userId（默认：自己）')
    parser.add_argument('--priority', choices=['低', '中', '高', '紧急'], help='优先级')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--list-projects', action='store_true', help='列出所有可选项目')
    
    args = parser.parse_args()
    
    # 列出项目
    if args.list_projects:
        projects = search_projects()
        print("\n可选项目:")
        print("-" * 50)
        for p in projects:
            print(f"  {p['name']} ({p['customCode']})")
        print()
        return
    
    config = load_config()
    
    # 获取项目 ID
    project_id = None
    project_name = None
    
    if args.project:
        # 尝试作为项目名称查找
        project = find_project_by_name(args.project)
        if project:
            project_id = project['id']
            project_name = project['name']
        else:
            # 作为 ID 使用
            project_id = args.project
            project_name = args.project
    else:
        # 没有指定项目，提示用户选择
        print("错误: 创建工作项需要指定项目")
        print("\n请使用 --project 指定项目名称")
        print("\n可选项目:")
        projects = search_projects()
        for p in projects[:10]:  # 只显示前10个
            print(f"  - {p['name']}")
        if len(projects) > 10:
            print(f"  ... 还有 {len(projects) - 10} 个项目")
        print(f"\n使用 --list-projects 查看全部项目")
        sys.exit(1)
    
    # 动态获取该项目的工作项类型 ID
    type_id = find_workitem_type_id(project_id, args.type)
    if not type_id:
        print(f"警告: 项目 '{project_name}' 中未找到工作项类型 '{args.type}'")
        # 尝试使用默认"任务"类型
        type_id = find_workitem_type_id(project_id, '任务')
        if type_id:
            print(f"已自动使用 '任务' 类型")
        else:
            print("错误: 无法确定工作项类型")
            sys.exit(1)
    
    # 获取优先级 ID（暂不支持，API 格式复杂）
    priority_id = None
    if args.priority:
        print("注意: 优先级设置暂不支持，请在云效界面中手动设置")
    
    # 获取负责人
    assignee = args.assignee or config.get('user_id')
    
    try:
        result = create_workitem(
            subject=args.subject,
            space_id=project_id,
            workitem_type_id=type_id,
            assigned_to=assignee,
            description=args.desc
        )
        
        workitem_id = result.get('id')
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n✓ 工作项创建成功!")
            print(f"  ID: {workitem_id}")
            print(f"  标题: {args.subject}")
            print(f"  类型: {args.type}")
            print(f"  项目: {project_name}")
            print(f"\n查看: https://devops.aliyun.com/projex/task/{workitem_id}")
            print()
        
        return workitem_id
        
    except Exception as e:
        print(f"创建失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()