#!/usr/bin/env python3
"""
批量趋势分析脚本
分析目录下所有股票数据文件
"""

import argparse
import sys
from pathlib import Path

# 导入单只股票分析功能
sys.path.insert(0, str(Path(__file__).parent))

try:
    from analyze_trend import analyze_trend
except ImportError as e:
    print(f"错误: 无法导入分析模块: {e}")
    sys.exit(1)


def find_csv_files(directory: str) -> list:
    """
    查找目录下的 CSV 文件
    
    Args:
        directory: 目录路径
    
    Returns:
        CSV 文件路径列表
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"错误: 目录不存在: {directory}")
        return []
    
    if not dir_path.is_dir():
        print(f"错误: 不是目录: {directory}")
        return []
    
    # 查找 CSV 文件
    csv_files = list(dir_path.glob("*.csv"))
    
    # 过滤：包含股票数据特征的文件
    stock_files = []
    for f in csv_files:
        # 排除一些明显不是股票数据的文件
        if any(keyword in f.name.lower() for keyword in ['trend', 'report', 'summary']):
            continue
        
        # 检查文件名是否看起来像股票数据
        if any(keyword in f.name for keyword in ['_', 'daily', 'A_', 'HK_', '600', '000', '300']):
            stock_files.append(f)
        elif f.stat().st_size > 10000:  # 大于 10KB 的可能是股票数据
            stock_files.append(f)
    
    return stock_files


def extract_stock_name(file_path: Path) -> str:
    """
    从文件名提取股票名称
    
    Args:
        file_path: 文件路径
    
    Returns:
        股票名称
    """
    name = file_path.stem
    
    # 尝试从文件名提取
    if "_" in name:
        parts = name.split("_")
        # 尝试找到最像名称的部分
        for part in parts:
            if any(c.isalpha() for c in part) and len(part) >= 2:
                if not part.isdigit():
                    return part
    
    return name


def batch_analyze(directory: str, output_dir: str = "trend_reports", period: int = 250):
    """
    批量分析股票数据
    
    Args:
        directory: 数据目录
        output_dir: 输出目录
        period: 分析周期
    
    Returns:
        (成功数, 失败数, 结果列表)
    """
    print("=" * 60)
    print("批量超级趋势分析")
    print("=" * 60)
    
    # 查找 CSV 文件
    print(f"\n正在扫描目录: {directory}")
    csv_files = find_csv_files(directory)
    
    if not csv_files:
        print("未找到合适的股票数据 CSV 文件")
        return 0, 0, []
    
    print(f"找到 {len(csv_files)} 个数据文件")
    
    # 逐个分析
    success_count = 0
    fail_count = 0
    results = []
    
    for i, file_path in enumerate(csv_files, 1):
        print(f"\n[{i}/{len(csv_files)}] " + "-" * 50)
        
        stock_name = extract_stock_name(file_path)
        print(f"分析: {stock_name} ({file_path.name})")
        
        try:
            success, report_file = analyze_trend(
                file_path=str(file_path),
                stock_name=stock_name,
                output_dir=output_dir,
                period=period,
                plot=False
            )
            
            if success:
                success_count += 1
                results.append((stock_name, "成功", report_file))
            else:
                fail_count += 1
                results.append((stock_name, "失败", None))
                
        except Exception as e:
            print(f"分析失败: {e}")
            fail_count += 1
            results.append((stock_name, f"错误: {e}", None))
    
    # 生成汇总报告
    print("\n" + "=" * 60)
    print("批量分析完成")
    print("=" * 60)
    print(f"成功: {success_count} 只")
    print(f"失败: {fail_count} 只")
    
    if results:
        print("\n分析结果汇总:")
        print("-" * 40)
        for name, status, _ in results:
            status_icon = "✅" if status == "成功" else "❌"
            print(f"{status_icon} {name}: {status}")
    
    return success_count, fail_count, results


def main():
    parser = argparse.ArgumentParser(
        description="批量超级趋势分析"
    )
    parser.add_argument("--dir", required=True, help="股票数据目录")
    parser.add_argument("--output", default="trend_reports", help="输出目录（默认：trend_reports）")
    parser.add_argument("--period", type=int, default=250, help="分析周期天数（默认：250）")
    
    args = parser.parse_args()
    
    success_count, fail_count, results = batch_analyze(
        directory=args.dir,
        output_dir=args.output,
        period=args.period
    )
    
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
