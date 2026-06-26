#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
readpaper技能主执行脚本 - v7.6 简化版
提取论文内容并保存为结构化文件，供AI直接读取生成报告

核心功能：
1. 智能PDF内容提取（多库支持，PyMuPDF优先，自动安装缺失库）
2. 结果缓存系统
3. 输出结构化内容文件供AI分析

版本更新：
v7.6 - 增加自动库安装功能：自动检查并安装PyMuPDF、pdfplumber、pypdf等依赖库
v7.5 - 优化PDF提取策略：10MB以下优先PyMuPDF，pdfplumber备选，pypdf最后备选
"""

import os
import sys
import re
import json
import time
import hashlib
from pathlib import Path

# 导入报告生成器
sys.path.insert(0, os.path.dirname(__file__))
from report_generator import PaperReportGenerator, generate_filename

# ============ 配置常量 ============
CACHE_DIR = Path.home() / ".workbuddy" / "cache" / "readpaper"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

MAX_PAGES_TO_EXTRACT = 25
MIN_VALID_CONTENT_LENGTH = 500


# ============ 缓存系统 ============
class PaperCache:
    """论文分析结果缓存系统"""
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        self.index_file = self.cache_dir / "cache_index.json"
        self.index = self._load_index()
    
    def _load_index(self):
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_index(self):
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def _get_fingerprint(self, pdf_path):
        try:
            stat = os.stat(pdf_path)
            content = f"{stat.st_size}_{stat.st_mtime}"
            return hashlib.md5(content.encode()).hexdigest()[:16]
        except:
            return None
    
    def get(self, pdf_path):
        fingerprint = self._get_fingerprint(pdf_path)
        if not fingerprint or fingerprint not in self.index:
            return None
        
        cache_file = self.cache_dir / f"{fingerprint}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def set(self, pdf_path, data):
        fingerprint = self._get_fingerprint(pdf_path)
        if not fingerprint:
            return False
        
        cache_file = self.cache_dir / f"{fingerprint}.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.index[fingerprint] = {
                'path': str(pdf_path),
                'title': data.get('title', '')[:100],
                'cached_at': time.time()
            }
            self._save_index()
            return True
        except:
            return False


# 全局缓存实例
cache = PaperCache()


# ============ 库安装管理器 ============
def ensure_package_installed(package_name, import_name=None):
    """
    确保指定的Python包已安装
    
    参数:
        package_name: pip安装时使用的包名
        import_name: 导入时使用的模块名，默认为package_name
    返回:
        bool: 是否成功安装/已安装
    """
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        print(f"  未检测到 {package_name}，正在安装...", end=' ')
        try:
            import subprocess
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package_name,
                '-q', '--disable-pip-version-check'
            ])
            print("成功")
            # 重新尝试导入
            try:
                __import__(import_name)
                return True
            except ImportError:
                print(f"安装后仍无法导入 {import_name}")
                return False
        except Exception as e:
            print(f"失败: {e}")
            return False


def ensure_pdf_libraries():
    """
    确保所有PDF处理库都已安装
    按优先级顺序检查和安装
    """
    print("检查PDF处理库...")
    
    # 定义需要安装的库 (pip包名, 导入名)
    libraries = [
        ('pymupdf', 'fitz'),      # PyMuPDF
        ('pdfplumber', 'pdfplumber'),  # pdfplumber
        ('pypdf', 'pypdf'),       # pypdf
    ]
    
    installed = {}
    for package, import_name in libraries:
        installed[package] = ensure_package_installed(package, import_name)
    
    # 检查是否至少有一个库可用
    if not any(installed.values()):
        print("错误: 无法安装任何PDF处理库，请手动安装 pymupdf、pdfplumber 或 pypdf")
        return False
    
    return True


# ============ PDF提取器 ============
def extract_with_pypdf(pdf_path):
    """使用pypdf提取"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        content = []
        
        for i, page in enumerate(reader.pages[:MAX_PAGES_TO_EXTRACT]):
            text = page.extract_text()
            if text and text.strip():
                content.append(f"=== Page {i+1} ===\n{text}")
        
        full_content = "\n\n".join(content)
        if len(full_content) > MIN_VALID_CONTENT_LENGTH:
            return full_content
    except:
        pass
    return None


def extract_with_pymupdf(pdf_path):
    """使用PyMuPDF提取"""
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        content = []
        
        for i in range(min(MAX_PAGES_TO_EXTRACT, len(doc))):
            text = doc[i].get_text()
            if text and text.strip():
                content.append(f"=== Page {i+1} ===\n{text}")
        
        doc.close()
        full_content = "\n\n".join(content)
        if len(full_content) > MIN_VALID_CONTENT_LENGTH:
            return full_content
    except:
        pass
    return None


