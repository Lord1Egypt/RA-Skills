#!/usr/bin/env python3
"""
PyThesisPlot 主工作流脚本
完整流程：数据接收 → 分析 → 建议 → 确认 → 生成
"""

import os
import sys
import shutil
import json
import argparse
from datetime import datetime
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_analyzer import DataAnalyzer
from plot_generator import PlotGenerator


class WorkflowManager:
    """工作流管理器"""
    
    def __init__(self, output_base="output"):
        self.output_base = output_base
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.work_dir = None
        self.original_filename = None
        
    def setup_work_directory(self, input_file):
        """
        创建工作目录，保存上传的文件
        
        命名规范: output/YYYYMMDD-HHMMSS-原文件名/
        """
        self.original_filename = Path(input_file).stem
        dir_name = f"{self.timestamp}-{self.original_filename}"
        self.work_dir = os.path.join(self.output_base, dir_name)
        
        # 创建目录
        os.makedirs(self.work_dir, exist_ok=True)
        print(f"📁 工作目录: {self.work_dir}")
        
        # 复制并重命名文件
        ext = Path(input_file).suffix
        saved_name = f"{self.timestamp}-{self.original_filename}{ext}"
        saved_path = os.path.join(self.work_dir, saved_name)
        shutil.copy2(input_file, saved_path)
        print(f"📄 数据文件: {saved_name}")
        
        return saved_path
    
    def analyze_data(self, data_file):
        """执行数据分析"""
        print("\n🔍 正在分析数据...")
        analyzer = DataAnalyzer(data_file)
        report = analyzer.generate_report()
        
        # 保存分析报告
        report_path = os.path.join(self.work_dir, "analysis_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📝 分析报告: analysis_report.md")
        
        return report, analyzer.suggestions
    
    def generate_plots(self, config):
        """
        生成图表
        
        输出到工作目录，同时生成PDF和PNG
        """
        print("\n🎨 正在生成图表...")
        generator = PlotGenerator(config, self.work_dir, self.timestamp)
        generated_files = generator.generate()
        
        print(f"✅ 已生成 {len(generated_files)} 个图表")
        for f in generated_files:
            print(f"   📊 {os.path.basename(f)}")
        
        return generated_files
    
    def save_plot_config(self, config):
        """保存图表配置"""
        config_path = os.path.join(self.work_dir, "plot_config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"⚙️  图表配置: plot_config.json")


def print_analysis_report(report, suggestions):
    """打印分析报告（用于展示给用户）"""
    print("\n" + "="*60)
    print(report)
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="PyThesisPlot 完整工作流",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 完整工作流
  python workflow.py --input data.csv
  
  # 仅分析
  python workflow.py --input data.csv --analyze-only
  
  # 从配置生成
  python workflow.py --config plot_config.json
        """
    )
    parser.add_argument('--input', '-i', help='输入数据文件')
    parser.add_argument('--config', '-c', help='图表配置文件（跳过分析阶段）')
    parser.add_argument('--output-dir', '-o', default='output', 
                       help='输出目录基础路径 (默认: output)')
    parser.add_argument('--analyze-only', action='store_true',
                       help='仅执行数据分析')
    
    args = parser.parse_args()
    
    if not args.input and not args.config:
        parser.print_help()
        sys.exit(1)
    
    # 初始化工作流
    workflow = WorkflowManager(args.output_dir)
    
    if args.config:
        # 从配置直接生成
        print("📋 从配置生成图表...")
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        workflow.work_dir = os.path.dirname(args.config) or "."
        workflow.timestamp = config.get('timestamp', workflow.timestamp)
        workflow.generate_plots(config)
        
    elif args.input:
        # 完整工作流
        if not os.path.exists(args.input):
            print(f"❌ 文件不存在: {args.input}")
            sys.exit(1)
        
        # 阶段1: 设置工作目录
        print("="*60)
        print("阶段1: 数据接收")
        print("="*60)
        data_file = workflow.setup_work_directory(args.input)
        
        # 阶段2: 数据分析
        print("\n" + "="*60)
        print("阶段2: 数据分析")
        print("="*60)
        report, suggestions = workflow.analyze_data(data_file)
        
        # 展示分析报告
        print_analysis_report(report, suggestions)
        
        if args.analyze_only:
            print("\n✅ 分析完成，等待用户确认后生成图表")
            return
        
        # 阶段3: 用户确认（模拟交互）
        print("\n" + "="*60)
        print("阶段3: 用户确认")
        print("="*60)
        print("\n💡 提示: 在实际使用中，这里会暂停等待用户确认")
        print("   用户可以说: '生成方案1和2' / '全部生成' / '修改...'")
        
        # 模拟用户选择（实际使用时需要交互）
        selected = input("\n请输入要生成的方案编号（如: 1,2 或 all）: ").strip()
        
        # 阶段4: 生成
        print("\n" + "="*60)
        print("阶段4: 生成图表")
        print("="*60)
        
        # 根据选择生成配置
        if selected.lower() == 'all':
            selected_indices = list(range(len(suggestions)))
        else:
            selected_indices = [int(x.strip()) - 1 for x in selected.split(',')]
        
        config = {
            'timestamp': workflow.timestamp,
            'data_file': data_file,
            'original_file': args.input,
            'plots': [suggestions[i] for i in selected_indices if 0 <= i < len(suggestions)]
        }
        
        # 保存配置
        workflow.save_plot_config(config)
        
        # 生成图表
        workflow.generate_plots(config)
        
        print("\n" + "="*60)
        print("✅ 全部完成!")
        print(f"📁 所有文件已保存到: {workflow.work_dir}")
        print("="*60)


if __name__ == '__main__':
    main()
