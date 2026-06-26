"""文字识别 (OCR) 模块"""
import pytesseract
from PIL import Image
import os


# Tesseract 路径配置（如果不在 PATH 中）
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path: str, lang: str = "eng", config: str = "") -> str:
    """从图片提取文字
    
    Args:
        image_path: 图片路径
        lang: 语言代码 (chi_sim=简体中文, eng=英文, 可用+连接如 "chi_sim+eng")
        config: 额外配置
        
    Returns:
        识别出的文字
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片不存在: {image_path}")
    
    # 打开图片
    img = Image.open(image_path)
    
    # OCR 识别
    text = pytesseract.image_to_string(img, lang=lang, config=config)
    
    return text.strip()


def extract_text_with_boxes(image_path: str, lang: str = "eng") -> list:
    """获取文字及位置信息
    
    Args:
        image_path: 图片路径
        lang: 语言代码
        
    Returns:
        文字块列表 [{"text": "...", "left": 0, "top": 0, "width": 100, "height": 20}, ...]
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片不存在: {image_path}")
    
    img = Image.open(image_path)
    
    # 获取带位置的信息
    data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
    
    results = []
    n_boxes = len(data["text"])
    
    for i in range(n_boxes):
        text = data["text"][i].strip()
        if text:  # 只返回非空文字
            results.append({
                "text": text,
                "left": data["left"][i],
                "top": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
                "confidence": data["conf"][i]
            })
    
    return results


def search_text(image_path: str, search_term: str, lang: str = "eng") -> list:
    """在图片中搜索指定文字的位置
    
    Args:
        image_path: 图片路径
        search_term: 要搜索的文字
        lang: 语言代码
        
    Returns:
        匹配的文字位置列表 [{"text": "...", "left": 0, "top": 0, "width": 100, "height": 20}, ...]
    """
    all_boxes = extract_text_with_boxes(image_path, lang)
    
    # 模糊匹配
    results = []
    search_lower = search_term.lower()
    
    for box in all_boxes:
        if search_lower in box["text"].lower():
            results.append(box)
    
    return results


if __name__ == "__main__":
    # 测试
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python ocr.py <图片路径> [语言]")
        print("语言: eng(默认), chi_sim(简体中文)")
        sys.exit(1)
    
    image_path = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "eng"
    
    print(f"正在识别: {image_path}")
    print("-" * 50)
    
    text = extract_text(image_path, lang)
    print(text)
