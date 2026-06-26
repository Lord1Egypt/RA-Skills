#!/usr/bin/env python3
"""Transform Tool - Convert data between formats."""

import argparse
import csv
import io
import json
import sys
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Union


def csv_to_json(csv_data: str, indent: int = 2) -> str:
    """Convert CSV to JSON."""
    reader = csv.DictReader(io.StringIO(csv_data))
    data = list(reader)
    return json.dumps(data, indent=indent, ensure_ascii=False)


def json_to_csv(json_data: str) -> str:
    """Convert JSON to CSV."""
    data = json.loads(json_data)
    
    if not data:
        return ""
    
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            fieldnames = data[0].keys()
        else:
            return str(data)
    elif isinstance(data, dict):
        fieldnames = data.keys()
        data = [data]
    else:
        return str(data)
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def json_to_yaml(json_data: str, indent: int = 2) -> str:
    """Convert JSON to YAML."""
    data = json.loads(json_data)
    
    def to_yaml(obj, level=0):
        indent_str = ' ' * (indent * level)
        
        if isinstance(obj, dict):
            if not obj:
                return '{}'
            lines = []
            for k, v in obj.items():
                if isinstance(v, (dict, list)) and v:
                    lines.append(f"{indent_str}{k}:")
                    lines.append(to_yaml(v, level + 1))
                else:
                    lines.append(f"{indent_str}{k}: {format_value(v)}")
            return '\n'.join(lines)
        elif isinstance(obj, list):
            if not obj:
                return '[]'
            lines = []
            for item in obj:
                if isinstance(item, dict):
                    lines.append(f"{indent_str}-")
                    for k, v in item.items():
                        if isinstance(v, (dict, list)) and v:
                            lines.append(f"{indent_str}  {k}:")
                            lines.append(to_yaml(v, level + 2))
                        else:
                            lines.append(f"{indent_str}  {k}: {format_value(v)}")
                else:
                    lines.append(f"{indent_str}- {format_value(item)}")
            return '\n'.join(lines)
        else:
            return format_value(obj)
    
    return to_yaml(data)


def yaml_to_json(yaml_data: str, indent: int = 2) -> str:
    """Convert YAML to JSON (basic implementation)."""
    # Simple YAML parser for basic structures
    import re
    
    def parse_yaml(text: str):
        lines = text.strip().split('\n')
        result = []
        stack = [result]
        
        for line in lines:
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            indent = len(line) - len(line.lstrip())
            key_val = line.strip()
            
            if ':' in key_val:
                key, val = key_val.split(':', 1)
                val = val.strip()
                
                if val.startswith('[') and val.endswith(']'):
                    # List
                    items = [i.strip().strip('"').strip("'") for i in val[1:-1].split(',')]
                    stack[-1].append({key: items})
                elif val.startswith('{') and val.endswith('}'):
                    # Dict
                    stack[-1].append({key: {}})
                elif val and val not in ['{}', '[]']:
                    stack[-1].append({key: val})
                else:
                    stack[-1].append({key: {}})
        
        return result
    
    # Use pyyaml if available
    try:
        import yaml
        data = yaml.safe_load(yaml_data)
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except ImportError:
        # Basic fallback
        data = parse_yaml(yaml_data)
        return json.dumps(data, indent=indent, ensure_ascii=False)


