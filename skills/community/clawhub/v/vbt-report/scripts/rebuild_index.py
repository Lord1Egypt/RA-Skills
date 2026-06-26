#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
扫描 D:\nginx\work\vbtr 根目录中所有 *_vbt_report.html 文件，从每个报告提取数据，生成统一索引页。
不递归子目录。
"""
import sys, os, warnings, io, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# batch_report.py 模块顶层会覆盖 sys.stdout，import 后必须重新设置
from batch_report import classify_signal, SIGNAL_CATS, SIGNAL_ORDER, parse_report_snapshot, gen_index_html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np


def scan_vbtr_reports(base_dir):
    """扫描 base_dir 根目录（不递归子目录），收集所有 *_vbt_report.html 报告文件"""
    all_stocks = {}

    for f in os.listdir(base_dir):
        if not f.endswith('_vbt_report.html'):
            continue

        file_path = os.path.join(base_dir, f)
        if not os.path.isfile(file_path):
            continue

        # 解析代码和名称: "000001_平安银行_vbt_report.html"
        parts = f.replace('_vbt_report.html', '').split('_', 1)
        if len(parts) < 1:
            continue
        code = parts[0]
        name = parts[1] if len(parts) > 1 else ''

        all_stocks[code] = {
            'code': code,
            'name': name,
            'report_file': f,
            'success': True,
        }

    # 按代码排序
    result = sorted(all_stocks.values(), key=lambda x: x['code'])
    print(f"扫描到 {len(result)} 个报告文件")
    return result


def extract_from_all_reports(stocks, base_dir):
    """从所有报告文件中提取回测数据"""
    for st in stocks:
        report_path = os.path.join(base_dir, st['report_file'])
        best_name, best_ret, best_ret_val, best_wr, best_sharpe, best_mdd, vbt_verdict, vbt_vcolor = parse_report_snapshot(report_path)
        st['best_name'] = best_name
        st['best_ret'] = best_ret
        st['best_ret_val'] = best_ret_val
        st['best_wr'] = best_wr
        st['best_sharpe'] = best_sharpe
        st['best_mdd'] = best_mdd
        st['vbt_verdict'] = vbt_verdict
        st['vbt_vcolor'] = vbt_vcolor
        st['signal'] = ''
        st['score'] = 0
    return stocks


if __name__ == '__main__':
    base_dir = r'D:\nginx\work\vbtr'

    print(f"扫描目录: {base_dir}")
    stocks = scan_vbtr_reports(base_dir)
    print(f"提取数据中...")
    stocks = extract_from_all_reports(stocks, base_dir)

    # 统计
    success = sum(1 for s in stocks if s.get('success'))
    print(f"成功提取: {success}/{len(stocks)}")

    # 生成索引页
    gen_index_html(stocks, base_dir)
    print(f"\n索引页已更新: {os.path.join(base_dir, 'index.html')}")
