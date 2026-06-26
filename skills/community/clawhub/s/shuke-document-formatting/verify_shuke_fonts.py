#!/usr/bin/env python3
"""
验证数科公司文印字体是否已正确安装
"""

import subprocess
import sys
import os

# 数科公司要求的精确字体
SHUKE_FONTS = [
    ("方正小标宋简体", ["方正小标宋简体", "fz xiao biao song"]),
    ("仿宋GB2312", ["仿宋gb2312", "fangsonggb2312"]),
    ("楷体GB2312", ["楷体gb2312", "kaitigb2312"]),
    ("黑体", ["黑体", "simhei", "hei ti"])
]

def check_fonts_with_fc_list():
    """使用fc-list检查字体"""
    print("🔍 使用fc-list检查系统字体...")
    
    try:
        result = subprocess.run(["fc-list", ":lang=zh"], 
                              capture_output=True, text=True)
        font_list = result.stdout.lower()
        
        if not font_list:
            print("  ✗ 未找到中文字体")
            return False
        
        print(f"  找到 {len(font_list.splitlines())} 个中文字体")
        
        # 检查每个数科字体
        found_fonts = []
        missing_fonts = []
        
        for display_name, search_terms in SHUKE_FONTS:
            found = False
            for term in search_terms:
                if term.lower() in font_list:
                    # 找到包含该字体的行
                    for line in result.stdout.splitlines():
                        if term.lower() in line.lower():
                            print(f"  ✓ {display_name}: {line.strip()[:80]}...")
                            found = True
                            break
                    if found:
                        break
            
            if found:
                found_fonts.append(display_name)
            else:
                missing_fonts.append(display_name)
        
        return found_fonts, missing_fonts
        
    except Exception as e:
        print(f"  ✗ 执行fc-list时出错: {e}")
        return [], SHUKE_FONTS

def check_fonts_with_fc_match():
    """使用fc-match检查字体"""
    print("\n🎯 使用fc-match检查字体匹配...")
    
    for display_name, search_terms in SHUKE_FONTS:
        # 使用第一个搜索词
        search_term = search_terms[0]
        try:
            result = subprocess.run(["fc-match", search_term], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                match_line = result.stdout.strip()
                print(f"  {display_name}: {match_line}")
            else:
                print(f"  {display_name}: 无匹配")
        except Exception as e:
            print(f"  {display_name}: 检查出错 - {e}")

def check_font_files():
    """检查字体文件是否存在于系统目录"""
    print("\n📁 检查字体文件安装目录...")
    
    font_dir = "/usr/share/fonts/数科文印字体"
    import os
    
    if os.path.exists(font_dir):
        print(f"  ✓ 字体目录存在: {font_dir}")
        files = os.listdir(font_dir)
        print(f"  目录中包含 {len(files)} 个文件:")
        for file in files:
            print(f"    - {file}")
        
        # 检查是否包含关键字体文件
        required_files = ["FZ XIAO BIAO SONG.TTF", "FANGSONGGB2312.TTF", 
                         "KAITIGB2312.TTF", "SIMHEI.TTF"]
        
        found_files = []
        for req_file in required_files:
            if req_file in files or req_file.lower() in [f.lower() for f in files]:
                found_files.append(req_file)
        
        print(f"\n  关键字体文件: {len(found_files)}/{len(required_files)} 个找到")
        for req_file in required_files:
            if req_file in found_files:
                print(f"    ✓ {req_file}")
            else:
                print(f"    ✗ {req_file} (缺失)")
                
        return len(found_files) > 0
    else:
        print(f"  ✗ 字体目录不存在: {font_dir}")
        return False

def test_pdf_generation():
    """测试PDF生成是否使用正确字体"""
    print("\n📄 测试PDF生成字体使用...")
    
    # 检查pdffonts工具是否可用
    try:
        result = subprocess.run(["which", "pdffonts"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("  ⚠ pdffonts工具不可用，无法检查PDF字体")
            return False
    except:
        print("  ⚠ pdffonts工具不可用，无法检查PDF字体")
        return False
    
    # 如果有测试PDF，检查其字体
    test_pdf = "/root/.openclaw/workspace/英文文件名文档/01_AI_Research_Scheduling_Platform_exact_fonts.pdf"
    if os.path.exists(test_pdf):
        try:
            result = subprocess.run(["pdffonts", test_pdf], 
                                  capture_output=True, text=True)
            print(f"  PDF字体信息 ({os.path.basename(test_pdf)}):")
            print(result.stdout[:500])  # 显示前500字符
            return True
        except Exception as e:
            print(f"  ✗ 检查PDF字体时出错: {e}")
            return False
    else:
        print(f"  ⚠ 测试PDF文件不存在: {test_pdf}")
        print("    请先生成PDF: python convert_to_pdf_exact_fonts.py")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("数科公司文印字体验证工具")
    print("=" * 60)
    
    import os
    
    # 检查1: fc-list
    found_fonts, missing_fonts = check_fonts_with_fc_list()
    
    # 检查2: fc-match
    check_fonts_with_fc_match()
    
    # 检查3: 字体文件
    files_ok = check_font_files()
    
    # 检查4: PDF生成
    pdf_ok = test_pdf_generation()
    
    print("\n" + "=" * 60)
    print("验证结果摘要")
    print("=" * 60)
    
    print(f"✓ 已安装的字体 ({len(found_fonts)}/{len(SHUKE_FONTS)}):")
    for font in found_fonts:
        print(f"  - {font}")
    
    if missing_fonts:
        print(f"\n✗ 缺失的字体 ({len(missing_fonts)}/{len(SHUKE_FONTS)}):")
        for font in missing_fonts:
            print(f"  - {font}")
    
    print(f"\n📁 字体文件检查: {'✓ 通过' if files_ok else '✗ 有问题'}")
    print(f"📄 PDF字体检查: {'✓ 通过' if pdf_ok else '⚠ 需要测试'}")
    
    if len(found_fonts) == len(SHUKE_FONTS) and files_ok:
        print("\n🎉 所有数科公司文印字体已正确安装！")
        print("  可以生成使用精确字体的PDF文档。")
    else:
        print("\n⚠ 字体安装不完整，请:")
        print("  1. 确保字体文件已上传")
        print("  2. 运行安装脚本: sudo python install_shuke_fonts.py")
        print("  3. 重新运行此验证工具")
    
    print("\n💡 使用说明:")
    print("  1. 生成精确字体PDF:")
    print("     python convert_to_pdf_exact_fonts.py 文档.docx")
    print("  2. 检查PDF字体:")
    print("     pdffonts 生成的文档.pdf")
    print("  3. 批量处理:")
    print("     python batch_convert_pdf.py 文件夹路径/")

if __name__ == "__main__":
    main()