#!/usr/bin/env python3
"""
创建印象笔记
用法: python create_note.py --title "标题" --content "<en-note>内容</en-note>"
       python create_note.py --title "标题" --content "<en-note>内容</en-note>" --notebook "笔记本名"
       python create_note.py --title "标题" --content "<en-note>内容</en-note>" --tags "标签1,标签2"
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import thrift.transport.THttpClient as THttpClient
import thrift.protocol.TBinaryProtocol as TBinaryProtocol


def load_config():
    """从 .env 文件加载配置"""
    script_dir = os.path.dirname(__file__)
    skill_dir = os.path.dirname(script_dir)
    skills_dir = os.path.dirname(skill_dir)
    workspace_dir = os.path.dirname(skills_dir)
    env_path = os.path.join(workspace_dir, '.env')

    token = None
    note_store_url = None

    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('EVERNOTE_TOKEN='):
                    token = line.split('=', 1)[1].strip()
                elif line.startswith('EVERNOTE_NOTESTORE_URL='):
                    note_store_url = line.split('=', 1)[1].strip()

    return token, note_store_url


def get_notebook_guid(note_store, token, notebook_name):
    """根据笔记本名获取 GUID"""
    notebooks = note_store.listNotebooks(token)
    for nb in notebooks:
        if nb.name == notebook_name:
            return nb.guid
    return None


def get_tag_guids(note_store, token, tag_names):
    """根据标签名列表获取 GUID 列表"""
    if not tag_names:
        return []
    tags = note_store.listTags(token)
    tag_guids = []
    for name in tag_names:
        for tag in tags:
            if tag.name == name:
                tag_guids.append(tag.guid)
                break
    return tag_guids


def create_note(title, content, notebook_name=None, tag_names=None):
    """创建笔记"""
    token, note_store_url = load_config()

    if not token:
        print("❌ 错误: 未找到 EVERNOTE_TOKEN")
        return None

    if not note_store_url:
        note_store_url = "https://app.yinxiang.com/shard/s16/notestore"

    print(f"🔄 正在连接印象笔记...")
    print(f"✅ Token: {token[:25]}...")

    transport = THttpClient.THttpClient(note_store_url)
    transport.setCustomHeaders({"Authorization": f"Bearer {token}"})
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    note_store = NoteStore.Client(protocol)

    print("✅ 连接成功")
    print()

    # 构建笔记
    note = Types.Note()
    note.title = title
    note.content = content

    # 设置笔记本
    if notebook_name:
        guid = get_notebook_guid(note_store, token, notebook_name)
        if guid:
            note.notebookGuid = guid
            print(f"📓 目标笔记本: {notebook_name}")
        else:
            print(f"⚠️ 未找到笔记本 '{notebook_name}'，将使用默认笔记本")

    # 设置标签
    if tag_names:
        tag_guids = get_tag_guids(note_store, token, tag_names)
        if tag_guids:
            note.tagGuids = tag_guids
            print(f"🏷️ 标签: {', '.join(tag_names)}")

    print(f"📝 创建笔记: {title}")

    try:
        result = note_store.createNote(token, note)
        print(f"✅ 创建成功!")
        print(f"   GUID: {result.guid}")
        print(f"   创建时间: {result.created}")
        return result
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == '__main__':
    args = sys.argv[1:]

    title = None
    content = None
    notebook = None
    tags = None

    i = 0
    while i < len(args):
        if args[i] == '--title' and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == '--content' and i + 1 < len(args):
            content = args[i + 1]
            i += 2
        elif args[i] == '--notebook' and i + 1 < len(args):
            notebook = args[i + 1]
            i += 2
        elif args[i] == '--tags' and i + 1 < len(args):
            tags = [t.strip() for t in args[i + 1].split(',')]
            i += 2
        else:
            i += 1

    if not title or not content:
        print("用法: python create_note.py --title \"标题\" --content \"<en-note>内容</en-note>\"")
        print("       python create_note.py --title \"标题\" --content \"<en-note>内容</en-note>\" --notebook \"笔记本名\"")
        print("       python create_note.py --title \"标题\" --content \"<en-note>内容</en-note>\" --tags \"标签1,标签2\"")
        sys.exit(1)

    create_note(title, content, notebook, tags)
