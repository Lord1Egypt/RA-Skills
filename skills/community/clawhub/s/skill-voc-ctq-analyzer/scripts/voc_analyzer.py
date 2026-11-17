#!/usr/bin/env python3
"""
VOC-CTQ Analyzer: 客户声音转关键质量特性分析工具
支持模式: input, import, analyze, extract-ctq, map, evaluate, visualize, full
"""

import argparse
import json
import csv
import os
import sys
import re
from datetime import datetime
from collections import Counter
from pathlib import Path

try:
    import jieba
    import jieba.posseg as pseg
except ImportError:
    print("Error: jieba not installed. Run: pip install jieba==0.42.1")
    sys.exit(1)

try:
    from snownlp import SnowNLP
except ImportError:
    print("Warning: snownlp not installed, sentiment analysis will use rule-based method")
    SnowNLP = None

try:
    from pyecharts import options as opts
    from pyecharts.charts import Sankey, WordCloud, Bar, Pie, Page
    from pyecharts.globals import SymbolType
except ImportError:
    print("Error: pyecharts not installed. Run: pip install pyecharts==2.0.4")
    sys.exit(1)


# 全局配置
DEFAULT_WEIGHT = 1.0
VOC_COUNTER = 0
CTQ_COUNTER = 0


def generate_voc_id():
    global VOC_COUNTER
    VOC_COUNTER += 1
    return f"voc_{VOC_COUNTER:03d}"


def generate_ctq_id():
    global CTQ_COUNTER
    CTQ_COUNTER += 1
    return f"ctq_{CTQ_COUNTER:03d}"


# ============ 文本分析模块 ============

def segment_text(text):
    """中文分词"""
    words = list(jieba.cut(text))
    return words


def extract_keywords(text, topk=10):
    """提取关键词"""
    words = list(jieba.cut(text))
    # 过滤停用词和单字
    stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
    filtered = [w for w in words if len(w) > 1 and w not in stopwords]
    word_freq = Counter(filtered)
    return word_freq.most_common(topk)


def analyze_sentiment(text):
    """情感分析"""
    if SnowNLP:
        try:
            s = SnowNLP(text)
            score = s.sentiments  # 0-1, 1=positive
            return score
        except:
            pass
    # 备用：基于情感词典
    positive_words = ['好', '满意', '喜欢', '赞', '棒', '优秀', '完美', '推荐', '感谢', '不错', '优质']
    negative_words = ['差', '坏', '烂', '失望', '投诉', '垃圾', '退货', '退款', '太差', '糟糕', '问题']
    text_lower = text.lower()
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    total = pos_count + neg_count
    if total == 0:
        return 0.5
    return pos_count / total


def classify_requirement(text):
    """需求分类"""
    keywords_map = {
        'quality': ['质量', '品质', '耐用', '故障', '损坏', '坏', '问题', '瑕疵'],
        'function': ['功能', '实用', '能用', '使用', '操作', '方便'],
        'service': ['服务', '态度', '售后', '客服', '响应', '处理'],
        'price': ['价格', '便宜', '贵', '性价比', '划算', '值'],
        'appearance': ['外观', '颜色', '设计', '好看', '漂亮', '款式'],
        'delivery': ['发货', '快递', '物流', '速度', '配送', '送货']
    }
    text_lower = text
    for req_type, keywords in keywords_map.items():
        if any(kw in text_lower for kw in keywords):
            return req_type
    return 'other'


def analyze_single_voc(voc_item):
    """分析单条VOC"""
    text = voc_item.get('text', '')
    if not text:
        return None
    
    words = segment_text(text)
    keywords = extract_keywords(text)
    sentiment_score = analyze_sentiment(text)
    
    if sentiment_score >= 0.6:
        sentiment_label = 'positive'
    elif sentiment_score <= 0.4:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'
    
    requirement_type = classify_requirement(text)
    
    return {
        'id': voc_item.get('id', generate_voc_id()),
        'original_text': text,
        'segmented_text': words,
        'keywords': [w for w, _ in keywords],
        'keyword_freq': dict(keywords),
        'sentiment_score': round(sentiment_score, 3),
        'sentiment_label': sentiment_label,
        'requirement_type': requirement_type,
        'source': voc_item.get('source', 'unknown'),
        'timestamp': voc_item.get('timestamp', datetime.now().isoformat()),
        'weight': voc_item.get('weight', DEFAULT_WEIGHT)
    }


