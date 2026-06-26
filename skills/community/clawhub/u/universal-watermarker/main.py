import os
import io
import math
import platform
import urllib.request
from typing import Union, List, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageStat
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def setup_environment():
    """
    Clawhub 云端环境初始化：自动下载必备字体文件
    """
    font_dir = "./fonts"
    font_name = "AlibabaPuHuiTi-3-65-Medium.ttf"
    font_path = os.path.join(font_dir, font_name)
    
    # 必须使用 raw.githubusercontent.com 获取真实二进制文件
    raw_url = "https://raw.githubusercontent.com/cribug/universal-watermarker/main/fonts/AlibabaPuHuiTi-3-65-Medium.ttf"
    
    if not os.path.exists(font_path):
        print(f"⏳ 检测到首次运行，正在自动拉取核心字体: {font_name} ...")
        # 自动创建 fonts 文件夹
        os.makedirs(font_dir, exist_ok=True)
        
        try:
            # 伪装 User-Agent，防止 GitHub API 拦截爬虫
            req = urllib.request.Request(
                raw_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            with urllib.request.urlopen(req) as response, open(font_path, 'wb') as out_file:
                # 将流写入本地文件
                out_file.write(response.read())
            print("✅ 字体文件下载并部署成功！环境已就绪。")
            
        except Exception as e:
            print(f"❌ 字体下载失败，请检查网络或 URL: {e}")
            # 如果下载失败，抛出异常阻断后续运行，符合我们“宁可报错不可乱码”的原则
            raise RuntimeError("初始化环境失败，无法获取字体文件。")
    else:
        print("✅ 字体文件已存在，无需重复下载。")

def register_pdf_font(font_path: str) -> str:
    """为 PDF 注册字体并返回字体名称"""
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"【关键错误】找不到指定的字体文件: {os.path.abspath(font_path)}。请确保 fonts 文件夹内有该文件。")
    
    # 提取文件名（不含后缀）作为 PDF 内部引用的字体名
    font_name = os.path.basename(font_path).split('.')[0]
    try:
        # 避免重复注册
        if font_name not in pdfmetrics.getRegisteredFontNames():
            # 兼容处理：如果是 ttc 则取第一个子字体，如果是 ttf 则直接加载
            if font_path.lower().endswith('.ttc'):
                pdfmetrics.registerFont(TTFont(font_name, font_path, subfontIndex=0))
            else:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
        return font_name
    except Exception as e:
        raise RuntimeError(f"字体注册失败: {e}")
    
def parse_color(c: Union[str, Tuple[int, int, int]]) -> Tuple[int, int, int]:
    """解析颜色输入，支持 '#FF0000' 或 (255, 0, 0)"""
    if isinstance(c, str):
        c = c.lstrip('#')
        if len(c) == 3: c = ''.join([x*2 for x in c]) # 处理 #F00 简写
        return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
    return tuple(c)

def get_brightness_and_color(image_obj: Image.Image, auto_adjust: bool) -> Tuple[int, Tuple]:
    """计算背景亮度并决定颜色 (R, G, B)"""
    if not auto_adjust:
        return (255, 255, 255) # 默认白色
    
    # 采样亮度
    stat = ImageStat.Stat(image_obj.convert('L'))
    avg_brightness = stat.mean[0]
    
    # 如果背景太亮 (>180)，使用深灰色；否则使用白色
    if avg_brightness > 180:
        return (60, 60, 60)
    return (255, 255, 255)

