import json
import os
import sys
from datetime import datetime

# Windows 中文控制台 UTF-8 修复
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

output_dir = r'C:\Users\beyon\.openclaw\workspace-dapingxia\skills\walter-info\output'
date_str = datetime.now().strftime("%Y%m%d")
json_path = os.path.join(output_dir, f"news_report_{date_str}.json")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# LLM 生成的摘要
llm_summaries = {
    "https://www.cifnews.com/article/184880": (
        "调研181家年销超20亿美元的跨境卖家，近四成利润下滑、38%陷入困境；"
        "亚马逊仍占绝对主导（82%首选平台），TikTok Shop成新兴增长渠道。"
    ),
    "https://www.cifnews.com/article/184883": (
        "穿戴甲按面积计价超越北京海淀区房价，2023-2024年搜索量同比增长超200%；"
        "深圳卖家通过TikTok社交电商出口穿戴甲，年收入最高达3千万美元。"
    ),
    "https://www.cifnews.com/article/184882": (
        "深圳税务向多家国际货代下发核查通知，锁定2025年8月至2026年3月开票及申报数据；"
        "要求4月3日前完成自查补税，部分企业借「包税」绕过6%增值税的漏洞被重点关注。"
    ),
    "https://www.cifnews.com/article/184881": (
        "美法院密集立案多起跨境电商侵权诉讼，超251个店铺收到临时限制令（TRO），"
        "涉及游戏IP、装饰图案、原创插画等热门类目，Yasmin Khalifa、Carolina-Clair等知名品牌批量维权。"
    ),
}

updated = 0
for item in data["data"]:
    url = item.get("url", "")
    if url in llm_summaries and item.get("source") == "cifnews":
        item["description"] = llm_summaries[url]
        item["summary_type"] = "llm"
        updated += 1
        print(f"Updated: {item['title'][:40]}")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nJSON updated: {updated} articles")

# Rebuild Markdown
news_data = data["data"]
lines = ["# 跨境电商热点资讯\n"]
lines.append(f"**获取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
lines.append(f"**数据来源**: ennews / cifnews\n")
lines.append(f"**当日资讯数量**: {len(news_data)} 条（LLM 摘要）\n\n")

for i, item in enumerate(news_data, 1):
    title = item.get("title", "")
    if not title:
        continue
    lines.append(f"### {i}. {title}\n")
    pub = item.get("published_at", "")
    if pub:
        lines.append(f"**发布时间**: {pub}\n")
    source = item.get("source", "")
    if source:
        lines.append(f"**来源**: {source}\n")
    desc = item.get("description", "")
    if desc:
        lines.append(f"**概要**: {desc}\n")
    url = item.get("url", "")
    if url:
        lines.append(f"**链接**: {url}\n")
    score = item.get("impact_score", 0)
    lines.append(f"**权重分**: {score}\n")
    lines.append("\n")

md_path = os.path.join(output_dir, f"news_report_{date_str}.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("".join(lines))
print(f"Markdown saved: {md_path}")

# Clean up llm_input
llm_input = os.path.join(output_dir, f"llm_input_{date_str}.json")
if os.path.exists(llm_input):
    os.remove(llm_input)
    print(f"Cleaned: {llm_input}")

print("\nDone.")