def extract_with_pdfplumber(pdf_path):
    """使用pdfplumber提取"""
    try:
        import pdfplumber
        content = []
        
        with pdfplumber.open(str(pdf_path)) as pdf:
            for i, page in enumerate(pdf.pages[:MAX_PAGES_TO_EXTRACT]):
                text = page.extract_text()
                if text and text.strip():
                    content.append(f"=== Page {i+1} ===\n{text}")
        
        full_content = "\n\n".join(content)
        if len(full_content) > MIN_VALID_CONTENT_LENGTH:
            return full_content
    except:
        pass
    return None


def smart_pdf_extract(pdf_path):
    """
    智能选择最优PDF提取方法
    策略：
    - 10MB以下文件：优先使用PyMuPDF，pdfplumber作为备选，pypdf作为最后备选
    - 10MB以上文件：优先使用pdfplumber（内存效率高），PyMuPDF作为备选
    """
    
    file_size = os.path.getsize(pdf_path)
    file_size_mb = file_size / 1024 / 1024
    print(f"文件大小: {file_size_mb:.2f} MB")
    
    if file_size_mb < 10:
        # 10MB以下文件：PyMuPDF优先
        print(f"尝试使用 PyMuPDF 提取...", end=' ')
        result = extract_with_pymupdf(pdf_path)
        if result and len(result) > MIN_VALID_CONTENT_LENGTH:
            print(f"成功 ({len(result)} 字符)")
            return result, 'pymupdf'
        print("失败")
        
        # 备选：pdfplumber
        print(f"尝试使用 pdfplumber 提取...", end=' ')
        result = extract_with_pdfplumber(pdf_path)
        if result and len(result) > MIN_VALID_CONTENT_LENGTH:
            print(f"成功 ({len(result)} 字符)")
            return result, 'pdfplumber'
        print("失败")
        
        # 最后备选：pypdf
        print(f"尝试使用 pypdf 提取...", end=' ')
        result = extract_with_pypdf(pdf_path)
        if result and len(result) > MIN_VALID_CONTENT_LENGTH:
            print(f"成功 ({len(result)} 字符)")
            return result, 'pypdf'
        print("失败")
    else:
        # 10MB以上文件：pdfplumber优先（内存效率高）
        print(f"尝试使用 pdfplumber 提取...", end=' ')
        result = extract_with_pdfplumber(pdf_path)
        if result and len(result) > MIN_VALID_CONTENT_LENGTH:
            print(f"成功 ({len(result)} 字符)")
            return result, 'pdfplumber'
        print("失败")
        
        # 备选：PyMuPDF
        print(f"尝试使用 PyMuPDF 提取...", end=' ')
        result = extract_with_pymupdf(pdf_path)
        if result and len(result) > MIN_VALID_CONTENT_LENGTH:
            print(f"成功 ({len(result)} 字符)")
            return result, 'pymupdf'
        print("失败")
        
        # 最后备选：pypdf
        print(f"尝试使用 pypdf 提取...", end=' ')
        result = extract_with_pypdf(pdf_path)
        if result and len(result) > MIN_VALID_CONTENT_LENGTH:
            print(f"成功 ({len(result)} 字符)")
            return result, 'pypdf'
        print("失败")
    
    return None, "failed"


