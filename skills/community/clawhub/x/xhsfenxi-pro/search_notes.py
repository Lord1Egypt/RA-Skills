"""
示例：搜索关键词，抓取笔记列表 + 详情
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from xhscosmoskill import XhsClient

KEYWORD = "咖啡"
LIMIT = 20

with XhsClient() as xhs:
    print(f"搜索: {KEYWORD}")
    notes = xhs.search(KEYWORD, limit=LIMIT)
    print(f"找到 {len(notes)} 篇笔记")

    for i, n in enumerate(notes[:5], 1):
        print(f"[{i}] {n.title} | 赞:{n.likes} | {n.type}")

    # 补充详情
    print("\n抓取详情...")
    notes = xhs.batch_get_details(notes, delay=1.5)

    xhs.save(notes, "search_results.json")
