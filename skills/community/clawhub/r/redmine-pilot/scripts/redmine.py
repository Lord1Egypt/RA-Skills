#!/usr/bin/env python3
"""
Redmine API 客户端
用法: python3 redmine.py <command> [options]
"""

import argparse
import json
import os
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

def get_config():
    """获取配置"""
    url = os.environ.get('REDMINE_URL', '').rstrip('/')
    key = os.environ.get('REDMINE_API_KEY', '')
    
    if not url or not key:
        print("错误: 请设置环境变量 REDMINE_URL 和 REDMINE_API_KEY", file=sys.stderr)
        sys.exit(1)
    
    return url, key

def api_request(method, endpoint, data=None):
    """发送 API 请求"""
    url, key = get_config()
    full_url = f"{url}{endpoint}"
    
    headers = {
        'X-Redmine-API-Key': key,
        'Content-Type': 'application/json'
    }
    
    body = json.dumps(data).encode() if data else None
    req = Request(full_url, data=body, headers=headers, method=method)
    
    try:
        with urlopen(req) as resp:
            if resp.status == 204:
                return None
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)

def list_issues(project_id=None, status='open', assigned_to=None, limit=25, offset=0):
    """查询 Issue 列表"""
    params = {'limit': limit, 'offset': offset}
    if project_id:
        params['project_id'] = project_id
    if status:
        params['status_id'] = status
    if assigned_to:
        params['assigned_to_id'] = assigned_to
    
    endpoint = f"/issues.json?{urlencode(params)}"
    result = api_request('GET', endpoint)
    return result

def get_issue(issue_id, include=None):
    """获取单个 Issue 详情"""
    params = {}
    if include:
        params['include'] = include
    
    endpoint = f"/issues/{issue_id}.json"
    if params:
        endpoint += f"?{urlencode(params)}"
    
    return api_request('GET', endpoint)

def create_issue(project_id, subject, description=None, tracker_id=None, 
                 priority_id=None, assigned_to_id=None, custom_fields=None):
    """创建 Issue"""
    issue_data = {
        'project_id': project_id,
        'subject': subject
    }
    
    if description:
        issue_data['description'] = description
    if tracker_id:
        issue_data['tracker_id'] = tracker_id
    if priority_id:
        issue_data['priority_id'] = priority_id
    if assigned_to_id:
        issue_data['assigned_to_id'] = assigned_to_id
    if custom_fields:
        issue_data['custom_fields'] = custom_fields
    
    return api_request('POST', '/issues.json', {'issue': issue_data})

def update_issue(issue_id, status_id=None, notes=None, assigned_to_id=None, 
                 subject=None, description=None, custom_fields=None):
    """更新 Issue"""
    issue_data = {}
    
    if status_id:
        issue_data['status_id'] = status_id
    if notes:
        issue_data['notes'] = notes
    if assigned_to_id:
        issue_data['assigned_to_id'] = assigned_to_id
    if subject:
        issue_data['subject'] = subject
    if description:
        issue_data['description'] = description
    if custom_fields:
        issue_data['custom_fields'] = custom_fields
    
    return api_request('PUT', f'/issues/{issue_id}.json', {'issue': issue_data})

def list_projects(limit=100):
    """获取项目列表"""
    return api_request('GET', f'/projects.json?limit={limit}')

def get_statuses():
    """获取状态列表"""
    return api_request('GET', '/issue_statuses.json')

def get_trackers():
    """获取跟踪器列表"""
    return api_request('GET', '/trackers.json')

def get_priorities():
    """获取优先级列表"""
    return api_request('GET', '/enumerations/issue_priorities.json')

def format_issue(issue):
    """格式化单个 Issue 输出"""
    return (f"#{issue['id']} [{issue.get('status', {}).get('name', '?')}] "
            f"{issue['subject']} "
            f"(项目: {issue.get('project', {}).get('name', '?')})")

