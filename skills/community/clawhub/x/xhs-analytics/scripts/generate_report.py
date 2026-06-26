#!/usr/bin/env python3
"""
小红书数据分析 - 报告生成
用法: python3 generate_report.py --keyword "关键词" --output report.md
"""

import argparse
import json
import os
import sys

# 导入其他脚本
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_config():
    config = {}
    config['api_key'] = os.environ.get('XHS_API_KEY', '')
    config['cookie'] = os.environ.get('XHS_COOKIE', '')
    return config

def generate_report(keyword, output_file, report_format='markdown'):
    """生成分析报告"""
    config = load_config()
    
    # 搜索笔记
    from search_notes import search_notes
    notes = search_notes(keyword, limit=50)
    
    # 计算统计数据
    total_likes = sum(n.get('likes', 0) for n in notes)
    total_collects = sum(n.get('收藏', 0) for n in notes)
    total_comments = sum(n.get('comments', 0) for n in notes)
    
    avg_likes = total_likes / len(notes) if notes else 0
    avg_collects = total_collects / len(notes) if notes else 0
    
    # 生成报告
    report = f"""# 📊 小红书数据分析报告

**关键词**: {keyword}  
**生成时间**: {sys.argv[2] if len(sys.argv) > 2 else 'N/A'}

---

## 📈 数据概览

| 指标 | 数值 |
|------|------|
| 笔记总数 | {len(notes)} |
| 总点赞 | {total_likes:,} |
| 总收藏 | {total_collects:,} |
| 总评论 | {total_comments:,} |
| 平均点赞 | {avg_likes:.0f} |
| 平均收藏 | {avg_collects:.0f} |

---

## 🔥 热门笔记 TOP 10

| 排名 | 标题 | 作者 | 点赞 | 收藏 |
|------|------|------|------|------|
"""
    
    # 排序取TOP10
    sorted_notes = sorted(notes, key=lambda x: x.get('likes', 0), reverse=True)[:10]
    
    for i, note in enumerate(sorted_notes, 1):
        report += f"| {i} | {note.get('title', 'N/A')[:30]} | {note.get('author', 'N/A')} | {note.get('likes', 0):,} | {note.get('收藏', 0):,} |\n"
    
    report += f"""

---

## 📝 分析结论

1. **热度分析**: "{keyword}" 相关笔记平均点赞约 {avg_likes:.0f}，属于{'热门' if avg_likes > 500 else '中等'}领域

2. **内容建议**:
   - 参考 TOP 10 笔记的标题风格
   - 关注热门标签: {', '.join(notes[0].get('tags', ['无'])[:5]) if notes else '无'}

3. **发布时间**: 建议在工作日 18:00-22:00 或周末发布

---

## ⚠️ 注意事项

- 数据为示例数据，实际使用请配置有效的 API 密钥
- 数据可能有延迟，建议交叉验证

---

*报告由帕瓦的小红书分析技能生成* 🤖
"""
    
    # 保存报告
    if output_file:
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到: {output_file}")
    else:
        print(report)

def main():
    parser = argparse.ArgumentParser(description='小红书分析报告生成')
    parser.add_argument('--keyword', '-k', required=True, help='分析关键词')
    parser.add_argument('--output', '-o', default='report.md', help='输出文件')
    parser.add_argument('--format', '-f', default='markdown', choices=['markdown', 'json'], help='输出格式')
    parser.add_argument('--limit', '-l', type=int, default=50, help='分析笔记数量')
    
    args = parser.parse_args()
    
    generate_report(args.keyword, args.output, args.format)

if __name__ == '__main__':
    main()
