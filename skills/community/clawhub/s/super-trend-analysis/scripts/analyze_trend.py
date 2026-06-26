#!/usr/bin/env python3
"""
单只股票趋势分析脚本
融合多种技术分析方法，生成趋势分析报告
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# 导入指标计算库
sys.path.insert(0, str(Path(__file__).parent))

try:
    import pandas as pd
    import numpy as np
    from indicators import (
        calculate_all_indicators,
        analyze_trend_signals,
        calculate_trend_score
    )
except ImportError as e:
    print(f"错误: 缺少必需的库: {e}")
    print("请运行: pip install pandas numpy")
    sys.exit(1)


def load_data(file_path: str) -> pd.DataFrame:
    """
    加载 CSV 数据文件
    
    Args:
        file_path: 文件路径
    
    Returns:
        DataFrame
    """
    try:
        df = pd.read_csv(file_path)
        
        # 尝试识别日期列
        date_columns = ['日期', 'Date', '交易时间', 'datetime']
        date_col = None
        for col in date_columns:
            if col in df.columns:
                date_col = col
                break
        
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.sort_values(date_col)
        
        return df
    except Exception as e:
        print(f"错误: 无法加载文件 {file_path}: {e}")
        sys.exit(1)


def detect_price_column(df: pd.DataFrame) -> str:
    """
    自动识别价格列
    
    Args:
        df: DataFrame
    
    Returns:
        价格列名
    """
    price_columns = ['收盘', 'Close', '收盘价', 'close']
    for col in price_columns:
        if col in df.columns:
            return col
    
    # 如果没有找到，返回第一列数值列
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        return numeric_cols[0]
    
    return df.columns[-1]


def generate_report(df: pd.DataFrame, signals: dict, score_data: dict, 
                   stock_name: str = "股票") -> str:
    """
    生成趋势分析报告（Markdown 格式）
    
    Args:
        df: 数据 DataFrame
        signals: 信号字典
        score_data: 评分数据
        stock_name: 股票名称
    
    Returns:
        Markdown 格式的报告
    """
    latest = df.iloc[-1]
    price_col = detect_price_column(df)
    
    report = []
    report.append(f"# 📊 超级趋势分析报告：{stock_name}")
    report.append("")
    report.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # 最新价格
    if price_col in df.columns:
        current_price = latest[price_col]
        report.append(f"**最新价格**: {current_price:.2f} 元")
        report.append("")
    
    # 综合评分
    report.append("## 🎯 综合趋势判断")
    report.append("")
    report.append(f"**趋势方向**: {score_data['trend_emoji']} {score_data['overall_trend']}")
    report.append(f"**综合评分**: {score_data['score']}/{score_data['max_score']} 分")
    report.append("")
    
    # 评分进度条
    score = score_data['score']
    bar_length = 50
    filled = int(score / 100 * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    report.append(f"[{bar}] {score}%")
    report.append("")
    
    # 各指标信号
    report.append("## 📈 技术指标分析")
    report.append("")
    
    report.append("### 移动平均线（MA）")
    report.append(f"- **信号**: {signals['ma_signal']}")
    report.append("")
    
    report.append("### MACD 指标")
    report.append(f"- **信号**: {signals['macd_signal']}")
    report.append("")
    
    report.append("### RSI 相对强弱指标")
    report.append(f"- **信号**: {signals['rsi_signal']}")
    report.append("")
    
    report.append("### 布林带（Bollinger Bands）")
    report.append(f"- **信号**: {signals['bb_signal']}")
    report.append("")
    
    # 操作建议
    report.append("## 💡 操作建议")
    report.append("")
    
    score = score_data['score']
    if score >= 70:
        report.append("✅ **建议**: 持有为主，可逢低加仓")
        report.append("- 趋势明确向上，顺势而为")
        report.append("- 关注支撑位，可作为买入参考")
    elif score >= 50:
        report.append("⚡ **建议**: 持有观望，等待明确信号")
        report.append("- 趋势中性，震荡为主")
        report.append("- 可做波段操作，高抛低吸")
    elif score >= 30:
        report.append("⚠️ **建议**: 谨慎操作，控制仓位")
        report.append("- 趋势偏弱，注意风险")
        report.append("- 反弹可减仓，破位止损")
    else:
        report.append("❌ **建议**: 观望为主，不要轻易抄底")
        report.append("- 下降趋势明显，顺势而为")
        report.append("- 等待底部信号出现再考虑")
    
    report.append("")
    
    # 数据概览
    report.append("## 📋 数据概览")
    report.append("")
    report.append(f"- **数据点数**: {len(df)} 条")
    if '日期' in df.columns:
        report.append(f"- **时间范围**: {df['日期'].iloc[0]} 至 {df['日期'].iloc[-1]}")
    report.append("")
    
    # 免责声明
    report.append("---")
    report.append("")
    report.append("⚠️ **免责声明**: 本分析仅供参考，不构成投资建议。")
    report.append("股市有风险，投资需谨慎！")
    
    return "\n".join(report)


def analyze_trend(file_path: str, stock_name: str = None, 
                 output_dir: str = "trend_reports", 
                 period: int = 250, plot: bool = False):
    """
    执行趋势分析
    
    Args:
        file_path: 数据文件路径
        stock_name: 股票名称
        output_dir: 输出目录
        period: 分析周期
        plot: 是否生成图表
    
    Returns:
        (成功标志, 报告文件路径)
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 从文件名提取股票名称
    if stock_name is None:
        file_name = Path(file_path).stem
        stock_name = file_name.split("_")[0] if "_" in file_name else file_name
    
    print("=" * 60)
    print(f"超级趋势分析：{stock_name}")
    print("=" * 60)
    
    # 加载数据
    print(f"\n正在加载数据: {file_path}")
    df = load_data(file_path)
    
    # 截取最近 N 天数据
    if len(df) > period:
        df = df.tail(period).copy()
        print(f"使用最近 {period} 天数据进行分析")
    
    print(f"数据加载完成，共 {len(df)} 条记录")
    
    # 计算技术指标
    print("\n正在计算技术指标...")
    price_col = detect_price_column(df)
    df_with_indicators = calculate_all_indicators(df, price_col)
    print("✓ 技术指标计算完成")
    
    # 分析趋势信号
    print("\n正在分析趋势信号...")
    signals = analyze_trend_signals(df_with_indicators)
    print("✓ 信号分析完成")
    
    # 计算综合评分
    print("\n正在计算综合评分...")
    score_data = calculate_trend_score(signals)
    print(f"✓ 综合评分: {score_data['score']}/{score_data['max_score']}")
    print(f"✓ 趋势判断: {score_data['trend_emoji']} {score_data['overall_trend']}")
    
    # 生成报告
    print("\n正在生成分析报告...")
    report = generate_report(df_with_indicators, signals, score_data, stock_name)
    
    # 保存报告
    report_file = output_path / f"{stock_name}_趋势分析_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✓ 报告已保存: {report_file}")
    
    # 控制台输出摘要
    print("\n" + "=" * 60)
    print("分析摘要")
    print("=" * 60)
    print(f"股票: {stock_name}")
    print(f"趋势: {score_data['trend_emoji']} {score_data['overall_trend']}")
    print(f"评分: {score_data['score']}/{score_data['max_score']}")
    print("")
    print(f"MA: {signals['ma_signal']}")
    print(f"MACD: {signals['macd_signal']}")
    print(f"RSI: {signals['rsi_signal']}")
    print(f"布林带: {signals['bb_signal']}")
    print("=" * 60)
    
    # 保存带指标的数据
    data_file = output_path / f"{stock_name}_技术指标.csv"
    df_with_indicators.to_csv(data_file, index=False, encoding="utf-8-sig")
    print(f"\n技术指标数据已保存: {data_file}")
    
    if plot:
        print("\n提示: 图表生成功能即将推出...")
    
    return True, str(report_file)


def main():
    parser = argparse.ArgumentParser(
        description="超级趋势分析 - 融合多种技术分析方法"
    )
    parser.add_argument("--file", required=True, help="CSV 数据文件路径")
    parser.add_argument("--name", help="股票名称（可选）")
    parser.add_argument("--output", default="trend_reports", help="输出目录（默认：trend_reports）")
    parser.add_argument("--period", type=int, default=250, help="分析周期天数（默认：250）")
    parser.add_argument("--plot", action="store_true", help="生成可视化图表（开发中）")
    
    args = parser.parse_args()
    
    success, report_file = analyze_trend(
        file_path=args.file,
        stock_name=args.name,
        output_dir=args.output,
        period=args.period,
        plot=args.plot
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
