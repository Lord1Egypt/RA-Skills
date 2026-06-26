from PIL import Image, ImageDraw

# 创建 512x512 的图标
size = 512
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 画一个圆角紫色背景
r = 80
draw.rounded_rectangle([20, 20, size-20, size-20], radius=r, fill=(138, 97, 214, 255))

# 画一个洗发水瓶身轮廓（简化）
# 瓶身
draw.rectangle([170, 180, 342, 400], fill=(255, 255, 255, 255))
# 瓶盖
draw.rectangle([205, 100, 307, 180], fill=(255, 255, 255, 255))
# 瓶口
draw.rectangle([220, 85, 292, 110], fill=(200, 170, 240, 255))
# 瓶身上的水滴形状
draw.polygon([(256, 230), (285, 290), (256, 320), (227, 290)], fill=(180, 140, 255, 255))

# 画左上角的泡沫圈
draw.ellipse([80, 80, 160, 160], fill=(200, 230, 255, 200))
draw.ellipse([340, 100, 410, 170], fill=(200, 230, 255, 200))
draw.ellipse([370, 290, 430, 350], fill=(200, 230, 255, 200))
draw.ellipse([70, 300, 140, 370], fill=(200, 230, 255, 200))

img.save("C:/Users/chenyuxin/.qclaw/workspace/skills/shampoo-recommender/assets/icon.png")
print("icon.png 生成成功！")
