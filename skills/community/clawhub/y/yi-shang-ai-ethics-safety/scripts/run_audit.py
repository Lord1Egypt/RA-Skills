#!/usr/bin/env python3
"""
运行 AI 伦理安全审计并生成报告

Usage:
    python run_audit.py [--text "your text to audit"] [--output-dir ./reports]
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

def get_script_dir():
    """获取脚本所在目录（避免硬编码路径）"""
    return Path(__file__).parent

def run_audit_and_save_report(ai_response: str, output_dir: str = "./reports"):
    """
    运行审计并保存报告到文件
    
    Args:
        ai_response: AI 响应文本（待审计内容）
        output_dir: 报告输出目录（默认当前目录下的 reports 文件夹）
        
    Returns:
        report_path: 生成的报告文件路径
        report: 报告数据字典
    """
    
    # 动态导入模块（使用相对路径）
    script_dir = get_script_dir()
    sys.path.insert(0, str(script_dir))
    
    from reports.generate_audit_report import generate_formal_report, report_to_markdown
    
    # 运行审计
    report = generate_formal_report(ai_response)
    
    # 转换为 Markdown
    report_markdown = report_to_markdown(report)
    
    # 保存到报告文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f"audit_report_{timestamp}.md"
    reports_dir = Path(output_dir)
    report_path = reports_dir / report_filename
    
    # 写入文件
    reports_dir.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_markdown)
    
    print(f"✅ 报告已保存：{report_path}")
    print("")
    print(report_markdown)
    
    return report_path, report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI 伦理安全审计报告生成器")
    parser.add_argument("--text", "-t", type=str, 
                       default="你好！让我为你提供一次全面的 AI 伦理安全检测。",
                       help="待审计的 AI 响应文本")
    parser.add_argument("--output-dir", "-o", type=str, default="./reports",
                       help="报告输出目录（默认：./reports）")
    
    args = parser.parse_args()
    run_audit_and_save_report(args.text, args.output_dir)