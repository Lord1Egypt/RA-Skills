# 卡片学习法 - 高级功能

## 批量操作

### 批量导入 Markdown 文件

```python
# 将现有笔记导入系统
import os
from pathlib import Path

source_dir = Path("~/old-notes")
cards_dir = Path("~/Desktop/cardsdata")

for md_file in source_dir.glob("*.md"):
    # 读取内容
    content = md_file.read_text()
    
    # 创建为永久笔记
    result = create_note(
        "permanent",
        title=md_file.stem,
        content=content,
        tags=["imported"]
    )
    print(f"导入: {result['id']}")
```

### 批量导出

```python
# 按标签导出
notes = search_notes("#时间管理")
for note in notes:
    print(f"[[{note['id']}]] {note['title']}")
```

## 知识图谱

### 生成链接图谱

```bash
# 提取所有链接关系
grep -r "^links:" ~/Desktop/cardsdata/zettel/ > links.txt

# 用 Python 生成 Graphviz DOT
cat links.txt | python3 -c "
import json, re, sys
print('digraph Zettelkasten {')
for line in sys.stdin:
    # 解析链接
    pass
print('}')
" > graph.dot

# 生成可视化
dot -Tpng graph.dot -o graph.png
```

## 标签统计

```python
from collections import Counter
import re

def get_all_tags():
    tags = Counter()
    for folder in ['zettel', 'lit', 'project']:
        folder_path = CARDS_DIR / folder
        for f in folder_path.glob("*.md"):
            content = f.read_text()
            # 提取 frontmatter 中的 tags
            match = re.search(r'^tags: (.+)$', content, re.MULTILINE)
            if match:
                try:
                    tag_list = json.loads(match.group(1))
                    tags.update(tag_list)
                except:
                    pass
    return tags

# 输出标签云
tags = get_all_tags()
for tag, count in tags.most_common(20):
    print(f"{tag}: {'#' * count}")
```

## 自动归档策略

### 清理过期闪念笔记

```python
def archive_old_fleeting(days=7):
    """归档超过N天的闪念笔记"""
    inbox = CARDS_DIR / "inbox"
    archive = CARDS_DIR / ".system" / "archive"
    archive.mkdir(exist_ok=True)
    
    from datetime import datetime, timedelta
    cutoff = datetime.now() - timedelta(days=days)
    
    for f in inbox.glob("*.md"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            f.rename(archive / f.name)
            print(f"归档: {f.name}")
```

### 清理孤儿笔记

```python
def find_orphan_notes():
    """查找没有入链的笔记"""
    # 收集所有链接
    all_links = set()
    for folder in ['zettel', 'lit', 'project']:
        for f in (CARDS_DIR / folder).glob("*.md"):
            content = f.read_text()
            # 提取 [[ID]] 格式的链接
            links = re.findall(r'\[\[(\d{8}-\d{4})\]\]', content)
            all_links.update(links)
    
    # 检查哪些笔记没有被链接
    orphans = []
    for folder in ['zettel']:
        for f in (CARDS_DIR / folder).glob("*.md"):
            note_id = f.stem[:13]  # 提取 ID 部分
            if note_id not in all_links:
                orphans.append(note_id)
    
    return orphans
```

## 与外部工具集成

### Obsidian 兼容

卡片系统使用标准 Markdown + YAML frontmatter，可直接用 Obsidian 打开：

```bash
# 在 Obsidian 中打开
open ~/Desktop/cardsdata
```

### Git 版本控制

```bash
cd ~/Desktop/cardsdata
git init
git add .
git commit -m "Initial zettelkasten"

# 定期备份
git add . && git commit -m "Daily backup $(date +%Y-%m-%d)"
```

## 搜索增强

### 使用 ripgrep 快速搜索

```bash
# 搜索标题
rg "^# " ~/Desktop/cardsdata/zettel/

# 搜索特定标签
rg "tags:.*时间管理" ~/Desktop/cardsdata/

# 搜索未完成的待办
rg "- \[ \]" ~/Desktop/cardsdata/project/
```

### 使用 fzf 交互式选择

```bash
# 列出所有笔记并选择
find ~/Desktop/cardsdata -name "*.md" | fzf --preview 'head -20 {}'
```
