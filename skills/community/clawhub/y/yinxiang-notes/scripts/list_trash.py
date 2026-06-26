#!/usr/bin/env python3
"""
查看废纸篓中的笔记
用法: python list_trash.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import evernote.edam.notestore.NoteStore as NoteStore
import thrift.transport.THttpClient as THttpClient
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
from datetime import datetime


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


def list_trash():
    """列出废纸篓中的笔记"""
    token, note_store_url = load_config()

    if not token:
        print("❌ 错误: 未找到 EVERNOTE_TOKEN")
        return []

    if not note_store_url:
        note_store_url = "https://app.yinxiang.com/shard/s16/notestore"

    print(f"🔄 正在连接印象笔记...")

    transport = THttpClient.THttpClient(note_store_url)
    transport.setCustomHeaders({"Authorization": f"Bearer {token}"})
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    note_store = NoteStore.Client(protocol)

    print("✅ 连接成功")
    print()

    deleted_notes = []
    offset = 0
    page_size = 100

    while True:
        try:
            result = note_store.findNotesMetadata(
                token,
                NoteStore.NoteFilter(),
                offset,
                page_size,
                NoteStore.NotesMetadataResultSpec(includeTitle=True, includeDeleted=True, includeCreated=True)
            )

            if not result.notes:
                break

            for note in result.notes:
                if hasattr(note, 'deleted') and note.deleted and note.deleted > 0:
                    deleted_notes.append(note)

            offset += page_size
            if offset >= result.totalNotes or len(deleted_notes) >= 500:
                break

        except Exception as e:
            print(f"❌ 扫描出错: {e}")
            break

    print(f"{'='*60}")
    print(f"🗑️  废纸篓 (共 {len(deleted_notes)} 条)")
    print(f"{'='*60}")
    print()

    if not deleted_notes:
        print("✅ 废纸篓是空的")
        return []

    for i, note in enumerate(deleted_notes, 1):
        dt = datetime.fromtimestamp(note.deleted / 1000)
        date_str = dt.strftime('%Y-%m-%d %H:%M')
        print(f"{i}. {note.title}")
        print(f"   删除时间: {date_str}")
        print(f"   GUID: {note.guid}")
        print()

    return deleted_notes


if __name__ == '__main__':
    list_trash()
