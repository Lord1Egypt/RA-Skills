#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道项目管理命令行工具
"""

import sys
import re
from pathlib import Path
from datetime import datetime

# 添加 lib 目录到 Python 路径
script_dir = Path(__file__).parent.absolute()
lib_path = script_dir.parent / 'lib'
sys.path.insert(0, str(lib_path))

# 直接导入
import importlib.util
client_path = lib_path / "zentao_client.py"
spec = importlib.util.spec_from_file_location("zentao_client", client_path)
zentao_client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zentao_client)
ZenTaoClient = zentao_client.ZenTaoClient
read_credentials = zentao_client.read_credentials


def format_table(headers: list, rows: list, max_width: int = 30) -> str:
    """格式化表格输出"""
    if not rows:
        return "无数据"
    
    # 计算列宽
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                cell_str = str(cell)[:max_width]
                col_widths[i] = max(col_widths[i], len(cell_str))
    
    # 构建表格
    lines = []
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    lines.append(header_line)
    lines.append("-+-".join("-" * w for w in col_widths))
    
    for row in rows:
        row_line = " | ".join(str(cell)[:max_width].ljust(col_widths[i]) for i, cell in enumerate(row))
        lines.append(row_line)
    
    return "\n".join(lines)


def cmd_products(client: ZenTaoClient) -> None:
    """查询产品列表"""
    print("📦 查询禅道产品列表...\n")
    
    # 优先使用 REST API
    success, products = client.get_products()
    
    if success and isinstance(products, list):
        print(f"✅ 共查询到 {len(products)} 个产品\n")
        headers = ['ID', '产品名称', '状态', '负责人']
        rows = []
        for p in products:
            rows.append([
                p.get('id', ''),
                p.get('name', ''),
                p.get('status', ''),
                p.get('owner', '')
            ])
        print(format_table(headers, rows))
    else:
        # 降级到老 API
        print("⚠️  REST API 失败，尝试老 API...\n")
        product_dict = client.get_product_list_old()
        if product_dict:
            print(f"✅ 共查询到 {len(product_dict)} 个产品\n")
            headers = ['产品名称', 'ID']
            rows = [[name, pid] for name, pid in product_dict.items()]
            print(format_table(headers, rows))
        else:
            print("❌ 查询失败")


def cmd_projects(client: ZenTaoClient, status: str = 'doing') -> None:
    """查询项目列表"""
    print(f"📋 查询禅道项目列表（状态：{status}）...\n")
    
    # 优先使用 REST API
    success, projects = client.get_projects(status)
    
    if success and isinstance(projects, list):
        print(f"✅ 共查询到 {len(projects)} 个项目\n")
        headers = ['ID', '项目名称', '状态', '开始日期', '结束日期']
        rows = []
        for p in projects:
            rows.append([
                p.get('id', ''),
                p.get('name', ''),
                p.get('status', ''),
                p.get('begin', ''),
                p.get('end', '')
            ])
        print(format_table(headers, rows))
    else:
        # 降级到老 API
        print("⚠️  REST API 失败，尝试老 API...\n")
        project_dict = client.get_project_list_old()
        if project_dict:
            print(f"✅ 共查询到 {len(project_dict)} 个项目\n")
            headers = ['项目名称', 'ID']
            rows = [[name, pid] for name, pid in project_dict.items()]
            print(format_table(headers, rows))
        else:
            print("❌ 查询失败")


def cmd_executions(client: ZenTaoClient, project_id: str) -> None:
    """查询执行列表"""
    print(f"🔄 查询项目 {project_id} 的执行列表...\n")
    
    success, executions = client.get_executions(project_id)
    
    if success and isinstance(executions, list):
        print(f"✅ 共查询到 {len(executions)} 个执行\n")
        headers = ['ID', '执行名称', '状态', '开始日期', '结束日期']
        rows = []
        for e in executions:
            rows.append([
                e.get('id', ''),
                e.get('name', ''),
                e.get('status', ''),
                e.get('begin', ''),
                e.get('end', '')
            ])
        print(format_table(headers, rows))
    else:
        print(f"❌ 查询失败：{executions}")


def cmd_stories(client: ZenTaoClient, project_id: str, limit: int = 50) -> None:
    """查询需求列表"""
    print(f"📖 查询项目 {project_id} 的需求列表...\n")
    
    success, stories = client.get_stories(project_id)
    
    if success and isinstance(stories, list):
        print(f"✅ 共查询到 {len(stories)} 个需求")
        if len(stories) > limit:
            print(f"（显示前 {limit} 条）\n")
            stories = stories[:limit]
        else:
            print()
        
        headers = ['ID', '需求标题', '状态', '优先级', '指派给']
        rows = []
        for s in stories:
            rows.append([
                s.get('id', ''),
                s.get('title', '')[:40],
                s.get('status', ''),
                s.get('priority', ''),
                s.get('assignedTo', '')
            ])
        print(format_table(headers, rows, max_width=40))
    else:
        print(f"❌ 查询失败：{stories}")


def cmd_tasks(client: ZenTaoClient, execution_id: str, limit: int = 50) -> None:
    """查询任务列表"""
    print(f"📝 查询执行 {execution_id} 的任务列表...\n")
    
    success, tasks = client.get_tasks(execution_id)
    
    if success and isinstance(tasks, list):
        print(f"✅ 共查询到 {len(tasks)} 个任务")
        if len(tasks) > limit:
            print(f"（显示前 {limit} 条）\n")
            tasks = tasks[:limit]
        else:
            print()
        
        headers = ['ID', '任务名称', '状态', '优先级', '指派给']
        rows = []
        for t in tasks:
            rows.append([
                t.get('id', ''),
                t.get('name', '')[:40],
                t.get('status', ''),
                t.get('priority', ''),
                t.get('assignedTo', '')
            ])
        print(format_table(headers, rows, max_width=40))
    else:
        print(f"❌ 查询失败：{tasks}")


def cmd_bugs(client: ZenTaoClient, product_id: str, limit: int = 50) -> None:
    """查询缺陷列表"""
    print(f"🐛 查询产品 {product_id} 的缺陷列表...\n")
    
    # 尝试 REST API
    success, bugs = client.get_bugs(product_id)
    
    if success and isinstance(bugs, list):
        print(f"✅ 共查询到 {len(bugs)} 个缺陷")
        if len(bugs) > limit:
            print(f"（显示前 {limit} 条）\n")
            bugs = bugs[:limit]
        else:
            print()
        
        headers = ['ID', '缺陷标题', '严重程度', '状态', '指派给']
        rows = []
        for b in bugs:
            rows.append([
                b.get('id', ''),
                b.get('title', '')[:40],
                b.get('severity', ''),
                b.get('status', ''),
                b.get('assignedTo', '')
            ])
        print(format_table(headers, rows, max_width=40))
    else:
        # 降级到老 API
        print("⚠️  REST API 失败，尝试老 API...\n")
        bugs = client.get_bug_list_old(product_id)
        if bugs:
            print(f"✅ 共查询到 {len(bugs)} 个缺陷\n")
            # 老 API 返回格式可能不同，需要适配
            headers = ['ID', '缺陷标题', '状态']
            rows = []
            for b in bugs[:limit]:
                if isinstance(b, dict):
                    rows.append([
                        b.get('id', ''),
                        b.get('title', '')[:40],
                        b.get('status', '')
                    ])
            print(format_table(headers, rows, max_width=40))
        else:
            print("❌ 查询失败")


def cmd_productplans(client: ZenTaoClient, product_id: str) -> None:
    """查询发布计划列表"""
    print(f"📅 查询产品 {product_id} 的发布计划...\n")
    
    productplan_dict = client.get_productplan_list_old(product_id)
    
    if productplan_dict:
        print(f"✅ 共查询到 {len(productplan_dict)} 个发布计划\n")
        headers = ['计划名称', 'ID']
        rows = [[name, pid] for name, pid in productplan_dict.items()]
        print(format_table(headers, rows))
    else:
        print("❌ 查询失败或无数据")


def confirm_action(action_name: str, details: dict) -> bool:
    """确认操作"""
    print(f"\n⚠️  确认执行操作：{action_name}")
    print("-" * 50)
    for k, v in details.items():
        print(f"  {k}: {v}")
    print("-" * 50)
    
    response = input("确认执行？(y/n): ").strip().lower()
    return response in ['y', 'yes', '是']


def cmd_create_story(client: ZenTaoClient, product_id: str, execution_id: str, 
                     title: str, plan_id: str = '0', reviewer: str = '') -> None:
    """新建需求"""
    if not confirm_action("新建需求", {
        '产品 ID': product_id,
        '执行 ID': execution_id,
        '需求标题': title,
        '计划 ID': plan_id,
        '评审人': reviewer or '默认'
    }):
        print("❌ 操作已取消")
        return
    
    success, result = client.create_story(product_id, execution_id, title, plan_id, reviewer)
    
    if success:
        msg = result.get('message', '新建成功') if isinstance(result, dict) else '新建成功'
        story_id = result.get('id', '未知') if isinstance(result, dict) else '未知'
        print(f"✅ {msg}，需求 ID: {story_id}")
    else:
        print(f"❌ 新建失败：{result}")


def cmd_create_task(client: ZenTaoClient, execution_id: str, story_id: str, 
                    name: str, assign_to: str, parent_id: str = None) -> None:
    """新建任务，支持创建子任务"""
    info = {
        '执行 ID': execution_id,
        '需求 ID': story_id,
        '任务名称': name,
        '指派给': assign_to
    }
    if parent_id:
        info['父任务 ID'] = parent_id
    if not confirm_action("新建任务", info):
        print("❌ 操作已取消")
        return
    
    success, result = client.create_task(execution_id, story_id, name, assign_to, parent_id)
    
    if success:
        msg = result.get('message', '新建成功') if isinstance(result, dict) else '新建成功'
        task_id = result.get('id', '未知') if isinstance(result, dict) else '未知'
        print(f"✅ {msg}，任务 ID: {task_id}")
    else:
        print(f"❌ 新建失败：{result}")

def cmd_batch_create_tasks(client: ZenTaoClient, execution_id: str, parent_id: str, 
                           tasks_str: str) -> None:
    """批量创建子任务
    
    tasks_str 格式: 任务1名称:工时,任务2名称:工时
    例如: 8个前端面试:16,4个后端面试:8
    """
    # 解析任务列表
    tasks = []
    for item in tasks_str.split(','):
        parts = item.strip().split(':')
        if len(parts) >= 1:
            task = {'name': parts[0].strip()}
            if len(parts) >= 2:
                task['estimate'] = parts[1].strip()
            tasks.append(task)
    
    if not tasks:
        print("❌ 未提供有效的任务信息")
        return
    
    if not confirm_action("批量创建子任务", {
        '执行 ID': execution_id,
        '父任务 ID': parent_id,
        '任务数量': len(tasks),
        '任务列表': ', '.join([f"{t['name']}({t.get('estimate', 'N/A')}h)" for t in tasks])
    }):
        print("❌ 操作已取消")
        return
    
    success, result = client.batch_create_tasks(execution_id, parent_id, tasks)
    
    if success:
        print(f"✅ {result.get('message', '创建成功')}")
    else:
        print(f"❌ 创建失败：{result}")



def cmd_create_productplan(client: ZenTaoClient, product_id: str, title: str) -> None:
    """新建发布计划"""
    if not confirm_action("新建发布计划", {
        '产品 ID': product_id,
        '计划名称': title
    }):
        print("❌ 操作已取消")
        return
    
    success, result = client.create_productplan(product_id, title)
    
    if success:
        msg = result.get('message', '新建成功') if isinstance(result, dict) else '新建成功'
        plan_id = result.get('id', '未知') if isinstance(result, dict) else '未知'
        print(f"✅ {msg}，计划 ID: {plan_id}")
    else:
        print(f"❌ 新建失败：{result}")


def cmd_review_story(client: ZenTaoClient, story_id: str) -> None:
    """评审需求"""
    if not confirm_action("评审需求", {
        '需求 ID': story_id,
        '评审结果': '通过'
    }):
        print("❌ 操作已取消")
        return
    
    success, result = client.review_story(story_id)
    
    if success:
        print(f"✅ 需求 {story_id} 评审通过")
    else:
        print(f"❌ 评审失败：{result}")


def parse_args(args: list) -> dict:
    """解析命令行参数"""
    result = {'command': None, 'params': {}}
    
    if not args:
        return result
    
    args_str = ' '.join(args)
    
    # 提取命令 - 按优先级匹配（长的关键字优先）
    command_keywords = [
        ('新建需求', 'create_story'),
        ('新建任务', 'create_task'),
        ('批量创建子任务', 'batch_create_tasks'),
        ('新建计划', 'create_productplan'),
        ('评审需求', 'review_story'),
        ('产品列表', 'products'),
        ('项目列表', 'projects'),
        ('执行列表', 'executions'),
        ('需求列表', 'stories'),
        ('任务列表', 'tasks'),
        ('缺陷列表', 'bugs'),
        ('计划列表', 'productplans'),
        ('产品', 'products'),
        ('项目', 'projects'),
        ('执行', 'executions'),
        ('需求', 'stories'),
        ('任务', 'tasks'),
        ('缺陷', 'bugs'),
        ('计划', 'productplans'),
    ]
    
    # 匹配命令
    for kw, cmd in command_keywords:
        if kw in args_str:
            result['command'] = cmd
            break
    
    # 提取参数
    param_patterns = [
        (r'产品\s*[=:]\s*(\S+)', 'product_id'),
        (r'项目\s*[=:]\s*(\S+)', 'project_id'),
        (r'执行\s*[=:]\s*(\S+)', 'execution_id'),
        (r'需求\s*[=:]\s*(\S+)', 'story_id'),
        (r'标题\s*[=:]\s*(.+?)(?:\s+\w+\s*[=:]|$)', 'title'),
        (r'计划\s*[=:]\s*(\S+)', 'plan_id'),
        (r'指派\s*[=:]\s*(\S+)', 'assign_to'),
        (r'评审人\s*[=:]\s*(\S+)', 'reviewer'),
        (r'状态\s*[=:]\s*(\S+)', 'status'),
        (r'限制\s*[=:]\s*(\d+)', 'limit'),
    ]
    
    for pattern, param_name in param_patterns:
        match = re.search(pattern, args_str)
        if match:
            result['params'][param_name] = match.group(1).strip()
    
    return result


def main():
    """主函数"""
    print("🔷 禅道项目管理工具")
    print("=" * 50)
    
    # 读取凭证
    credentials = read_credentials()
    if not credentials:
        print("\n❌ 错误：未找到禅道 API 凭证")
        print("\n请在 TOOLS.md 文件中添加以下配置：")
        print("\n```markdown")
        print("## 禅道 API")
        print("")
        print("- **API 地址：** http://<your-zentao-host>/")
        print("- **用户名：** <your-username>")
        print("- **密码：** <your-password>")
        print("```")
        return 1
    
    print(f"\n📍 API 地址：{credentials['endpoint']}")
    print(f"👤 用户：{credentials['username']}")
    
    # 创建客户端
    client = ZenTaoClient(
        credentials['endpoint'],
        credentials['username'],
        credentials['password']
    )
    
    # 解析命令
    args = sys.argv[1:]
    parsed = parse_args(args)
    
    command = parsed.get('command')
    params = parsed.get('params', {})
    
    print(f"\n📋 命令：{command or '无'}")
    print(f"📝 参数：{params}\n")
    
    # 执行命令
    if command == 'products':
        cmd_products(client)
    elif command == 'projects':
        cmd_projects(client, params.get('status', 'doing'))
    elif command == 'executions':
        if 'project_id' in params:
            cmd_executions(client, params['project_id'])
        else:
            print("❌ 请指定项目 ID，例如：项目=176")
    elif command == 'stories':
        if 'project_id' in params:
            cmd_stories(client, params['project_id'], int(params.get('limit', 50)))
        else:
            print("❌ 请指定项目 ID，例如：项目=176")
    elif command == 'tasks':
        if 'execution_id' in params:
            cmd_tasks(client, params['execution_id'], int(params.get('limit', 50)))
        else:
            print("❌ 请指定执行 ID，例如：执行=176")
    elif command == 'bugs':
        if 'product_id' in params:
            cmd_bugs(client, params['product_id'], int(params.get('limit', 50)))
        else:
            print("❌ 请指定产品 ID，例如：产品=21")
    elif command == 'productplans':
        if 'product_id' in params:
            cmd_productplans(client, params['product_id'])
        else:
            print("❌ 请指定产品 ID，例如：产品=21")
    elif command == 'create_story':
        required = ['product_id', 'execution_id', 'title']
        if all(p in params for p in required):
            cmd_create_story(client, params['product_id'], params['execution_id'], 
                           params['title'], params.get('plan_id', '0'), params.get('reviewer', ''))
        else:
            print(f"❌ 缺少必需参数：{[p for p in required if p not in params]}")
    elif command == 'create_task':
        required = ['execution_id', 'story_id', 'name', 'assign_to']
        if all(p in params for p in required):
            cmd_create_task(client, params['execution_id'], params['story_id'], 
                          params['name'], params['assign_to'])
        else:
            print(f"❌ 缺少必需参数：{[p for p in required if p not in params]}")
    elif command == 'create_productplan':
        required = ['product_id', 'title']
        if all(p in params for p in required):
            cmd_create_productplan(client, params['product_id'], params['title'])
        else:
            print(f"❌ 缺少必需参数：{[p for p in required if p not in params]}")
    elif command == 'review_story':
        if 'story_id' in params:
            cmd_review_story(client, params['story_id'])
        else:
            print("❌ 请指定需求 ID，例如：需求=1234")
    else:
        print("\n📖 可用命令:")
        print("  禅道产品列表                 - 查询所有产品")
        print("  禅道项目列表                 - 查询进行中的项目")
        print("  禅道执行列表 项目=ID         - 查询项目的执行列表")
        print("  禅道需求列表 项目=ID         - 查询项目的需求列表")
        print("  禅道任务列表 执行=ID         - 查询执行的任务列表")
        print("  禅道缺陷列表 产品=ID         - 查询产品的缺陷列表")
        print("  禅道计划列表 产品=ID         - 查询产品的发布计划")
        print("\n  (需要确认的操作)")
        print("  禅道新建需求 产品=ID 执行=ID 标题=xxx 计划=xxx")
        print("  禅道新建任务 执行=ID 需求=ID 标题=xxx 指派=xxx [父任务=ID]")
        print("  禅道批量创建子任务 执行=ID 父任务=ID 任务=任务1:工时,任务2:工时")
        print("  禅道新建计划 产品=ID 标题=xxx")
        print("  禅道评审需求 需求=ID")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
