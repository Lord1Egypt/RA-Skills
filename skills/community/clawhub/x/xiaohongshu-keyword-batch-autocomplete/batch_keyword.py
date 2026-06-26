#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书关键词联想词批量采集工具
支持多轮次深度联想、自动去重、批量导入
"""

import requests
import argparse
import time
import os
from typing import List, Dict, Set
from datetime import datetime
from collections import OrderedDict

# 可选依赖：pandas 和 openpyxl 用于 Excel 导出
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("警告: pandas 未安装，Excel 导出功能不可用")
    print("安装命令: pip3 install pandas openpyxl")

class XiaohongshuBatchAutocomplete:
    def __init__(self, delay: float = 1.0, dedup: bool = True):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://www.xiaohongshu.com',
            'Referer': 'https://www.xiaohongshu.com/'
        })
        self.delay = delay
        self.dedup = dedup
        self.seen_keywords: Set[str] = set()
        self.all_suggestions: OrderedDict[str, Dict] = OrderedDict()

    def get_suggestions(self, keyword: str, source: str = "root") -> List[Dict]:
        """获取单个关键词的联想词"""
        try:
            # 模拟数据（真实场景需要对接小红书 API）
            suggestions = self._generate_mock_suggestions(keyword, source)
            
            # 去重处理
            if self.dedup:
                unique_suggestions = []
                for sug in suggestions:
                    kw = sug['keyword']
                    if kw not in self.seen_keywords:
                        self.seen_keywords.add(kw)
                        unique_suggestions.append(sug)
                    else:
                        # 更新已存在词条的引用计数
                        if kw in self.all_suggestions:
                            self.all_suggestions[kw]['ref_count'] += 1
                return unique_suggestions
            else:
                for sug in suggestions:
                    self.seen_keywords.add(sug['keyword'])
                return suggestions
            
        except Exception as e:
            print(f"获取关键词 '{keyword}' 联想词失败: {e}")
            return []

    def _generate_mock_suggestions(self, keyword: str, source: str) -> List[Dict]:
        """生成模拟联想词（用于演示）"""
        suffixes = [
            '2025', '新款', '推荐', '攻略', '教程',
            '平价', '学生党', '小个子', '微胖', '通勤'
        ]
        
        suggestions = []
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i, suffix in enumerate(suffixes[:12]):
            kw = f"{keyword} {suffix}"
            sug = {
                'keyword': kw,
                'score': 100 - i * 5,
                'type': 'suggest',
                'rank': i + 1,
                'source': source,
                'depth': 0,
                'ref_count': 1,
                'collected_at': timestamp
            }
            suggestions.append(sug)
            self.all_suggestions[kw] = sug
        
        return suggestions

    def deep_collect(self, keyword: str, max_depth: int = 2, current_depth: int = 0, source: str = None) -> List[Dict]:
        """深度采集（递归采集联想词的联想词）"""
        if current_depth >= max_depth:
            return []
        
        if source is None:
            source = keyword
        
        print(f"{'  ' * current_depth}深度 {current_depth + 1}: {keyword}")
        
        # 获取当前关键词的联想词
        suggestions = self.get_suggestions(keyword, source)
        
        # 更新深度信息
        for sug in suggestions:
            sug['depth'] = current_depth + 1
        
        # 递归采集每个联想词的联想词
        if current_depth + 1 < max_depth:
            time.sleep(self.delay)
            for sug in suggestions:
                child_suggestions = self.deep_collect(
                    sug['keyword'],
                    max_depth,
                    current_depth + 1,
                    keyword
                )
                suggestions.extend(child_suggestions)
        
        return suggestions

    def batch_collect(self, keywords: List[str], max_depth: int = 1) -> Dict[str, List[Dict]]:
        """批量采集关键词联想词"""
        results = {}
        total_before = 0
        
        print(f"\n开始批量采集，共 {len(keywords)} 个关键词，深度: {max_depth}")
        print("=" * 60)
        
        for keyword in keywords:
            suggestions = self.deep_collect(keyword, max_depth)
            results[keyword] = suggestions
            total_before += len(suggestions)
            time.sleep(self.delay)
        
        print("=" * 60)
        print(f"采集完成: 原始 {total_before} 个，去重后 {len(self.all_suggestions)} 个\n")
        
        return results

    def export_txt(self, results: Dict[str, List[Dict]], output_path: str, max_depth: int):
        """导出为TXT格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"小红书关键词联想词批量采集报告\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"采集深度: {max_depth}\n")
            f.write(f"原始数量: {sum(len(s) for s in results.values())}\n")
            f.write(f"去重数量: {len(self.all_suggestions)}\n")
            f.write("=" * 60 + "\n\n")
            
            # 按关键词分组输出
            for keyword, suggestions in results.items():
                f.write(f"\n【主关键词】{keyword}\n")
                f.write("-" * 40 + "\n")
                
                # 按深度分组显示
                for depth in range(1, max_depth + 1):
                    depth_sugs = [s for s in suggestions if s['depth'] == depth]
                    if depth_sugs:
                        f.write(f"\n  深度 {depth}:\n")
                        for sug in depth_sugs[:10]:  # 每个深度最多显示10个
                            f.write(f"    {sug['rank']:2d}. {sug['keyword']} (热度: {sug['score']})\n")
                        if len(depth_sugs) > 10:
                            f.write(f"    ... 还有 {len(depth_sugs) - 10} 个\n")
            
            # 热门词汇总（按热度排序）
            f.write("\n\n" + "=" * 60 + "\n")
            f.write("【热门词汇总 TOP 20】\n")
            f.write("-" * 40 + "\n")
            sorted_sugs = sorted(self.all_suggestions.values(), key=lambda x: x['score'], reverse=True)
            for i, sug in enumerate(sorted_sugs[:20], 1):
                f.write(f"{i:2d}. {sug['keyword']} (热度: {sug['score']}, 来源: {sug['source']})\n")
        
        print(f"TXT文件已导出: {output_path}")

    def export_excel(self, results: Dict[str, List[Dict]], output_path: str, max_depth: int):
        """导出为Excel格式"""
        if not PANDAS_AVAILABLE:
            print("错误: 请先安装 pandas 和 openpyxl 才能使用 Excel 导出功能")
            print("安装命令: pip3 install pandas openpyxl")
            return False
        
        # 详细数据表
        detail_rows = []
        for keyword, suggestions in results.items():
            for sug in suggestions:
                detail_rows.append({
                    '主关键词': keyword,
                    '联想词': sug['keyword'],
                    '热度分数': sug['score'],
                    '排名': sug['rank'],
                    '采集深度': sug['depth'],
                    '来源关键词': sug['source'],
                    '引用次数': sug['ref_count'],
                    '采集时间': sug['collected_at']
                })
        
        # 汇总表（去重后）
        summary_rows = []
        sorted_sugs = sorted(self.all_suggestions.values(), key=lambda x: x['score'], reverse=True)
        for sug in sorted_sugs:
            summary_rows.append({
                '联想词': sug['keyword'],
                '热度分数': sug['score'],
                '来源关键词': sug['source'],
                '首次采集深度': sug['depth'],
                '引用次数': sug['ref_count'],
                '采集时间': sug['collected_at']
            })
        
        # 写入 Excel（多个 Sheet）
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            pd.DataFrame(detail_rows).to_excel(writer, sheet_name='详细数据', index=False)
            pd.DataFrame(summary_rows).to_excel(writer, sheet_name='汇总（去重）', index=False)
            
            # 统计信息 Sheet
            stats = pd.DataFrame([
                {'统计项': '采集时间', '数值': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                {'统计项': '主关键词数量', '数值': len(results)},
                {'统计项': '采集深度', '数值': max_depth},
                {'统计项': '原始词条数', '数值': len(detail_rows)},
                {'统计项': '去重后词条数', '数值': len(summary_rows)},
                {'统计项': '去重率', '数值': f"{(1 - len(summary_rows)/len(detail_rows))*100:.1f}%"},
            ])
            stats.to_excel(writer, sheet_name='统计信息', index=False)
        
        print(f"Excel文件已导出: {output_path}")
        return True

def main():
    parser = argparse.ArgumentParser(description='小红书关键词联想词批量采集工具')
    parser.add_argument('--keyword', type=str, help='单个关键词')
    parser.add_argument('--file', type=str, help='批量关键词文件（每行一个）')
    parser.add_argument('--depth', type=int, default=1, choices=[1, 2, 3], help='联想深度（1-3），默认 1')
    parser.add_argument('--no-dedup', action='store_true', help='关闭自动去重')
    
    # 根据 pandas 是否可用设置可选值
    format_choices = ['txt']
    if PANDAS_AVAILABLE:
        format_choices.append('excel')
    
    parser.add_argument('--format', type=str, choices=format_choices, default='txt', help='输出格式')
    parser.add_argument('--output', type=str, default='./output', help='输出目录')
    parser.add_argument('--delay', type=float, default=0.5, help='请求延迟（秒），默认 0.5')
    
    args = parser.parse_args()
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    
    # 初始化采集器
    collector = XiaohongshuBatchAutocomplete(
        delay=args.delay,
        dedup=not args.no_dedup
    )
    
    # 获取关键词列表
    keywords = []
    if args.keyword:
        keywords.append(args.keyword)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        print("请使用 --keyword 指定关键词或 --file 指定关键词文件")
        return
    
    if not keywords:
        print("未找到有效关键词")
        return
    
    # 执行采集
    results = collector.batch_collect(keywords, args.depth)
    
    # 生成输出文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if args.format == 'txt':
        output_path = os.path.join(args.output, f'batch_keywords_{timestamp}.txt')
        collector.export_txt(results, output_path, args.depth)
    else:
        output_path = os.path.join(args.output, f'batch_keywords_{timestamp}.xlsx')
        collector.export_excel(results, output_path, args.depth)
    
    # 控制台预览
    print("结果预览（TOP 10）:")
    print("-" * 40)
    sorted_sugs = sorted(collector.all_suggestions.values(), key=lambda x: x['score'], reverse=True)
    for i, sug in enumerate(sorted_sugs[:10], 1):
        print(f"{i:2d}. {sug['keyword']} (热度: {sug['score']}, 深度: {sug['depth']})")

if __name__ == '__main__':
    main()
