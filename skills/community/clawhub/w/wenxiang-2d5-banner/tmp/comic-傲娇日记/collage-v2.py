from PIL import Image, ImageDraw
import os

# 12 格漫画布局（含过渡镜头）
panel_files = [
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel01.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel02.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel03.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel04.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel05.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel06.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel07.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel08.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel09.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel10.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel11.png",
    "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/panel12.png",
]

# 加载所有图片
panels = []
for i, f in enumerate(panel_files):
    if os.path.exists(f):
        img = Image.open(f)
        panels.append(img.resize((768, 768)))
        print(f"Loaded panel {i+1}: {f}")
    else:
        print(f"Warning: File not found {f}")
        # 创建占位图
        placeholder = Image.new('RGB', (768, 768), 'white')
        draw = ImageDraw.Draw(placeholder)
        draw.text((384, 384), f"Panel {i+1}\nMissing", fill='gray', anchor='center')
        panels.append(placeholder)

# 创建画布（4 列×4 行，每格 768x768）
canvas_width = 768 * 4
canvas_height = 768 * 4
gap = 8  # 2mm 间隙（约 8 像素@300DPI）
canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
draw = ImageDraw.Draw(canvas)

# 布局配置 (x, y, width_multiplier, height_multiplier) - 12 格
layout = [
    (0, 0, 1, 1),      # 1
    (1, 0, 1, 1),      # 2
    (2, 0, 1, 1),      # 3
    (3, 0, 1, 1),      # 4
    (0, 1, 1, 1),      # 5
    (1, 1, 2, 1),      # 6 (跨两列)
    (3, 1, 1, 1),      # 7
    (0, 2, 1, 1),      # 8
    (1, 2, 1, 1),      # 9
    (2, 2, 1, 1),      # 10
    (3, 2, 1, 1),      # 11
    (0, 3, 4, 1),      # 12 (跨四列)
]

# 计算实际位置（加入间隙）
def calc_position(x, y, w_mult, h_mult):
    x_pos = x * 768 + x * gap
    y_pos = y * 768 + y * gap
    w = 768 * w_mult + (w_mult - 1) * gap
    h = 768 * h_mult + (h_mult - 1) * gap
    return x_pos, y_pos, w, h

# 粘贴图片
for i, (x, y, w_mult, h_mult) in enumerate(layout):
    if i < len(panels):
        x_pos, y_pos, w, h = calc_position(x, y, w_mult, h_mult)
        panel = panels[i].resize((w, h))
        canvas.paste(panel, (x_pos, y_pos))
        # 画黑色边框
        draw.rectangle([x_pos, y_pos, x_pos+w, y_pos+h], outline='black', width=3)
        print(f"Pasted panel {i+1}: ({x_pos}, {y_pos}) size {w}x{h}")

# 保存
output_path = "C:/Users/Xiabi/.openclaw/workspace/tmp/comic-傲娇日记/final-comic-v2.png"
canvas.save(output_path, 'PNG')
print(f"Comic collage completed: {output_path}")
print(f"MEDIA: {output_path}")
