"""
视频帧渲染模板（思维导图动画）
复制此文件到 output/videos/<project>/<episode>/render_<episode>.py
修改 SCENE_MAP 和各 render_s<N> 函数即可。
"""
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
import sys

# ============== 配置 ==============
W, H = 1080, 1920
FPS = 30
DURATION = 240  # 4 分钟
TOTAL_FRAMES = FPS * DURATION

OUT_BASE = r"<修改：项目根目录>"
FRAMES_DIR = os.path.join(OUT_BASE, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

# ============== 调色板 ==============
COL_BG = (250, 248, 244)
COL_NAVY = (30, 58, 95)
COL_GOLD = (212, 175, 55)
COL_RED = (192, 57, 43)
COL_GRAY = (44, 62, 80)

# ============== 字体 ==============
FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

F_TITLE = ImageFont.truetype(FONT_BOLD, 56)
F_BIG = ImageFont.truetype(FONT_BOLD, 132)
F_LABEL = ImageFont.truetype(FONT_PATH, 44)
F_SUB = ImageFont.truetype(FONT_PATH, 50)
F_TINY = ImageFont.truetype(FONT_PATH, 36)

# ============== 缓动 ==============
def ease_out_cubic(t): return 1 - (1 - t) ** 3
def ease_in_out_cubic(t):
    if t < 0.5: return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2

# ============== Alpha 处理 ==============
def apply_layer_alpha(layer, factor):
    r, g, b, a = layer.split()
    a = a.point(lambda p: int(p * factor))
    return Image.merge("RGBA", (r, g, b, a))

def make_layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

# ============== 场景函数（每个场景一个）==============
def render_s1(frame_idx, total):
    """场景 1"""
    t = frame_idx / total
    img = Image.new("RGB", (W, H), COL_BG)
    # 在此绘制元素...
    return img

# ============== 调度 ==============
SCENE_MAP = [
    (0, 450, render_s1, "S1"),
    # 添加更多场景...
]

def get_scene(frame_idx):
    for start, end, fn, name in SCENE_MAP:
        if start <= frame_idx < end:
            return fn, name, start, end

# ============== 主循环 ==============
def main():
    batch = sys.argv[1] if len(sys.argv) > 1 else "all"
    start_frame = 0 if batch in ("A", "all") else 4500
    end_frame = 4500 if batch == "A" else 7200 if batch == "B" else 7200

    print(f"渲染 {start_frame}-{end_frame} ({end_frame-start_frame} 帧)...")
    for i in range(start_frame, end_frame):
        scene_fn, name, s, e = get_scene(i)
        img = scene_fn(i - s, e - s)
        img.save(os.path.join(FRAMES_DIR, f"frame_{i:04d}.png"), "PNG")
        if (i - start_frame + 1) % 60 == 0:
            print(f"  [{((i-start_frame+1)/(end_frame-start_frame)*100):.1f}%] {name}")

if __name__ == "__main__":
    main()
