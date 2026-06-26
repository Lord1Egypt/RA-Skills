#!/usr/bin/env python3
"""
数科公司文印格式PDF生成工具（最终版）
使用精确字体：方正小标宋简体、仿宋GB2312、楷体GB2312、黑体
"""

import subprocess
import os
import sys
import tempfile
from pathlib import Path

def check_shuke_fonts():
    """检查数科公司文印字体是否已安装"""
    print("🔍 检查数科公司文印字体...")
    
    required_fonts = [
        "方正小标宋简体",
        "仿宋GB2312",
        "楷体GB2312",
        "黑体"
    ]
    
    try:
        result = subprocess.run(["fc-list", ":lang=zh"], 
                              capture_output=True, text=True)
        font_list = result.stdout.lower()
        
        all_found = True
        for font in required_fonts:
            if font.lower() in font_list:
                print(f"  ✓ {font}")
            else:
                print(f"  ✗ {font} (未找到)")
                all_found = False
        
        if not all_found:
            print("\n⚠ 部分字体未找到，PDF可能使用替代字体")
            print("  请运行字体安装: sudo python install_shuke_fonts.py")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ 检查字体时出错: {e}")
        return False

def docx_to_html(docx_path, html_path):
    """使用pandoc将docx转换为html"""
    cmd = ['pandoc', docx_path, '-o', html_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"pandoc转换错误: {result.stderr}")
        return False
    return True

