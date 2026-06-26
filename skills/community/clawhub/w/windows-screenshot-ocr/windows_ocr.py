# ============================================
# 脚本名称：windows_ocr.py
# 功能：使用 Windows 原生 OCR 识别图片中的文字
# 作者：QClaw AI Assistant（由用户对话生成）
# 生成日期：2026-03-26
# 依赖：Pillow, winrt（pip install winrt）
# 用法：python windows_ocr.py
# ============================================

from PIL import Image
import winrt.windows.media.ocr as ocr
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams
import asyncio
from io import BytesIO
import sys

async def recognize(image_path):
    # 加载图片
    img = Image.open(image_path)
    
    # 创建 OCR 引擎
    engine = ocr.OcrEngine.try_create_from_user_profile_languages()
    if engine is None:
        return "错误：未找到 OCR 语言包，请先安装语言包"
    
    # 转换图片为流
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    # 写入内存流
    stream = streams.InMemoryRandomAccessStream()
    writer = streams.DataWriter(stream)
    writer.write_bytes(buf.read())
    await writer.store_async()
    stream.seek(0)
    
    # 创建位图解码器
    decoder = await imaging.BitmapDecoder.create_async(stream)
    bitmap = await decoder.get_software_bitmap_async()
    
    # 执行 OCR
    result = await engine.recognize_async(bitmap)
    return result.text

if __name__ == "__main__":
    image_path = r"E:\桌面\auto_screenshot\screen_20260326_091124.png"
    text = asyncio.run(recognize(image_path))
    with open(r"E:\桌面\auto_screenshot\ocr_result.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("识别结果已保存到 ocr_result.txt")
