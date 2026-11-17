#!/usr/bin/env python3
"""
故障树概率计算脚本
计算顶事件概率及基本事件重要性分析
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict


def load_fta_data(input_path):
    """加载FTA数据文件"""
    path = Path(input_path)
    suffix = path.suffix.lower()
    
    if suffix == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif suffix in ['.yaml', '.yml']:
        try:
            import yaml
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except ImportError:
            print(json.dumps({"status": "error", "message": "请安装 pyyaml: pip install pyyaml"}))
            sys.exit(1)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)


def build_tree_structure(data):
    """构建树结构"""
    nodes = data.get('nodes', {})
    edges = data.get('edges', [])
    
    children = defaultdict(list)
    for edge in edges:
        children[edge['from']].append(edge['to'])
    
    return nodes, children


def calculate_gate_probability(node_type, child_probs):
    """计算逻辑门概率"""
    if not child_probs:
        return 0.0
    
    if node_type == 'and':
        result = 1.0
        for p in child_probs.values():
            result *= p
        return result
    elif node_type == 'or':
        result = 1.0
        for p in child_probs.values():
            result *= (1 - p)
        return 1 - result
    else:
        return list(child_probs.values())[0] if child_probs else 0.0


def calculate_probabilities(data):
    """递归计算所有节点概率"""
    nodes, children = build_tree_structure(data)
    top_event = data.get('top_event')
    
    prob_cache = {}
    
    def calculate_recursive(node_id):
        if node_id in prob_cache:
            return prob_cache[node_id]
        
        node = nodes.get(node_id)
        if not node:
            return 0.0
        
        if node['type'] == 'basic':
            prob_cache[node_id] = node.get('probability', 0.0)
            return prob_cache[node_id]
        
        child_probs = {}
        for child_id in children.get(node_id, []):
            child_probs[child_id] = calculate_recursive(child_id)
        
        prob_cache[node_id] = calculate_gate_probability(node['type'], child_probs)
        return prob_cache[node_id]
    
    top_prob = calculate_recursive(top_event) if top_event else 0.0
    
    return prob_cache, top_prob


def find_minimal_cut_sets(data):
    """寻找最小割集"""
    nodes, children = build_tree_structure(data)
    top_event = data.get('top_event')
    
    def get_cut_sets_recursive(node_id):
        node = nodes.get(node_id)
        if not node:
            return [set()]
        
        if node['type'] == 'basic':
            return [{node_id}]
        
        child_cuts = []
        for child_id in children.get(node_id, []):
            child_cuts.append(get_cut_sets_recursive(child_id))
        
        if node['type'] == 'and':
            result = [set()]
            for cuts in child_cuts:
                new_result = []
                for r in result:
                    for c in cuts:
                        new_result.append(r | c)
                result = new_result
            return result
        elif node['type'] == 'or':
            result = []
            for cuts in child_cuts:
                result.extend(cuts)
            return result
        else:
            return child_cuts[0] if child_cuts else [set()]
    
    all_cuts = get_cut_sets_recursive(top_event)
    
    minimal_cuts = []
    all_cuts = [frozenset(c) for c in all_cuts if c]
    
    for cut in all_cuts:
        is_minimal = True
        for other in all_cuts:
            if cut != other and cut.issuperset(other):
                is_minimal = False
                break
        if is_minimal and cut not in [frozenset(c) for c in minimal_cuts]:
            minimal_cuts.append(set(cut))
    
    minimal_cuts.sort(key=lambda x: len(x))
    return minimal_cuts


def calculate_importance(data, node_probs, top_prob):
    """计算重要性指标"""
    nodes = data.get('nodes', {})
    importance = {}
    
    basic_nodes = [nid for nid, n in nodes.items() if n['type'] == 'basic']
    
    for node_id in basic_nodes:
        original_prob = nodes[node_id]['probability']
        
        nodes[node_id]['probability'] = 1.0
        prob_at_1, _ = calculate_probabilities(data)
        nodes[node_id]['probability'] = 0.0
        prob_at_0, _ = calculate_probabilities(data)
        nodes[node_id]['probability'] = original_prob
        
        birnbaum = prob_at_1.get(data['top_event'], 0) - prob_at_0.get(data['top_event'], 0)
        
        critical = (original_prob / top_prob * birnbaum) if top_prob > 0 else 0
        
        importance[node_id] = {
            'name': nodes[node_id]['name'],
            'probability': original_prob,
            'birnbaum': round(birnbaum, 6),
            'critical': round(critical, 6)
        }
    
    return importance


def calculate_structural_importance(data):
    """计算结构重要度"""
    nodes, children = build_tree_structure(data)
    basic_nodes = [nid for nid, n in nodes.items() if n['type'] == 'basic']
    
    all_nodes = list(nodes.keys())
    n = len(all_nodes)
    
    structural = {}
    
    for basic_id in basic_nodes:
        count = 0
        for node_id in all_nodes:
            node = nodes.get(node_id)
            if node['type'] in ['intermediate', 'and', 'or']:
                descendants = get_descendants(node_id, children)
                if basic_id in descendants:
                    child_count = len(children.get(node_id, []))
                    if child_count > 0:
                        count += 1.0 / child_count
        
        structural[basic_id] = round(count / n, 6)
    
    return structural


def get_descendants(node_id, children):
    """获取节点的所有后代"""
    result = set()
    stack = list(children.get(node_id, []))
    
    while stack:
        current = stack.pop()
        result.add(current)
        stack.extend(children.get(current, []))
    
    return result


def format_output(data, node_probs, top_prob, min_cuts, importance, structural):
    """格式化输出结果"""
    nodes = data.get('nodes', {})
    top_event = data.get('top_event', '')
    
    result = {
        "status": "success",
        "system_name": data.get('name', '未命名系统'),
        "top_event": {
            "id": top_event,
            "name": nodes.get(top_event, {}).get('name', ''),
            "probability": round(top_prob, 8),
            "probability_scientific": f"{top_prob:.6e}"
        },
        "node_probabilities": [
            {
                "id": nid,
                "name": nodes[nid]['name'],
                "type": nodes[nid]['type'],
                "probability": round(prob, 8)
            }
            for nid, prob in sorted(node_probs.items(), key=lambda x: -x[1]) 
            if nodes.get(x[0], {}).get('type') != 'basic'
        ],
        "minimal_cut_sets": [
            {
                "order": len(cut),
                "events": [
                    {
                        "id": eid,
                        "name": nodes[eid]['name'],
                        "probability": nodes[eid].get('probability', 0)
                    }
                    for eid in sorted(cut)
                ]
            }
            for cut in min_cuts[:20]
        ],
        "minimal_cut_sets_summary": {
            "total": len(min_cuts),
            "first_order": len([c for c in min_cuts if len(c) == 1]),
            "second_order": len([c for c in min_cuts if len(c) == 2])
        },
        "importance_analysis": {
            "birnbaum_importance": sorted(
                [(eid, v['name'], v['birnbaum']) for eid, v in importance.items()],
                key=lambda x: -x[2]
            ),
            "critical_importance": sorted(
                [(eid, v['name'], v['critical']) for eid, v in importance.items()],
                key=lambda x: -x[2]
            ),
            "structural_importance": sorted(
                [(eid, nodes[eid]['name'], v) for eid, v in structural.items()],
                key=lambda x: -x[2]
            )
        }
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description='故障树概率计算工具')
    parser.add_argument('--input', '-i', required=True, help='输入FTA数据文件(JSON/YAML)')
    parser.add_argument('--output', '-o', required=True, help='输出结果文件(JSON)')
    
    args = parser.parse_args()
    
    try:
        data = load_fta_data(args.input)
        
        node_probs, top_prob = calculate_probabilities(data)
        min_cuts = find_minimal_cut_sets(data)
        importance = calculate_importance(data, node_probs, top_prob)
        structural = calculate_structural_importance(data)
        
        result = format_output(data, node_probs, top_prob, min_cuts, importance, structural)
        
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(json.dumps({
            "status": "success",
            "output": str(output_path),
            "top_event_probability": result['top_event']['probability'],
            "minimal_cut_sets_count": result['minimal_cut_sets_summary']['total']
        }, ensure_ascii=False))
        
    except Exception as e:
        import traceback
        print(json.dumps({
            "status": "error", 
            "message": str(e),
            "trace": traceback.format_exc()
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
