#!/usr/bin/env python3
"""下载指定笔记的原始 ENML 内容"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from list_notebooks import load_config
import evernote.edam.notestore.NoteStore as NoteStore
import thrift.transport.THttpClient as THttpClient
import thrift.protocol.TBinaryProtocol as TBinaryProtocol

TARGET_GUID = "97701f2b-0a68-468c-bb09-7fe646b521ce"
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "note_enml_output.xml")

def main():
    token, note_store_url = load_config()
    if not token:
        print("❌ 错误: 未找到 EVERNOTE_TOKEN")
        return

    transport = THttpClient.THttpClient(note_store_url)
    transport.setCustomHeaders({"Authorization": f"Bearer {token}"})
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    note_store = NoteStore.Client(protocol)

    print(f"📥 获取笔记: {TARGET_GUID}")

    try:
        note = note_store.getNote(token, TARGET_GUID, True, True, False, False)
    except Exception as e:
        print(f"❌ 获取笔记失败: {e}")
        return

    print(f"标题: {note.title}")
    print(f"内容长度: {len(note.content)} 字符")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(note.content)

    print(f"✅ 已保存到: {OUTPUT_FILE}")

    content = note.content

    has_doctype = '<!DOCTYPE' in content.upper()
    has_html_tags = '<html' in content.lower()
    has_head = '<head' in content.lower()
    has_body = '<body' in content.lower()
    has_en_note = '<en-note' in content.lower()
    en_clipped = '--en-clipped-content' in content

    div_count = content.count('<div')
    span_count = content.count('<span')
    p_count = content.count('<p')

    print("\n📊 内容结构分析:")
    print(f"  - DOCTYPE: {'✅' if has_doctype else '❌'}")
    print(f"  - <html> 标签: {'✅' if has_html_tags else '❌'}")
    print(f"  - <head> 标签: {'✅' if has_head else '❌'}")
    print(f"  - <body> 标签: {'✅' if has_body else '❌'}")
    print(f"  - <en-note> 标签: {'✅' if has_en_note else '❌'}")
    print(f"  - --en-clipped-content: {'✅' if en_clipped else '❌'}")
    print(f"\n  - <div> 标签数量: {div_count}")
    print(f"  - <span> 标签数量: {span_count}")
    print(f"  - <p> 标签数量: {p_count}")

    if has_html_tags and has_head and has_body:
        print("\n🔍 结论: 这是【完整的HTML文档】结构")
    elif has_en_note:
        print("\n🔍 结论: 这是【印象笔记 ENML 格式】")
    else:
        print("\n🔍 结论: 这是【简单文本/片段】")

if __name__ == "__main__":
    main()
