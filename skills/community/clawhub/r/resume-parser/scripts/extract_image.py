import sys
try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Error: Please install pillow and pytesseract first: pip install pillow pytesseract")
    print("Note: You also need to install Tesseract OCR engine from https://github.com/tesseract-ocr/tesseract")
    sys.exit(1)

def extract_image_text(image_path):
    try:
        # 打开图片
        img = Image.open(image_path)
        # 识别文字，默认中文+英文
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        return text
    except Exception as e:
        return f"Error extracting image text: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_image.py <input-image-path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    text = extract_image_text(image_path)
    print(text)
