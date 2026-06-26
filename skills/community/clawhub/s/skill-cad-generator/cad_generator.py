#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CAD施工图生成工具 - DXF/SVG输出"""

import json, os, argparse, datetime

PROJECTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects")
os.makedirs(PROJECTS_DIR, exist_ok=True)

TEMPLATES = {
    "演出": {"width": 20, "depth": 12, "elements": [
        {"type": "stage", "x": 0, "y": 0, "w": 20, "h": 12},
        {"type": "truss", "x": 0, "y": -2, "w": 20, "h": 0.5},
        {"type": "truss", "x": 0, "y": 14, "w": 20, "h": 0.5},
    ]},
    "会议": {"width": 15, "depth": 10, "elements": [
        {"type": "stage", "x": 2, "y": 0, "w": 11, "h": 6},
        {"type": "screen", "x": 4, "y": 1, "w": 7, "h": 3},
    ]},
    "展览": {"width": 30, "depth": 20, "elements": [
        {"type": "booth", "x": 0, "y": 0, "w": 30, "h": 20},
    ]},
}

def load_project(name):
    path = os.path.join(PROJECTS_DIR, f"{name}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    return None

def save_project(name, data):
    path = os.path.join(PROJECTS_DIR, f"{name}.json")
    with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=2)

def create_cmd(args):
    w, d = float(args.width), float(args.depth)
    project = {"name": args.project, "width": w, "depth": d, "elements": [], "created": datetime.datetime.now().isoformat()}
    # 添加舞台底板
    project["elements"].append({"type": "stage", "x": 0, "y": 0, "w": w, "h": d, "layer": "舞台"})
    save_project(args.project, project)
    print(f"✅ CAD项目已创建: {args.project} ({w}m × {d}m)")

def add_element(args):
    project = load_project(args.project)
    if not project:
        print(f"❌ 项目不存在: {args.project}"); return
    elem = {"type": args.type, "x": float(args.x), "y": float(args.y), "w": float(args.w), "h": float(args.h), "layer": args.type}
    project["elements"].append(elem)
    save_project(args.project, project)
    print(f"✅ 已添加: {args.type} @ ({args.x},{args.y}) 尺寸 {args.w}×{args.h}m")

def generate_dxf(args):
    project = load_project(args.project)
    if not project:
        print(f"❌ 项目不存在: {args.project}"); return
    output = os.path.join(PROJECTS_DIR, f"{args.project}.dxf")
    with open(output, 'w', encoding='utf-8') as f:
        f.write("0\nSECTION\n2\nHEADER\n0\nENDSEC\n")
        f.write("0\nSECTION\n2\nENTITIES\n")
        for elem in project["elements"]:
            x, y, w, h = elem["x"], elem["y"], elem["w"], elem["h"]
            # 写4条线组成矩形
            for x1,y1,x2,y2 in [(x,y,x+w,y),(x+w,y,x+w,y+h),(x+w,y+h,x,y+h),(x,y+h,x,y)]:
                f.write(f"0\nLINE\n8\n{elem['layer']}\n10\n{x1:.2f}\n20\n{y1:.2f}\n11\n{x2:.2f}\n21\n{y2:.2f}\n")
            # 添加文字标注
            f.write(f"0\nTEXT\n8\n标注\n10\n{x+w/2:.2f}\n20\n{y+h/2:.2f}\n40\n0.5\n1\n{elem['type']}\n")
        f.write("0\nENDSEC\n0\nEOF\n")
    print(f"✅ DXF已生成: {output} ({len(project['elements'])}个元素)")

