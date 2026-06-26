#!/usr/bin/env python3
"""Figma API 解析器 - 提取文件中的设计数据"""
import argparse
import json
import requests
import os

FIGMA_API = "https://api.figma.com/v1"


def get_file(file_key, token):
    headers = {"X-Figma-Token": token}
    r = requests.get(f"{FIGMA_API}/files/{file_key}", headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()


def get_assets(file_key, node_ids, token, format="png", scale=2):
    headers = {"X-Figma-Token": token}
    params = {"ids": ",".join(node_ids), "format": format, "scale": scale}
    r = requests.get(f"{FIGMA_API}/images/{file_key}", headers=headers, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def parse_components(document, result=None, parent_name=""):
    if result is None:
        result = []
    kind = document.get('type', 'UNKNOWN')
    name = document.get('name', '')
    full_name = f"{parent_name}/{name}" if parent_name else name
    children = document.get('children', [])
    # 收集组件
    if kind == 'COMPONENT' or kind == 'COMPONENT_SET':
        result.append({
            'type': kind,
            'name': full_name,
            'id': document.get('id'),
            'childrenCount': len(children)
        })
    for child in children:
        parse_components(child, result, full_name)
    return result


def extract_colors(document, result=None, parent_path=""):
    if result is None:
        result = []
    fills = document.get('fills', [])
    strokes = document.get('strokes', [])
    for fill in fills:
        if fill.get('type') == 'SOLID':
            color = fill.get('color', {})
            rgb = (
                int(color.get('r', 0) * 255),
                int(color.get('g', 0) * 255),
                int(color.get('b', 0) * 255)
            )
            hex_color = "#{:02X}{:02X}{:02X}".format(*rgb)
            opacity = fill.get('opacity', 1.0)
            result.append({
                'path': f"{parent_path}/{document.get('name', '')}",
                'hex': hex_color,
                'opacity': opacity,
                'id': document.get('id')
            })
    for child in document.get('children', []):
        extract_colors(child, result, f"{parent_path}/{document.get('name', '')}")
    return result


def extract_text_styles(document, result=None, parent_path=""):
    if result is None:
        result = []
    style = document.get('style', {})
    if style:
        result.append({
            'name': f"{parent_path}/{document.get('name', '')}".strip('/'),
            'fontSize': style.get('fontSize'),
            'fontFamily': style.get('fontFamily'),
            'fontWeight': style.get('fontWeight'),
            'lineHeightPx': style.get('lineHeightPx'),
            'letterSpacing': style.get('letterSpacing'),
        })
    for child in document.get('children', []):
        extract_text_styles(child, result, f"{parent_path}/{document.get('name', '')}")
    return result


def export_report(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] 设计报告已生成: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Figma 设计解析')
    parser.add_argument('--file-key', '-f', help='Figma 文件 Key')
    parser.add_argument('--token', '-t', help='Figma Personal Access Token')
    parser.add_argument('--output', '-o', default='figma_report.json', help='输出报告路径')
    parser.add_argument('--colors', '-c', action='store_true', help='提取颜色规范')
    parser.add_argument('--text', action='store_true', help='提取文字样式')
    parser.add_argument('--components', action='store_true', help='提取组件列表')
    args = parser.parse_args()
    if args.file_key and args.token:
        file_data = get_file(args.file_key, args.token)
        doc = file_data.get('document', {})
        report = {'file_key': args.file_key, 'name': file_data.get('name')}
        if args.colors:
            report['colors'] = extract_colors(doc)
        if args.text:
            report['textStyles'] = extract_text_styles(doc)
        if args.components:
            report['components'] = parse_components(doc)
        export_report(report, args.output)
    else:
        print("需要 --file-key 和 --token")
