#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Xtranslate 主程序入口"""

import os
import time
import argparse
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 模块导入带重试机制
MAX_RETRIES = 3
RETRY_DELAY = 1

for attempt in range(MAX_RETRIES):
    try:
        from config_loader import CONFIG
        from file_handler import FileHandler
        from translator import TranslatorModule
        from analyzer import TextAnalyzer
        from formatter import WordFormatter
        from translation_monitor import monitor  # 导入监控器
        break
    except KeyboardInterrupt:
        print("\n[中断] 用户取消操作")
        sys.exit(1)
    except Exception as e:
        if attempt < MAX_RETRIES - 1:
            print(f"[警告] 导入模块失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
            time.sleep(RETRY_DELAY)
        else:
            print(f"[错误] 模块导入失败: {e}")
            sys.exit(1)

print("[就绪] Xtranslate 翻译引擎已加载")


class TranslationTimer:
    """翻译耗时统计器"""
    def __init__(self):
        self.timings = {}
        self.start_times = {}
    
    def start(self, step_name):
        self.start_times[step_name] = time.time()
    
    def end(self, step_name):
        if step_name in self.start_times:
            elapsed = time.time() - self.start_times[step_name]
            self.timings[step_name] = elapsed
            return elapsed
        return 0
    
    def report(self):
        print("\n" + "="*60)
        print("【翻译耗时统计】")
        print("="*60)
        total = sum(self.timings.values())
        for step, elapsed in self.timings.items():
            percentage = (elapsed / total * 100) if total > 0 else 0
            print(f"  {step:20s}: {elapsed:6.2f}s ({percentage:5.1f}%)")
        print("-"*60)
        print(f"  {'总计':20s}: {total:6.2f}s")
        print("="*60)

def process_file(file_path, engine_type=None, output_dir=None, source_lang=None, target_lang=None, cloud_model=None, custom_url=None, custom_name=None, timer=None):
    """处理单个文件的翻译流程"""
    if timer is None:
        timer = TranslationTimer()
    
    if not engine_type:
        engine_type = CONFIG.get("TRANSLATE_ENGINE", "cloud")
    
    if cloud_model:
        CONFIG["CURRENT_CLOUD_MODEL"] = cloud_model
        if cloud_model == "自定义 (OpenAI 兼容)":
            if custom_url:
                CONFIG["CLOUD_MODELS"]["自定义 (OpenAI 兼容)"]["base_url"] = custom_url
            if custom_name:
                CONFIG["CLOUD_MODELS"]["自定义 (OpenAI 兼容)"]["model"] = custom_name
        
    s_lang = source_lang if source_lang else CONFIG.get("SOURCE_LANG", "auto")
    t_lang = target_lang if target_lang else CONFIG.get("TARGET_LANG", "zh-CN")
        
    handler = FileHandler()
    file_ext = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    
    # 开始监控记录
    monitor_record = monitor.start_translation(file_path, engine_type, target_lang)
    monitor.record_phase(monitor_record, "初始化")
    
    # 确定输出目录
    if not output_dir:
        if CONFIG.get("SAVE_IN_SOURCE_DIR", True):
            output_dir = file_dir if file_dir else "."
        else:
            output_dir = CONFIG.get("OUTPUT_DIR", "output")
    
    # 确保输出目录有效
    if not output_dir:
        output_dir = "."
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # 1. 文件读取与预处理
        timer.start("文件读取")
        monitor.record_phase(monitor_record, "文件读取")
        analysis_text = ""
        current_work_path = file_path
        
        if file_ext == '.pdf':
            if CONFIG.get("VERBOSE_OUTPUT", True):
                print(f"  [PDF -> DOCX] 正在转换以进行分析...")
            current_work_path = handler.pdf_to_docx(file_path, CONFIG["PDF_TO_DOCX_TMP"])
            paragraphs = handler.read_docx(current_work_path)
            analysis_text = "\n".join(paragraphs[:50]) # 取前50段进行分析
        elif file_ext in ['.docx', '.wps']:
            paragraphs = handler.read_docx(file_path)
            analysis_text = "\n".join(paragraphs[:50])
        elif file_ext == '.txt':
            analysis_text = handler.read_txt(file_path)[:5000] # 取前5000字
        elif file_ext == '.xlsx':
            texts = handler.read_xlsx(file_path)
            analysis_text = "\n".join(texts[:50])
        elif file_ext == '.pptx':
            texts = handler.read_pptx(file_path)
            analysis_text = "\n".join(texts[:50])
        elif file_ext == '.rtf':
            analysis_text = handler.read_rtf(file_path)[:5000]
        timer.end("文件读取")
        monitor.end_phase(monitor_record, "文件读取", success=True)
                
        # 2. 关键词提取
        timer.start("关键词提取")
        monitor.record_phase(monitor_record, "关键词提取")
        if CONFIG.get("VERBOSE_OUTPUT", True):
            print(f"  [分析] 正在提取关键词...")
        keywords = TextAnalyzer.extract_keywords(analysis_text)
        if CONFIG.get("VERBOSE_OUTPUT", True):
            print(f"  [分析] 提取到关键词: {', '.join(keywords)}")
        timer.end("关键词提取")
        monitor.end_phase(monitor_record, "关键词提取", success=True)

        # 3. 翻译执行
        timer.start("翻译执行")
        monitor.record_phase(monitor_record, "翻译执行")
        translator = TranslatorModule(
            engine=engine_type,
            source_lang=s_lang,
            target_lang=t_lang,
            keywords=keywords
        )

        # 3. 执行翻译并保存
        output_name = f"translated_{os.path.basename(current_work_path)}"
        output_path = os.path.join(output_dir, output_name)
        
        if file_ext in ['.pdf', '.docx', '.wps']:
            if CONFIG.get("VERBOSE_OUTPUT", True):
                print(f"  [翻译] 正在翻译 Word 内容并保留格式...")
            handler.translate_docx_in_place(current_work_path, translator, output_path)
            monitor.end_phase(monitor_record, "翻译执行", success=True)
            
            # 4. 自动排版优化 (如果配置开启)
            if CONFIG.get("AUTO_FORMAT_LAYOUT", True) and file_ext != '.wps':
                monitor.record_phase(monitor_record, "排版优化")
                if CONFIG.get("VERBOSE_OUTPUT", True):
                    print(f"  [排版] 正在进行排版优化...")
                formatter = WordFormatter()
                formatter.format_document(output_path, output_path)
                monitor.end_phase(monitor_record, "排版优化", success=True)
        elif file_ext == '.xlsx':
            if CONFIG.get("VERBOSE_OUTPUT", True):
                print(f"  [翻译] 正在翻译 Excel 内容...")
            handler.translate_xlsx_in_place(file_path, translator, output_path)
        elif file_ext == '.pptx':
            if CONFIG.get("VERBOSE_OUTPUT", True):
                print(f"  [翻译] 正在翻译 PPT 内容...")
            handler.translate_pptx_in_place(file_path, translator, output_path)
        elif file_ext in ['.txt', '.rtf']:
            if CONFIG.get("VERBOSE_OUTPUT", True):
                print(f"  [翻译] 正在翻译文本内容...")
            content = handler.read_txt(file_path) if file_ext == '.txt' else handler.read_rtf(file_path)
            translated_content = translator.translate_text(content)
            handler.save_txt(translated_content, output_path)

        timer.end("翻译执行")
        
        # 记录成功完成
        result_stats = {
            "output_path": output_path,
            "file_extension": file_ext
        }
        monitor.finish_translation(monitor_record, success=True, result_stats=result_stats)
        
        print(f"  [完成] {output_path}")
        return True, output_path, timer

    except Exception as e:
        timer.end("翻译执行")
        # 记录失败
        monitor.finish_translation(monitor_record, success=False, error_msg=str(e))
        print(f"  [错误] 处理文件 {file_path} 时出错: {e}")
        return False, str(e), timer

def main():
    # 显示版本和欢迎信息
    version = CONFIG.get('VERSION', '1.0.0')
    print(f"=" * 50)
    print(f"Xtranslate {version} - 智能文档翻译工具")
    print(f"=" * 50)
    print()
    
    parser = argparse.ArgumentParser(
        description=f"Xtranslate {version} 翻译程序命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py --file document.docx --engine cloud --tl zh-CN
  python main.py --dir ./docs --engine ollama --tl English
  python main.py --file input.pdf --engine python --sl English --tl 中文
        """
    )
    parser.add_argument("--engine", choices=["cloud", "ollama", "python"], help="指定翻译引擎")
    parser.add_argument("--file", help="指定待翻译的单个文件路径")
    parser.add_argument("--dir", help="指定待翻译的文件夹路径")
    parser.add_argument("--output", help="指定输出目录")
    parser.add_argument("--sl", help="源语言 (例如: en, zh-CN, auto)")
    parser.add_argument("--tl", help="目标语言 (例如: en, zh-CN)")
    parser.add_argument("--model", help="指定云端模型名称 (例如: GPT-4o, Claude 3.5 Sonnet, 自定义 (OpenAI 兼容))")
    parser.add_argument("--custom_url", help="自定义模型 API Base URL")
    parser.add_argument("--custom_name", help="自定义模型名称")
    
    args = parser.parse_args()

    handler = FileHandler()
    all_files = []

    # 1. 确定待翻译文件
    if args.file:
        if os.path.exists(args.file):
            all_files.append(args.file)
        else:
            print(f"错误: 找不到文件 {args.file}")
            return
    elif args.dir:
        if os.path.isdir(args.dir):
            all_files.extend(handler.get_all_files(args.dir))
        else:
            print(f"错误: 找不到目录 {args.dir}")
            return
    else:
        # 默认从 targets.txt 读取
        if not os.path.exists(CONFIG["TARGETS_FILE"]):
            print(f"提示: 未指定 --file 或 --dir，且找不到目标文件 {CONFIG['TARGETS_FILE']}")
            return

        with open(CONFIG["TARGETS_FILE"], 'r', encoding='utf-8') as f:
            targets = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        if not targets:
            print("提示: targets.txt 中没有有效的文件路径。")
            return

        for target in targets:
            all_files.extend(handler.get_all_files(target))

    if not all_files:
        print("提示: 没有找到可翻译的文件。")
        return

    # 2. 执行翻译
    engine = args.engine if args.engine else CONFIG.get("TRANSLATE_ENGINE", "cloud")
    
    for file_path in all_files:
        print(f"翻译: {os.path.basename(file_path)}")
        success, result, timer = process_file(file_path, engine_type=engine, output_dir=args.output, 
                     source_lang=args.sl, target_lang=args.tl, 
                     cloud_model=args.model, custom_url=args.custom_url, custom_name=args.custom_name)
        # 显示耗时统计
        if success and timer:
            timer.report()

    print("完成")

if __name__ == "__main__":
    main()