def generate_svg(args):
    project = load_project(args.project)
    if not project:
        print(f"❌ 项目不存在: {args.project}"); return
    output = os.path.join(PROJECTS_DIR, f"{args.project}.svg")
    w, d = project["width"], project["depth"]
    scale = 50
    colors = {"stage": "#2a2a3a", "truss": "#89b4fa", "screen": "#a6e3a1", "light": "#f9e2af", "speaker": "#cba6f7", "booth": "#313244"}
    with open(output, 'w', encoding='utf-8') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*scale+40}" height="{d*scale+40}">\n')
        f.write(f'<rect x="20" y="20" width="{w*scale}" height="{d*scale}" fill="#1e1e2e" stroke="#313244" stroke-width="2"/>\n')
        for elem in project["elements"]:
            x, y, ew, eh = elem["x"]*scale+20, elem["y"]*scale+20, elem["w"]*scale, elem["h"]*scale
            color = colors.get(elem["type"], "#45475a")
            f.write(f'<rect x="{x:.0f}" y="{y:.0f}" width="{ew:.0f}" height="{eh:.0f}" fill="{color}" stroke="#cdd6f4" stroke-width="1" opacity="0.8"/>\n')
            f.write(f'<text x="{x+ew/2:.0f}" y="{y+eh/2:.0f}" text-anchor="middle" fill="#cdd6f4" font-size="12">{elem["type"]}</text>\n')
        f.write('</svg>\n')
    print(f"✅ SVG已生成: {output}")

def from_template(args):
    template = TEMPLATES.get(args.template)
    if not template:
        print(f"❌ 未知模板: {args.template}"); return
    project = {"name": args.project, "width": template["width"], "depth": template["depth"],
               "elements": template["elements"][:], "created": datetime.datetime.now().isoformat()}
    save_project(args.project, project)
    print(f"✅ 已从模板'{args.template}'创建: {args.project}")

def list_templates(args):
    print("📋 可用模板:")
    for name, t in TEMPLATES.items():
        print(f"  {name}: {t['width']}m × {t['depth']}m ({len(t['elements'])}个元素)")

def export_cmd(args):
    project = load_project(args.project)
    if not project:
        print(f"❌ 项目不存在: {args.project}"); return
    fmt = args.format or "json"
    if fmt == "json":
        print(json.dumps(project, ensure_ascii=False, indent=2))
    elif fmt == "dxf":
        generate_dxf(args)
    elif fmt == "svg":
        generate_svg(args)

def list_projects(args):
    projects = [f[:-5] for f in os.listdir(PROJECTS_DIR) if f.endswith('.json')]
    if not projects:
        print("暂无项目"); return
    print(f"📋 项目列表 ({len(projects)}个):")
    for name in projects:
        p = load_project(name)
        print(f"  📐 {name}: {p['width']}m×{p['depth']}m ({len(p['elements'])}元素)")

def main():
    parser = argparse.ArgumentParser(description='CAD施工图生成工具')
    sub = parser.add_subparsers(dest='command')
    p = sub.add_parser('create', help='创建项目'); p.add_argument('project'); p.add_argument('width'); p.add_argument('depth')
    p = sub.add_parser('add_element', help='添加元素'); p.add_argument('project'); p.add_argument('type'); p.add_argument('x'); p.add_argument('y'); p.add_argument('w'); p.add_argument('h')
    p = sub.add_parser('generate_dxf', help='生成DXF'); p.add_argument('project')
    p = sub.add_parser('generate_svg', help='生成SVG'); p.add_argument('project')
    p = sub.add_parser('from_template', help='从模板创建'); p.add_argument('template'); p.add_argument('project')
    sub.add_parser('list_templates', help='列出模板')
    p = sub.add_parser('export', help='导出'); p.add_argument('project'); p.add_argument('--format', default='json')
    sub.add_parser('list', help='列出项目')
    args = parser.parse_args()
    if args.command == 'create': create_cmd(args)
    elif args.command == 'add_element': add_element(args)
    elif args.command == 'generate_dxf': generate_dxf(args)
    elif args.command == 'generate_svg': generate_svg(args)
    elif args.command == 'from_template': from_template(args)
    elif args.command == 'list_templates': list_templates(args)
    elif args.command == 'export': export_cmd(args)
    elif args.command == 'list': list_projects(args)
    else: parser.print_help()

if __name__ == '__main__': main()


class CadGenerator:
    """skill_cad_generator技能"""
    
    def __init__(self):
        self.name = "skill_cad_generator"
    
    def execute(self, params: Dict = None) -> Dict:
        """执行主要功能"""
        return {"success": True, "skill": self.name}
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {"skill": self.name, "status": "active"}
    
    def validate_input(self, data: Any) -> bool:
        """验证输入"""
        return data is not None