def main():
    parser = argparse.ArgumentParser(description='Redmine API 客户端')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # my-issues
    my_parser = subparsers.add_parser('my-issues', help='查询指派给我的 Issue')
    my_parser.add_argument('--limit', type=int, default=25)
    
    # issues
    issues_parser = subparsers.add_parser('issues', help='查询 Issue 列表')
    issues_parser.add_argument('--project', help='项目 ID')
    issues_parser.add_argument('--status', default='open', help='状态 (open/closed/*)')
    issues_parser.add_argument('--assigned', help='指派人 ID')
    issues_parser.add_argument('--limit', type=int, default=25)
    issues_parser.add_argument('--offset', type=int, default=0)
    
    # get
    get_parser = subparsers.add_parser('get', help='获取 Issue 详情')
    get_parser.add_argument('issue_id', type=int, help='Issue ID')
    get_parser.add_argument('--include', default='journals', 
                           help='包含数据 (journals,attachments,relations)')
    
    # create
    create_parser = subparsers.add_parser('create', help='创建 Issue')
    create_parser.add_argument('--project', required=True, help='项目 ID')
    create_parser.add_argument('--subject', required=True, help='标题')
    create_parser.add_argument('--description', help='描述')
    create_parser.add_argument('--tracker', type=int, help='跟踪器 ID')
    create_parser.add_argument('--priority', type=int, help='优先级 ID')
    create_parser.add_argument('--assigned', type=int, help='指派人 ID')
    
    # update
    update_parser = subparsers.add_parser('update', help='更新 Issue')
    update_parser.add_argument('issue_id', type=int, help='Issue ID')
    update_parser.add_argument('--status', type=int, help='状态 ID')
    update_parser.add_argument('--notes', help='备注')
    update_parser.add_argument('--assigned', type=int, help='指派人 ID')
    update_parser.add_argument('--subject', help='标题')
    
    # projects
    subparsers.add_parser('projects', help='获取项目列表')
    
    # statuses
    subparsers.add_parser('statuses', help='获取状态列表')
    
    # trackers
    subparsers.add_parser('trackers', help='获取跟踪器列表')
    
    # priorities
    subparsers.add_parser('priorities', help='获取优先级列表')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'my-issues':
        result = list_issues(assigned_to='me', limit=args.limit)
        for issue in result.get('issues', []):
            print(format_issue(issue))
        print(f"\n共 {result.get('total_count', 0)} 条")
    
    elif args.command == 'issues':
        result = list_issues(
            project_id=args.project,
            status=args.status,
            assigned_to=args.assigned,
            limit=args.limit,
            offset=args.offset
        )
        for issue in result.get('issues', []):
            print(format_issue(issue))
        print(f"\n共 {result.get('total_count', 0)} 条 (显示 {args.offset+1}-{args.offset+len(result.get('issues', []))})")
    
    elif args.command == 'get':
        result = get_issue(args.issue_id, args.include)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'create':
        result = create_issue(
            project_id=args.project,
            subject=args.subject,
            description=args.description,
            tracker_id=args.tracker,
            priority_id=args.priority,
            assigned_to_id=args.assigned
        )
        print(f"创建成功: #{result['issue']['id']}")
    
    elif args.command == 'update':
        update_issue(
            issue_id=args.issue_id,
            status_id=args.status,
            notes=args.notes,
            assigned_to_id=args.assigned,
            subject=args.subject
        )
        print(f"更新成功: #{args.issue_id}")
    
    elif args.command == 'projects':
        result = list_projects()
        for p in result.get('projects', []):
            print(f"{p['id']}: {p['name']} ({p.get('identifier', '')})")
    
    elif args.command == 'statuses':
        result = get_statuses()
        for s in result.get('issue_statuses', []):
            print(f"{s['id']}: {s['name']}")
    
    elif args.command == 'trackers':
        result = get_trackers()
        for t in result.get('trackers', []):
            print(f"{t['id']}: {t['name']}")
    
    elif args.command == 'priorities':
        result = get_priorities()
        for p in result.get('issue_priorities', []):
            print(f"{p['id']}: {p['name']}")

if __name__ == '__main__':
    main()