# ============ 主分析函数 ============
def analyze_paper(pdf_path, output_dir=".", use_cache=True):
    """
    分析论文的主函数 - 方案B：提取内容供AI直接分析
    
    参数:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        use_cache: 是否使用缓存
    
    返回:
        包含提取内容的字典，供AI生成报告
    """
    start_time = time.time()
    pdf_path = Path(pdf_path)
    
    print("=" * 60)
    print("readpaper v7.6 (简化版)")
    print("=" * 60)
    print(f"分析文件: {pdf_path.name}")
    
    # 1. 检查并安装必要的PDF处理库
    if not ensure_pdf_libraries():
        print("错误: 无法安装必要的PDF处理库")
        return {'error': 'Failed to install PDF libraries'}
    
    # 2. 检查缓存
    if use_cache:
        cached = cache.get(pdf_path)
        if cached:
            elapsed = time.time() - start_time
            print(f"缓存命中！响应时间: {elapsed:.3f}秒")
            print("=" * 60)
            return cached
    
    # 3. PDF内容提取
    content, method_used = smart_pdf_extract(pdf_path)
    
    if not content:
        print("错误: PDF内容提取失败")
        return {'error': 'PDF extraction failed'}
    
    print(f"PDF内容提取成功 ({method_used})")
    
    # 4. 提取论文结构化内容
    print("提取论文结构化内容...")
    generator = PaperReportGenerator()
    extracted_data = generator.extract_all_content(pdf_path, content)
    
    # 5. 保存提取的内容供AI读取
    elapsed = time.time() - start_time
    
    # 生成内容文件路径
    content_file = generate_filename(pdf_path, output_dir).replace('_报告.md', '_提取内容.txt')
    
    # 构建结构化内容文本
    structured_content = build_structured_content(extracted_data, pdf_path.name)
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(structured_content)
        print(f"提取内容已保存: {content_file}")
    except Exception as e:
        print(f"保存提取内容失败: {e}")
        content_file = None
    
    # 6. 构建结果
    result = {
        'pdf_path': str(pdf_path),
        'content_file': content_file,
        'extracted_data': extracted_data,
        'structured_content': structured_content,
        'elapsed_time': elapsed,
        'method': method_used,
        'cached': False
    }
    
    # 7. 缓存结果
    if use_cache:
        cache.set(pdf_path, result)
    
    print(f"总耗时: {elapsed:.3f}秒")
    print("=" * 60)
    
    # 8. 输出完成标记，供AI识别
    if content_file:
        print(f"\n[READPAPER_COMPLETE] 提取内容文件: {content_file}")
        print(f"[READPAPER_PDF_NAME] {pdf_path.stem}")
    
    return result


def build_structured_content(extracted_data, pdf_filename):
    """
    构建结构化内容文本，供AI直接读取生成报告
    """
    metadata = extracted_data['metadata']
    abstract = extracted_data.get('abstract', '') or ''
    background = extracted_data.get('background', []) or []
    methods = extracted_data.get('methods', '') or ''
    figures = extracted_data.get('figures_tables', []) or []
    results = extracted_data.get('results', '') or ''
    conclusion = extracted_data.get('conclusion', '') or ''
    raw_content = extracted_data.get('raw_content', '') or ''
    
    content = f"""# 论文提取内容

> 来源文件: {pdf_filename}
> 提取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}

---

## 一、论文基本信息

- **论文标题（英文）**: {metadata.get('title', '未识别')}
- **期刊/会议**: {metadata.get('journal', '未识别')}
- **作者**: {metadata.get('authors', '未识别')}
- **作者单位**: {metadata.get('affiliation', '未识别')}
- **发表时间**: {metadata.get('year', '未识别')}
- **DOI**: {metadata.get('doi', '未识别')}

---

## 二、论文摘要（英文原文）

{abstract[:3000] if abstract else '未提取到摘要'}

---

## 三、研究背景（英文原文）

"""
    
    if background:
        for i, para in enumerate(background[:6], 1):
            content += f"段落{i}: {para[:600]}\n\n"
    else:
        content += "未提取到背景信息\n"
    
    content += f"""---

## 四、研究方法（英文原文）

{methods[:2500] if methods else '未提取到方法部分'}

---

## 五、主要图表说明（英文原文）

"""
    
    if figures:
        for item in figures[:10]:
            content += f"{item['type']} {item['number']}: {item['caption'][:400]}\n\n"
    else:
        content += "未提取到图表信息\n"
    
    content += f"""---

## 六、研究结果（英文原文）

{results[:2000] if results else '未提取到结果部分'}

---

## 七、结论（英文原文）

{conclusion[:2000] if conclusion else '未提取到结论部分'}

---

## 八、原始内容片段（供参考）

{raw_content[:3000] if raw_content else ''}

---

*内容由 readpaper skill v7.6 自动提取*
"""
    
    return content


# ============ 命令行接口 ============
def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='readpaper v7.6 (简化版)')
    parser.add_argument('pdf_path', help='PDF文件路径')
    parser.add_argument('-o', '--output', default='.', help='输出目录')
    parser.add_argument('--no-cache', action='store_true', help='禁用缓存')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"错误: 文件不存在 - {args.pdf_path}")
        sys.exit(1)
    
    result = analyze_paper(
        args.pdf_path,
        output_dir=args.output,
        use_cache=not args.no_cache
    )
    
    if result.get('content_file'):
        print(f"\n提取内容文件: {result['content_file']}")
        print("\n请将此文件内容发送给AI助手，让AI生成完整的中文阅读报告。")


if __name__ == "__main__":
    main()
