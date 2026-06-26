#!/usr/bin/env python3
"""
删除印象笔记（移至废纸篓）
用法: python delete_note.py --guid "笔记GUID"
       python delete_note.py --guid "笔记GUID" --confirm
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import evernote.edam.notestore.NoteStore as NoteStore
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


def get_note_title(note_store, token, guid):
    """获取笔记标题"""
    try:
        note = note_store.getNote(token, guid, False, False, False, False)
        return note.title
    except Exception:
        return None


def delete_note(guid, confirm=True):
    """删除笔记（移至废纸篓，客户端清空废纸篓后永久删除）"""
    token, note_store_url = load_config()

    if not token:
        print("❌ 错误: 未找到 EVERNOTE_TOKEN")
        return False

    if not note_store_url:
        note_store_url = "https://app.yinxiang.com/shard/s16/notestore"

    print(f"🔄 正在连接印象笔记...")

    transport = THttpClient.THttpClient(note_store_url)
    transport.setCustomHeaders({"Authorization": f"Bearer {token}"})
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    note_store = NoteStore.Client(protocol)

    print("✅ 连接成功")
    print()

    # 先获取笔记标题
    title = get_note_title(note_store, token, guid)
    if not title:
        print(f"❌ 未找到笔记 GUID: {guid}")
        return False

    print(f"📝 准备删除笔记: {title}")
    print(f"   GUID: {guid}")
    print()

    if not confirm:
        print("⚠️ 未指定 --confirm 参数，取消删除")
        return False

    print("🗑️  将笔记移至废纸篓...")

    try:
        note_store.deleteNote(token, guid)
        print(f"\n✅ 删除成功！笔记已移至废纸篓")
        print(f"   标题: {title}")
        print(f"   GUID: {guid}")
        print()
        print("💡 提示：笔记已进入废纸篓，在印象笔记客户端中清空废纸篓才会永久删除")
        return True
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    args = sys.argv[1:]

    guid = None
    confirm = False

    i = 0
    while i < len(args):
        if args[i] == '--guid' and i + 1 < len(args):
            guid = args[i + 1]
            i += 2
        elif args[i] == '--confirm':
            confirm = True
            i += 1
        else:
            i += 1

    if not guid:
        print("用法: python delete_note.py --guid \"笔记GUID\" [--confirm]")
        print()
        print("示例:")
        print("  python delete_note.py --guid \"xxx-yyy-zzz\"          # 预览（不删除）")
        print("  python delete_note.py --guid \"xxx-yyy-zzz\" --confirm  # 确认删除")
        sys.exit(1)

    delete_note(guid, confirm)
