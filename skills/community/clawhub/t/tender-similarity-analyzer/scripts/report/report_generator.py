# -*- coding: utf-8 -*-
"""
HTML查重报告生成器
"""

import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    from jinja2 import Template
except ImportError:
    raise ImportError("Jinja2 >= 3.0.0 is required. Install: pip install Jinja2")


class ReportGenerator:
    """
    HTML查重报告生成器
    
    生成专业的查重报告，包含：
    - 总体统计
    - 重复详情
    - 文件对比矩阵
    - 修改建议
    """
    
    def __init__(self):
        self.template_path = Path(__file__).parent / 'templates' / 'report_template.html'
        
    def generate(self, documents: Dict, results: Dict, output_path: str) -> Dict:
        """
        生成查重报告
        
        @param documents: 文档字典
        @param results: 查重结果
        @param output_path: 输出路径
        @return: 报告数据字典
        """
        # 准备报告数据
        report_data = self._prepare_report_data(documents, results)
        
        # 生成HTML
        html_content = self._render_html(report_data)
        
        # 保存报告
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        # 同时返回报告数据
        report_data['output_path'] = output_path
        return report_data
        
    def _prepare_report_data(self, documents: Dict, results: Dict) -> Dict:
        """
        准备报告数据
        
        @param documents: 文档字典
        @param results: 查重结果
        @return: 报告数据
        """
        # 总体统计
        total_paras = results.get('total_paras', 0)
        total_files = results.get('total_files', len(documents))
        
        # 正文 vs 标题段落数
        body_paras = results.get('body_paras', total_paras)
        title_paras = results.get('title_paras', 0)
        
        # 正文重复统计（优化版核心指标）
        body_duplicate_count = results.get('body_duplicate_count', 0)
        body_involved_paragraphs = results.get('body_involved_paragraphs', 0)
        body_duplication_rate = results.get('body_duplication_rate', 0)
        body_avg_similarity = results.get('body_avg_similarity', 0)
        body_severe_count = results.get('body_severe_count', 0)
        
        # 兼容旧字段（用于显示）
        duplicate_count = body_duplicate_count
        involved_paragraphs = body_involved_paragraphs
        para_duplication_rate = body_duplication_rate
        avg_similarity = body_avg_similarity
        severe_count = body_severe_count
        
        # 计算每份文件的段落数
        file_para_counts = self._count_paragraphs_per_file(documents)
        
        # 计算每份文件的重复段落数（统计段落出现在任一端的次数）
        tfidf_results = results.get('tfidf_results', [])
        file_duplicate_counts = {path: 0 for path in documents.keys()}
        for r in tfidf_results:
            # 只统计超过30%阈值的重复段落
            if r.get('tfidf_similarity', 0) >= 0.30:
                # 统计para1
                file_duplicate_counts[r['para1']['file_path']] = \
                    file_duplicate_counts.get(r['para1']['file_path'], 0) + 1
                # 统计para2
                file_duplicate_counts[r['para2']['file_path']] = \
                    file_duplicate_counts.get(r['para2']['file_path'], 0) + 1
        
        # 文件列表
        file_list = []
        for path, info in documents.items():
            short_name = info['name'][:30] + '...' if len(info['name']) > 30 else info['name']
            file_list.append({
                'name': info['name'],
                'short_name': short_name,
                'path': path,
                'char_count': len(info['text']),
                'para_count': file_para_counts.get(path, 0),
                'duplicate_count': file_duplicate_counts.get(path, 0)
            })
        
        # 统计重复段落分布
        dup_by_level = {'fail': 0, 'warning': 0, 'pass': 0}
        for r in results.get('tfidf_results', []):
            level = r.get('level', 'pass')
            dup_by_level[level] = dup_by_level.get(level, 0) + 1
            
        # 重复详情（完整版 - 显示全部）
        duplicate_details = []
        for i, r in enumerate(results.get('tfidf_results', []), 1):
            # 完整原文（不做截取）
            source_text = r['para1']['text']
            target_text = r['para2']['text']
            
            level_info = {
                'fail': {'color': '#f5222d', 'text': '🔴 严重', 'badge': 'fail'},
                'warning': {'color': '#faad14', 'text': '🟡 中等', 'badge': 'warning'},
                'pass': {'color': '#52c41a', 'text': '🟢 轻微', 'badge': 'pass'}
            }.get(r.get('level', 'pass'), {'color': '#999', 'text': '未知', 'badge': 'pass'})
            
            # 获取所属章节标题
            source_heading = r.get('para1', {}).get('heading', '') or ''
            target_heading = r.get('para2', {}).get('heading', '') or ''
            
            duplicate_details.append({
                'index': i,
                'id': f"dup-{i}",
                'source': {
                    'text': source_text,
                    'file': r['para1']['file_name'],
                    'index': r['para1']['index'],
                    'char_count': len(source_text),
                    'heading': source_heading
                },
                'target': {
                    'text': target_text,
                    'file': r['para2']['file_name'],
                    'index': r['para2']['index'],
                    'char_count': len(target_text),
                    'heading': target_heading
                },
                'source_file': r['para1']['file_name'],
                'source_index': r['para1']['index'],
                'source_heading': source_heading,
                'target_file': r['para2']['file_name'],
                'target_index': r['para2']['index'],
                'target_heading': target_heading,
                'similarity': r['tfidf_similarity'],
                'similarity_percent': f"{r['tfidf_similarity'] * 100:.1f}%",
                'preview': source_text[:50],
                'level': r.get('level', 'pass'),
                'level_color': level_info['color'],
                'level_text': level_info['text'],
                'level_badge': level_info['badge']
            })
            
        # 文件对比矩阵
        matrix = self._build_comparison_matrix(documents, results)
        
        # 大段落重复
        large_blocks = []
        for i, block in enumerate(results.get('large_block_results', []), 1):
            large_blocks.append({
                'index': i,
                'file1': block['file1'],
                'file2': block['file2'],
                'start_index': block['start_index'],
                'end_index': block['end_index'],
                'count': block['count'],
                'paragraphs': block.get('paragraphs', [])
            })
            
        # 修改建议（示例）
        suggestions = self._generate_suggestions(duplicate_details)
        
        # 整体状态判定（基于重复段落比例）
        if para_duplication_rate >= 0.3:
            pass_status = 'fail'
        elif para_duplication_rate >= 0.1:
            pass_status = 'warning'
        else:
            pass_status = 'pass'
        
        return {
            'report_id': f"PDC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_files': total_files,
            'total_paras': total_paras,
            'body_paras': body_paras,
            'title_paras': title_paras,
            'duplicate_count': duplicate_count,
            'involved_paragraphs': involved_paragraphs,
            'para_duplication_rate': para_duplication_rate,
            'para_duplication_percent': f"{para_duplication_rate * 100:.1f}%",
            'avg_similarity': avg_similarity,
            'avg_similarity_percent': f"{avg_similarity * 100:.1f}%",
            'severe_count': severe_count,
            'duplicate_by_level': dup_by_level,
            'pass_status': pass_status,
            'file_list': file_list,
            'duplicate_details': duplicate_details,  # 显示全部重复
            'duplicate_total': len(results.get('tfidf_results', [])),
            'comparison_matrix': matrix,
            'large_blocks': large_blocks,
            'suggestions': suggestions,
            'elapsed_time': results.get('elapsed_time', 0)
        }
        
    def _count_paragraphs_per_file(self, documents: Dict) -> Dict[str, int]:
        """计算每个文件的段落数"""
        counts = {}
        from engine.paragraph_splitter import ParagraphSplitter
        splitter = ParagraphSplitter()
        for path, info in documents.items():
            paras = splitter.split(info['text'])
            counts[path] = len(paras)
        return counts
        
    def _build_comparison_matrix(self, documents: Dict, results: Dict) -> List[List]:
        """
        构建文件对比矩阵
        
        @param documents: 文档字典
        @param results: 查重结果
        @return: 矩阵数据
        """
        file_names = [info['name'] for path, info in documents.items()]
        file_paths = list(documents.keys())
        n = len(file_names)
        
        # 初始化矩阵
        matrix = [[0.0 if i != j else None for j in range(n)] for i in range(n)]
        
        # 填充相似度
        for r in results.get('simhash_results', []):
            path1 = r['doc1']['path']
            path2 = r['doc2']['path']
            
            if path1 in file_paths and path2 in file_paths:
                i = file_paths.index(path1)
                j = file_paths.index(path2)
                sim = r['similarity']
                matrix[i][j] = sim
                matrix[j][i] = sim
                
        return {
            'files': file_names,
            'matrix': matrix
        }
        
    def _generate_suggestions(self, duplicates: List[Dict]) -> List[Dict]:
        """
        生成修改建议
        
        @param duplicates: 重复详情（简化版）
        @return: 建议列表
        """
        suggestions = []
        
        for dup in duplicates:
            if dup['level'] in ['warning', 'fail']:
                suggestions.append({
                    'id': dup['id'],
                    'source_file': dup.get('source_file', ''),
                    'target_file': dup.get('target_file', ''),
                    'position': f"第{dup.get('source_index', 0)}段",
                    'original_text': dup.get('preview', ''),
                    'suggestion': self._rewrite_text(dup.get('preview', ''))
                })
                
        return suggestions
        
    def _rewrite_text(self, text: str) -> str:
        """
        改写文本建议（简单的模板替换）
        
        @param text: 原始文本
        @return: 改写建议
        """
        # 这里可以使用更复杂的NLP模型来生成改写建议
        # 目前返回简单的模板
        rewrites = [
            ("投标有效期", "投标有效期须满足招标文件要求"),
            ("投标人", "本项目投标方"),
            ("招标人", "项目发包方"),
            ("中标", "合同授予"),
            ("质量保证期", "售后服务期限"),
            ("竣工验收", "项目终验"),
            ("投标保证金", "履约担保"),
        ]
        
        result = text
        for old, new in rewrites:
            if old in result:
                result = result.replace(old, new)
                
        if result == text:
            return f"建议将上述表述调整为更加具体的描述方式，避免直接引用招标文件中已给出的表述。"
            
        return f"可调整为：「{result[:80]}{'...' if len(result) > 80 else ''}」"
        
    def _render_html(self, data: Dict) -> str:
        """
        渲染HTML报告
        
        @param data: 报告数据
        @return: HTML内容
        """
        # 尝试从文件加载模板
        if self.template_path.exists():
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            template = Template(template_content)
        else:
            # 使用内置模板
            template = Template(self._get_default_template())
            
        return template.render(**data)
        
    def _get_default_template(self) -> str:
        """获取默认HTML模板"""
        return '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投标文件查重报告 - {{ report_id }}</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: "Microsoft YaHei", "SimSun", sans-serif; font-size: 14px; line-height: 1.6; color: #333; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        /* 报告头部 */
        .report-header { background: linear-gradient(135deg, #1e3a5f, #2d5a87); color: white; padding: 32px; border-radius: 8px; margin-bottom: 24px; }
        .report-header h1 { font-size: 28px; margin-bottom: 8px; }
        .report-header .meta { opacity: 0.9; font-size: 13px; }
        
        /* 统计卡片 */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .stat-card .label { color: #666; font-size: 13px; margin-bottom: 4px; }
        .stat-card .value { font-size: 28px; font-weight: bold; color: #1e3a5f; }
        .stat-card .value.pass { color: #52c41a; }
        .stat-card .value.warning { color: #faad14; }
        .stat-card .value.fail { color: #f5222d; }
        
        /* 重复率条 */
        .similarity-bar { width: 100%; height: 24px; background: #f0f0f0; border-radius: 12px; overflow: hidden; margin-top: 12px; }
        .similarity-fill { height: 100%; background: #52c41a; transition: width 0.3s; }
        .similarity-fill.warning { background: #faad14; }
        .similarity-fill.fail { background: #f5222d; }
        
        /* 内容区域 */
        .content-section { background: white; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .content-section h2 { font-size: 18px; color: #1e3a5f; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #1e3a5f; }
        
        /* 表格 */
        table { width: 100%; border-collapse: collapse; margin-top: 12px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background: #1e3a5f; color: white; font-weight: normal; }
        tr:nth-child(even) { background: #f9f9f9; }
        
        /* 重复块 */
        .duplicate-block { background: #fff2f0; border-left: 4px solid #f5222d; padding: 16px; margin: 16px 0; border-radius: 4px; }
        .duplicate-block.warning { background: #fffbe6; border-color: #faad14; }
        .duplicate-block.pass { background: #f6ffed; border-color: #52c41a; }
        
        .duplicate-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .duplicate-header h3 { font-size: 15px; color: #333; }
        .duplicate-header .badge { padding: 4px 12px; border-radius: 12px; font-size: 12px; color: white; }
        .badge.fail { background: #f5222d; }
        .badge.warning { background: #faad14; }
        .badge.pass { background: #52c41a; }
        
        /* 文本对比 */
        .text-comparison { display: flex; gap: 16px; margin-top: 12px; }
        .text-box { flex: 1; padding: 12px; border-radius: 4px; font-size: 13px; }
        .text-box.source { background: #ffe7e7; }
        .text-box.target { background: #fff7e6; }
        .text-box .label { font-weight: bold; margin-bottom: 8px; color: #666; font-size: 12px; }
        
        /* 建议框 */
        .suggestion-box { background: #f6ffed; border-left: 4px solid #52c41a; padding: 12px; margin-top: 12px; border-radius: 4px; }
        .suggestion-box .label { font-weight: bold; color: #52c41a; margin-bottom: 8px; font-size: 13px; }
        
        /* 矩阵 */
        .matrix-table th, .matrix-table td { text-align: center; min-width: 80px; }
        .matrix-table td.pass { color: #52c41a; font-weight: bold; }
        .matrix-table td.warning { color: #faad14; font-weight: bold; }
        .matrix-table td.fail { color: #f5222d; font-weight: bold; }
        
        /* 底部 */
        .footer { text-align: center; color: #999; font-size: 12px; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <!-- 报告头部 -->
        <div class="report-header">
            <h1>📋 投标文件查重报告</h1>
            <div class="meta">
                <span>报告编号: {{ report_id }}</span> &nbsp;|&nbsp;
                <span>生成时间: {{ generated_at }}</span> &nbsp;|&nbsp;
                <span>耗时: {{ "%.2f"|format(elapsed_time) }}s</span>
            </div>
        </div>
        
        <!-- 统计卡片 -->
        <div class="stats-grid" style="grid-template-columns: repeat(5, 1fr);">
            <div class="stat-card">
                <div class="label">检测文件</div>
                <div class="value">{{ total_files }} 个</div>
            </div>
            <div class="stat-card">
                <div class="label">总段落数</div>
                <div class="value">{{ total_paras }}</div>
            </div>
            <div class="stat-card">
                <div class="label">正文段落</div>
                <div class="value">{{ body_paras }}</div>
            </div>
            <div class="stat-card">
                <div class="label">涉及重复正文</div>
                <div class="value">{{ involved_paragraphs }} 段</div>
            </div>
            <div class="stat-card">
                <div class="label">正文重复率</div>
                <div class="value {% if para_duplication_rate >= 0.3 %}fail{% elif para_duplication_rate >= 0.1 %}warning{% else %}pass{% endif %}">{{ para_duplication_percent }}</div>
            </div>
        </div>
        
        <!-- 核心指标说明 - 优化版 -->
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 24px; border-radius: 12px; margin-bottom: 20px; font-size: 13px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 20px;">📊</span>
                    <p style="margin: 0; font-weight: bold; color: #333; font-size: 15px;">正文重复检测报告</p>
                </div>
                <div style="display: flex; align-items: center; gap: 16px;">
                    <span style="background: #e8f5e9; color: #2e7d32; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 500;">
                        📄 正文 {{ body_paras }} 段 | 📑 标题 {{ title_paras }} 段（已过滤）
                    </span>
                </div>
            </div>
            
            <!-- 三大核心指标卡片 -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px;">
                <!-- 重复率指标 -->
                <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="color: #666; font-size: 13px;">正文重复率</span>
                        <span style="background: {% if para_duplication_rate >= 0.3 %}#ffebee{% elif para_duplication_rate >= 0.1 %}#fff3e0{% else %}#e8f5e9{% endif %}; color: {% if para_duplication_rate >= 0.3 %}#c62828{% elif para_duplication_rate >= 0.1 %}#ef6c00{% else %}#2e7d32{% endif %}; padding: 2px 10px; border-radius: 10px; font-size: 12px; font-weight: 600;">
                            {{ para_duplication_percent }}
                        </span>
                    </div>
                    <!-- 重复率进度条 -->
                    <div style="background: #f0f0f0; border-radius: 6px; height: 10px; overflow: hidden;">
                        <div style="background: {% if para_duplication_rate >= 0.3 %}linear-gradient(90deg, #ef5350, #c62828){% elif para_duplication_rate >= 0.1 %}linear-gradient(90deg, #ffb74d, #ef6c00){% else %}linear-gradient(90deg, #66bb6a, #43a047){% endif %}; width: {{ (para_duplication_rate * 100)|round|int }}%; height: 100%; border-radius: 6px; transition: width 0.5s;"></div>
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #999;">
                        涉及重复 {{ involved_paragraphs }} / {{ body_paras }} 段
                    </div>
                </div>
                
                <!-- 重复段落对指标 -->
                <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="color: #666; font-size: 13px;">重复段落对</span>
                        <span style="background: #e3f2fd; color: #1565c0; padding: 2px 10px; border-radius: 10px; font-size: 12px; font-weight: 600;">
                            {{ duplicate_count }} 对
                        </span>
                    </div>
                    <div style="display: flex; gap: 8px; margin-top: 8px;">
                        <div style="flex: 1; background: #ffebee; border-radius: 6px; padding: 10px; text-align: center;">
                            <div style="font-size: 18px; font-weight: bold; color: #c62828;">{{ severe_count }}</div>
                            <div style="font-size: 11px; color: #c62828;">严重(≥50%)</div>
                        </div>
                        <div style="flex: 1; background: #fff3e0; border-radius: 6px; padding: 10px; text-align: center;">
                            <div style="font-size: 18px; font-weight: bold; color: #ef6c00;">{{ duplicate_by_level.warning }}</div>
                            <div style="font-size: 11px; color: #ef6c00;">中等</div>
                        </div>
                        <div style="flex: 1; background: #e8f5e9; border-radius: 6px; padding: 10px; text-align: center;">
                            <div style="font-size: 18px; font-weight: bold; color: #2e7d32;">{{ duplicate_by_level.pass }}</div>
                            <div style="font-size: 11px; color: #2e7d32;">轻微</div>
                        </div>
                    </div>
                </div>
                
                <!-- 平均相似度指标 -->
                <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="color: #666; font-size: 13px;">平均相似度</span>
                        <span style="background: {% if avg_similarity >= 0.5 %}#ffebee{% elif avg_similarity >= 0.3 %}#fff3e0{% else %}#e8f5e9{% endif %}; color: {% if avg_similarity >= 0.5 %}#c62828{% elif avg_similarity >= 0.3 %}#ef6c00{% else %}#2e7d32{% endif %}; padding: 2px 10px; border-radius: 10px; font-size: 12px; font-weight: 600;">
                            {{ avg_similarity_percent }}
                        </span>
                    </div>
                    <!-- 相似度仪表盘 -->
                    <div style="position: relative; height: 60px; display: flex; align-items: flex-end; justify-content: center;">
                        <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 8px; background: #f0f0f0; border-radius: 4px;"></div>
                        <div style="position: absolute; bottom: 0; left: 0; width: 30%; background: #66bb6a; border-radius: 4px 0 0 4px;"></div>
                        <div style="position: absolute; bottom: 0; left: 30%; width: 20%; background: #ffb74d; border-radius: 0;"></div>
                        <div style="position: absolute; bottom: 0; left: 50%; width: 50%; background: #ef5350; border-radius: 0 4px 4px 0;"></div>
                        <div style="position: absolute; bottom: {% if avg_similarity >= 0.5 %}40{% elif avg_similarity >= 0.3 %}25{% else %}10{% endif %}px; left: calc({{ (avg_similarity * 100)|round|int }}% - 8px); width: 16px; height: 16px; background: white; border: 3px solid #333; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 11px; color: #999;">
                        <span>0%</span><span>30%</span><span>50%</span><span>100%</span>
                    </div>
                </div>
            </div>
            
            <!-- 状态判定 -->
            <div style="background: white; border-radius: 10px; padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    {% if pass_status == 'pass' %}
                    <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #66bb6a, #43a047); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 12px rgba(67, 160, 71, 0.4);">✅</div>
                    <div>
                        <div style="font-weight: bold; color: #2e7d32; font-size: 16px;">状态：通过</div>
                        <div style="color: #666; font-size: 13px;">正文重复率低于 10%，符合投标文件规范</div>
                    </div>
                    {% elif pass_status == 'warning' %}
                    <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #ffb74d, #ef6c00); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 12px rgba(239, 108, 0, 0.4);">⚠️</div>
                    <div>
                        <div style="font-weight: bold; color: #ef6c00; font-size: 16px;">状态：警告</div>
                        <div style="color: #666; font-size: 13px;">正文重复率 10%-30%，建议检查重复内容</div>
                    </div>
                    {% else %}
                    <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #ef5350, #c62828); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 12px rgba(198, 40, 40, 0.4);">❌</div>
                    <div>
                        <div style="font-weight: bold; color: #c62828; font-size: 16px;">状态：不合格</div>
                        <div style="color: #666; font-size: 13px;">正文重复率超过 30%，需大幅修改</div>
                    </div>
                    {% endif %}
                </div>
                <div style="text-align: right; color: #999; font-size: 12px;">
                    <div>已过滤标题段落 <strong>{{ title_paras }}</strong> 段</div>
                    <div>总段落数 <strong>{{ total_paras }}</strong> 段</div>
                </div>
            </div>
        </div>
        
        <!-- 文件列表 -->
        <div class="content-section">
            <h2>📁 检测文件列表</h2>
            <table>
                <thead>
                    <tr>
                        <th>序号</th>
                        <th>文件名</th>
                        <th>字符数</th>
                        <th>段落数</th>
                        <th>涉及重复</th>
                    </tr>
                </thead>
                <tbody>
                    {% for file in file_list %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>{{ file.name }}</td>
                        <td>{{ file.char_count }}</td>
                        <td>{{ file.para_count }}</td>
                        <td>{{ file.duplicate_count }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <!-- 重复详情 -->
        <div class="content-section">
            <h2>📍 重复段落详情（共 {{ duplicate_total }} 对）</h2>
            
            {% if duplicate_details %}
            <!-- 重复统计摘要 -->
            <div style="background: #f5f5f5; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                <p style="margin: 0 0 8px 0; color: #666; font-size: 13px;">
                    以下列出所有检测到的重复段落对。相似度越高说明重复越严重，建议优先修改。
                </p>
                <div style="display: flex; gap: 12px; font-size: 13px;">
                    <span style="color: #f5222d;">● 🔴 严重（≥50%）：{{ duplicate_by_level.fail }} 对</span>
                    <span style="color: #faad14;">● 🟡 中等（30-50%）：{{ duplicate_by_level.warning }} 对</span>
                    <span style="color: #52c41a;">● 🟢 轻微（<30%）：{{ duplicate_by_level.pass }} 对</span>
                </div>
            </div>
            
            <!-- 重复段落列表 -->
            {% for dup in duplicate_details %}
            <div class="duplicate-block {{ dup.level }}" id="{{ dup.id }}" style="margin-bottom: 24px; page-break-inside: avoid;">
                <div class="duplicate-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h3 style="margin: 0; font-size: 15px;">
                        {% if dup.level == 'fail' %}🔴{% elif dup.level == 'warning' %}🟡{% else %}🟢{% endif %}
                        第{{ dup.index }}对重复 — 相似度 {{ dup.similarity_percent }}
                    </h3>
                    <span class="badge {{ dup.level_badge }}">{{ dup.level_text }}</span>
                </div>
                
                <p style="margin: 0 0 12px 0; color: #666; font-size: 13px;">
                    <strong>位置：</strong>
                    {% if dup.source_heading %}<em>{{ dup.source_heading }}</em> → {% endif %}
                    {{ dup.source_file }} <strong>第{{ dup.source_index }}段</strong>（{{ dup.source.char_count }}字）
                    <br>
                    <span style="margin-left: 40px;">
                    {% if dup.target_heading %}<em>{{ dup.target_heading }}</em> → {% endif %}
                    {{ dup.target_file }} <strong>第{{ dup.target_index }}段</strong>（{{ dup.target.char_count }}字）
                    </span>
                </p>
                
                <div style="margin-top: 12px;">
                    <div style="font-weight: bold; color: #333; margin-bottom: 8px; font-size: 13px;">
                        📄 重复内容对比：
                    </div>
                    <div style="display: flex; gap: 12px;">
                        <div style="flex: 1; background: #ffe7e7; padding: 12px; border-radius: 4px;">
                            <div style="font-size: 12px; color: #666; margin-bottom: 6px;">
                                {% if dup.source_heading %}<strong>所属章节：</strong>{{ dup.source_heading }}<br>{% endif %}
                                📄 <strong>{{ dup.source_file }}</strong> 第{{ dup.source_index }}段：
                            </div>
                            <pre style="margin: 0; font-size: 13px; line-height: 1.8; white-space: pre-wrap; word-break: break-word; font-family: inherit;">{{ dup.source.text }}</pre>
                        </div>
                        <div style="flex: 1; background: #fff7e6; padding: 12px; border-radius: 4px;">
                            <div style="font-size: 12px; color: #666; margin-bottom: 6px;">
                                📄 <strong>{{ dup.target_file }}</strong> 第{{ dup.target_index }}段：
                            </div>
                            <pre style="margin: 0; font-size: 13px; line-height: 1.8; white-space: pre-wrap; word-break: break-word; font-family: inherit;">{{ dup.target.text }}</pre>
                        </div>
                    </div>
                </div>
                
                <div style="margin-top: 12px; background: #f6ffed; padding: 10px; border-radius: 4px; border-left: 3px solid #52c41a;">
                    <div style="font-size: 12px; color: #52c41a; font-weight: bold; margin-bottom: 4px;">💡 修改建议</div>
                    <p style="margin: 0; font-size: 13px; color: #666;">
                        建议调整表述方式，换用同义词或改变句式结构，避免与对比文件高度相似。
                    </p>
                </div>
            </div>
            {% endfor %}
            
            {% else %}
            <p style="text-align: center; color: #52c41a; padding: 40px;">✅ 未检测到重复段落</p>
            {% endif %}
        </div>
        
        <!-- 大段落重复 -->
        {% if large_blocks %}
        <div class="content-section">
            <h2>⚠️ 大段落连续重复警告</h2>
            {% for block in large_blocks %}
            <div class="duplicate-block warning">
                <h3>连续 {{ block.count }} 段重复：{{ block.file1 }} vs {{ block.file2 }}</h3>
                <p>位置：第{{ block.start_index }}段 - 第{{ block.end_index }}段</p>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <!-- 底部 -->
        <div class="footer">
            <p>投标文件查重报告 | 由 tender-similarity-analyzer 生成</p>
            <p>本报告仅供内部参考，请妥善保管</p>
        </div>
    </div>
</body>
</html>
        '''
