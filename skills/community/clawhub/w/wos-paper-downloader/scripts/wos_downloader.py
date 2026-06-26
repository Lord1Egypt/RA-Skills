#!/usr/bin/env python3
"""
Web of Science 文献下载器
支持检索、元数据提取和批量下载
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, urlencode

import requests


class WOSDownloader:
    """Web of Science 文献下载管理器"""
    
    def __init__(self, output_dir=None, delay=2):
        self.delay = delay  # 请求间隔（秒）
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 设置输出目录
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            timestamp = datetime.now().strftime('%Y-%m-%d')
            self.output_dir = Path(f'papers/{timestamp}_wos_search')
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 子目录
        self.oa_dir = self.output_dir / 'oa_papers'
        self.subscribed_dir = self.output_dir / 'subscribed'
        self.oa_dir.mkdir(exist_ok=True)
        self.subscribed_dir.mkdir(exist_ok=True)
        
        # 数据存储
        self.papers = []
        
    def build_search_url(self, query, advanced=False):
        """构建 Web of Science 检索 URL"""
        base_url = 'https://www.webofscience.com/wos/woscc/advanced-search'
        
        if advanced:
            # 高级检索模式
            search_query = query
        else:
            # 基础检索模式 - 自动添加 TS= 前缀
            search_query = f'TS=({query})'
        
        # 注意：实际执行需要浏览器自动化
        print(f'检索式: {search_query}')
        return search_query
    
    def search_with_browser(self, query, limit=50):
        """
        使用浏览器执行检索（需要手动登录）
        这是半自动化方案，指导用户完成检索
        """
        search_url = self.build_search_url(query)
        
        print('\n' + '='*60)
        print('Web of Science 文献检索助手')
        print('='*60)
        print(f'\n检索关键词: {query}')
        print(f'限制数量: {limit}')
        print('\n--- 手动操作步骤 ---')
        print('1. 打开浏览器访问: https://www.webofscience.com')
        print('2. 使用你的机构账号登录')
        print('3. 进入高级检索页面')
        print(f'4. 输入检索式: {search_url}')
        print('5. 执行检索并按相关性排序')
        print('6. 选择前 {} 条记录，导出为「其他文件格式」'.format(limit))
        print('7. 选择「制表符分隔的 UTF-8 格式」')
        print('8. 选择「全记录与引用的参考文献」')
        print('9. 导出并保存到: {}'.format(self.output_dir))
        print('\n导出完成后，将文件命名为 "wos_export.txt" 放在上述目录')
        print('='*60)
        
        return True
    
    def parse_wos_export(self, filepath):
        """解析 Web of Science 导出的文本文件"""
        papers = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # WOS 导出文件以 PT（出版物类型）分隔记录
            records = content.split('PT ')
            
            for record in records[1:]:  # 跳过第一个空项
                paper = self._parse_record(record)
                if paper:
                    papers.append(paper)
            
            print(f'成功解析 {len(papers)} 条记录')
            return papers
            
        except Exception as e:
            print(f'解析文件出错: {e}')
            return []
    
    def _parse_record(self, record):
        """解析单条记录"""
        paper = {}
        
        # 提取各字段
        patterns = {
            'title': r'TI (.+?)(?=\n[A-Z]{2} |\Z)',
            'authors': r'AU (.+?)(?=\n[A-Z]{2} |\Z)',
            'source': r'SO (.+?)(?=\n[A-Z]{2} |\Z)',
            'doi': r'DI (.+?)(?=\n[A-Z]{2} |\Z)',
            'abstract': r'AB (.+?)(?=\n[A-Z]{2} |\Z)',
            'year': r'PY (\d{4})',
            'volume': r'VL (.+?)(?=\n[A-Z]{2} |\Z)',
            'issue': r'IS (.+?)(?=\n[A-Z]{2} |\Z)',
            'pages': r'PG (.+?)(?=\n[A-Z]{2} |\Z)',
            'wos_id': r'UT (.+?)(?=\n[A-Z]{2} |\Z)',
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, record, re.DOTALL)
            if match:
                value = match.group(1).strip()
                # 清理多行内容
                value = ' '.join(value.split())
                paper[field] = value
        
        return paper if paper else None
    
    def check_open_access(self, doi):
        """
        检查文献是否为开放获取
        使用 Unpaywall API
        """
        if not doi:
            return None
        
        # 清理 DOI
        doi = doi.replace('doi:', '').replace('DOI:', '').strip()
        
        url = f'https://api.unpaywall.org/v2/{doi}?email=user@example.com'
        
        try:
            time.sleep(self.delay)  # 控制请求频率
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'is_oa': data.get('is_oa', False),
                    'oa_url': data.get('best_oa_location', {}).get('url_for_pdf') if data.get('best_oa_location') else None,
                    'journal': data.get('journal_name', ''),
                    'publisher': data.get('publisher', '')
                }
        except Exception as e:
            print(f'检查 OA 状态出错 ({doi}): {e}')
        
        return None
    
    def download_pdf(self, url, filename):
        """下载 PDF 文件"""
        try:
            time.sleep(self.delay)
            response = self.session.get(url, timeout=30, stream=True)
            
            if response.status_code == 200:
                filepath = self.oa_dir / filename
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f'  ✓ 下载成功: {filename}')
                return True
            else:
                print(f'  ✗ 下载失败 (HTTP {response.status_code}): {filename}')
                return False
                
        except Exception as e:
            print(f'  ✗ 下载出错: {filename} - {e}')
            return False
    
    def process_papers(self, papers, oa_only=False):
        """处理文献列表，检查OA状态并下载"""
        print(f'\n开始处理 {len(papers)} 篇文献...')
        print('='*60)
        
        results = {
            'oa_found': 0,
            'oa_downloaded': 0,
            'subscription_required': 0,
            'no_doi': 0
        }
        
        subscription_list = []
        
        for i, paper in enumerate(papers, 1):
            print(f'\n[{i}/{len(papers)}] {paper.get("title", "Unknown")[:60]}...')
            
            doi = paper.get('doi', '')
            if not doi:
                print('  - 无 DOI，跳过')
                results['no_doi'] += 1
                continue
            
            # 检查开放获取状态
            oa_info = self.check_open_access(doi)
            
            if oa_info and oa_info['is_oa'] and oa_info['oa_url']:
                results['oa_found'] += 1
                print(f'  ✓ 发现开放获取版本')
                
                # 生成文件名
                safe_title = re.sub(r'[^\w\s-]', '', paper.get('title', 'unknown')[:50])
                filename = f"{i:03d}_{safe_title.replace(' ', '_')}.pdf"
                
                # 下载
                if self.download_pdf(oa_info['oa_url'], filename):
                    results['oa_downloaded'] += 1
                    paper['local_pdf'] = str(self.oa_dir / filename)
                    paper['oa_status'] = 'downloaded'
                else:
                    paper['oa_status'] = 'download_failed'
            else:
                results['subscription_required'] += 1
                print('  - 需要订阅权限')
                paper['oa_status'] = 'subscription_required'
                subscription_list.append(paper)
        
        # 保存结果
        self.save_results(papers, subscription_list)
        
        # 打印统计
        print('\n' + '='*60)
        print('处理完成！')
        print(f'  开放获取文献: {results["oa_found"]} (成功下载 {results["oa_downloaded"]})')
        print(f'  需要订阅: {results["subscription_required"]}')
        print(f'  无 DOI: {results["no_doi"]}')
        print(f'\n文件保存位置: {self.output_dir}')
        print('='*60)
        
        return results
    
    def save_results(self, all_papers, subscription_list):
        """保存结果到文件"""
        # 保存所有元数据为 CSV
        csv_path = self.output_dir / 'metadata.csv'
        if all_papers:
            keys = all_papers[0].keys()
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(all_papers)
            print(f'\n元数据已保存: {csv_path}')
        
        # 保存订阅文献清单
        if subscription_list:
            list_path = self.output_dir / 'download_list.txt'
            with open(list_path, 'w', encoding='utf-8') as f:
                f.write('需要手动下载的文献清单\n')
                f.write('='*60 + '\n\n')
                for paper in subscription_list:
                    f.write(f"标题: {paper.get('title', 'N/A')}\n")
                    f.write(f"作者: {paper.get('authors', 'N/A')[:100]}...\n")
                    f.write(f"期刊: {paper.get('source', 'N/A')}\n")
                    f.write(f"年份: {paper.get('year', 'N/A')}\n")
                    f.write(f"DOI: {paper.get('doi', 'N/A')}\n")
                    f.write(f"WOS ID: {paper.get('wos_id', 'N/A')}\n")
                    f.write('-'*60 + '\n\n')
            print(f'订阅文献清单: {list_path}')
        
        # 保存为 JSON（便于程序处理）
        json_path = self.output_dir / 'papers.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_papers, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Web of Science 文献下载助手')
    parser.add_argument('--query', '-q', help='检索关键词')
    parser.add_argument('--advanced', '-a', action='store_true', help='使用高级检索模式')
    parser.add_argument('--limit', '-l', type=int, default=50, help='限制数量（默认50）')
    parser.add_argument('--output', '-o', help='输出目录')
    parser.add_argument('--oa-only', action='store_true', help='只处理开放获取文献')
    parser.add_argument('--delay', '-d', type=float, default=2, help='请求间隔（秒）')
    parser.add_argument('--parse', help='解析已导出的 WOS 文件')
    
    args = parser.parse_args()
    
    # 初始化下载器
    downloader = WOSDownloader(output_dir=args.output, delay=args.delay)
    
    if args.parse:
        # 解析已有文件
        print(f'解析文件: {args.parse}')
        papers = downloader.parse_wos_export(args.parse)
        if papers:
            downloader.process_papers(papers, oa_only=args.oa_only)
    
    elif args.query:
        # 指导用户进行检索
        downloader.search_with_browser(args.query, args.limit)
        
        print('\n等待你完成导出...')
        export_path = downloader.output_dir / 'wos_export.txt'
        
        if export_path.exists():
            print(f'\n发现导出文件，开始处理...')
            papers = downloader.parse_wos_export(export_path)
            if papers:
                downloader.process_papers(papers, oa_only=args.oa_only)
        else:
            print(f'\n请将导出的文件保存到: {export_path}')
            print('然后运行: python wos_downloader.py --parse {}'.format(export_path))
    
    else:
        parser.print_help()
        print('\n示例:')
        print('  python wos_downloader.py -q "restorative environment health" -l 50')
        print('  python wos_downloader.py --parse ./papers/2024-01-15/wos_export.txt')


if __name__ == '__main__':
    main()
