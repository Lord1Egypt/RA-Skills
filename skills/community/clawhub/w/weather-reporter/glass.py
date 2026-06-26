from PIL import Image, ImageFilter, ImageDraw

def add_rounded_frosted_glass_antialias(
    image_path,
    output_path,
    rect_center=None,          # 矩形中心坐标 (cx, cy)，与 rect_top_left 二选一
    rect_top_left=None,        # 矩形左上角坐标 (left, top)，优先使用该参数
    rect_size=(300, 200),
    corner_radius=30,
    blur_radius=15,
    overlay_opacity=120,       # 0-255，半透玻璃层的透明度
    ssaa_scale=6,              # 超采样倍数（2 即可，4 更平滑但慢）
    edge_transition_radius=5   # 边缘过渡羽化半径（像素），越大边缘越柔和
):
    """
    在原图上绘制圆角矩形毛玻璃效果（抗锯齿 + 边缘羽化过渡）
    现在可以直接指定矩形左上角位置 rect_top_left，也可用 rect_center。
    """
    # 加载原图并转换为 RGBA
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    # 确定矩形区域
    rw, rh = rect_size
    if rect_top_left is not None:
        left, top = rect_top_left
        box = (left, top, left + rw, top + rh)
    elif rect_center is not None:
        cx, cy = rect_center
        box = (cx - rw//2, cy - rh//2, cx + rw//2, cy + rh//2)
    else:
        # 默认居中
        cx, cy = w // 2, h // 2
        box = (cx - rw//2, cy - rh//2, cx + rw//2, cy + rh//2)

    # ------------------------------
    # 1. 生成平滑的 alpha 遮罩（抗锯齿 + 边缘过渡）
    # ------------------------------
    scale = ssaa_scale
    big_w, big_h = w * scale, h * scale
    big_box = (box[0]*scale, box[1]*scale, box[2]*scale, box[3]*scale)
    big_radius = corner_radius * scale

    # 在放大画布上绘制圆角矩形（白色填充）
    big_mask = Image.new("L", (big_w, big_h), 0)
    draw = ImageDraw.Draw(big_mask)
    draw.rounded_rectangle(big_box, radius=big_radius, fill=255)

    # 缩放回原始尺寸，获得抗锯齿的 alpha 通道
    mask = big_mask.resize((w, h), Image.Resampling.LANCZOS)

    # 对 mask 进行高斯模糊，实现边缘羽化过渡
    transition_radius = max(1, edge_transition_radius)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=transition_radius))

    # ------------------------------
    # 2. 生成模糊背景图
    # ------------------------------
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # ------------------------------
    # 3. 利用平滑 mask 合成模糊区域
    # ------------------------------
    frosted = Image.composite(blurred_img, img, mask)

    # ------------------------------
    # 4. 创建半透明玻璃层（同样使用过渡 mask）
    # ------------------------------
    glass_color = (240, 250, 255)  # 淡蓝白
    overlay = Image.new("RGBA", (w, h), glass_color + (0,))
    # 将 mask 值乘以透明度系数，作为 overlay 的 alpha 通道
    alpha = mask.point(lambda p: p * overlay_opacity // 255)
    overlay.putalpha(alpha)

    # ------------------------------
    # 5. 最终合成
    # ------------------------------
    result = Image.alpha_composite(frosted, overlay)
    result.save(output_path, "PNG")
    # print(f"圆角矩形毛玻璃效果（抗锯齿+边缘过渡）已保存至: {output_path}")
    return result


# ------------------- 使用示例 -------------------
if __name__ == "__main__":
    # 示例1：通过左上角坐标指定位置（距左上角 (100, 50) 开始）
    add_rounded_frosted_glass_antialias(
        image_path="input.png",
        output_path="frosted_left_top.png",
        rect_top_left=(100, 50),   # 直接指定左上角
        rect_size=(220, 220),
        corner_radius=40,
        blur_radius=12,
        overlay_opacity=100,
        ssaa_scale=2,
        edge_transition_radius=3
    )

    # 示例2：仍然支持通过中心点定位（原有方式）
    # add_rounded_frosted_glass_antialias(
    #     image_path="input.png",
    #     output_path="frosted_center.png",
    #     rect_center=(300, 250),    # 中心点
    #     rect_size=(300, 200),
    #     corner_radius=30,
    #     blur_radius=10,
    #     overlay_opacity=80,
    #     ssaa_scale=2,
    #     edge_transition_radius=5
    # )

    # 示例3：不指定任何位置参数，则默认居中
    # add_rounded_frosted_glass_antialias(
    #     image_path="input.png",
    #     output_path="frosted_default_center.png",
    #     rect_size=(400, 300),
    #     corner_radius=50,
    #     blur_radius=15,
    #     overlay_opacity=120,
    #     ssaa_scale=2,
    #     edge_transition_radius=4
    # )