def xml_to_json(xml_data: str, indent: int = 2) -> str:
    """Convert XML to JSON."""
    root = ET.fromstring(xml_data)
    
    def xml_to_dict(element) -> Union[Dict, List]:
        result = {}
        
        # Attributes
        if element.attrib:
            result['@attributes'] = element.attrib
        
        # Child elements
        children = list(element)
        if children:
            child_dict = {}
            for child in children:
                child_data = xml_to_dict(child)
                
                if child.tag in child_dict:
                    # Multiple children with same tag -> list
                    if not isinstance(child_dict[child.tag], list):
                        child_dict[child.tag] = [child_dict[child.tag]]
                    child_dict[child.tag].append(child_data)
                else:
                    child_dict[child.tag] = child_data
            
            if result.get('@attributes'):
                result = {'@attributes': result['@attributes'], **child_dict}
            else:
                result = child_dict
        
        # Text content
        if element.text and element.text.strip():
            if result:
                result['#text'] = element.text.strip()
            else:
                return element.text.strip()
        
        return result
    
    json_data = {root.tag: xml_to_dict(root)}
    return json.dumps(json_data, indent=indent, ensure_ascii=False)


def tsv_to_json(tsv_data: str, indent: int = 2) -> str:
    """Convert TSV to JSON."""
    reader = csv.DictReader(io.StringIO(tsv_data), delimiter='\t')
    data = list(reader)
    return json.dumps(data, indent=indent, ensure_ascii=False)


def json_to_tsv(json_data: str) -> str:
    """Convert JSON to TSV."""
    data = json.loads(json_data)
    
    if not data:
        return ""
    
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            fieldnames = list(data[0].keys())
        else:
            return '\t'.join(str(x) for x in data)
    elif isinstance(data, dict):
        fieldnames = list(data.keys())
        data = [data]
    else:
        return str(data)
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def format_value(val: str) -> str:
    """Format a value for YAML."""
    if val.lower() in ('true', 'false', 'null', 'none'):
        return val.lower()
    try:
        return str(int(val))
    except:
        try:
            return str(float(val))
        except:
            if ',' in val or ':' in val or '#' in val:
                return f'"{val}"'
            return val


def convert(data: str, from_format: str, to_format: str, indent: int = 2) -> str:
    """Convert between formats."""
    from_format = from_format.lower()
    to_format = to_format.lower()
    
    if from_format == to_format:
        return data
    
    # Normalize input
    if from_format == 'csv':
        json_data = csv_to_json(data, indent)
    elif from_format == 'tsv':
        json_data = tsv_to_json(data, indent)
    elif from_format == 'xml':
        json_data = xml_to_json(data, indent)
    elif from_format == 'yaml':
        json_data = yaml_to_json(data, indent)
    elif from_format == 'json':
        json_data = data
    else:
        raise ValueError(f"Unknown source format: {from_format}")
    
    # Convert to target
    if to_format == 'json':
        # Validate JSON first
        json.loads(json_data)
        if indent:
            return json.dumps(json.loads(json_data), indent=indent, ensure_ascii=False)
        return json_data
    elif to_format == 'csv':
        return json_to_csv(json_data)
    elif to_format == 'tsv':
        return json_to_tsv(json_data)
    elif to_format == 'yaml':
        return json_to_yaml(json_data, indent)
    else:
        raise ValueError(f"Unknown target format: {to_format}")


def main():
    parser = argparse.ArgumentParser(description='Data format conversion tool')
    
    parser.add_argument('--input', '-i', help='Input file (or use stdin)')
    parser.add_argument('--output', '-o', help='Output file (or use stdout)')
    parser.add_argument('--from', '-f', dest='from_format', required=True,
                       help='Source format (csv, json, xml, yaml, tsv)')
    parser.add_argument('--to', '-t', dest='to_format', required=True,
                       help='Target format (csv, json, xml, yaml, tsv)')
    parser.add_argument('--pretty', action='store_true', help='Pretty print')
    parser.add_argument('--indent', type=int, default=2, help='Indentation size')
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        try:
            with open(args.input, 'r') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
    else:
        data = sys.stdin.read()
    
    if not data.strip():
        print("Error: No input data", file=sys.stderr)
        sys.exit(1)
    
    try:
        indent = args.indent if args.pretty else None
        result = convert(data, args.from_format, args.to_format, indent)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"Converted {args.from_format} -> {args.to_format}: {args.output}")
        else:
            print(result)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
