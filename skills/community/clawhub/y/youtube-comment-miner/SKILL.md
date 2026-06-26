# SKILL.md - YouTube Comment Miner

> 通过 YouTube **评论**挖掘用户痛点，发现新产品机会

**别名**: YouTube 评论痛点挖掘机 / YouTube Comment Pain Point Miner

## 🎯 核心价值

| 用途 | 说明 |
|------|------|
| **痛点挖掘** | 从评论中提取用户真实问题 |
| **竞品分析** | 分析竞品视频下的用户反馈 |
| **需求发现** | 识别高频功能请求 |
| **市场调研** | 了解用户对某技术的担忧/期待 |

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 搜索并获取评论 (默认搜索 openclaw)
./scripts/fetch_comments.sh "搜索关键词" 10

# 3. 分析评论
python3 scripts/analyze.py youtube_comments/
```

---

## 完整文档

## 功能

- 搜索指定话题的热门 YouTube 视频
- 获取视频的全部评论
- 分析评论内容，提取问题/建议
- 生成结构化报告

## 前置要求

- `yt-dlp` (带 JavaScript 运行时)
- `youtube-search` Python 包
- Python 3.8+

## 安装依赖

```bash
pip install yt-dlp youtube-search python-dotenv
```

## 使用方法

### 1. 搜索视频

```bash
# 搜索 OpenClaw 相关视频
youtube-search "openclaws" --max 10
```

或使用 yt-dlp：

```bash
yt-dlp "https://www.youtube.com/results?search_query=openclaws" --dump-json --flat-playlist | jq -r '.id' | head -10
```

### 2. 获取视频评论

核心命令（绕过 JS 运行时问题）：

```bash
# 获取单个视频评论
yt-dlp --write-comments --dump-json "VIDEO_URL" > comments.json

# 示例
yt-dlp --write-comments --dump-json "https://www.youtube.com/watch?v=xxxxx" > video_comments.json
```

**关键参数：**
- `--write-comments` - 启用评论抓取
- `--dump-json` - 输出 JSON 格式
- `--extractor-args "youtube:comments=10"` - 获取更多评论

### 3. 批量获取评论

```bash
#!/bin/bash
# fetch_comments.sh

VIDEO_IDS=("video_id_1" "video_id_2" "video_id_3")

for id in "${VIDEO_IDS[@]}"; do
    echo "获取评论: https://youtube.com/watch?v=$id"
    yt-dlp --write-comments --dump-json "https://www.youtube.com/watch?v=$id" > "openclaw_$id.json"
    echo "完成: $id"
done
```

### 4. 分析评论

创建分析脚本 `analyze_comments.py`：

```python
#!/usr/bin/env python3
"""分析 YouTube 评论，提取问题和建议"""
import json
import os
import re
from collections import Counter

