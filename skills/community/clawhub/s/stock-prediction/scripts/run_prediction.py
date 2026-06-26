#!/usr/bin/env python3
"""
执行批量预测脚本
"""
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime

PREDICT_DIR = r"C:\Users\Administrator\Desktop\kronos\kronos-ai"
CONDA_ENV = "my_project_env"


def run_prediction(start_date: str, samples: int, output_dir: str):
    """
    执行批量预测
    
    Args:
        start_date: 预测开始日期 (YYYY-MM-DD)
        samples: 采样次数
        output_dir: 输出目录（用于查找输入文件）
    """
    # 构建命令
    cmd = f'conda activate {CONDA_ENV} && python .\\batch_predict.py --start_date {start_date} --samples {samples}'
    
    print(f"执行预测: {cmd}")
    print(f"工作目录: {PREDICT_DIR}")
    
    result = subprocess.run(
        ['powershell', '-Command', cmd],
        cwd=PREDICT_DIR,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"预测执行失败: {result.stderr}", file=sys.stderr)
        return False
    
    print(f"预测执行成功: {result.stdout}")
    return True


def get_prediction_result(output_dir: str, input_filename: str):
    """
    读取预测结果文件
    
    Args:
        output_dir: 输出目录
        input_filename: 输入文件名（如 143022.txt）
    
    Returns:
        结果文件内容
    """
    result_filename = f"result_{input_filename}"
    result_path = Path(output_dir) / result_filename
    
    if not result_path.exists():
        raise FileNotFoundError(f"结果文件不存在: {result_path}")
    
    content = result_path.read_text(encoding='utf-8')
    
    if not content.strip():
        raise ValueError(f"结果文件为空: {result_path}")
    
    return content


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='执行股票批量预测')
    parser.add_argument('--start_date', required=True, help='预测开始日期 (YYYY-MM-DD)')
    parser.add_argument('--samples', type=int, required=True, help='采样次数')
    parser.add_argument('--output_dir', required=True, help='输出目录')
    parser.add_argument('--input_file', required=True, help='输入文件名')
    
    args = parser.parse_args()
    
    # 执行预测
    success = run_prediction(args.start_date, args.samples, args.output_dir)
    
    if not success:
        sys.exit(1)
    
    # 读取结果
    try:
        result = get_prediction_result(args.output_dir, args.input_file)
        print("\n===== 预测结果 =====")
        print(result)
        print("===================")
    except Exception as e:
        print(f"读取结果失败: {e}", file=sys.stderr)
        sys.exit(1)
