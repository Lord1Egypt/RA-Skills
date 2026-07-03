#!/usr/bin/env python3
"""
Sketch2CAD - 手绘草图转CAD DXF
Usage: python3 scripts/convert.py <output.dxf> <x1,y1> <x2,y2> ...
   or: python3 scripts/convert.py --polygon <output.dxf> <x1,y1> <x2,y2> ...

Examples:
  # L-shape polygon (auto-closed)
  python3 scripts/convert.py output.dxf 0,5 5,5 5,0 8,0 8,10 0,10

  # Rectangle
  python3 scripts/convert.py rect.dxf 0,0 10,0 10,8 0,8
"""

import sys
import os
import subprocess

VENV_DIR = os.path.expanduser("~/.openclaw/workspace/venv_dxf")

def ensure_venv():
    """确保虚拟环境和ezdxf已安装"""
    venv_python = os.path.join(VENV_DIR, "bin", "python3")
    
    if not os.path.exists(venv_python):
        print("[sketch2cad] 首次使用，创建虚拟环境并安装依赖...")
        os.makedirs(VENV_DIR, exist_ok=True)
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
        subprocess.run([venv_python, "-m", "pip", "install", "ezdxf", "-q"], check=True)
        print("[sketch2cad] 环境准备完成")
    
    return venv_python

def parse_points(args):
    """解析坐标参数 'x,y' -> (float(x), float(y))"""
    points = []
    for arg in args:
        try:
            x, y = arg.split(',')
            points.append((float(x.strip()), float(y.strip())))
        except ValueError:
            print(f"[sketch2cad] 错误: 无法解析坐标 '{arg}'，格式应为 'x,y'")
            sys.exit(1)
    return points

def generate_dxf(venv_python, output_path, points):
    """调用venv中的ezdxf生成DXF"""
    
    # 构建内嵌的Python代码
    code = f'''
import ezdxf

doc = ezdxf.new("R2010")
msp = doc.modelspace()

points = {points}
msp.add_lwpolyline(points, close=True)

doc.saveas("{output_path}")
print("[sketch2cad] DXF已生成: {output_path}")
'''
    
    result = subprocess.run(
        [venv_python, "-c", code],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"[sketch2cad] 生成失败: {result.stderr}")
        sys.exit(1)
    
    print(result.stdout.strip())

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    output_path = sys.argv[1]
    raw_points = sys.argv[2:]
    
    points = parse_points(raw_points)
    
    if len(points) < 2:
        print("[sketch2cad] 错误: 至少需要2个坐标点")
        sys.exit(1)
    
    venv_python = ensure_venv()
    generate_dxf(venv_python, output_path, points)

if __name__ == "__main__":
    main()