def load_voc_data(input_path):
    """加载VOC数据"""
    path = Path(input_path)
    suffix = path.suffix.lower()
    
    feedbacks = []
    
    if suffix == '.json':
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'feedbacks' in data:
                feedbacks = data['feedbacks']
            elif isinstance(data, list):
                feedbacks = data
            else:
                feedbacks = [data]
    elif suffix == '.csv':
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                feedbacks.append(row)
    elif suffix == '.txt':
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    feedbacks.append({'text': line})
    else:
        raise ValueError(f"Unsupported file format: {suffix}")
    
    return feedbacks


# ============ CTQ提取模块 ============

def extract_ctq_candidates(analyzed_vocs, min_frequency=3):
    """从分析结果中提取CTQ候选"""
    all_keywords = Counter()
    keyword_by_type = {}
    
    for voc in analyzed_vocs:
        req_type = voc['requirement_type']
        if req_type not in keyword_by_type:
            keyword_by_type[req_type] = Counter()
        for kw, freq in voc['keyword_freq'].items():
            all_keywords[kw] += freq
            keyword_by_type[req_type][kw] += freq
    
    # 按类别提取高频关键词作为CTQ候选
    category_names = {
        'quality': '质量特性',
        'function': '功能特性',
        'service': '服务特性',
        'price': '价格特性',
        'appearance': '外观特性',
        'delivery': '交付特性',
        'other': '其他特性'
    }
    
    ctqs = []
    for req_type, keywords in keyword_by_type.items():
        top_keywords = keywords.most_common(5)
        for kw, freq in top_keywords:
            if freq >= min_frequency:
                ctqs.append({
                    'id': generate_ctq_id(),
                    'name': f"{kw}相关特性",
                    'description': f"与{kw}相关的{category_names.get(req_type, '特性')}",
                    'category': req_type,
                    'keywords': [kw],
                    'frequency': freq,
                    'weight': DEFAULT_WEIGHT,
                    'status': 'candidate'
                })
    
    # 全局高频词作为独立CTQ
    global_top = all_keywords.most_common(10)
    existing_names = {ctq['keywords'][0] for ctq in ctqs}
    for kw, freq in global_top:
        if freq >= min_frequency and kw not in existing_names:
            ctqs.append({
                'id': generate_ctq_id(),
                'name': f"{kw}优化",
                'description': f"关于{kw}的质量改进需求",
                'category': 'other',
                'keywords': [kw],
                'frequency': freq,
                'weight': DEFAULT_WEIGHT,
                'status': 'candidate'
            })
    
    return ctqs


