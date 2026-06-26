"""
示例：抓取指定用户所有笔记（含详情）
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from xhscosmoskill import XhsClient

# A 荒诞美学代表的用户 ID
USER_ID = "USER_ID_HEX_HERE"

with XhsClient(scroll_times=8) as xhs:
    print(f"抓取用户主页: {USER_ID}")
    notes = xhs.get_user_notes(USER_ID, limit=100)
    print(f"列表: {len(notes)} 篇")

    print("\n抓取每篇详情...")
    notes = xhs.batch_get_details(notes, delay=2.0)

    xhs.save(notes, f"user_{USER_ID}.json")
    print(f"\n完成，正文有内容: {len([n for n in notes if n.content])} 篇")