def add_image_watermark(
    input_path: str,
    output_path: str,
    text: str,
    opacity: float,
    scale: float,
    mode: str,
    angle: int,
    auto_adjust: bool,
    color: Union[str, Tuple],
    font_path: str,
):
    with Image.open(input_path) as img:
        # 处理图片旋转元数据（防止手机拍的照片水印方向错了）
        try:
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
        except:
            pass

        base = img.convert("RGBA")
        w, h = base.size
        
        # 响应式字号计算，如果是对角线模式，参考线为对角线长度
        available_width = math.hypot(w, h) if mode == 'diagonal' else w
        test_size = 50
        test_font = ImageFont.truetype(font_path, test_size)
        # 获取文字真实的像素包围盒，完美兼容中英文及符号差异
        left, top, right, bottom = test_font.getbbox(text)
        test_text_width = right - left
        
        target_width = available_width * scale # 目标宽度为画布宽度的 scale 比例
        # 线性推导实际需要的多大字号
        dynamic_font_size = max(1, int(test_size * (target_width / max(test_text_width, 1))))
        
        font = ImageFont.truetype(font_path, dynamic_font_size)
        
        # 颜色决断逻辑：用户自定义优先 > 自动亮度调整
        if color:
            rgb_color = parse_color(color)
        else:
            rgb_color = get_brightness_and_color(base, auto_adjust)
        fill_color = (*rgb_color, int(255 * opacity))
        
        txt_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt_layer)

        if mode == 'tile':
            # 获取文字实际宽高
            bbox = draw.textbbox((0, 0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            
            # 画布扩容以支持旋转
            diagonal = int(math.hypot(w, h) * 1.5)
            overlay = Image.new("RGBA", (diagonal, diagonal), (0, 0, 0, 0))
            d_overlay = ImageDraw.Draw(overlay)
            
            # 间距随字号动态调整
            x_spacing, y_spacing = tw * 2.0, th * 5.0
            for i, y in enumerate(range(0, diagonal, int(y_spacing))):
                offset = (x_spacing / 2) if i % 2 != 0 else 0
                for x in range(0, diagonal, int(x_spacing)):
                    d_overlay.text((x + offset, y), text, font=font, fill=fill_color, anchor="mm")
            
            rotated = overlay.rotate(angle, resample=Image.BICUBIC, center=(diagonal/2, diagonal/2))
            txt_layer = rotated.crop(((diagonal-w)/2, (diagonal-h)/2, (diagonal+w)/2, (diagonal+h)/2))
        else:
            diag = int(math.hypot(w, h))
            # 创建一个足够大的正方形画布来保证旋转不被裁剪
            temp_layer = Image.new("RGBA", (diag, diag), (0, 0, 0, 0))
            d_temp = ImageDraw.Draw(temp_layer)
            d_temp.text((diag/2, diag/2), text, font=font, fill=fill_color, anchor="mm")
            
            if mode == 'diagonal':
                # 计算左下角到右上角的完美倾斜角
                rot_angle = math.degrees(math.atan2(h, w))
                temp_layer = temp_layer.rotate(rot_angle, resample=Image.BICUBIC, center=(diag/2, diag/2))
            
            # 将中心区域裁切回图片原尺寸
            txt_layer = temp_layer.crop(((diag-w)/2, (diag-h)/2, (diag+w)/2, (diag+h)/2))

        # 合并并保存为 JPEG (注意：RGBA -> RGB)
        combined = Image.alpha_composite(base, txt_layer)
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            combined.convert("RGB").save(output_path, "JPEG", quality=90)
        else:
            combined.save(output_path)

def create_watermark_pdf(
    text: str,
    canvas_width: float,
    canvas_height: float,
    center_x: float,
    center_y: float,
    opacity: float,
    scale: float,
    mode: str,
    angle: int,
    color_rgb: tuple,
    font_path: str
) -> io.BytesIO:
    packet = io.BytesIO()
    # 画布大小等同于原 PDF 的底层绝对大小
    can = canvas.Canvas(packet, pagesize=(canvas_width, canvas_height))
    font_name = register_pdf_font(font_path)

    # 响应式字号计算
    available_width = math.hypot(canvas_width, canvas_height) if mode == 'diagonal' else canvas_width
    base_size = 50.0
    base_text_width = pdfmetrics.stringWidth(text, font_name, base_size)
    
    target_width = available_width * scale
    dynamic_font_size = base_size * (target_width / max(base_text_width, 1))
    
    can.setFont(font_name, dynamic_font_size)
    can.setFillAlpha(opacity)
    can.setFillColorRGB(color_rgb[0]/255, color_rgb[1]/255, color_rgb[2]/255)
    
    text_width = can.stringWidth(text, font_name, dynamic_font_size)
    y_fix = dynamic_font_size / 3.0 # 视觉垂直居中修正

    if mode == 'tile':
        # 将原点平移到我们计算出的可视区域中心
        can.translate(center_x, center_y)
        can.rotate(angle)
        diagonal = math.hypot(canvas_width, canvas_height) * 1.5
        x_spacing, y_spacing = text_width * 2.5, dynamic_font_size * 4.0
        
        for i, y in enumerate(range(int(-diagonal), int(diagonal), int(y_spacing))):
            offset = (x_spacing / 2) if i % 2 != 0 else 0
            for x in range(int(-diagonal), int(diagonal), int(x_spacing)):
                can.drawCentredString(x + offset, y - y_fix, text)
    elif mode == 'diagonal':
        can.translate(center_x, center_y)
        # 计算 PDF 画布的对角线倾斜角
        rot_angle = math.degrees(math.atan2(canvas_height, canvas_width))
        can.rotate(rot_angle)
        can.drawCentredString(0, -y_fix, text)
    else:
        # 直接在可视区域中心绘制
        can.drawCentredString(center_x, center_y - y_fix, text)
        
    can.save()
    packet.seek(0)
    return packet

def add_pdf_watermark(
    input_path: str,
    output_path: str,
    text: str,
    opacity: float,
    scale: float,
    mode: str,
    angle: int,
    auto_adjust: bool,
    color: Union[str, Tuple],
    font_path: str
):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        # 1. 获取底层 MediaBox 的绝对尺寸
        m_left, m_bottom = float(page.mediabox.left), float(page.mediabox.bottom)
        m_right, m_top = float(page.mediabox.right), float(page.mediabox.top)
        canvas_width = m_right - m_left
        canvas_height = m_top - m_bottom
        
        # 2. 获取实际可视区域 CropBox 的坐标
        c_left, c_bottom = float(page.cropbox.left), float(page.cropbox.bottom)
        c_right, c_top = float(page.cropbox.right), float(page.cropbox.top)
        
        # 3. 计算可视区域的中心点，并将其映射到从 0 开始的 Canvas 坐标系中
        center_x = ((c_left + c_right) / 2.0) - m_left
        center_y = ((c_bottom + c_top) / 2.0) - m_bottom
        
        # PDF 颜色决断
        if color:
            color_rgb = parse_color(color)
        else:
            color_rgb = (60, 60, 60) if auto_adjust else (255, 255, 255)
        
        # 4. 生成与原 PDF 同样大小的纯净画布，但内容画在 center_x, center_y
        wm_buffer = create_watermark_pdf(text, canvas_width, canvas_height, center_x, center_y, opacity, scale, mode, angle, color_rgb, font_path)
        watermark_page = PdfReader(wm_buffer).pages[0]
        
        # 5. 直接叠加，完美对齐
        page.merge_page(watermark_page)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

def process_files(
    files: Union[str, List[str]],
    text: str,
    opacity: float = 0.3,
    scale: float = 0.5,
    mode: str = 'diagonal',
    angle: int = 30,
    auto_adjust: bool = True,
    color: Union[str, Tuple[int, int, int]] = None,
    font_path: str = "./fonts/AlibabaPuHuiTi-3-65-Medium.ttf",
) -> List[str]:
    # 智能推断响应式比例默认值
    if scale is None:
        if mode == 'diagonal':
            scale = 0.8
        elif mode == 'center':
            scale = 0.5
        else:
            scale = 0.25

    if isinstance(files, str):
        files = [files]

    results = []
    for f in files:
        if not os.path.exists(f):
            print(f"警告：文件未找到 {f}")
            continue
            
        ext = os.path.splitext(f)[1].lower()
        output_name = os.path.join(os.path.dirname(f), f"wm_{os.path.basename(f)}")

        try:
            if ext == '.pdf':
                add_pdf_watermark(f, output_name, text, opacity, scale, mode, angle, auto_adjust, color, font_path)
            elif ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                add_image_watermark(f, output_name, text, opacity, scale, mode, angle, auto_adjust, color, font_path)
            results.append(output_name)
            print(f"成功处理: {output_name}")
        except Exception as e:
            print(f"处理 {f} 失败: {str(e)}")
    return results

if __name__ == "__main__":
    setup_environment()
    # process_files(
    #     [
    #         '../test/1.pdf',
    #         '../test/2.pdf',
    #         '../test/3.pdf',
    #         '../test/4.pdf',
    #         '../test/5.jpg',
    #         '../test/6.png',
    #     ],
    #     '仅供内部测试使用',
    #     # color='#FF0000',
    #     # mode='tile',
    #     # mode='center',
    # )
    