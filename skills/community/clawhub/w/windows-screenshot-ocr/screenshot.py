# ============================================
# 脚本名称：screenshot.py
# 功能：截取全屏并标记当前鼠标位置（红色准星）
# 作者：QClaw AI Assistant（由用户对话生成）
# 生成日期：2026-03-26
# 依赖：mss, pyautogui, Pillow
# 用法：python screenshot.py
# ============================================

import mss
import os
from datetime import datetime
import pyautogui
from PIL import Image, ImageDraw

# 固定保存到 E:\桌面\auto_screenshot\
save_folder = r"E:\桌面\auto_screenshot"
os.makedirs(save_folder, exist_ok=True)

# 获取当前鼠标位置
mouse_x, mouse_y = pyautogui.position()

# 生成带时间戳的文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"screen_{timestamp}.png"
filepath = os.path.join(save_folder, filename)

# 截图
with mss.mss() as sct:
    sct.shot(output=filepath)

# 打开截图并标记鼠标位置
img = Image.open(filepath)
draw = ImageDraw.Draw(img)

# 绘制准星（红色圆点 + 白色边框）
radius = 8
draw.ellipse([mouse_x - radius - 2, mouse_y - radius - 2, mouse_x + radius + 2, mouse_y + radius + 2], fill='white')
draw.ellipse([mouse_x - radius, mouse_y - radius, mouse_x + radius, mouse_y + radius], fill='red')
draw.line([mouse_x - 15, mouse_y, mouse_x + 15, mouse_y], fill='red', width=2)
draw.line([mouse_x, mouse_y - 15, mouse_x, mouse_y + 15], fill='red', width=2)

# 保存标记后的截图
img.save(filepath)

print(f"截图已保存：{filepath}")
print(f"鼠标位置：({mouse_x}, {mouse_y})")
