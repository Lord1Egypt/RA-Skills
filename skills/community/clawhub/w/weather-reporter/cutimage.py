from PIL import Image


def cutimage():
    img = Image.open("make.png")   # 1024x1024

    img1 = Image.open("1.png")
    img2 = Image.open("2.png")
    img3 = Image.open("3.png")

    # 1. 等比放大到 2670x2670
    scale = (3370+img1.height+img2.height+img3.height) / 1024
    new_size = (int(1024 * scale), int(1024 * scale))  # 2670x2670
    img_resized = img.resize(new_size, Image.LANCZOS)

    # 2. 左对齐裁剪 2510x2670
    left = 0                      # 左对齐
    top = 0
    box = (left, top, left + 2510, top + (3370+img1.height+img2.height+img3.height))
    cropped = img_resized.crop(box)

    cropped.save("bg.png")