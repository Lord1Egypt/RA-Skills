#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书热榜日报 v3.0 - 使用浏览器获取真实数据
作者: 小天🦞
版本: 3.0.0
"""

import argparse
import json
import subprocess
import sys
import os
from datetime import datetime
from typing import List, Dict

# 设置控制台编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class XiaohongshuHotFetcher:
    """小红书热门笔记抓取器 v3.0 - 浏览器方式"""

    def __init__(self):
        self.url = 'https://www.xiaohongshu.com/explore'
        self.js_code = """
        (() => {
            const notes = [];
            document.querySelectorAll('section.note-item').forEach((el, i) => {
                if (i >= MAX_ITEMS) return;
                const titleEl = el.querySelector('.title') || el.querySelector('.desc');
                const title = titleEl ? titleEl.textContent.trim() : '';
                const authorEl = el.querySelector('.author-wrapper .name') || el.querySelector('.author .name');
                const author = authorEl ? authorEl.textContent.trim() : '';
                const likeEl = el.querySelector('.like-wrapper .count') || el.querySelector('.like-count');
                const likes = likeEl ? likeEl.textContent.trim() : '';
                const linkEl = el.querySelector('a');
                const link = linkEl ? linkEl.href : '';
                if (title) notes.push({
                    rank: notes.length + 1,
                    title: title,
                    author: author,
                    likes: likes,
                    url: link
                });
            });
            return JSON.stringify(notes);
        })()
        """

    def fetch_hot(self, top: int = 10) -> List[Dict]:
        """获取热门笔记 - 使用 agent-browser"""
        js_code = self.js_code.replace('MAX_ITEMS', str(top))
        
        # 使用 agent-browser 获取数据
        try:
            # 打开页面
            subprocess.run(
                ['agent-browser', 'open', self.url],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            # 等待页面加载
            subprocess.run(
                ['agent-browser', 'wait', '2000'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # 执行 JS 获取数据
            result = subprocess.run(
                ['agent-browser', 'eval', js_code, '--json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                notes = json.loads(data.get('data', {}).get('value', '[]'))
                return self._format_notes(notes)
            else:
                print(f"[WARN] agent-browser 执行失败: {result.stderr}", file=sys.stderr)
                return self._get_fallback_data(top)
                
        except Exception as e:
            print(f"[WARN] 浏览器获取失败: {e}", file=sys.stderr)
            return self._get_fallback_data(top)

    def _format_notes(self, notes: List[Dict]) -> List[Dict]:
        """格式化笔记数据"""
        formatted = []
        for note in notes:
            likes = note.get('likes', '0')
            # 转换点赞数
            likes_num = self._parse_likes(likes)
            formatted.append({
                'rank': note.get('rank', len(formatted) + 1),
                'title': note.get('title', ''),
                'author': note.get('author', ''),
                'likes': likes_num,
                'likes_text': likes,
                'url': note.get('url', ''),
                'category': self._guess_category(note.get('title', ''))
            })
        return formatted

    def _parse_likes(self, likes_str: str) -> int:
        """解析点赞数字符串"""
        likes_str = likes_str.replace(',', '').replace(' ', '')
        if '万' in likes_str:
            try:
                return int(float(likes_str.replace('万', '')) * 10000)
            except:
                return 0
        try:
            return int(likes_str)
        except:
            return 0

    def _guess_category(self, title: str) -> str:
        """根据标题猜测分类"""
        categories = {
            '穿搭': ['穿搭', '搭配', '服装', '衣服', '裙子'],
            '美食': ['美食', '食谱', '做饭', '早餐', '晚餐', '减脂'],
            '旅行': ['旅行', '旅游', '攻略', '城市', '景点'],
            '健身': ['健身', '运动', '瑜伽', '锻炼', '减肥'],
            '美妆': ['美妆', '化妆', '护肤', '口红'],
            '家居': ['家居', '装修', '收纳', '柜子'],
            '娱乐': ['明星', '电视剧', '电影', '综艺'],
        }
        for cat, keywords in categories.items():
            if any(kw in title for kw in keywords):
                return cat
        return '其他'

    def _get_fallback_data(self, top: int) -> List[Dict]:
        """获取备用数据（模拟数据）"""
        print("[INFO] 使用模拟数据", file=sys.stderr)
        return [
            {'rank': 1, 'title': '2026春季穿搭指南｜这5套搭配绝了', 'author': '时尚博主', 'likes': 12580, 'likes_text': '1.3万', 'url': 'https://www.xiaohongshu.com/explore', 'category': '穿搭'},
            {'rank': 2, 'title': '10分钟搞定早餐｜懒人必备食谱', 'author': '美食达人', 'likes': 9870, 'likes_text': '9870', 'url': 'https://www.xiaohongshu.com/explore', 'category': '美食'},
            {'rank': 3, 'title': '北京周边游｜周末好去处推荐', 'author': '旅行博主', 'likes': 8540, 'likes_text': '8540', 'url': 'https://www.xiaohongshu.com/explore', 'category': '旅行'},
        ][:top]


def format_number(num: int) -> str:
    """格式化数字（万/亿）"""
    if num >= 10000:
        return f"{num/10000:.1f}万"
    return str(num)


def generate_summary(notes: List[Dict]) -> str:
    """生成摘要"""
    if not notes:
        return "暂无数据"

    total_likes = sum(n.get('likes', 0) for n in notes)
    
    # 统计分类
    categories = {}
    for n in notes:
        cat = n.get('category', '其他')
        categories[cat] = categories.get(cat, 0) + 1
    
    top_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
    cat_str = "、".join([c[0] for c in top_cats])

    return (
        f"[SUMMARY] 今日小红书热榜摘要\n"
        f"共 {len(notes)} 个热门笔记\n"
        f"总点赞：{format_number(total_likes)}\n"
        f"热门分类：{cat_str}\n"
        f"Top 1：{notes[0]['title']}（点赞 {notes[0]['likes_text']}）"
    )


def output_json(notes: List[Dict], output_file: str, summary: str = ""):
    """输出JSON格式"""
    result = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'total': len(notes),
        'source': 'xiaohongshu.com/explore',
        'summary': summary,
        'notes': notes
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[OK] 已保存到 {output_file}")


def main():
    parser = argparse.ArgumentParser(description='📕 小红书热榜日报 v3.0')
    parser.add_argument('--top', type=int, default=10, help='获取数量 (默认: 10)')
    parser.add_argument('--summary', action='store_true', help='生成摘要')
    parser.add_argument('--output', type=str, help='输出文件路径')
    parser.add_argument('--quiet', action='store_true', help='静默模式')

    args = parser.parse_args()

    fetcher = XiaohongshuHotFetcher()
    notes = fetcher.fetch_hot(args.top)

    # 输出
    if not args.quiet:
        print("\n" + "="*80)
        print(f"[HOT] 小红书热榜 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*80)

        for note in notes:
            print(f"\n#{note['rank']} {note['title']}")
            print(f"   [AUTHOR] {note['author']} | [CAT] {note['category']}")
            print(f"   [LIKE] {note['likes_text']}")
            print(f"   [LINK] {note['url']}")

        print("\n" + "="*80)

    # 生成摘要
    summary = ""
    if args.summary:
        summary = generate_summary(notes)
        if not args.quiet:
            print(f"\n{summary}")

    # 保存文件
    if args.output:
        output_json(notes, args.output, summary)

    return notes


if __name__ == '__main__':
    main()
