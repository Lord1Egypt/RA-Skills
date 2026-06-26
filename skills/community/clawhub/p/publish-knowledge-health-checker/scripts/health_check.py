#!/usr/bin/env python3
"""
知识库健康检查核心引擎
检测空壳文件、断链、内容密度、知识网络完整性
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
import json
import signal
from tqdm import tqdm


class KnowledgeHealthChecker:
    def __init__(self, scan_path: str):
        self.scan_path = Path(scan_path)
        self.files = []
        self.file_index = {}  # 文件名 -> 完整路径
        self.links = {}  # 源文件 -> [目标文件列表]
        self.reverse_links = {}  # 目标文件 -> [源文件列表]

    def scan_files(self, exclude_dirs=None, quiet=False):
        """扫描所有Markdown文件，构建文件索引"""
        if exclude_dirs is None:
            exclude_dirs = {'.git', 'node_modules', '__pycache__', '.obsidian'}

        self.files = []
        self.file_index = {}

        for root, dirs, files in os.walk(self.scan_path):
            # 排除隐藏目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in exclude_dirs]

            for file in files:
                if file.endswith('.md') and not file.startswith('.'):
                    full_path = Path(root) / file
                    self.files.append(full_path)
                    self.file_index[file.lower()] = full_path

        if not quiet:
            print(f"扫描完成：发现 {len(self.files)} 个Markdown文件", file=sys.stderr)
        return self.files

    def detect_empty_files(self, min_chars=200) -> List[Dict]:
        """检测空壳文件"""
        empty_files = []

        for file_path in self.files:
            try:
                content = file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                # 尝试其他编码
                try:
                    content = file_path.read_text(encoding='gbk')
                except:
                    continue
            except PermissionError:
                continue

            # 检测条件
            issues = []

            # 1. 内容过短
            if len(content.strip()) < min_chars:
                issues.append('内容过短')

            # 2. 缺少标题
            if not re.search(r'^#', content, re.MULTILINE):
                issues.append('缺少标题')

            # 3. 占位符检测
            placeholders = ['待补充', 'TODO', '占位', '待完善', 'TBD']
            if any(p in content for p in placeholders):
                issues.append('占位符')

            # 4. 纯图片笔记（检测图片标签数量）
            image_count = len(re.findall(r'!\[.*?\]\(.*?\)', content))
            if image_count > 3 and len(content.strip()) < 100:
                issues.append('纯图片笔记')

            if issues:
                empty_files.append({
                    'file': str(file_path.relative_to(self.scan_path)),
                    'issues': issues,
                    'size': len(content),
                    'image_count': image_count
                })

        return empty_files

    def extract_links(self, content: str) -> List[Tuple[str, str]]:
        """提取所有Wiki链接"""
        links = []

        # 文件链接 [[filename]]
        for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
            link = match.group(1)
            # 提取锚点
            if '#' in link:
                filename = link.split('#')[0]
                anchor = link.split('#')[1]
            else:
                filename = link
                anchor = None

            links.append((filename, anchor))

        return links

    def detect_broken_links(self) -> List[Dict]:
        """检测断链"""
        broken_links = []

        for file_path in self.files:
            try:
                content = file_path.read_text(encoding='utf-8')
            except (UnicodeDecodeError, PermissionError):
                continue

            links = self.extract_links(content)

            for filename, anchor in links:
                target_file = filename.lower()

                # 检查文件是否存在
                if target_file not in self.file_index:
                    broken_links.append({
                        'source': str(file_path.relative_to(self.scan_path)),
                        'type': '文件不存在',
                        'target': filename,
                        'error': '找不到目标文件'
                    })
                    continue

                # 检查锚点是否存在
                if anchor:
                    target_content = self.file_index[target_file].read_text(encoding='utf-8')
                    # 查找锚点对应的标题
                    anchor_pattern = re.escape(anchor)
                    if not re.search(rf'^#+\s*{anchor_pattern}', target_content, re.MULTILINE | re.IGNORECASE):
                        broken_links.append({
                            'source': str(file_path.relative_to(self.scan_path)),
                            'type': '锚点不存在',
                            'target': filename,
                            'error': f'找不到锚点 #{anchor}'
                        })

        return broken_links

    def analyze_content_density(self) -> List[Dict]:
        """分析内容密度"""
        density_stats = []

        for file_path in self.files:
            try:
                content = file_path.read_text(encoding='utf-8')
            except (UnicodeDecodeError, PermissionError):
                continue

            char_count = len(content.strip())
            word_count = len(content.split())

            # 结构分析
            h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
            h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
            h3_count = len(re.findall(r'^### ', content, re.MULTILINE))

            list_count = len(re.findall(r'^[-*]\s+', content, re.MULTILINE))
            code_block_count = len(re.findall(r'```', content)) // 2
            table_count = len(re.findall(r'\|.*\|', content)) // 3

            # 链接分析
            links = self.extract_links(content)
            internal_links = len(links)
            external_links = len(re.findall(r'\[.*?\]\(http', content))

            # 状态判断
            status = []
            if char_count < 300:
                status.append('过短')
            elif char_count > 3000:
                status.append('过长')

            structure_score = min(100, (h1_count * 10 + h2_count * 5 + h3_count * 2 + list_count * 2 + code_block_count * 5 + table_count * 5))

            if internal_links == 0:
                status.append('孤岛')

            density_stats.append({
                'file': str(file_path.relative_to(self.scan_path)),
                'char_count': char_count,
                'word_count': word_count,
                'structure_score': structure_score,
                'internal_links': internal_links,
                'external_links': external_links,
                'status': status
            })

        return density_stats

    def build_knowledge_graph(self) -> Tuple[Dict, Set, Set]:
        """构建知识图谱"""
        # 构建邻接表
        graph = defaultdict(set)

        for file_path in self.files:
            try:
                content = file_path.read_text(encoding='utf-8')
            except (UnicodeDecodeError, PermissionError):
                continue

            links = self.extract_links(content)
            source = file_path.stem.lower()

            for filename, _ in links:
                target = filename.lower()
                if target in self.file_index:
                    graph[source].add(target)

        # 找孤立节点
        all_nodes = set(self.file_index.keys())
        nodes_with_edges = set()
        for source, targets in graph.items():
            nodes_with_edges.add(source)
            nodes_with_edges.update(targets)

        isolated_nodes = all_nodes - nodes_with_edges

        # 找中心节点（度数>10）
        degrees = defaultdict(int)
        for source, targets in graph.items():
            degrees[source] += len(targets)
            for target in targets:
                degrees[target] += 1

        central_nodes = {node for node, degree in degrees.items() if degree > 10}

        return dict(graph), isolated_nodes, central_nodes

    def get_mtime(self, file_path: Path) -> float:
        """获取文件修改时间"""
        try:
            return file_path.stat().st_mtime
        except:
            return 0

    def calculate_health_score(self, empty_files, broken_links, density_stats) -> Dict:
        """计算健康评分"""
        total_files = len(self.files)

        # 防止除零
        if total_files == 0:
            return {
                'total_score': 0,
                'empty_score': 0,
                'broken_score': 0,
                'density_score': 0,
                'network_score': 0
            }

        # 空壳文件率（权重25%）
        empty_score = max(0, 100 - (len(empty_files) / total_files * 100))

        # 断链接率（权重30%）
        broken_score = max(0, 100 - (len(broken_links) / total_files * 10))

        # 内容密度（权重25%）
        healthy_files = sum(1 for f in density_stats if not f['status'])
        density_score = (healthy_files / total_files * 100)

        # 网络完整性（权重20%）
        _, isolated_nodes, _ = self.build_knowledge_graph()
        network_score = max(0, 100 - (len(isolated_nodes) / total_files * 100))

        # 加权总分
        total_score = (empty_score * 0.25 + broken_score * 0.3 + density_score * 0.25 + network_score * 0.2)

        return {
            'total_score': round(total_score, 1),
            'empty_score': round(empty_score, 1),
            'broken_score': round(broken_score, 1),
            'density_score': round(density_score, 1),
            'network_score': round(network_score, 1)
        }

    def run_full_check(self, quiet=False) -> Dict:
        """运行完整检查"""
        if not quiet:
            print(f"开始扫描：{self.scan_path}", file=sys.stderr)

        # 扫描文件
        self.scan_files(quiet=quiet)

        # 执行各项检测
        if not quiet:
            print("检测空壳文件...", file=sys.stderr)
        empty_files = self.detect_empty_files()

        if not quiet:
            print("检测断链...", file=sys.stderr)
        broken_links = self.detect_broken_links()

        if not quiet:
            print("分析内容密度...", file=sys.stderr)
        density_stats = self.analyze_content_density()

        if not quiet:
            print("构建知识图谱...", file=sys.stderr)
        graph, isolated_nodes, central_nodes = self.build_knowledge_graph()

        if not quiet:
            print("计算健康评分...", file=sys.stderr)
        scores = self.calculate_health_score(empty_files, broken_links, density_stats)

        # 汇总结果
        results = {
            'scan_path': str(self.scan_path),
            'total_files': len(self.files),
            'empty_files': empty_files,
            'broken_links': broken_links,
            'density_stats': density_stats,
            'isolated_nodes': list(isolated_nodes),
            'central_nodes': list(central_nodes),
            'scores': scores,
            'graph_stats': {
                'total_nodes': len(self.files),
                'isolated_count': len(isolated_nodes),
                'central_count': len(central_nodes),
                'edge_count': sum(len(targets) for targets in graph.values())
            }
        }

        if not quiet:
            print(f"检查完成！健康分：{scores['total_score']}", file=sys.stderr)
        return results


if __name__ == '__main__':
    import sys

    scan_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    quiet = '--quiet' in sys.argv or '-q' in sys.argv

    checker = KnowledgeHealthChecker(scan_path)
    results = checker.run_full_check(quiet=quiet)

    # 输出JSON
    print(json.dumps(results, ensure_ascii=False, indent=2))