def load_ctq_data(ctq_path):
    """加载CTQ数据"""
    with open(ctq_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('ctqs', [])


# ============ 映射模块 ============

def create_voc_ctq_mapping(analyzed_vocs, ctqs):
    """建立VOC与CTQ的映射关系"""
    mappings = []
    unmapped_vocs = []
    
    for voc in analyzed_vocs:
        voc_keywords = set(voc['keywords'])
        best_mapping = None
        best_confidence = 0
        
        for ctq in ctqs:
            ctq_keywords = set(ctq.get('keywords', []))
            match = voc_keywords & ctq_keywords
            
            if match:
                confidence = len(match) / max(len(voc_keywords), 1)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_mapping = {
                        'voc_id': voc['id'],
                        'ctq_id': ctq['id'],
                        'ctq_name': ctq['name'],
                        'confidence': round(confidence, 2),
                        'match_keywords': list(match)
                    }
        
        if best_mapping:
            mappings.append(best_mapping)
        else:
            unmapped_vocs.append(voc['id'])
    
    # 统计
    total_vocs = len(analyzed_vocs)
    mapped_count = len(mappings)
    unique_ctqs = len(set(m['ctq_id'] for m in mappings))
    
    summary = {
        'total_vocs': total_vocs,
        'mapped_vocs': mapped_count,
        'unmapped_vocs': len(unmapped_vocs),
        'unmapped_voc_ids': unmapped_vocs,
        'total_ctqs': len(ctqs),
        'covered_ctqs': unique_ctqs,
        'coverage_rate': round(mapped_count / total_vocs, 2) if total_vocs > 0 else 0
    }
    
    return {'mappings': mappings, 'mapping_summary': summary}


# ============ 评估模块 ============

def evaluate_ctq_priority(mapping_data, analyzed_vocs):
    """评估CTQ优先级"""
    mappings = mapping_data['mappings']
    voc_dict = {v['id']: v for v in analyzed_vocs}
    
    # 收集每个CTQ的统计数据
    ctq_stats = {}
    for mapping in mappings:
        ctq_id = mapping['ctq_id']
        voc_id = mapping['voc_id']
        voc = voc_dict.get(voc_id, {})
        
        if ctq_id not in ctq_stats:
            ctq_stats[ctq_id] = {
                'ctq_id': ctq_id,
                'ctq_name': mapping['ctq_name'],
                'voc_count': 0,
                'total_sentiment': 0,
                'total_weight': 0,
                'avg_confidence': 0,
                'voc_ids': []
            }
        
        stats = ctq_stats[ctq_id]
        stats['voc_count'] += 1
        stats['total_sentiment'] += voc.get('sentiment_score', 0.5)
        stats['total_weight'] += voc.get('weight', DEFAULT_WEIGHT)
        stats['avg_confidence'] += mapping['confidence']
        stats['voc_ids'].append(voc_id)
    
    # 计算各项分数
    max_voc_count = max(s['voc_count'] for s in ctq_stats.values()) if ctq_stats else 1
    scores = []
    
    for ctq_id, stats in ctq_stats.items():
        freq_score = stats['voc_count'] / max_voc_count
        sentiment_score = 1 - (stats['total_sentiment'] / stats['voc_count'])  # 负面越多分数越高
        importance_score = stats['total_weight'] / stats['voc_count']
        
        # 综合评分
        final_score = (0.4 * freq_score + 0.3 * sentiment_score + 0.3 * importance_score)
        
        # 确定优先级
        if final_score >= 0.8:
            priority_level = 'P0'
        elif final_score >= 0.6:
            priority_level = 'P1'
        elif final_score >= 0.4:
            priority_level = 'P2'
        else:
            priority_level = 'P3'
        
        scores.append({
            'ctq_id': ctq_id,
            'ctq_name': stats['ctq_name'],
            'voc_count': stats['voc_count'],
            'frequency_score': round(freq_score, 3),
            'sentiment_score': round(sentiment_score, 3),
            'importance_score': round(importance_score, 3),
            'final_score': round(final_score, 3),
            'priority_level': priority_level,
            'voc_ids': stats['voc_ids']
        })
    
    # 按分数排序
    scores.sort(key=lambda x: x['final_score'], reverse=True)
    
    # 添加排名
    for i, score in enumerate(scores):
        score['priority_rank'] = i + 1
    
    return {
        'ctq_scores': scores,
        'scoring_method': {
            'frequency_weight': 0.4,
            'sentiment_weight': 0.3,
            'importance_weight': 0.3
        },
        'total_ctqs_evaluated': len(scores)
    }


# ============ 可视化模块 ============

def generate_html_report(scored_data, analyzed_vocs, mapping_data, output_path):
    """生成HTML可视化报告"""
    
    page = Page(page_title="VOC-CTQ分析报告")
    
    # 1. 桑基图 - VOC到CTQ的映射关系
    sankey_data = []
    sankey_links = []
    
    # 构建节点
    req_types = set(v['requirement_type'] for v in analyzed_vocs)
    type_names = {
        'quality': '质量需求',
        'function': '功能需求',
        'service': '服务需求',
        'price': '价格需求',
        'appearance': '外观需求',
        'delivery': '交付需求',
        'other': '其他需求'
    }
    
    for req_type in req_types:
        sankey_data.append({"name": type_names.get(req_type, req_type)})
    
    ctq_names = {}
    for score in scored_data['ctq_scores'][:10]:  # 只显示top10
        sankey_data.append({"name": score['ctq_name']})
        ctq_names[score['ctq_id']] = score['ctq_name']
    
    # 构建链接
    voc_dict = {v['id']: v for v in analyzed_vocs}
    type_count = Counter(v['requirement_type'] for v in analyzed_vocs)
    
    for mapping in mapping_data['mappings']:
        voc = voc_dict.get(mapping['voc_id'], {})
        req_type = voc.get('requirement_type', 'other')
        ctq_name = ctq_names.get(mapping['ctq_id'])
        
        if ctq_name:
            sankey_links.append({
                "source": type_names.get(req_type, req_type),
                "target": ctq_name,
                "value": 1
            })
    
    if sankey_data and sankey_links:
        sankey = (
            Sankey()
            .add("VOC-CTQ映射",
                 sankey_data,
                 sankey_links,
                 linestyle_opt=opts.LineStyleOpts(opacity=0.3, curve=0.5, color="source"),
                 node_align="left")
            .set_global_opts(title_opts=opts.TitleOpts(title="客户需求流向图"))
        )
        page.add(sankey)
    
    # 2. 词云 - 高频需求词
    word_freq = Counter()
    for voc in analyzed_vocs:
        for kw in voc['keywords']:
            word_freq[kw] += 1
    
    wordcloud_words = [(w, c) for w, c in word_freq.most_common(50)]
    if wordcloud_words:
        wordcloud = (
            WordCloud()
            .add("", wordcloud_words, word_size_range=[20, 80], shape=SymbolType.ROUND_RECT)
            .set_global_opts(title_opts=opts.TitleOpts(title="高频需求词云"))
        )
        page.add(wordcloud)
    
    # 3. 饼图 - 需求类型分布
    type_data = [(type_names.get(t, t), c) for t, c in type_count.items()]
    if type_data:
        pie_items = [opts.PieItem(name=n, value=v) for n, v in type_data]
        pie = (
            Pie()
            .add("", pie_items, radius=["30%", "70%"], label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
            .set_global_opts(title_opts=opts.TitleOpts(title="需求类型分布"), legend_opts=opts.LegendOpts(orient="vertical", pos_left="left"))
        )
        page.add(pie)
    
    # 4. 柱状图 - CTQ优先级
    ctq_names_sorted = [s['ctq_name'] for s in scored_data['ctq_scores'][:8]]
    ctq_scores_sorted = [s['final_score'] for s in scored_data['ctq_scores'][:8]]
    ctq_colors = {
        'P0': '#FF4444',
        'P1': '#FF8800',
        'P2': '#4488FF',
        'P3': '#88AA88'
    }
    ctq_levels = [s['priority_level'] for s in scored_data['ctq_scores'][:8]]
    
    if ctq_names_sorted:
        bar = (
            Bar()
            .add_xaxis(ctq_names_sorted)
            .add_yaxis("优先级评分", ctq_scores_sorted, 
                       color=[ctq_colors.get(l, '#4488FF') for l in ctq_levels])
            .set_global_opts(title_opts=opts.TitleOpts(title="CTQ优先级排名"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
                             datazoom_opts=opts.DataZoomOpts())
        )
        page.add(bar)
    
    # 生成HTML
    html_content = page.render_embed()
    
    # 添加完整HTML包装
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>VOC-CTQ 分析报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .header p {{ margin: 0; opacity: 0.9; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-card h3 {{ color: #666; font-size: 14px; margin: 0 0 10px 0; }}
        .stat-card .value {{ font-size: 28px; font-weight: bold; color: #333; }}
        .chart-section {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .chart-section h2 {{ margin: 0 0 15px 0; color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        .priority-badge {{ padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; color: white; }}
        .priority-P0 {{ background: #FF4444; }}
        .priority-P1 {{ background: #FF8800; }}
        .priority-P2 {{ background: #4488FF; }}
        .priority-P3 {{ background: #88AA88; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>VOC-CTQ 分析报告</h1>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <h3>客户反馈数量</h3>
                <div class="value">{len(analyzed_vocs)}</div>
            </div>
            <div class="stat-card">
                <h3>提取CTQ数量</h3>
                <div class="value">{scored_data['total_ctqs_evaluated']}</div>
            </div>
            <div class="stat-card">
                <h3>映射覆盖率</h3>
                <div class="value">{mapping_data['mapping_summary']['coverage_rate']*100:.1f}%</div>
            </div>
            <div class="stat-card">
                <h3>P0优先级数量</h3>
                <div class="value">{sum(1 for s in scored_data['ctq_scores'] if s['priority_level']=='P0')}</div>
            </div>
        </div>
        
        <div class="chart-section">
            <h2>可视化图表</h2>
            {html_content}
        </div>
        
        <div class="chart-section">
            <h2>CTQ优先级评分表</h2>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>CTQ名称</th>
                        <th>频率评分</th>
                        <th>情感评分</th>
                        <th>权重评分</th>
                        <th>综合评分</th>
                        <th>优先级</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''<tr>
                        <td>{s['priority_rank']}</td>
                        <td>{s['ctq_name']}</td>
                        <td>{s['frequency_score']:.2f}</td>
                        <td>{s['sentiment_score']:.2f}</td>
                        <td>{s['importance_score']:.2f}</td>
                        <td><strong>{s['final_score']:.3f}</strong></td>
                        <td><span class="priority-badge priority-{s['priority_level']}">{s['priority_level']}</span></td>
                    </tr>''' for s in scored_data['ctq_scores'])}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"HTML报告已生成: {output_path}")


# ============ 命令行模式 ============

def mode_input():
    """交互式录入模式"""
    print("=" * 50)
    print("VOC-CTQ 分析工具 - 交互式录入")
    print("=" * 50)
    print("请输入客户反馈(输入空行结束):")
    print()
    
    feedbacks = []
    while True:
        try:
            line = input()
            if not line.strip():
                if feedbacks:
                    break
                continue
            feedbacks.append({'text': line.strip()})
        except EOFError:
            break
    
    if feedbacks:
        result = {'feedbacks': feedbacks}
        print(f"\n已录入 {len(feedbacks)} 条客户反馈")
        return result
    return None


def mode_import(args):
    """导入文件模式"""
    if not os.path.exists(args.file):
        print(f"Error: 文件不存在: {args.file}")
        return None
    
    feedbacks = load_voc_data(args.file)
    print(f"成功导入 {len(feedbacks)} 条客户反馈")
    return {'feedbacks': feedbacks}


def mode_analyze(args):
    """分析模式"""
    if args.input:
        feedbacks = load_voc_data(args.input)
    elif args.data:
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)
            feedbacks = data.get('feedbacks', [])
    else:
        print("Error: 需要指定 --input 或 --data 参数")
        return None
    
    analyzed = []
    for fb in feedbacks:
        result = analyze_single_voc(fb)
        if result:
            analyzed.append(result)
    
    # 统计
    word_freq_global = Counter()
    for voc in analyzed:
        for kw, freq in voc['keyword_freq'].items():
            word_freq_global[kw] += freq
    
    stats = {
        'total_count': len(analyzed),
        'positive_count': sum(1 for v in analyzed if v['sentiment_label'] == 'positive'),
        'negative_count': sum(1 for v in analyzed if v['sentiment_label'] == 'negative'),
        'neutral_count': sum(1 for v in analyzed if v['sentiment_label'] == 'neutral'),
        'word_frequency': dict(word_freq_global.most_common(30))
    }
    
    result = {'analyzed_vocs': analyzed, 'statistics': stats}
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"分析结果已保存: {args.output}")
    
    return result


def mode_extract_ctq(args):
    """提取CTQ模式"""
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    analyzed_vocs = data.get('analyzed_vocs', [])
    if not analyzed_vocs:
        print("Error: 未找到分析数据")
        return None
    
    ctqs = extract_ctq_candidates(analyzed_vocs, min_frequency=args.min_freq)
    result = {'ctqs': ctqs}
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"CTQ候选已保存: {args.output}")
        print(f"共提取 {len(ctqs)} 个CTQ候选")
    
    return result


def mode_map(args):
    """映射模式"""
    # 加载VOC数据
    with open(args.voc, 'r', encoding='utf-8') as f:
        voc_data = json.load(f)
    analyzed_vocs = voc_data.get('analyzed_vocs', [])
    
    # 加载CTQ数据
    ctqs = load_ctq_data(args.ctq)
    
    mapping_result = create_voc_ctq_mapping(analyzed_vocs, ctqs)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(mapping_result, f, ensure_ascii=False, indent=2)
        print(f"映射关系已保存: {args.output}")
        print(f"覆盖率: {mapping_result['mapping_summary']['coverage_rate']*100:.1f}%")
    
    return mapping_result


def mode_evaluate(args):
    """评估模式"""
    # 加载映射数据
    with open(args.mapping, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)
    
    # 尝试加载VOC数据
    analyzed_vocs = []
    if os.path.exists(args.mapping.replace('_mapping.json', '_analyzed.json')):
        with open(args.mapping.replace('_mapping.json', '_analyzed.json'), 'r', encoding='utf-8') as f:
            analyzed_vocs = json.load(f).get('analyzed_vocs', [])
    
    if not analyzed_vocs and os.path.exists('analyzed_vocs.json'):
        with open('analyzed_vocs.json', 'r', encoding='utf-8') as f:
            analyzed_vocs = json.load(f).get('analyzed_vocs', [])
    
    if not analyzed_vocs:
        print("Warning: 未找到VOC数据，使用默认情感值")
    
    scored_result = evaluate_ctq_priority(mapping_data, analyzed_vocs)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(scored_result, f, ensure_ascii=False, indent=2)
        print(f"评分结果已保存: {args.output}")
        
        print("\n优先级排名:")
        for s in scored_result['ctq_scores'][:10]:
            print(f"  {s['priority_rank']}. {s['ctq_name']} ({s['priority_level']}): {s['final_score']:.3f}")
    
    return scored_result


def mode_visualize(args):
    """可视化模式"""
    # 加载数据
    with open(args.data, 'r', encoding='utf-8') as f:
        scored_data = json.load(f)
    
    analyzed_vocs = []
    mapping_data = {'mappings': [], 'mapping_summary': {}}
    
    # 尝试加载VOC和映射数据
    base_path = os.path.dirname(args.data)
    base_name = os.path.splitext(os.path.basename(args.data))[0]
    
    voc_path = os.path.join(base_path, 'analyzed_vocs.json')
    map_path = os.path.join(base_path, 'mapping.json')
    
    if os.path.exists(voc_path):
        with open(voc_path, 'r', encoding='utf-8') as f:
            analyzed_vocs = json.load(f).get('analyzed_vocs', [])
    
    if os.path.exists(map_path):
        with open(map_path, 'r', encoding='utf-8') as f:
            mapping_data = json.load(f)
    
    generate_html_report(scored_data, analyzed_vocs, mapping_data, args.output)
    return True


def mode_full(args):
    """全流程模式"""
    print("=" * 50)
    print("VOC-CTQ 全流程分析")
    print("=" * 50)
    
    # 1. 导入数据
    print("\n[1/5] 导入客户反馈...")
    if args.input:
        feedbacks = load_voc_data(args.input)
    else:
        print("Error: 需要指定 --input 参数")
        return None
    print(f"  导入 {len(feedbacks)} 条反馈")
    
    # 2. 分析VOC
    print("\n[2/5] 分析客户反馈...")
    analyzed = []
    for fb in feedbacks:
        result = analyze_single_voc(fb)
        if result:
            analyzed.append(result)
    
    word_freq = Counter()
    for voc in analyzed:
        for kw, freq in voc['keyword_freq'].items():
            word_freq[kw] += freq
    
    analyzed_result = {
        'analyzed_vocs': analyzed,
        'statistics': {
            'total_count': len(analyzed),
            'word_frequency': dict(word_freq.most_common(30))
        }
    }
    
    analyzed_path = os.path.join(args.output, 'analyzed_vocs.json')
    os.makedirs(args.output, exist_ok=True)
    with open(analyzed_path, 'w', encoding='utf-8') as f:
        json.dump(analyzed_result, f, ensure_ascii=False, indent=2)
    print(f"  分析完成，结果保存至: {analyzed_path}")
    
    # 3. 提取CTQ
    print("\n[3/5] 提取CTQ候选...")
    ctqs = extract_ctq_candidates(analyzed, min_frequency=2)
    
    # 如果有模板，合并CTQ
    if args.ctq_template and os.path.exists(args.ctq_template):
        with open(args.ctq_template, 'r', encoding='utf-8') as f:
            template_ctqs = json.load(f).get('ctqs', [])
        ctqs.extend(template_ctqs)
    
    ctq_result = {'ctqs': ctqs}
    ctq_path = os.path.join(args.output, 'ctq_candidates.json')
    with open(ctq_path, 'w', encoding='utf-8') as f:
        json.dump(ctq_result, f, ensure_ascii=False, indent=2)
    print(f"  提取 {len(ctqs)} 个CTQ候选")
    print(f"  建议确认或编辑后保存为: ctq_confirmed.json")
    
    # 4. 映射
    print("\n[4/5] 建立映射关系...")
    print("  请先确认CTQ文件(保存为 ctq_confirmed.json)，然后运行:")
    print(f"    python scripts/voc_analyzer.py --mode map --voc {analyzed_path} --ctq ctq_confirmed.json --output mapping.json")
    
    # 5. 生成可视化
    print("\n[5/5] 完成")
    print(f"  完整流程:")
    print(f"    1. 编辑 {ctq_path} 确认CTQ")
    print(f"    2. 重命名为 ctq_confirmed.json")
    print(f"    3. python scripts/voc_analyzer.py --mode map ...")
    print(f"    4. python scripts/voc_analyzer.py --mode evaluate ...")
    print(f"    5. python scripts/voc_analyzer.py --mode visualize ...")
    
    return analyzed_result


# ============ 主入口 ============

def main():
    parser = argparse.ArgumentParser(description='VOC-CTQ 分析工具')
    parser.add_argument('--mode', choices=['input', 'import', 'analyze', 'extract-ctq', 'map', 'evaluate', 'visualize', 'full'],
                        required=True, help='运行模式')
    
    # 通用参数
    parser.add_argument('--input', help='输入文件路径(JSON/CSV/TXT)')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--data', help='中间数据文件路径')
    
    # import模式
    parser.add_argument('--file', help='导入的文件路径')
    
    # analyze模式
    parser.add_argument('--min-freq', type=int, default=3, help='最小词频阈值')
    
    # map模式
    parser.add_argument('--voc', help='VOC分析结果文件')
    parser.add_argument('--ctq', help='CTQ定义文件')
    
    # mapping/evaluate模式
    parser.add_argument('--mapping', help='映射关系文件')
    
    # extract-ctq模式
    parser.add_argument('--ctq-template', help='CTQ模板文件(可合并)')
    
    args = parser.parse_args()
    
    # 执行对应模式
    if args.mode == 'input':
        result = mode_input()
    elif args.mode == 'import':
        result = mode_import(args)
    elif args.mode == 'analyze':
        result = mode_analyze(args)
    elif args.mode == 'extract-ctq':
        result = mode_extract_ctq(args)
    elif args.mode == 'map':
        result = mode_map(args)
    elif args.mode == 'evaluate':
        result = mode_evaluate(args)
    elif args.mode == 'visualize':
        result = mode_visualize(args)
    elif args.mode == 'full':
        result = mode_full(args)
    
    if result:
        print("\n执行完成!")
    else:
        print("\n执行失败或无输出")


if __name__ == "__main__":
    main()
