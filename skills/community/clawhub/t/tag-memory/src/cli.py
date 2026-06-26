#!/usr/bin/env python3
"""
TagMemory CLI - 命令行接口
供 Node.js Skill 调用
"""

import sys
import json
import argparse
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent))

from skill import TagMemorySkill
from deduplication import DeduplicationManager


def format_output(result):
    """格式化输出"""
    if isinstance(result, dict):
        if 'message' in result:
            print(result['message'])
        elif 'error' in result:
            print(f"❌ 错误: {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)


# JSON 命令处理器
def run_query(args):
    skill = TagMemorySkill()
    tags = args.get('tags')
    if isinstance(tags, str):
        tags = tags.split(',')
    time_range = args.get('time_range')
    if time_range:
        time_range = (time_range.get('start'), time_range.get('end'))
    return skill.memory_query(
        query=args.get('query', ''),
        tags=tags,
        time_range=time_range,
        limit=args.get('limit', 5)
    )

def run_store(args):
    skill = TagMemorySkill()
    dedup = DeduplicationManager(skill.db)
    content = args.get('content', '')
    tags = args.get('tags', [])
    force = args.get('force', False)
    
    # 处理 agent_id（CLI 用 args.agent，JSON 用 args['agent_id']）
    agent_id = getattr(args, 'agent', None) or args.get('agent_id', 'main')
    
    should = dedup.should_store(content, tags, force)
    if not should['should_store'] and not force:
        return {
            'success': True,
            'stored': False,
            'action': 'skip',
            'message': f"⏭️ {should['reason']}，跳过存储"
        }
    
    if should['action'] == 'update' and should.get('existing_memory'):
        skill.db.delete(should['existing_memory']['id'])
    
    return skill.memory_store(
        content=content,
        tags=tags,
        time_label=args.get('time_label'),
        source=args.get('source', 'dialogue'),
        agent_id=agent_id
    )

def run_verify(args):
    skill = TagMemorySkill()
    return skill.memory_verify(
        memory_id=args.get('memory_id'),
        action=args.get('action'),
        correction=args.get('correction')
    )

def run_list(args):
    skill = TagMemorySkill()
    tags = args.get('tags')
    if isinstance(tags, str):
        tags = tags.split(',')
    
    # agent_id 过滤
    agent_id = args.get('agent_id')
    
    result = skill.memory_list(
        tags=tags,
        verified_only=args.get('verified_only', False),
        page=args.get('page', 1),
        page_size=args.get('page_size', 20)
    )
    
    # 按 agent_id 过滤结果
    if agent_id and result.get('results'):
        result['results'] = [r for r in result['results'] if r.get('agent_id') == agent_id]
        result['total'] = len(result['results'])
    
    # 格式化输出
    if result['success'] and result.get('results'):
        lines = [f"📋 共 {result['total']} 条记忆:\n"]
        for r in result['results']:
            verified = '✅' if r['verified'] else '❓'
            agent = r.get('agent_id', 'main')
            lines.append(f"{verified} [{agent}] {r['content'][:50]}...")
        result['message'] = '\n'.join(lines)
    
    return result

def run_verify_pending(args):
    skill = TagMemorySkill()
    return skill.memory_verify_get_pending(max_count=args.get('max_count', 3))

def run_verify_result(args):
    skill = TagMemorySkill()
    return skill.memory_verify_result(
        index=args.get('index'),
        action=args.get('action'),
        correction=args.get('correction')
    )

def run_summarize(args):
    skill = TagMemorySkill()
    return skill.memory_summarize(days=args.get('days', 7))

def run_summarize_confirm(args):
    skill = TagMemorySkill()
    return skill.memory_summarize_confirm(feedback=args.get('feedback', 'confirm'))

def run_stats():
    skill = TagMemorySkill()
    dedup = DeduplicationManager(skill.db)
    stats = skill.get_stats()
    tag_stats = dedup.get_storage_stats()
    
    result = {
        'success': True,
        'stats': stats['stats'],
        'tag_distribution': tag_stats.get('tag_distribution', {})
    }
    
    # 格式化消息
    s = stats['stats']
    lines = [f"📊 记忆统计:",
             f"- 总数: {s['total']}",
             f"- ✅ 已确认: {s['verified']} ({s['verified_rate']})",
             f"- ❓ 待确认: {s['unverified']}"]
    
    if tag_stats.get('tag_distribution'):
        lines.append("\n🏷️ 标签分布:")
        for tag, count in tag_stats['tag_distribution'].items():
            lines.append(f"  - {tag}: {count}")
    
    result['message'] = '\n'.join(lines)
    return result


def main():
    # 支持 JSON 输入（通过 stdin）
    if '--json' in sys.argv:
        sys.argv.remove('--json')
        try:
            json_input = json.loads(sys.stdin.read())
            command = sys.argv[1] if len(sys.argv) > 1 else None
            if command == 'query':
                result = run_query(json_input)
            elif command == 'store':
                result = run_store(json_input)
            elif command == 'verify':
                result = run_verify(json_input)
            elif command == 'list':
                result = run_list(json_input)
            elif command == 'verify-pending':
                result = run_verify_pending(json_input)
            elif command == 'verify-result':
                result = run_verify_result(json_input)
            elif command == 'summarize':
                result = run_summarize(json_input)
            elif command == 'summarize-confirm':
                result = run_summarize_confirm(json_input)
            elif command == 'stats':
                result = run_stats()
            else:
                result = {'error': f'Unknown command: {command}'}
            print(json.dumps(result, ensure_ascii=False))
            return
        except Exception as e:
            print(json.dumps({'error': str(e)}), file=sys.stderr)
            sys.exit(1)
    
    parser = argparse.ArgumentParser(description='TagMemory CLI')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # store 命令
    store_parser = subparsers.add_parser('store', help='存储记忆')
    store_parser.add_argument('content', help='记忆内容')
    store_parser.add_argument('tags', nargs='*', help='标签列表')
    store_parser.add_argument('--time-label', help='时间标签 YYYY-MM')
    store_parser.add_argument('--source', default='dialogue', help='来源')
    store_parser.add_argument('--force', action='store_true', help='强制存储')
    store_parser.add_argument('--agent', default='main', help='agent ID (默认 main)')
    
    # query 命令
    query_parser = subparsers.add_parser('query', help='查询记忆')
    query_parser.add_argument('query', help='查询内容')
    query_parser.add_argument('--limit', type=int, default=5, help='返回数量')
    query_parser.add_argument('--tags', help='标签过滤（逗号分隔）')
    query_parser.add_argument('--start', help='开始时间')
    query_parser.add_argument('--end', help='结束时间')
    
    # verify 命令
    verify_parser = subparsers.add_parser('verify', help='核对记忆')
    verify_parser.add_argument('memory_id', help='记忆 ID')
    verify_parser.add_argument('action', choices=['confirm', 'correct', 'delete'], help='操作')
    verify_parser.add_argument('correction', nargs='?', help='修正内容')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出记忆')
    list_parser.add_argument('--page', type=int, default=1, help='页码')
    list_parser.add_argument('--page-size', type=int, default=20, help='每页数量')
    list_parser.add_argument('--verified-only', action='store_true', help='仅已确认')
    list_parser.add_argument('--tags', help='标签过滤（逗号分隔）')
    
    # verify-pending 命令
    pending_parser = subparsers.add_parser('verify-pending', help='待核对列表')
    pending_parser.add_argument('--max', type=int, default=3, help='最大数量')
    
    # verify-result 命令
    result_parser = subparsers.add_parser('verify-result', help='核对结果')
    result_parser.add_argument('index', type=int, help='索引')
    result_parser.add_argument('action', choices=['confirm', 'correct', 'delete'], help='操作')
    result_parser.add_argument('correction', nargs='?', help='修正内容')
    
    # summarize 命令
    summarize_parser = subparsers.add_parser('summarize', help='生成总结')
    summarize_parser.add_argument('--days', type=int, default=7, help='天数')
    
    # summarize-confirm 命令
    confirm_parser = subparsers.add_parser('summarize-confirm', help='确认总结')
    confirm_parser.add_argument('feedback', nargs='?', default='confirm', help='反馈')
    
    # stats 命令
    subparsers.add_parser('stats', help='统计信息')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    skill = TagMemorySkill()
    dedup = DeduplicationManager(skill.db)
    
    try:
        if args.command == 'store':
            # 处理去重
            should = dedup.should_store(args.content, args.tags, args.force)
            
            if not should['should_store'] and not args.force:
                result = {
                    'success': True,
                    'stored': False,
                    'action': 'skip',
                    'message': f"⏭️ {should['reason']}，跳过存储"
                }
                format_output(result)
                return
            
            # 处理更新
            if should['action'] == 'update' and should.get('existing_memory'):
                skill.db.delete(should['existing_memory']['id'])
            
            result = skill.memory_store(
                content=args.content,
                tags=args.tags,
                time_label=args.time_label,
                source=args.source,
                agent_id=getattr(args, 'agent', 'main')
            )
            format_output(result)
        
        elif args.command == 'query':
            tags = args.tags.split(',') if args.tags else None
            time_range = (args.start, args.end) if args.start or args.end else None
            
            result = skill.memory_query(
                query=args.query,
                tags=tags,
                time_range=time_range,
                limit=args.limit
            )
            format_output(result)
        
        elif args.command == 'verify':
            result = skill.memory_verify(
                memory_id=args.memory_id,
                action=args.action,
                correction=args.correction
            )
            format_output(result)
        
        elif args.command == 'list':
            tags = args.tags.split(',') if args.tags else None
            
            result = skill.memory_list(
                tags=tags,
                verified_only=args.verified_only,
                page=args.page,
                page_size=args.page_size
            )
            
            if result['success']:
                lines = [f"📋 共 {result['total']} 条记忆:\n"]
                for r in result.get('results', []):
                    verified = '✅' if r['verified'] else '❓'
                    lines.append(f"{verified} [{r['id'][:8]}] {r['content'][:50]}...")
                if not result.get('results'):
                    lines.append("  （无）")
                result['message'] = '\n'.join(lines)
            
            format_output(result)
        
        elif args.command == 'verify-pending':
            result = skill.memory_verify_get_pending(max_count=args.max)
            format_output(result)
        
        elif args.command == 'verify-result':
            result = skill.memory_verify_result(
                index=args.index,
                action=args.action,
                correction=args.correction
            )
            format_output(result)
        
        elif args.command == 'summarize':
            result = skill.memory_summarize(days=args.days)
            format_output(result)
        
        elif args.command == 'summarize-confirm':
            result = skill.memory_summarize_confirm(feedback=args.feedback)
            format_output(result)
        
        elif args.command == 'stats':
            stats = skill.get_stats()
            
            if stats['success']:
                s = stats['stats']
                message = f"""📊 记忆统计:
- 总数: {s['total']}
- ✅ 已确认: {s['verified']} ({s['verified_rate']})
- ❓ 待确认: {s['unverified']}"""
                
                # 按标签统计
                tag_stats = dedup.get_storage_stats()
                if tag_stats.get('tag_distribution'):
                    message += "\n\n🏷️ 标签分布:"
                    for tag, count in tag_stats['tag_distribution'].items():
                        message += f"\n  - {tag}: {count}"
                
                stats['message'] = message
            
            format_output(stats)
        
        else:
            print(f"未知命令: {args.command}", file=sys.stderr)
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
