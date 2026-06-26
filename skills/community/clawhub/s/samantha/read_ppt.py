import zipfile
import xml.etree.ElementTree as ET
import os

def extract_ppt_text(ppt_path):
    """从PPT文件中提取文本内容"""
    try:
        # 解压PPT文件（PPTX是ZIP格式）
        with zipfile.ZipFile(ppt_path, 'r') as ppt_zip:
            # 获取所有幻灯片文件
            slide_files = [f for f in ppt_zip.namelist() if f.startswith('ppt/slides/slide')]
            
            all_text = []
            
            for slide_file in slide_files:
                try:
                    # 读取幻灯片XML
                    with ppt_zip.open(slide_file) as slide_xml:
                        content = slide_xml.read()
                        
                        # 尝试解析XML
                        try:
                            root = ET.fromstring(content)
                            # 提取文本（简化处理）
                            text_elements = root.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}t')
                            slide_text = ' '.join([elem.text for elem in text_elements if elem.text])
                            
                            if slide_text:
                                all_text.append(f"幻灯片 {slide_file}: {slide_text}")
                        except ET.ParseError:
                            # 如果XML解析失败，尝试直接查找文本
                            content_str = content.decode('utf-8', errors='ignore')
                            # 简单提取文本内容
                            import re
                            texts = re.findall(r'<a:t[^>]*>([^<]+)</a:t>', content_str)
                            if texts:
                                all_text.append(f"幻灯片 {slide_file}: {' '.join(texts)}")
                            
                except Exception as e:
                    all_text.append(f"读取 {slide_file} 时出错: {str(e)}")
            
            return "\n\n".join(all_text)
            
    except Exception as e:
        return f"读取PPT文件时出错: {str(e)}"

if __name__ == "__main__":
    ppt_path = r"D:\xuyan\桌面\Samantha\邓小闲koki-寻找Samantha.pptx"
    
    if os.path.exists(ppt_path):
        print("正在读取PPT文件...")
        text_content = extract_ppt_text(ppt_path)
        
        # 保存提取的文本
        output_path = r"D:\openclaw\workspace\ppt_content.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"PPT内容已提取到: {output_path}")
        print(f"\n提取的内容预览:\n{text_content[:1000]}...")
    else:
        print(f"文件不存在: {ppt_path}")