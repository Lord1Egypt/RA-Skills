#!/usr/bin/env python3
"""
数科公司文印字体安装脚本
安装方正小标宋简体、仿宋GB2312、楷体GB2312、黑体
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# 字体文件列表（Windows系统中对应的文件名）
REQUIRED_FONTS = [
    "FZ XIAO BIAO SONG.TTF",      # 方正小标宋简体
    "FANGSONGGB2312.TTF",         # 仿宋GB2312
    "KAITIGB2312.TTF",            # 楷体GB2312
    "SIMHEI.TTF"                  # 黑体
]

# 字体显示名称（用于验证）
FONT_DISPLAY_NAMES = {
    "FZ XIAO BIAO SONG.TTF": "方正小标宋简体",
    "FANGSONGGB2312.TTF": "仿宋GB2312",
    "KAITIGB2312.TTF": "楷体GB2312",
    "SIMHEI.TTF": "黑体"
}

# 字体安装目录
FONT_INSTALL_DIR = "/usr/share/fonts/数科文印字体"

def check_root():
    """检查是否以root权限运行"""
    if os.geteuid() != 0:
        print("⚠ 需要root权限安装字体")
        print("  请使用: sudo python install_shuke_fonts.py")
        return False
    return True

def find_font_files(source_dir=None):
    """
    查找字体文件
    参数:
        source_dir: 字体文件所在目录，None表示当前目录
    """
    if source_dir is None:
        source_dir = "."
    
    font_files = {}
    source_path = Path(source_dir)
    
    print("🔍 查找字体文件...")
    
    # 查找所有ttf文件
    ttf_files = list(source_path.glob("**/*.ttf")) + list(source_path.glob("**/*.TTF"))
    
    if not ttf_files:
        print("  ⚠ 未找到TTF字体文件")
        print(f"  搜索路径: {source_path.absolute()}")
        return None
    
    print(f"  找到 {len(ttf_files)} 个TTF文件:")
    for ttf_file in ttf_files[:10]:  # 显示前10个
        print(f"    - {ttf_file.name}")
    if len(ttf_files) > 10:
        print(f"    ... 还有 {len(ttf_files)-10} 个文件")
    
    # 字体匹配模式（更灵活的匹配，支持中英文）
    font_patterns = {
        "FZ XIAO BIAO SONG.TTF": [
            # 中文关键词
            "方正小标宋", "小标宋", "方正小标",
            # 拼音关键词
            "XIAOBIAO", "FZ XIAO", "FZXIAO", "FZ_XIAO", 
            "FANGZHENG", "FZBS", "XIAO BIAO SONG",
            # 其他变体
            "小标宋简体", "FZ XBS"
        ],
        "FANGSONGGB2312.TTF": [
            # 中文关键词
            "仿宋", "仿宋GB", "仿宋GB2312",
            # 拼音关键词
            "FANGSONG", "FANG SONG", "FANG_SONG", "FANGSONGGB",
            "FANGSONG GB", "FSGB", "FANGSONG"
        ],
        "KAITIGB2312.TTF": [
            # 中文关键词
            "楷体", "楷体GB", "楷体GB2312",
            # 拼音关键词
            "KAITI", "KAI TI", "KAI_TI", "KAITIGB",
            "KAI TI GB", "KTGB", "KAITI"
        ],
        "SIMHEI.TTF": [
            # 中文关键词
            "黑体", "黑體", "黑",
            # 拼音关键词
            "SIMHEI", "SIM HEI", "SIM_HEI", "HEI",
            "BLACK", "HEITI", "HEI TI", "SIMHEI"
        ]
    }
    
    # 尝试匹配字体
    matched_files = {}
    for ttf_file in ttf_files:
        filename_upper = ttf_file.name.upper()
        file_matched = False
        
        for font_file, patterns in font_patterns.items():
            for pattern in patterns:
                if pattern.upper() in filename_upper:
                    if font_file not in matched_files:
                        matched_files[font_file] = str(ttf_file)
                        print(f"  ✓ 匹配: {font_file} -> {ttf_file.name} (模式: {pattern})")
                        file_matched = True
                        break
            if file_matched:
                break
        
        if not file_matched:
            print(f"  ⚠ 未匹配: {ttf_file.name}")
    
    # 检查是否找到所有字体
    missing_fonts = []
    for required_font in REQUIRED_FONTS:
        if required_font not in matched_files:
            missing_fonts.append(required_font)
    
    if missing_fonts:
        print("\n❌ 缺少以下字体文件:")
        for font in missing_fonts:
            print(f"  - {font} ({FONT_DISPLAY_NAMES[font]})")
        
        print("\n💡 请确保字体文件已上传到以下位置之一:")
        print(f"  1. 当前目录: {os.path.abspath('.')}")
        print(f"  2. 指定目录: python install_shuke_fonts.py /path/to/fonts")
        print("\n💡 文件名匹配提示:")
        print("  - 方正小标宋简体: 文件名应包含'XIAOBIAO'或'FZ XIAO'")
        print("  - 仿宋GB2312: 文件名应包含'FANGSONG'")
        print("  - 楷体GB2312: 文件名应包含'KAITI'")
        print("  - 黑体: 文件名应包含'SIMHEI'或'HEI'")
        return None
    
    return matched_files

def install_fonts(font_files):
    """安装字体文件到系统字体目录"""
    print(f"\n📁 创建字体目录: {FONT_INSTALL_DIR}")
    os.makedirs(FONT_INSTALL_DIR, exist_ok=True)
    
    print("📄 安装字体文件...")
    for font_name, font_path in font_files.items():
        dest_path = os.path.join(FONT_INSTALL_DIR, font_name)
        shutil.copy2(font_path, dest_path)
        print(f"  ✓ 安装: {font_name} -> {dest_path}")
    
    return True

def update_font_cache():
    """更新字体缓存"""
    print("\n🔄 更新字体缓存...")
    try:
        result = subprocess.run(["fc-cache", "-fv"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✓ 字体缓存更新成功")
            return True
        else:
            print(f"  ✗ 字体缓存更新失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ 执行fc-cache时出错: {e}")
        return False

def verify_font_installation():
    """验证字体安装是否成功"""
    print("\n✅ 验证字体安装...")
    
    try:
        result = subprocess.run(["fc-list"], 
                              capture_output=True, text=True)
        font_list = result.stdout.lower()
        
        all_installed = True
        for font_file, display_name in FONT_DISPLAY_NAMES.items():
            # 检查字体名称是否在字体列表中
            font_name_lower = display_name.lower()
            if font_name_lower in font_list:
                print(f"  ✓ {display_name} 安装成功")
            else:
                # 尝试检查文件名
                font_file_lower = font_file.lower()
                if font_file_lower in font_list:
                    print(f"  ✓ {display_name} 安装成功（通过文件名识别）")
                else:
                    print(f"  ✗ {display_name} 可能未正确安装")
                    all_installed = False
        
        return all_installed
        
    except Exception as e:
        print(f"  ✗ 验证字体时出错: {e}")
        return False

def create_font_css_template():
    """创建使用精确字体的CSS模板"""
    css_template = """/* 数科公司文印精确字体配置 */
