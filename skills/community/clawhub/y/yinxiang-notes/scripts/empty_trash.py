#!/usr/bin/env python3
"""
清空印象笔记废纸篓（永久删除所有废纸篓中的笔记）
用法: python empty_trash.py
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


def find_deleted_notes(note_store, token, max_count=500):
    """通过遍历所有笔记找到已删除的笔记"""
    deleted = []
    offset = 0
    page_size = 100

    while True:
        result = note_store.findNotesMetadata(
            token,
            NoteStore.NoteFilter(),
            offset,
            page_size,
            NoteStore.NotesMetadataResultSpec(includeTitle=True, includeDeleted=True)
        )

        if not result.notes:
            break

        for note in result.notes:
            # 检查笔记是否有 deleted 属性且不为0
            if hasattr(note, 'deleted') and note.deleted and note.deleted > 0:
                deleted.append(note)

        offset += page_size
        if offset >= result.totalNotes or offset >= max_count:
            break

    return deleted


def empty_trash():
    """清空废纸篓"""
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

    print("🔍 扫描废纸篓中的笔记...")
    deleted_notes = find_deleted_notes(note_store, token)

    print(f"📋 废纸篓中共有 {len(deleted_notes)} 条笔记")
    print()

    if len(deleted_notes) == 0:
        print("✅ 废纸篓已是空的")
        return True

    for note in deleted_notes:
        print(f"  🗑️  {note.title}")

    print()
    print("⚠️  即将永久删除所有废纸篓中的笔记...")
    print()

    count = 0
    for note in deleted_notes:
        try:
            note_store.expungeNote(token, note.guid)
            count += 1
            print(f"  ✅ 永久删除: {note.title}")
        except Exception as e:
            print(f"  ❌ 删除失败: {note.title} - {e}")

    print()
    print(f"✅ 清空完成！共永久删除 {count} 条笔记")
    return True


if __name__ == '__main__':
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print("用法: python empty_trash.py")
        print()
        print("⚠️  注意：此操作会永久删除废纸篓中的所有笔记，无法恢复！")
        sys.exit(0)

    print("=" * 60)
    print("🗑️  清空印象笔记废纸篓")
    print("=" * 60)
    print()
    print("⚠️  警告：此操作将永久删除废纸篓中的所有笔记！")
    print("   按 Ctrl+C 取消，或关闭此窗口退出。")
    print()
    input("按 Enter 键继续...")

    empty_trash()
