#!/usr/bin/env python3
"""
故障树数据导入导出脚本
支持JSON和YAML格式互转
"""

import argparse
import json
import sys
from pathlib import Path


SUPPORTED_FORMATS = ['json', 'yaml', 'yml']


def load_file(file_path):
    """加载文件，自动识别格式"""
    path = Path(file_path)
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
        raise ValueError(f"不支持的格式: {suffix}")


def save_json(data, output_path):
    """保存为JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=False)
    return output_path


def save_yaml(data, output_path):
    """保存为YAML"""
    try:
        import yaml
    except ImportError:
        print(json.dumps({"status": "error", "message": "请安装 pyyaml: pip install pyyaml"}))
        sys.exit(1)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    return output_path


def validate_fta_data(data):
    """验证FTA数据结构"""
    errors = []
    
    if not isinstance(data, dict):
        errors.append("数据必须是JSON对象")
        return errors
    
    if 'top_event' not in data:
        errors.append("E003: 缺少 top_event 字段")
    
    if 'nodes' not in data:
        errors.append("缺少 nodes 字段")
    else:
        nodes = data.get('nodes', {})
        if not isinstance(nodes, dict):
            errors.append("nodes 必须是对象")
        else:
            for node_id, node in nodes.items():
                if not isinstance(node, dict):
                    errors.append(f"节点 '{node_id}' 必须是对象")
                    continue
                
                if 'type' not in node:
                    errors.append(f"节点 '{node_id}' 缺少 type 字段")
                elif node['type'] not in ['basic', 'intermediate', 'and', 'or']:
                    errors.append(f"E001: 无效的节点类型 '{node['type']}'")
                
                if 'name' not in node:
                    errors.append(f"节点 '{node_id}' 缺少 name 字段")
                
                if node.get('type') == 'basic':
                    if 'probability' not in node:
                        errors.append(f"E002: 基本事件 '{node_id}' 缺少 probability 字段")
                    elif not isinstance(node['probability'], (int, float)):
                        errors.append(f"节点 '{node_id}' 的 probability 必须是数字")
                    elif not (0 <= node['probability'] <= 1):
                        errors.append(f"E007: 节点 '{node_id}' 概率超出范围 [0,1]")
    
    if 'edges' not in data:
        errors.append("缺少 edges 字段")
    elif not isinstance(data['edges'], list):
        errors.append("edges 必须是数组")
    else:
        node_ids = set(data.get('nodes', {}).keys())
        for i, edge in enumerate(data['edges']):
            if not isinstance(edge, dict):
                errors.append(f"边 {i} 必须是对象")
                continue
            if 'from' not in edge:
                errors.append(f"边 {i} 缺少 from 字段")
            if 'to' not in edge:
                errors.append(f"边 {i} 缺少 to 字段")
            if 'from' in edge and edge['from'] not in node_ids:
                errors.append(f"E005: 边引用未定义节点 '{edge['from']}'")
            if 'to' in edge and edge['to'] not in node_ids:
                errors.append(f"E005: 边引用未定义节点 '{edge['to']}'")
    
    top_event = data.get('top_event')
    if top_event and top_event not in data.get('nodes', {}):
        errors.append(f"E003: 顶事件 '{top_event}' 未定义")
    
    return errors


def convert_format(data, output_path):
    """转换数据格式"""
    suffix = Path(output_path).suffix.lower()
    
    if suffix == '.json':
        return save_json(data, output_path)
    elif suffix in ['.yaml', '.yml']:
        return save_yaml(data, output_path)
    else:
        raise ValueError(f"不支持的输出格式: {suffix}")


def export_to_standard(data, output_path):
    """导出为标准JSON格式"""
    result = {
        "name": data.get('name', '未命名'),
        "description": data.get('description', ''),
        "version": data.get('version', '1.0'),
        "top_event": data.get('top_event'),
        "nodes": data.get('nodes', {}),
        "edges": data.get('edges', [])
    }
    return save_json(result, output_path)


def main():
    parser = argparse.ArgumentParser(description='故障树数据导入导出工具')
    parser.add_argument('--mode', '-m', required=True, 
                        choices=['import', 'export', 'validate'],
                        help='操作模式: import(导入) / export(导出) / validate(验证)')
    parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径 (validate模式不需要)')
    parser.add_argument('--standard', action='store_true', 
                        help='导出为标准格式 (仅export模式)')
    
    args = parser.parse_args()
    
    try:
        data = load_file(args.input)
        
        if args.mode == 'validate':
            errors = validate_fta_data(data)
            if errors:
                print(json.dumps({
                    "status": "error",
                    "valid": False,
                    "errors": errors
                }, ensure_ascii=False))
            else:
                print(json.dumps({
                    "status": "success",
                    "valid": True,
                    "message": "数据结构验证通过"
                }, ensure_ascii=False))
            return
        
        if not args.output:
            print(json.dumps({
                "status": "error",
                "message": "export模式必须指定 --output 参数"
            }, ensure_ascii=False))
            sys.exit(1)
        
        errors = validate_fta_data(data)
        if errors:
            print(json.dumps({
                "status": "error",
                "errors": errors
            }, ensure_ascii=False))
            sys.exit(1)
        
        if args.mode == 'import':
            output_path = convert_format(data, args.output)
        elif args.mode == 'export':
            if args.standard:
                output_path = export_to_standard(data, args.output)
            else:
                output_path = convert_format(data, args.output)
        
        print(json.dumps({
            "status": "success",
            "input": args.input,
            "output": output_path,
            "node_count": len(data.get('nodes', {})),
            "edge_count": len(data.get('edges', []))
        }, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