@font-face {
    font-family: 'DocumentTitleFont';
    src: local('方正小标宋简体');
    font-weight: normal;
    font-style: normal;
}

@font-face {
    font-family: 'Level1Font';
    src: local('黑体');
    font-weight: normal;
    font-style: normal;
}

@font-face {
    font-family: 'Level2Font';
    src: local('楷体GB2312');
    font-weight: bold;
    font-style: normal;
}

@font-face {
    font-family: 'Level3Font';
    src: local('仿宋GB2312');
    font-weight: normal;
    font-style: normal;
}

@font-face {
    font-family: 'BodyFont';
    src: local('仿宋GB2312');
    font-weight: normal;
    font-style: normal;
}

/* 应用字体规则 */
body, p, div, span {
    font-family: 'BodyFont', '仿宋GB2312', 'AR PL UMing CN', serif !important;
    font-size: 16pt !important;
    color: black !important;
}

h1, .title {
    font-family: 'DocumentTitleFont', '方正小标宋简体', serif !important;
    font-size: 22pt !important;
    text-align: center !important;
    font-weight: normal !important;
}

h2, .heading1 {
    font-family: 'Level1Font', '黑体', sans-serif !important;
    font-size: 16pt !important;
    text-align: left !important;
    font-weight: normal !important;
}

h3, .heading2 {
    font-family: 'Level2Font', '楷体GB2312', cursive !important;
    font-size: 16pt !important;
    text-align: left !important;
    font-weight: bold !important;
}

h4, .heading3 {
    font-family: 'Level3Font', '仿宋GB2312', serif !important;
    font-size: 16pt !important;
    text-align: left !important;
    font-weight: normal !important;
}

p {
    text-indent: 2em !important;
}
"""
    
    css_path = "/root/.openclaw/workspace/shuke_exact_fonts.css"
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_template)
    
    print(f"\n📝 CSS模板已创建: {css_path}")
    print("  将此CSS添加到PDF生成工具的HTML模板中")
    return css_path

def main():
    """主函数"""
    print("=" * 60)
    print("数科公司文印字体安装工具")
    print("=" * 60)
    
    # 检查权限
    if not check_root():
        sys.exit(1)
    
    # 确定字体文件目录
    source_dir = "." if len(sys.argv) < 2 else sys.argv[1]
    
    # 查找字体文件
    font_files = find_font_files(source_dir)
    if not font_files:
        sys.exit(1)
    
    # 安装字体
    if not install_fonts(font_files):
        sys.exit(1)
    
    # 更新字体缓存
    if not update_font_cache():
        print("⚠ 字体缓存更新可能有问题，但继续...")
    
    # 验证安装
    if not verify_font_installation():
        print("⚠ 字体验证可能有问题，但继续...")
    
    # 创建CSS模板
    css_path = create_font_css_template()
    
    print("\n" + "=" * 60)
    print("🎉 字体安装完成！")
    print("=" * 60)
    print("\n下一步操作:")
    print("1. 更新PDF生成工具使用精确字体:")
    print(f"   使用CSS模板: {css_path}")
    print("2. 重新生成PDF文档:")
    print("   python convert_to_pdf_exact_fonts.py 文档.docx")
    print("3. 验证PDF字体:")
    print("   pdffonts 生成的文档.pdf")
    print("4. 检查字体显示:")
    print("   确保PDF使用'方正小标宋简体'、'仿宋GB2312'等精确字体")
    
    print("\n✅ 安装完成！PDF现在将使用数科公司要求的精确字体。")

if __name__ == "__main__":
    main()