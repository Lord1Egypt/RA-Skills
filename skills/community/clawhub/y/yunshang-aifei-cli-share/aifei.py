#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
云上艾飞 CLI 入口

用法：
  python aifei.py todo              查询工作待办（正式环境）
  python aifei.py todo --env test   查询工作待办（测试环境）
  python aifei.py user              查询当前用户信息
  python aifei.py projects          查询项目列表
  python aifei.py projects --name xxx  按名称搜索项目
  python aifei.py reimbursement     查询报销列表
  python aifei.py contracts         查询合同列表
  python aifei.py business          查询商机列表
"""

import sys
import io
import json
import argparse
from aifei_api import create_client

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def cmd_user(client, args):
    """查询用户信息"""
    info = client.get_user_info()
    user = info.get('user', {})
    dept = user.get('dept', {})
    roles = info.get('roles', [])
    print(f'\n👤 用户信息')
    print(f'   姓名: {user.get("nickName", "?")}')
    print(f'   账号: {user.get("userName", "?")}')
    print(f'   部门: {dept.get("deptName", "?")}')
    print(f'   角色: {", ".join(roles)}')
    print(f'   邮箱: {user.get("email", "?")}')
    print(f'   手机: {user.get("phonenumber", "?")}')


def cmd_todo(client, args):
    """查询工作待办"""
    todos = client.get_todos()
    total = todos.get('total', 0)
    print(f'\n📋 工作待办: 共 {total} 条\n')

    for i, row in enumerate(todos.get('rows', []), 1):
        title = row.get('taskTitle', '未命名')
        task_type = row.get('taskTypeName', '')
        create_time = row.get('createTime', '')
        status_map = {'01': '待处理', '02': '已处理', '03': '已完成'}
        status = status_map.get(row.get('taskStatus', ''), row.get('taskStatus', ''))
        print(f'  {i}. {title}')
        print(f'     类型: {task_type} | 状态: {status} | 时间: {create_time}')
        print()

    if total == 0:
        print('  （无待办事项）')


def cmd_projects(client, args):
    """查询项目列表"""
    result = client.get_projects(name=args.name)
    total = result.get('total', 0)
    print(f'\n📂 项目列表: 共 {total} 条\n')

    for i, row in enumerate(result.get('rows', []), 1):
        name = row.get('projectName', '?')
        code = row.get('projectNo', '')
        manager = row.get('projectByName', '')
        status_map = {'01': '进行中', '02': '已完成', '03': '已关闭', '04': '暂停'}
        status = status_map.get(row.get('projectStatus', ''), row.get('projectStatus', ''))
        dept = row.get('ownerDeptName', '')
        start = row.get('projectStartDate', '')
        end = row.get('expectEndDate', '')
        print(f'  {i}. [{code}] {name}')
        print(f'     负责人: {manager} | 部门: {dept} | 状态: {status}')
        if start or end:
            print(f'     周期: {start} ~ {end}')
        print()

    if total == 0:
        print('  （无项目）')


def cmd_reimbursement(client, args):
    """查询报销列表"""
    result = client.get_reimbursements()
    total = result.get('total', 0)
    print(f'\n💰 报销列表: 共 {total} 条\n')

    for i, row in enumerate(result.get('rows', [])[:10], 1):
        title = row.get('expenseName', row.get('expenseTitle', '?'))
        amount = row.get('totalAmount', row.get('expenseAmount', '?'))
        status = row.get('approveStatusName', row.get('approveStatus', ''))
        time = row.get('createTime', '')
        print(f'  {i}. {title}')
        print(f'     金额: ¥{amount} | 状态: {status} | 时间: {time}')
        print()

    if total == 0:
        print('  （无报销记录）')


def cmd_contracts(client, args):
    """查询合同列表"""
    result = client.get_contracts()
    total = result.get('total', 0)
    print(f'\n📝 合同列表: 共 {total} 条\n')

    for i, row in enumerate(result.get('rows', [])[:10], 1):
        name = row.get('contractName', '?')
        code = row.get('contractCode', '')
        amount = row.get('contractAmount', '?')
        print(f'  {i}. [{code}] {name}')
        print(f'     金额: ¥{amount}')
        print()

    if total == 0:
        print('  （无合同记录）')


def cmd_business(client, args):
    """查询商机列表"""
    result = client.get_business_opportunities()
    total = result.get('total', 0)
    print(f'\n🎯 商机列表: 共 {total} 条\n')

    for i, row in enumerate(result.get('rows', [])[:10], 1):
        name = row.get('businessName', '?')
        code = row.get('businessCode', '')
        status = row.get('businessStatusName', row.get('businessStatus', ''))
        amount = row.get('businessAmount', '?')
        print(f'  {i}. [{code}] {name}')
        print(f'     金额: ¥{amount} | 状态: {status}')
        print()

    if total == 0:
        print('  （无商机记录）')


def cmd_raw(client, args):
    """原始 API 调用（调试用）"""
    method = args.method.upper()
    path = args.path
    data = json.loads(args.data) if args.data else None

    if method == 'GET':
        result = client.get(path, biz=args.biz)
    elif method == 'POST':
        result = client.post(path, data, biz=args.biz)
    elif method == 'PUT':
        result = client.put(path, data, biz=args.biz)
    else:
        print(f'不支持的方法: {method}')
        return

    print(json.dumps(result, ensure_ascii=False, indent=2)[:2000])


def main():
    parser = argparse.ArgumentParser(description='云上艾飞 CLI')
    parser.add_argument('--env', default='prod', choices=['test', 'prod'], help='环境 (默认 prod)')

    subparsers = parser.add_subparsers(dest='command', help='命令')

    subparsers.add_parser('user', help='查询用户信息')
    subparsers.add_parser('todo', help='查询工作待办')

    p_proj = subparsers.add_parser('projects', help='查询项目列表')
    p_proj.add_argument('--name', help='按名称搜索')

    subparsers.add_parser('reimbursement', help='查询报销列表')
    subparsers.add_parser('contracts', help='查询合同列表')
    subparsers.add_parser('business', help='查询商机列表')

    p_raw = subparsers.add_parser('raw', help='原始 API 调用')
    p_raw.add_argument('method', help='HTTP 方法')
    p_raw.add_argument('path', help='API 路径')
    p_raw.add_argument('--data', help='请求体 JSON')
    p_raw.add_argument('--biz', action='store_true', help='使用业务前缀')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    client = create_client(env=args.env)

    commands = {
        'user': cmd_user,
        'todo': cmd_todo,
        'projects': cmd_projects,
        'reimbursement': cmd_reimbursement,
        'contracts': cmd_contracts,
        'business': cmd_business,
        'raw': cmd_raw,
    }

    commands[args.command](client, args)


if __name__ == '__main__':
    main()
