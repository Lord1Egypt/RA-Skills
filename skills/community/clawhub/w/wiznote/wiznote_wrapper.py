#!/usr/bin/env python3
"""为知笔记Wrapper - 简化API调用（v2 全协作笔记模式）"""

import sys
import os
import json
import time

sys.path.insert(0, '/root/.openclaw/workspace-zhongshu/skills/wiz-mcp')

from scripts.wiz_open_api import WizOpenApi
from scripts.config import get_config

COMMANDS = {
    'list': '列出笔记',
    'search': '搜索笔记',
    'get': '读取笔记内容',
    'create': '创建笔记（默认协作笔记）',
    'update': '更新笔记（默认协作笔记）',
    'delete': '删除笔记',
    'move': '移动笔记到指定分类',
    'copy': '复制笔记',
    'categories': '列出所有分类',
    'create_category': '创建分类',
    'delete_category': '删除分类',
    'tags': '列出所有标签',
    'add_tags': '添加标签',
    'remove_tags': '移除标签',
    'comments': '获取评论',
    'add_comment': '添加评论',
    'history': '获取历史版本',
    'share': '分享笔记',
    'shares': '列出分享',
    'attachments': '列出附件',
    'upload': '上传附件',
    'template': '从模板创建笔记',
    'templates': '列出可用模板',
    'md2blocks': 'Markdown转blocks预览',
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help', 'help'):
        print("用法: wiznote_wrapper.py <command> [args]\n")
        print("命令列表:")
        for cmd, desc in COMMANDS.items():
            print(f"  {cmd:20s} {desc}")
        return

    config = get_config()
    api = WizOpenApi(config)
    cmd = sys.argv[1]

    try:
        if cmd == 'list':
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            print(json.dumps(api.get_note_list(version=0, count=count), indent=2, ensure_ascii=False))

        elif cmd == 'search':
            assert len(sys.argv) >= 3, "需要搜索关键词"
            print(json.dumps(api.search_notes(keyword=sys.argv[2]), indent=2, ensure_ascii=False))

        elif cmd == 'get':
            assert len(sys.argv) >= 3, "需要笔记GUID"
            result = api.get_note_content(doc_guid=sys.argv[2])
            print(result if isinstance(result, str) else json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'create':
            # create <title> [content] [--category /path/] [--tags tag1,tag2]
            assert len(sys.argv) >= 3, "需要标题"
            title = sys.argv[2]
            content = sys.argv[3] if len(sys.argv) > 3 else ''
            category = '/My Notes/'
            tags = ''
            for i, arg in enumerate(sys.argv):
                if arg == '--category' and i + 1 < len(sys.argv):
                    category = sys.argv[i + 1]
                elif arg == '--tags' and i + 1 < len(sys.argv):
                    tags = sys.argv[i + 1]
            result = api.create_note(title, content, category, tags)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'update':
            # update <doc_guid> [content] [--title new_title]
            assert len(sys.argv) >= 3, "需要笔记GUID"
            doc_guid = sys.argv[2]
            content = sys.argv[3] if len(sys.argv) > 3 else ''
            title = None
            for i, arg in enumerate(sys.argv):
                if arg == '--title' and i + 1 < len(sys.argv):
                    title = sys.argv[i + 1]
            result = api.update_note(doc_guid, content, title)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'delete':
            assert len(sys.argv) >= 3, "需要笔记GUID"
            result = api.delete_note(sys.argv[2])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'move':
            assert len(sys.argv) >= 4, "需要: move <doc_guid> <category>"
            result = api.move_note(sys.argv[2], sys.argv[3])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'copy':
            assert len(sys.argv) >= 3, "需要笔记GUID"
            title = sys.argv[3] if len(sys.argv) > 3 else None
            category = sys.argv[4] if len(sys.argv) > 4 else None
            result = api.copy_note(sys.argv[2], title, category)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'categories':
            print(json.dumps(api.list_categories(), indent=2, ensure_ascii=False))

        elif cmd == 'create_category':
            assert len(sys.argv) >= 4, "需要: create_category <parent> <name>"
            result = api.create_category(sys.argv[2], sys.argv[3])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'delete_category':
            assert len(sys.argv) >= 3, "需要分类路径"
            result = api.delete_category(sys.argv[2])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'tags':
            print(json.dumps(api.list_tags(), indent=2, ensure_ascii=False))

        elif cmd == 'add_tags':
            assert len(sys.argv) >= 4, "需要: add_tags <doc_guid> <tags>"
            result = api.add_tags(sys.argv[2], sys.argv[3])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'remove_tags':
            assert len(sys.argv) >= 4, "需要: remove_tags <doc_guid> <tags>"
            result = api.remove_tags(sys.argv[2], sys.argv[3])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'comments':
            assert len(sys.argv) >= 3, "需要笔记GUID"
            result = api.get_comments(sys.argv[2])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'add_comment':
            assert len(sys.argv) >= 4, "需要: add_comment <doc_guid> <text>"
            result = api.add_comment(sys.argv[2], ' '.join(sys.argv[3:]))
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'history':
            assert len(sys.argv) >= 3, "需要笔记GUID"
            result = api.get_note_history(sys.argv[2])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'share':
            assert len(sys.argv) >= 3, "需要笔记GUID"
            access = sys.argv[3] if len(sys.argv) > 3 else 'read'
            expire = int(sys.argv[4]) if len(sys.argv) > 4 else 30
            result = api.share_note(sys.argv[2], access, expire)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'shares':
            print(json.dumps(api.list_shares(), indent=2, ensure_ascii=False))

        elif cmd == 'attachments':
            assert len(sys.argv) >= 3, "需要笔记GUID"
            result = api.get_note_attachments(sys.argv[2])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'upload':
            assert len(sys.argv) >= 4, "需要: upload <doc_guid> <file_path>"
            result = api.upload_attachment(sys.argv[2], sys.argv[3])
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'template':
            assert len(sys.argv) >= 3, "需要模板名称"
            template = sys.argv[2]
            title = sys.argv[3] if len(sys.argv) > 3 else f'新建{template}'
            category = sys.argv[4] if len(sys.argv) > 4 else '/My Notes/'
            result = api.create_from_template(template, title, category)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif cmd == 'templates':
            print("可用模板:")
            for t in ['weekly_report', 'meeting_minutes', 'todo', 'reading_notes', 'project_plan', 'blank']:
                print(f"  - {t}")

        elif cmd == 'md2blocks':
            assert len(sys.argv) >= 3, "需要Markdown内容"
            md = ' '.join(sys.argv[2:])
            blocks = api.markdown_to_blocks(md)
            print(json.dumps(blocks, indent=2, ensure_ascii=False))

        else:
            print(f"未知命令: {cmd}\n可用命令: {', '.join(COMMANDS.keys())}")

    except AssertionError as e:
        print(f"参数错误: {e}")
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
