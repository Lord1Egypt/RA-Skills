"""
示例：抓取单篇笔记详情（正文 + 评论）
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from xhscosmoskill import XhsClient

NOTE_URL = "https://www.xiaohongshu.com/explore/6912a3c8000000000f03e0a5"

with XhsClient() as xhs:
    note = xhs.get_note_detail(NOTE_URL)

    if note:
        print(f"标题: {note.title}")
        print(f"作者: {note.author}")
        print(f"赞/藏/评: {note.likes}/{note.collects}/{note.comments_count}")
        print(f"正文:\n{note.content}")
        print(f"\n评论 ({len(note.comments)}条):")
        for c in note.comments[:5]:
            print(f"  @{c.user}: {c.text}")
    else:
        print("未能抓取到内容")
