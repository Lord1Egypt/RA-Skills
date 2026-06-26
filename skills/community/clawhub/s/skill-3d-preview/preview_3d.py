#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D效果预览工具 - ASCII渲染+Three.js导出"""
import json, os, argparse

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")
os.makedirs(DIR, exist_ok=True)

def create_scene(args):
    scene = {"name": args.name, "size": [float(args.width), float(args.depth), float(args.height)],
             "objects": [], "lights": [], "created": ""}
    with open(os.path.join(DIR, f"{args.name}.json"), 'w') as f:
        json.dump(scene, f, ensure_ascii=False, indent=2)
    print(f"✅ 3D场景已创建: {args.name} ({args.width}×{args.depth}×{args.height}m)")

def add_object(args):
    path = os.path.join(DIR, f"{args.scene}.json")
    if not os.path.exists(path): print(f"❌ 场景不存在"); return
    with open(path) as f: scene = json.load(f)
    pos = [float(x) for x in args.position.split(',')]
    size = [float(x) for x in args.size.split(',')]
    scene["objects"].append({"type": args.type, "position": pos, "size": size})
    with open(path, 'w') as f: json.dump(scene, f, ensure_ascii=False, indent=2)
    print(f"✅ 已添加: {args.type} @ {args.position}")

def render_ascii(args):
    path = os.path.join(DIR, f"{args.scene}.json")
    if not os.path.exists(path): print(f"❌ 场景不存在"); return
    with open(path) as f: scene = json.load(f)
    w, d = int(scene["size"][0]), int(scene["size"][1])
    print(f"📐 俯视图: {scene['name']} ({w}m×{d}m)")
    print("┌" + "─" * (w*2) + "┐")
    grid = [['·'] * (w*2) for _ in range(d)]
    icons = {"stage": "▓", "truss": "═", "screen": "█", "light": "●", "speaker": "◎"}
    for obj in scene["objects"]:
        x, y = int(obj["position"][0]*2), int(obj["position"][1])
        ow, oh = int(obj["size"][0]*2), int(obj["size"][1])
        icon = icons.get(obj["type"], "□")
        for dy in range(min(oh, d-y)):
            for dx in range(min(ow, w*2-x)):
                if 0 <= y+dy < d and 0 <= x+dx < w*2:
                    grid[y+dy][x+dx] = icon
    for row in grid:
        print("│" + "".join(row) + "│")
    print("└" + "─" * (w*2) + "┘")
    print(f"  ▓=舞台 ═=桁架 █=屏幕 ●=灯光 ◎=音箱 ·=空地")

def export_threejs(args):
    path = os.path.join(DIR, f"{args.scene}.json")
    if not os.path.exists(path): print(f"❌ 场景不存在"); return
    with open(path) as f: scene = json.load(f)
    output = os.path.join(DIR, f"{args.scene}_preview.html")
    html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{scene["name"]} 3D预览</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head>
<body style="margin:0;background:#1e1e2e"><script>
const scene=new THREE.Scene();scene.background=new THREE.Color(0x1e1e2e);
const camera=new THREE.PerspectiveCamera(75,innerWidth/innerHeight,0.1,1000);
const renderer=new THREE.WebGLRenderer();renderer.setSize(innerWidth,innerHeight);document.body.appendChild(renderer.domElement);
const light=new THREE.DirectionalLight(0xffffff,1);light.position.set(5,10,5);scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));
// 地板
const floor=new THREE.Mesh(new THREE.PlaneGeometry({scene["size"][0]},{scene["size"][1]}),new THREE.MeshPhongMaterial({{color:0x2a2a3a}}));
floor.rotation.x=-Math.PI/2;scene.add(floor);
// 物体
{chr(10).join([f'const o{i}=new THREE.Mesh(new THREE.BoxGeometry({",".join(str(x) for x in o["size"])}),new THREE.MeshPhongMaterial({{color:0x89b4fa}}));o{i}.position.set({o["position"][0]+o["size"][0]/2},{o["size"][1]/2},{o["position"][1]+o["size"][2]/2});scene.add(o{i});' for i, o in enumerate(scene.get("objects", []))])}
camera.position.set({scene["size"][0]/2},{scene["size"][2]+5},{scene["size"][1]+10});camera.lookAt({scene["size"][0]/2},0,{scene["size"][1]/2});
function animate(){{requestAnimationFrame(animate);renderer.render(scene,camera);}}animate();
</script></body></html>'''
    with open(output, 'w', encoding='utf-8') as f: f.write(html)
    print(f"✅ Three.js HTML已生成: {output}")

def main():
    parser = argparse.ArgumentParser(description='3D效果预览工具')
    sub = parser.add_subparsers(dest='command')
    p = sub.add_parser('create_scene', help='创建场景'); p.add_argument('name'); p.add_argument('width'); p.add_argument('depth'); p.add_argument('height')
    p = sub.add_parser('add_object', help='添加物体'); p.add_argument('scene'); p.add_argument('type'); p.add_argument('position'); p.add_argument('size')
    p = sub.add_parser('render_ascii', help='ASCII渲染'); p.add_argument('scene')
    p = sub.add_parser('export_threejs', help='导出Three.js'); p.add_argument('scene')
    args = parser.parse_args()
    if args.command == 'create_scene': create_scene(args)
    elif args.command == 'add_object': add_object(args)
    elif args.command == 'render_ascii': render_ascii(args)
    elif args.command == 'export_threejs': export_threejs(args)
    else: parser.print_help()

if __name__ == '__main__': main()


class Preview3D:
    """skill_3d_preview技能"""
    
    def __init__(self):
        self.name = "skill_3d_preview"
    
    def execute(self, params: Dict = None) -> Dict:
        """执行主要功能"""
        return {"success": True, "skill": self.name}
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {"skill": self.name, "status": "active"}
    
    def validate_input(self, data: Any) -> bool:
        """验证输入"""
        return data is not None