def add_shuke_font_css(html_path):
    """
    添加数科公司文印格式的精确字体CSS
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 数科公司文印精确字体CSS
    css = """
    <style>
    /* 数科公司文印格式 - 精确字体配置 */
    
    /* 字体定义 */
    @font-face {
        font-family: 'ShukeDocumentTitle';
        src: local('方正小标宋简体'), local('FZ Xiao Biao Song');
        font-weight: normal;
        font-style: normal;
    }
    
    @font-face {
        font-family: 'ShukeLevel1';
        src: local('黑体'), local('SimHei');
        font-weight: normal;
        font-style: normal;
    }
    
    @font-face {
        font-family: 'ShukeLevel2';
        src: local('楷体GB2312'), local('KaiTiGB2312');
        font-weight: bold;
        font-style: normal;
    }
    
    @font-face {
        font-family: 'ShukeLevel3';
        src: local('仿宋GB2312'), local('FangSongGB2312');
        font-weight: normal;
        font-style: normal;
    }
    
    @font-face {
        font-family: 'ShukeBody';
        src: local('仿宋GB2312'), local('FangSongGB2312');
        font-weight: normal;
        font-style: normal;
    }
    
    /* 页面设置 */
    @page {
        margin: 3.5cm 2.8cm;  /* 上3.5cm，下3.5cm，左2.8cm，右2.8cm */
        size: A4;
    }
    
    /* 基础样式 */
    body {
        font-family: 'ShukeBody', '仿宋GB2312', 'AR PL UMing CN', serif;
        font-size: 16pt;  /* 三号字体约16磅 */
        line-height: 28pt;  /* 行距固定值28磅 */
        color: #000000;  /* 黑色 */
        margin: 0;
        padding: 0;
    }
    
    /* 文档标题：方正小标宋简体二号居中 */
    h1 {
        font-family: 'ShukeDocumentTitle', '方正小标宋简体', serif;
        font-size: 22pt;  /* 二号字体约22磅 */
        text-align: center;
        font-weight: normal;
        margin-top: 0;
        margin-bottom: 28pt;
    }
    
    /* 一级标题：黑体三号左对齐，不加粗 */
    h2 {
        font-family: 'ShukeLevel1', '黑体', sans-serif;
        font-size: 16pt;  /* 三号 */
        text-align: left;
        font-weight: normal;  /* 一级标题不加粗 */
        margin-top: 21pt;  /* 段前间距 */
        margin-bottom: 14pt;
    }
    
    /* 二级标题：楷体GB2312三号加粗左对齐 */
    h3 {
        font-family: 'ShukeLevel2', '楷体GB2312', cursive;
        font-size: 16pt;  /* 三号 */
        text-align: left;
        font-weight: bold;  /* 二级标题加粗 */
        margin-top: 14pt;
        margin-bottom: 7pt;
    }
    
    /* 三级标题：仿宋GB2312三号左对齐 */
    h4 {
        font-family: 'ShukeLevel3', '仿宋GB2312', serif;
        font-size: 16pt;  /* 三号 */
        text-align: left;
        font-weight: normal;
        margin-top: 7pt;
        margin-bottom: 7pt;
    }
    
    /* 正文段落：仿宋GB2312三号，首行缩进2字符 */
    p {
        font-family: 'ShukeBody', '仿宋GB2312', serif;
        font-size: 16pt;
        text-align: justify;
        text-indent: 2em;  /* 首行缩进2字符 */
        margin: 0;
        padding: 0;
        margin-bottom: 7pt;
    }
    
    /* 列表项 */
    li {
        font-family: 'ShukeBody', '仿宋GB2312', serif;
        font-size: 16pt;
        text-indent: 0;
        margin-bottom: 3.5pt;
    }
    
    /* 表格 */
    table {
        font-family: 'ShukeBody', '仿宋GB2312', serif;
        font-size: 16pt;
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 14pt;
    }
    
    th, td {
        border: 1pt solid #000;
        padding: 3.5pt 7pt;
        text-align: left;
    }
    
    /* 强制所有文本为黑色 */
    * {
        color: #000000 !important;
    }
    
    /* 确保无背景色 */
    body, div, p, span, h1, h2, h3, h4, li, td, th {
        background-color: transparent !important;
    }
    </style>
    """
    
    # 插入CSS到HTML的head中
    head_end = html_content.find('</head>')
    if head_end == -1:
        # 如果没有head，添加完整的head
        html_start = html_content.find('<html')
        if html_start != -1:
            html_tag_end = html_content.find('>', html_start) + 1
            html_content = (html_content[:html_tag_end] + 
                          '<head><meta charset="utf-8">' + css + '</head>' + 
                          html_content[html_tag_end:])
    else:
        html_content = html_content[:head_end] + css + html_content[head_end:]
    
    return html_content

def convert_with_weasyprint(html_content, pdf_path):
    """使用weasyprint生成PDF"""
    try:
        from weasyprint import HTML
        HTML(string=html_content).write_pdf(pdf_path)
        return True
    except Exception as e:
        print(f"weasyprint转换错误: {e}")
        return False

def convert_docx_to_pdf_shuke(docx_path, pdf_path=None):
    """将DOCX转换为数科公司文印格式的PDF"""
    if not os.path.exists(docx_path):
        print(f"文件不存在: {docx_path}")
        return False
    
    if pdf_path is None:
        # 生成输出文件名
        base_name = Path(docx_path).stem
        pdf_path = str(Path(docx_path).with_name(f"{base_name}_shuke_format.pdf"))
    
    print(f"📄 转换: {Path(docx_path).name} → {Path(pdf_path).name}")
    print("  格式: 数科公司文印精确字体")
    
    # 检查字体
    fonts_ok = check_shuke_fonts()
    if not fonts_ok:
        print("⚠ 字体不完整，将使用替代字体")
    
    # 创建临时HTML文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp_html:
        html_temp_path = tmp_html.name
    
    try:
        # 步骤1: DOCX → HTML
        print("1. 将DOCX转换为HTML...")
        if not docx_to_html(docx_path, html_temp_path):
            return False
        
        # 步骤2: 添加数科格式CSS
        print("2. 应用数科文印格式...")
        html_with_css = add_shuke_font_css(html_temp_path)
        
        # 可选：保存HTML用于调试
        debug_html = pdf_path.replace('.pdf', '_debug.html')
        with open(debug_html, 'w', encoding='utf-8') as f:
            f.write(html_with_css)
        print(f"  调试HTML已保存: {debug_html}")
        
        # 步骤3: HTML → PDF
        print("3. 生成PDF...")
        if not convert_with_weasyprint(html_with_css, pdf_path):
            return False
        
        print(f"✓ PDF生成完成: {pdf_path}")
        print(f"  文件大小: {os.path.getsize(pdf_path):,} 字节")
        
        # 检查PDF字体
        check_pdf_fonts(pdf_path)
        
        return pdf_path
        
    finally:
        # 清理临时文件
        if os.path.exists(html_temp_path):
            os.unlink(html_temp_path)

def check_pdf_fonts(pdf_path):
    """检查PDF使用的字体"""
    print("\n🔍 检查PDF字体使用...")
    
    try:
        result = subprocess.run(['pdffonts', pdf_path], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
            
            # 分析字体使用
            lines = result.stdout.strip().split('\n')
            if len(lines) > 2:  # 有字体信息
                font_lines = lines[2:]
                print(f"  PDF使用了 {len(font_lines)} 种字体")
                
                # 检查是否包含数科字体
                font_text = result.stdout.lower()
                shuke_fonts = ["方正", "仿宋", "楷体", "黑体", "fz", "fangsong", "kaiti", "simhei"]
                found = False
                for font in shuke_fonts:
                    if font in font_text:
                        found = True
                        break
                
                if found:
                    print("  ✓ PDF使用了数科公司要求的字体")
                else:
                    print("  ⚠ PDF可能未使用精确字体")
            return True
        else:
            print("  ⚠ 无法检查PDF字体")
            return False
    except Exception as e:
        print(f"  ✗ 检查PDF字体时出错: {e}")
        return False

def batch_convert(folder_path):
    """批量转换文件夹中的所有DOCX文件"""
    folder = Path(folder_path)
    if not folder.exists():
        print(f"文件夹不存在: {folder_path}")
        return
    
    docx_files = list(folder.glob("**/*.docx"))
    if not docx_files:
        print(f"在 {folder_path} 中未找到DOCX文件")
        return
    
    print(f"找到 {len(docx_files)} 个DOCX文件")
    
    successful = 0
    for docx_file in docx_files:
        print(f"\n{'='*40}")
        print(f"处理: {docx_file.name}")
        
        pdf_path = convert_docx_to_pdf_shuke(str(docx_file))
        if pdf_path:
            successful += 1
    
    print(f"\n{'='*60}")
    print(f"批量转换完成: {successful}/{len(docx_files)} 成功")
    print(f"输出文件夹: {folder_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("数科公司文印格式PDF生成工具（最终版）")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            # 批量转换文件夹
            batch_convert(sys.argv[1])
        else:
            # 转换单个文件
            input_file = sys.argv[1]
            output_file = None
            if len(sys.argv) > 2:
                output_file = sys.argv[2]
            
            pdf_path = convert_docx_to_pdf_shuke(input_file, output_file)
            if pdf_path:
                print(f"\n✅ 转换完成: {pdf_path}")
    else:
        # 显示使用说明
        print("\n使用方法:")
        print("  1. 转换单个文件:")
        print("     python convert_to_pdf_shuke_final.py 文档.docx [输出.pdf]")
        print("  2. 批量转换文件夹:")
        print("     python convert_to_pdf_shuke_final.py 文件夹路径")
        print("\n示例:")
        print("  python convert_to_pdf_shuke_final.py 算力调度平台.docx")
        print("  python convert_to_pdf_shuke_final.py ./英文文件名文档/")
        print("\n字体要求:")
        print("  - 方正小标宋简体 (文档标题)")
        print("  - 黑体 (一级标题)")
        print("  - 楷体GB2312 (二级标题)")
        print("  - 仿宋GB2312 (三级标题/正文)")

if __name__ == "__main__":
    main()