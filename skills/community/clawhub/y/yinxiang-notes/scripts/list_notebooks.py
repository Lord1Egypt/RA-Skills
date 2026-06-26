#!/usr/bin/env python3
"""
获取印象笔记笔记本列表
直接使用 NoteStore URL
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


def list_notebooks(verbose=False):
    """获取并显示笔记本列表"""
    print("🔄 正在连接印象笔记...")
    print()

    try:
        token, note_store_url = load_config()
        
        if not token:
            print("❌ 错误: 未找到 EVERNOTE_TOKEN")
            sys.exit(1)
        
        if not note_store_url:
            print("❌ 错误: 未找到 EVERNOTE_NOTESTORE_URL")
            print("请在 .env 文件中设置: EVERNOTE_NOTESTORE_URL=https://app.yinxiang.com/shard/s16/notestore")
            sys.exit(1)
        
        print(f"✅ Token 已加载: {token[:25]}...")
        print(f"✅ NoteStore URL: {note_store_url}")
        print()

        # 直接连接 NoteStore
        transport = THttpClient.THttpClient(note_store_url)
        transport.setCustomHeaders({"Authorization": f"Bearer {token}"})
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        note_store = NoteStore.Client(protocol)

        print("✅ 成功连接到 NoteStore")
        print()

        # 获取笔记本列表
        notebooks = note_store.listNotebooks(token)

        print(f"📓 笔记本列表 (共 {len(notebooks)} 个):\n")

        for i, notebook in enumerate(notebooks, 1):
            print(f"{i}. {notebook.name}")
            
            if verbose:
                try:
                    # 获取笔记数量
                    filter = NoteStore.NoteFilter(notebookGuid=notebook.guid)
                    result = note_store.findNotesMetadata(token, filter,
                        NoteStore.NotesMetadataResultSpec(includeTitle=True), 0, 1)
                    print(f"   └─ 笔记数量: {result.totalNotes}")
                except Exception as e:
                    print(f"   └─ 无法获取笔记数量: {e}")

        print("\n✅ 连接成功!")
        return notebooks

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    list_notebooks(verbose=verbose)