def load_comments(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data.get('comments', [])

def categorize_comment(text):
    text_lower = text.lower()
    categories = []
    
    # 问题分类
    if any(k in text_lower for k in ['error', 'fail', 'bug', 'not working', 'stuck', 'cannot', "can't", 'unable', 'crash']):
        categories.append('问题-技术')
    if any(k in text_lower for k in ['install', 'deploy', 'setup', '配置', '部署', '安装']):
        categories.append('问题-安装部署')
    if any(k in text_lower for k in ['security', 'privacy', 'safe', 'hack', 'injection', '安全', '隐私']):
        categories.append('问题-安全')
    if any(k in text_lower for k in ['ollama', 'local', 'model', 'gpu', 'ram', 'cost', 'expensive', 'token']):
        categories.append('问题-成本')
    if any(k in text_lower for k in ['slow', 'performance', 'fast', 'speed']):
        categories.append('问题-性能')
    
    # 建议分类
    if any(k in text_lower for k in ['should', 'would be nice', 'wish', 'hope', 'suggest', '建议', '希望']):
        categories.append('建议-功能')
    if any(k in text_lower for k in ['document', 'tutorial', 'video', 'explain', '文档', '教程']):
        categories.append('建议-文档')
    
    return categories if categories else ['其他']

def analyze_all_comments(folder='.'):
    all_comments = []
    
    for f in os.listdir(folder):
        if f.startswith('openclaw_') and f.endswith('.json') and 'analysis' not in f:
            try:
                comments = load_comments(f)
                all_comments.extend(comments)
            except Exception as e:
                print(f"Error loading {f}: {e}")
    
    # 分类统计
    category_counts = Counter()
    issues = []
    
    for comment in all_comments:
        text = comment.get('text', '')
        cats = categorize_comment(text)
        for cat in cats:
            category_counts[cat] += 1
        if any(c.startswith('问题') for c in cats):
            issues.append({
                'text': text[:300],
                'likes': comment.get('like_count', 0),
                'author': comment.get('author', 'unknown'),
                'categories': cats
            })
    
    # 按点赞排序
    issues.sort(key=lambda x: x['likes'], reverse=True)
    
    return {
        'total_comments': len(all_comments),
        'category_counts': dict(category_counts),
        'issue_examples': issues[:100]
    }

if __name__ == '__main__':
    result = analyze_all_comments('.')
    print(f"总评论数: {result['total_comments']}")
    print(f"\n分类统计:")
    for cat, count in sorted(result['category_counts'].items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    # 保存分析结果
    with open('analysis_result.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\n分析结果已保存到 analysis_result.json")
```

### 5. 运行分析

```bash
python3 analyze_comments.py
```

## 常见问题解决

### 问题：yt-dlp 报错 "Unable to extract JavaScript player"

**原因**：需要 JavaScript 运行时

**解决**：使用 `--write-comments --dump-json` 组合，可以绕过 JS 运行时问题

### 问题：评论数量不全

**解决**：添加 `--extractor-args "youtube:comments=10"` 获取更多评论

### 问题：请求超时

**解决**：
- 增加超时时间：`yt-dlp --socket-timeout 60`
- 分批获取评论

## 输出格式

评论 JSON 结构：
```json
{
  "id": "comment_id",
  "text": "评论内容",
  "like_count": 10,
  "author": "@username",
  "author_thumbnail": "https://...",
  "timestamp": 1234567890,
  "parent": "root" // 或父评论ID
}
```

## 完整工作流示例

```bash
# 1. 搜索视频
youtube-search "openclaws tutorial" --max 10 > videos.txt

# 2. 批量获取评论
while read video; do
    yt-dlp --write-comments --dump-json "$video" > "comments_$(basename $video).json"
done < videos.txt

# 3. 分析评论
python3 analyze_comments.py

# 4. 生成报告
python3 generate_report.py
```

## 💡 产品痛点挖掘指南

### 分析维度

| 维度 | 关键词 | 解读 |
|------|--------|------|
| **安全问题** | security, privacy, hack, injection, vulnerability | 用户担心安全风险 |
| **成本问题** | expensive, cost, token, price, free, $5 | 付费意愿/预算限制 |
| **性能问题** | slow, speed, RAM, GPU, memory | 硬件/性能瓶颈 |
| **易用性问题** | difficult, complex, confusing, setup, install | 学习曲线太陡 |
| **功能缺失** | wish, hope, should, please, feature | 用户期望功能 |

### 输出报告模板

```markdown
# {话题} 用户痛点分析报告

## 📊 数据概览
- 视频数量: X 个
- 评论总数: X 条
- 问题反馈: X 条

## 🔴 Top 问题
1. [安全问题] X 条 - 具体描述...
2. [成本问题] X 条 - 具体描述...
3. [易用性] X 条 - 具体描述...

## 💡 产品机会
- 机会1: ...
- 机会2: ...

## 📋 建议
- 短期: ...
- 长期: ...
```

## 相关工具

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube 下载器
- [youtube-search](https://pypi.org/project/youtube-search/) - 视频搜索
- [yt-dlp-nb](https://github.com/theghostjw/yt-dlp-nb) - 评论专用版本
