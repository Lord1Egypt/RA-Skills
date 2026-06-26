#!/usr/bin/env python3
"""
每日发布脚本：从队列发布论文到网站

功能:
1. 从 pending-papers.json 选取指定数量论文
2. 复制对应图片到发布目录
3. 更新 paper-index.json
4. 更新网站版本号
"""

import json
import os
import shutil
from datetime import datetime

# ============ 配置区域 ============
PENDING_FILE = "pending-papers.json"
INDEX_FILE = "paper-index.json"
PUBLISH_COUNT = 5  # 每次发布数量
# ==================================

def main():
    print("=" * 50)
    print(" 每日发布脚本")
    print("=" * 50)
    print(f"发布数量: {PUBLISH_COUNT}")
    print()
    
    # 检查队列
    if not os.path.exists(PENDING_FILE):
        print("错误: 队列文件不存在")
        return
    
    with open(PENDING_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
    
    pending_papers = queue.get("papers", [])
    
    if len(pending_papers) < PUBLISH_COUNT:
        print(f"警告: 队列仅剩 {len(pending_papers)} 篇论文")
        publish_count = len(pending_papers)
    else:
        publish_count = PUBLISH_COUNT
    
    if publish_count == 0:
        print("队列已空，跳过发布")
        return
    
    # 选取要发布的论文
    to_publish = pending_papers[:publish_count]
    remaining = pending_papers[publish_count:]
    
    print(f"准备发布 {publish_count} 篇论文:")
    for i, p in enumerate(to_publish, 1):
        print(f"  {i}. {p.get('chineseTitle', p.get('title', 'Unknown'))[:40]}...")
    
    # 更新 paper-index.json
    index_data = {
        "updateTime": datetime.now().isoformat(),
        "papers": to_publish
    }
    
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n已发布到 {INDEX_FILE}")
    
    # 更新队列
    queue["papers"] = remaining
    queue["updateTime"] = datetime.now().isoformat()
    
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)
    
    print(f"队列剩余 {len(remaining)} 篇论文")
    
    # 更新版本号（用于缓存刷新）
    version_file = "version.txt"
    with open(version_file, "w") as f:
        f.write(datetime.now().strftime("%Y%m%d%H%M"))
    
    print(f"版本号已更新")
    print("=" * 50)

if __name__ == "__main__":
    main()
