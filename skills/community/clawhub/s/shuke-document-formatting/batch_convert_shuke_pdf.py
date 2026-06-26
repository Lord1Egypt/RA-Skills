#!/usr/bin/env python3
"""
数科公司文印格式PDF批量转换工具
批量处理文件夹中的所有DOCX文档
"""

import os
import sys
from pathlib import Path
import subprocess

def get_docx_files(folder_path):
    """获取文件夹中的所有DOCX文件"""
    folder = Path(folder_path)
    if not folder.exists():
        print(f"❌ 文件夹不存在: {folder_path}")
        return []
    
    # 递归查找所有DOCX文件
    docx_files = list(folder.glob("**/*.docx"))
    
    # 过滤掉以~$开头的临时文件
    docx_files = [f for f in docx_files if not f.name.startswith('~$')]
    
    return docx_files

def convert_single_file(docx_path, output_dir=None):
    """转换单个DOCX文件为PDF"""
    try:
        # 导入转换函数
        from convert_to_pdf_shuke_final import convert_docx_to_pdf_shuke
        
        docx_file = Path(docx_path)
        
        # 确定输出路径
        if output_dir:
            output_path = Path(output_dir) / f"{docx_file.stem}_shuke_format.pdf"
        else:
            output_path = docx_file.with_name(f"{docx_file.stem}_shuke_format.pdf")
        
        print(f"📄 处理: {docx_file.name}")
        
        # 转换
        pdf_path = convert_docx_to_pdf_shuke(str(docx_file), str(output_path))
        
        if pdf_path and os.path.exists(pdf_path):
            print(f"  ✓ 生成: {Path(pdf_path).name}")
            return True, pdf_path
        else:
            print(f"  ✗ 转换失败")
            return False, None
            
    except Exception as e:
        print(f"  ✗ 转换错误: {e}")
        return False, None

def main():
    """主函数"""
    print("=" * 60)
    print("数科公司文印格式PDF批量转换工具")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n使用方法:")
        print("  python batch_convert_shuke_pdf.py <输入文件夹> [输出文件夹]")
        print("\n示例:")
        print("  python batch_convert_shuke_pdf.py ./英文文件名文档/")
        print("  python batch_convert_shuke_pdf.py ./中文文档/ ./PDF输出/")
        print("\n输出文件命名: 原文件名_shuke_format.pdf")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 创建输出文件夹
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        print(f"输出文件夹: {output_folder}")
    
    # 获取DOCX文件
    print(f"\n📁 扫描文件夹: {input_folder}")
    docx_files = get_docx_files(input_folder)
    
    if not docx_files:
        print("❌ 未找到DOCX文件")
        sys.exit(1)
    
    print(f"找到 {len(docx_files)} 个DOCX文件:")
    for i, file in enumerate(docx_files[:10], 1):  # 只显示前10个
        print(f"  {i:2d}. {file.name}")
    if len(docx_files) > 10:
        print(f"  ... 还有 {len(docx_files)-10} 个文件")
    
    # 确认
    print("\n是否开始转换? (y/n): ", end="")
    response = input().strip().lower()
    if response not in ['y', 'yes', '是']:
        print("取消转换")
        sys.exit(0)
    
    # 批量转换
    print("\n" + "=" * 60)
    print("开始批量转换...")
    print("=" * 60)
    
    successful = 0
    failed = 0
    results = []
    
    for i, docx_file in enumerate(docx_files, 1):
        print(f"\n[{i}/{len(docx_files)}] ", end="")
        
        success, pdf_path = convert_single_file(str(docx_file), output_folder)
        
        if success:
            successful += 1
            results.append(("✓", docx_file.name, pdf_path))
        else:
            failed += 1
            results.append(("✗", docx_file.name, "转换失败"))
    
    # 输出结果
    print("\n" + "=" * 60)
    print("批量转换完成")
    print("=" * 60)
    
    print(f"\n📊 转换结果:")
    print(f"  成功: {successful}/{len(docx_files)}")
    print(f"  失败: {failed}/{len(docx_files)}")
    
    if successful > 0:
        print("\n✅ 生成的PDF文件:")
        for status, name, path in results:
            if status == "✓":
                print(f"  {status} {name} -> {Path(path).name}")
    
    if failed > 0:
        print("\n❌ 失败的文件:")
        for status, name, path in results:
            if status == "✗":
                print(f"  {status} {name}")
    
    # 生成汇总报告
    report_file = "batch_conversion_report.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("数科公司文印格式PDF批量转换报告\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"输入文件夹: {input_folder}\n")
        if output_folder:
            f.write(f"输出文件夹: {output_folder}\n")
        f.write(f"总文件数: {len(docx_files)}\n")
        f.write(f"成功: {successful}\n")
        f.write(f"失败: {failed}\n\n")
        
        f.write("详细结果:\n")
        for status, name, path in results:
            f.write(f"{status} {name}\n")
            if status == "✓":
                f.write(f"   -> {path}\n")
    
    print(f"\n📝 详细报告已保存: {report_file}")
    
    # 提供后续操作建议
    print("\n💡 后续操作:")
    print("  1. 检查PDF字体是否正确:")
    print("     pdffonts 生成的文档.pdf")
    print("  2. 如果需要重新转换单个文件:")
    print("     python convert_to_pdf_shuke_final.py 文档.docx")
    print("  3. 验证字体安装:")
    print("     python verify_shuke_fonts.py")

if __name__ == "__main__":
    main()