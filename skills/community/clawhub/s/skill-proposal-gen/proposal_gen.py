#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全案方案生成工具"""

import json, os, argparse, datetime

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proposals")
os.makedirs(DIR, exist_ok=True)

TEMPLATES = {
    "演出": ["项目背景", "设计理念", "灯光方案", "音响方案", "视频方案", "舞台方案", "施工计划", "应急预案", "报价概算"],
    "文旅": ["地域文化", "故事背景", "市场分析", "设计理念", "灯光方案", "音响方案", "视频方案", "特效方案", "运营方案", "投资预算"],
    "会议": ["会议概况", "场地布置", "设备配置", "流程安排", "技术保障", "应急预案", "报价清单"],
    "展览": ["项目概述", "展位设计", "灯光布置", "多媒体方案", "互动体验", "施工计划", "预算报价"],
}

def load(name):
    p = os.path.join(DIR, f"{name}.json")
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f: return json.load(f)
    return None

def save(name, data):
    with open(os.path.join(DIR, f"{name}.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_cmd(args):
    sections = TEMPLATES.get(args.type, TEMPLATES["演出"])
    proposal = {"name": args.project, "type": args.type, "sections": {s: f"待填写-{s}" for s in sections},
                "created": datetime.datetime.now().isoformat(), "status": "draft"}
    save(args.project, proposal)
    print(f"✅ 方案已创建: {args.project} ({args.type}型, {len(sections)}个章节)")

def add_section(args):
    p = load(args.project)
    if not p: print(f"❌ 不存在: {args.project}"); return
    p["sections"][args.section] = args.content
    save(args.project, p)
    print(f"✅ 已更新: {args.section}")

def generate_cmd(args):
    p = load(args.project)
    if not p: print(f"❌ 不存在: {args.project}"); return
    print(f"📋 自动生成方案: {p['name']}")
    print("=" * 50)
    for section, content in p["sections"].items():
        print(f"\n## {section}\n{content}")
    p["status"] = "generated"
    save(args.project, p)
    output = os.path.join(DIR, f"{args.project}.md")
    with open(output, 'w', encoding='utf-8') as f:
        f.write(f"# {p['name']} - {p['type']}方案\n\n")
        for section, content in p["sections"].items():
            f.write(f"## {section}\n\n{content}\n\n")
    print(f"\n✅ 方案已导出: {output}")

def template_cmd(args):
    t = args.type or "演出"
    sections = TEMPLATES.get(t, [])
    print(f"📋 {t}方案模板:")
    for i, s in enumerate(sections, 1):
        print(f"  {i}. {s}")

def export_cmd(args):
    p = load(args.project)
    if not p: print(f"❌ 不存在: {args.project}"); return
    print(json.dumps(p, ensure_ascii=False, indent=2))

def list_cmd(args):
    files = [f[:-5] for f in os.listdir(DIR) if f.endswith('.json')]
    if not files: print("暂无方案"); return
    print(f"📋 方案列表 ({len(files)}个):")
    for n in files:
        p = load(n)
        print(f"  📄 {n} [{p['type']}] - {p['status']}")

def main():
    parser = argparse.ArgumentParser(description='全案方案生成工具')
    sub = parser.add_subparsers(dest='command')
    p = sub.add_parser('create', help='创建方案'); p.add_argument('project'); p.add_argument('--type', default='演出', choices=['演出','文旅','会议','展览'])
    p = sub.add_parser('add_section', help='添加章节'); p.add_argument('project'); p.add_argument('section'); p.add_argument('content')
    sub.add_parser('generate', help='生成方案').add_argument('project')
    p = sub.add_parser('template', help='查看模板'); p.add_argument('--type', default='演出')
    p = sub.add_parser('export', help='导出方案'); p.add_argument('project')
    sub.add_parser('list', help='列出方案')
    args = parser.parse_args()
    if args.command == 'create': create_cmd(args)
    elif args.command == 'add_section': add_section(args)
    elif args.command == 'generate': generate_cmd(args)
    elif args.command == 'template': template_cmd(args)
    elif args.command == 'export': export_cmd(args)
    elif args.command == 'list': list_cmd(args)
    else: parser.print_help()

if __name__ == '__main__': main()


class ProposalGen:
    """skill_proposal_gen技能"""
    
    def __init__(self):
        self.name = "skill_proposal_gen"
    
    def execute(self, params: Dict = None) -> Dict:
        """执行主要功能"""
        return {"success": True, "skill": self.name}
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {"skill": self.name, "status": "active"}
    
    def validate_input(self, data: Any) -> bool:
        """验证输入"""
        return data is not None
