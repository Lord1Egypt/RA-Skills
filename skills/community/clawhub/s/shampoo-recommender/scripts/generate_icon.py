from PIL import Image, ImageDraw

size = 512
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 紫色圆角背景
draw.rounded_rectangle([20, 20, size-20, size-20], radius=80, fill=(138, 97, 214, 255))

# 洗发水瓶身
draw.rectangle([170, 180, 342, 400], fill=(255, 255, 255, 255))
# 瓶盖
draw.rectangle([205, 100, 307, 180], fill=(255, 255, 255, 255))
# 瓶口
draw.rectangle([220, 85, 292, 110], fill=(200, 170, 240, 255))
# 水滴
draw.polygon([(256, 230), (285, 290), (256, 320), (227, 290)], fill=(180, 140, 255, 255))
# 泡沫圈
draw.ellipse([80, 80, 160, 160], fill=(200, 230, 255, 200))
draw.ellipse([340, 100, 410, 170], fill=(200, 230, 255, 200))
draw.ellipse([370, 290, 430, 350], fill=(200, 230, 255, 200))
draw.ellipse([70, 300, 140, 370], fill=(200, 230, 255, 200))

img.save(r"C:\Users\chenyuxin\.qclaw\workspace\skills\shampoo-recommender\assets\icon.png")
print("done")
