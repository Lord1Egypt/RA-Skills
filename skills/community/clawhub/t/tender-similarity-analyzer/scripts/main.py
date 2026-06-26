#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投标文件查重与分析工具 - 主入口
tender-similarity-analyzer

支持两种输入模式：
1. 直接指定文件列表：--files file1.docx file2.docx
2. 扫描本地目录：--dir /path/to/directory [--recursive] [--include docx,pdf]

首次使用时会自动检测并安装缺失的依赖。
"""

import argparse
import json
import sys
import time
import os
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# 首次使用检查依赖（手动安装模式）
try:
    from check_dependencies import ensure_dependencies, get_missing_requirements
    _deps_ok = ensure_dependencies(auto_install=False, verbose=True)
    if not _deps_ok:
        missing = get_missing_requirements()
        print(f"\n❌ 依赖缺失: {', '.join(missing.keys())}")
        print("请先执行: pip install -r requirements.txt")
        sys.exit(1)
except ImportError:
    pass

from security.network_isolator import NetworkIsolator
from security.audit_logger import AuditLogger
from extractors.docx_extractor import DocxExtractor
from extractors.pdf_extractor import PdfExtractor
from extractors.txt_extractor import TxtExtractor
from engine.checker import PlagiarismChecker
from report.report_generator import ReportGenerator
from utils.file_utils import ensure_dir, get_file_hash, cleanup_temp_files


class TenderSimilarityAnalyzer:
    """投标文件查重分析器主类"""
    
    def __init__(self):
        self.isolator = NetworkIsolator(self._alert_callback)
        self.audit_logger = AuditLogger()
        self.checker = PlagiarismChecker()
        self.report_generator = ReportGenerator()
        self.temp_files = []
        
    def _alert_callback(self, message):
        """安全告警回调（仅本地打印，不发送外部）"""
        print(f"[安全] {message}")
            
    def _get_extractor(self, file_path):
        """根据文件扩展名获取提取器"""
        ext = Path(file_path).suffix.lower()
        extractors = {
            '.docx': DocxExtractor(),
            '.doc': DocxExtractor(),  # python-docx 也支持 .doc
            '.pdf': PdfExtractor(),
            '.txt': TxtExtractor(),
            '.md': TxtExtractor(),
        }
        return extractors.get(ext)
    
    def analyze_files(self, file_paths, output_path=None):
        """
        分析多个文件并生成查重报告
        
        @param file_paths: 文件路径列表
        @param output_path: 报告输出路径
        @return: 查重报告字典
        """
        print(f"[*] 启动查重分析，共 {len(file_paths)} 个文件")
        
        # 步骤1: 启用网络隔离
        print("[*] 启用网络安全隔离...")
        self.isolator.enable_isolation()
        
        try:
            # 步骤2: 提取文本
            print("[*] 提取文件文本...")
            documents = {}
            for file_path in file_paths:
                extractor = self._get_extractor(file_path)
                if not extractor:
                    print(f"[!] 不支持的文件格式: {file_path}")
                    continue
                    
                try:
                    text = extractor.extract(file_path)
                    file_hash = get_file_hash(file_path)
                    documents[file_path] = {
                        'text': text,
                        'hash': file_hash,
                        'name': Path(file_path).name
                    }
                    print(f"    ✓ {Path(file_path).name} ({len(text)} 字)")
                except Exception as e:
                    print(f"[!] 提取失败 {file_path}: {e}")
                    
            if len(documents) < 2:
                print("[!] 需要至少2个文件才能进行查重")
                return None
                
            # 步骤3: 执行查重
            print("[*] 执行查重分析...")
            start_time = time.time()
            results = self.checker.check(documents)
            elapsed = time.time() - start_time
            print(f"    ✓ 分析完成，耗时 {elapsed:.2f} 秒")
            
            # 步骤4: 生成报告
            print("[*] 生成查重报告...")
            report = self.report_generator.generate(
                documents=documents,
                results=results,
                output_path=output_path
            )
            
            # 步骤5: 验算0出站
            print("[*] 安全验算...")
            if not self.isolator.verify_zero_exfiltration():
                self.alert_manager.send_alert(
                    "CRITICAL",
                    "数据泄露警告",
                    "检测到异常网络流量！"
                )
                raise SecurityError("检测到文件内容可能泄露！")
                
            # 记录审计日志
            self.audit_logger.log_operation(
                op_type="analyze",
                file_info=[f"{d['name']} ({d['hash'][:8]})" for d in documents.values()],
                result="success",
                total_paras=results.get('total_paras', 0),
                duplicate_paras=results.get('duplicate_paras', 0)
            )
            
            print(f"[*] 查重完成！报告: {output_path}")
            return report
            
        finally:
            # 解除隔离
            self.isolator.disable_isolation()
            print("[*] 网络隔离已解除")
    
    def auto_fix_document(self, file_path, suggestions):
        """
        根据查重建议自动修改文档
        
        @param file_path: 文档路径
        @param suggestions: 修改建议列表
        @return: 修改后的文档路径
        """
        print(f"[*] 开始自动修改文档: {file_path}")
        
        self.isolator.enable_isolation()
        
        try:
            editor = FormatPreservingEditor(file_path)
            
            for suggestion in suggestions:
                para_idx = suggestion.get('para_index')
                old_text = suggestion.get('old_text')
                new_text = suggestion.get('new_text')
                
                if para_idx is not None and old_text and new_text:
                    count = editor.replace_text_in_para_preserving_format(
                        para_idx, old_text, new_text
                    )
                    print(f"    ✓ 段落{para_idx}: 已修改")
                    
            output_path = file_path.replace('.docx', '_fixed.docx')
            editor.save(output_path)
            print(f"[*] 文档已保存: {output_path}")
            return output_path
            
        finally:
            self.isolator.disable_isolation()


def scan_directory(dir_path, extensions=None, recursive=False):
    """
    扫描目录获取支持的文件列表
    
    @param dir_path: 目录路径
    @param extensions: 文件扩展名列表，如 ['docx', 'pdf', 'txt']
    @param recursive: 是否递归子目录
    @return: 文件路径列表
    """
    if extensions is None:
        extensions = ['.docx', '.doc', '.pdf', '.txt', '.md']
    
    # 统一添加点前缀
    ext_set = set(ext if ext.startswith('.') else f'.{ext}' for ext in extensions)
    
    files = []
    dir_path = Path(dir_path)
    
    if not dir_path.exists():
        print(f"[!] 目录不存在: {dir_path}")
        return files
        
    if not dir_path.is_dir():
        print(f"[!] 路径不是目录: {dir_path}")
        return files
    
    # 扫描文件
    if recursive:
        for ext in ext_set:
            files.extend(str(f) for f in dir_path.rglob(f'*{ext}'))
    else:
        for ext in ext_set:
            files.extend(str(f) for f in dir_path.glob(f'*{ext}'))
    
    # 去重并排序
    return sorted(list(set(files)))


def main():
    parser = argparse.ArgumentParser(
        description='投标文件查重分析工具 - 本地多文档交叉查重',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
💡 使用示例:

  # 扫描本地目录（推荐，完全本地）
  python main.py --dir ~/Desktop/投标文件
  
  # 递归扫描子目录
  python main.py --dir ./chapters --recursive
  
  # 指定文件格式
  python main.py --dir ./docs --include docx,pdf
  
  # 直接指定文件
  python main.py --files a.docx b.docx c.pdf
  
  # 组合使用
  python main.py --files a.docx --dir ./ref --recursive
'''
    )
    
    # 文件输入模式
    parser.add_argument('--files', nargs='+', 
                       help='要查重的文件列表')
    
    # 目录输入模式
    parser.add_argument('--dir', nargs='+',
                       help='本地目录路径（可指定多个）')
    parser.add_argument('--recursive', action='store_true',
                       help='递归扫描子目录')
    parser.add_argument('--include', 
                       help='仅扫描指定扩展名，如: docx,pdf,txt')
    
    # 输出配置
    parser.add_argument('--output', '-o', default='tender_plagiarism_report.html',
                       help='报告输出路径 (默认: tender_plagiarism_report.html)')
    args = parser.parse_args()
    
    # 收集所有要查重的文件
    file_paths = []
    
    # 方式1: 直接指定文件
    if args.files:
        file_paths.extend(args.files)
        print(f"[*] 📄 已添加 {len(args.files)} 个指定文件")
    
    # 方式2: 扫描目录
    if args.dir:
        extensions = args.include.split(',') if args.include else None
        
        for dir_path in args.dir:
            dir_files = scan_directory(dir_path, extensions, args.recursive)
            
            if not dir_files:
                print(f"[*] 目录中无支持文件: {dir_path}")
                continue
                    
            file_paths.extend(dir_files)
            print(f"[*] 📁 已从目录扫描: {dir_path}")
            print(f"    找到 {len(dir_files)} 个文件")
    
    # 检查文件数量
    if len(file_paths) < 2:
        print("\n❌ 错误：需要至少2个文件才能进行查重分析\n")
        print("用法：")
        print("  查重 --dir <目录路径>              # 扫描本地目录")
        print("  查重 --files <文件1> <文件2> ...   # 直接指定文件")
        print("  查重 --dir <目录> --recursive      # 递归扫描子目录")
        print("")
        print("完整帮助：python main.py --help")
        return
    
    # 去重
    file_paths = sorted(list(set(file_paths)))
    print(f"\n[*] 共识别 {len(file_paths)} 个文件待查重")
    print("-" * 50)
    
    # 显示文件列表
    for i, f in enumerate(file_paths, 1):
        print(f"  {i}. {f}")
    print("-" * 50)
    
    # 执行查重
    print("\n[*] 🔍 启动查重分析...")
    analyzer = TenderSimilarityAnalyzer()
    report = analyzer.analyze_files(file_paths, args.output)
    
    if report:
        print("\n" + "=" * 50)
        print("📊 查重结果摘要")
        print("=" * 50)
        print(f"   检测文件数:     {report.get('total_files', 0)}")
        print(f"   总段落数:       {report.get('total_paras', 0)}")
        print(f"   涉及重复段落:   {report.get('involved_paragraphs', 0)} 段")
        print(f"   重复段落比例:   {report.get('para_duplication_rate', 0):.1%}")
        
        dup_count = report.get('duplicate_count', 0)
        severe_count = report.get('severe_count', 0)
        print(f"   重复段落对:     {dup_count} 对")
        if severe_count > 0:
            print(f"   🔴 严重(≥50%): {severe_count} 对")
        
        avg_sim = report.get('avg_similarity', 0)
        print(f"\n   重复内容相似度: {avg_sim:.1%}")
        
        status = report.get('pass_status', 'pass')
        status_text = "✅ 通过" if status == 'pass' else "⚠️ 需修改" if status == 'warning' else "❌ 不合格"
        print(f"   状态:           {status_text}")
        print("=" * 50)
        print(f"\n[*] ✅ 查重完成！报告已保存: {args.output}")


if __name__ == '__main__':
    main()
