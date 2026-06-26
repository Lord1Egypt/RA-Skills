#!/usr/bin/env python3
"""
更新印象笔记
用法: python update_note.py --guid "笔记GUID" --title "新标题"
       python update_note.py --guid "笔记GUID" --content "<en-note>新内容</en-note>"
       python update_note.py --guid "笔记GUID" --add-tags "标签1,标签2"
       python update_note.py --guid "笔记GUID" --remove-tags "标签3"
       python update_note.py --guid "笔记GUID" --title "新标题" --content "<en-note>新内容</en-note>" --add-tags "标签1,标签2"
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


def get_note(note_store, token, guid):
    """获取笔记"""
    return note_store.getNote(token, guid, True, False, False, False)


def get_tag_guid_by_name(note_store, token, tag_name):
    """根据标签名获取 GUID"""
    tags = note_store.listTags(token)
    for tag in tags:
        if tag.name == tag_name:
            return tag.guid
    return None


def update_note(guid, title=None, content=None, add_tags=None, remove_tags=None):
    """更新笔记"""
    token, note_store_url = load_config()

    if not token:
        print("❌ 错误: 未找到 EVERNOTE_TOKEN")
        return None

    if not note_store_url:
        note_store_url = "https://app.yinxiang.com/shard/s16/notestore"

    print(f"🔄 正在连接印象笔记...")

    transport = THttpClient.THttpClient(note_store_url)
    transport.setCustomHeaders({"Authorization": f"Bearer {token}"})
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    note_store = NoteStore.Client(protocol)

    print("✅ 连接成功")
    print()

    # 获取原笔记
    try:
        original = get_note(note_store, token, guid)
        print(f"📝 当前笔记: {original.title}")
    except Exception as e:
        print(f"❌ 获取笔记失败: {e}")
        return None

    # 构建更新对象
    update_note = Types.Note()
    update_note.guid = guid
    update_note.title = original.title
    update_note.content = original.content if content is None else content
    update_note.tagGuids = list(original.tagGuids) if original.tagGuids else []

    # 添加标签
    if add_tags:
        for tag_name in add_tags:
            tag_guid = get_tag_guid_by_name(note_store, token, tag_name)
            if tag_guid and tag_guid not in update_note.tagGuids:
                update_note.tagGuids.append(tag_guid)
                print(f"   🏷️ +添加标签: {tag_name}")
            elif not tag_guid:
                print(f"   ⚠️ 标签不存在: {tag_name}")

    # 移除标签
    if remove_tags:
        for tag_name in remove_tags:
            tag_guid = get_tag_guid_by_name(note_store, token, tag_name)
            if tag_guid and tag_guid in update_note.tagGuids:
                update_note.tagGuids.remove(tag_guid)
                print(f"   🏷️ -移除标签: {tag_name}")

    if title:
        update_note.title = title
        print(f"   📝 新标题: {title}")

    if content:
        print(f"   📄 内容已更新")

    try:
        result = note_store.updateNote(token, update_note)
        print(f"\n✅ 更新成功!")
        print(f"   GUID: {result.guid}")
        print(f"   更新时间: {result.updated}")
        return result
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == '__main__':
    args = sys.argv[1:]

    guid = None
    title = None
    content = None
    add_tags = None
    remove_tags = None

    i = 0
    while i < len(args):
        if args[i] == '--guid' and i + 1 < len(args):
            guid = args[i + 1]
            i += 2
        elif args[i] == '--title' and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == '--content' and i + 1 < len(args):
            content = args[i + 1]
            i += 2
        elif args[i] == '--add-tags' and i + 1 < len(args):
            add_tags = [t.strip() for t in args[i + 1].split(',')]
            i += 2
        elif args[i] == '--remove-tags' and i + 1 < len(args):
            remove_tags = [t.strip() for t in args[i + 1].split(',')]
            i += 2
        else:
            i += 1

    if not guid:
        print("用法: python update_note.py --guid \"笔记GUID\" [--title \"新标题\"] [--content \"<en-note>内容</en-note>\"] [--add-tags \"标签1,标签2\"] [--remove-tags \"标签3\"]")
        sys.exit(1)

    update_note(guid, title, content, add_tags, remove_tags)
