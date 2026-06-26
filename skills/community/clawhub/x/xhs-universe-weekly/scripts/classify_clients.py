#!/usr/bin/env python3
"""
classify_clients.py - 广告主三类分层分析
用法: python3 classify_clients.py <zc_csv> <yu_csv> <output_json>

zc_csv: 整体种草投放情况 CSV (analysisId=42626327)
yu_csv: 广告主人群宇宙投放分析 CSV (analysisId=42623804)
"""
import csv, json, sys
import pandas as pd
import numpy as np

def read_csv_safe(path):
    rows = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return pd.DataFrame(rows)

def fmt_pct(v):
    if pd.isna(v): return '-'
    return f'{float(v)*100:.1f}%'

def fmt_wan(v):
    if pd.isna(v) or float(v) == 0: return '-'
    return f'{float(v)/10000:.2f}万'

def fmt_cost(v):
    if pd.isna(v): return '-'
    return f'{float(v):.1f}元'

def classify_clients(zc_path, yu_path, output_path):
    zc = read_csv_safe(zc_path)
    yu = read_csv_safe(yu_path)

    zc = zc[zc['广告主名称'] != '总计'].copy()
    yu = yu[yu['广告主名称'] != '总计'].copy()

    num_cols = ['策略消耗（复记）','CTR','I+TI转化率','淘宝进店率','淘宝进店成本']
    for c in num_cols:
        zc[c] = pd.to_numeric(zc[c], errors='coerce')
        yu[c] = pd.to_numeric(yu[c], errors='coerce')

    zc_k = zc[['广告主名称']+num_cols].copy()
    yu_k = yu[['广告主名称']+num_cols].copy()
    zc_k.columns = ['客户','zc_消耗','zc_CTR','zc_ITI','zc_进店率','zc_进店成本']
    yu_k.columns = ['客户','yu_消耗','yu_CTR','yu_ITI','yu_进店率','yu_进店成本']

    df = pd.merge(zc_k, yu_k, on='客户', how='left')
    df['有宇宙投放'] = df['yu_消耗'].notna() & (df['yu_消耗'] > 0)
    df['消耗渗透率'] = df.apply(
        lambda r: r['yu_消耗']/r['zc_消耗'] if r['有宇宙投放'] and r['zc_消耗'] > 0 else 0, axis=1)

    def judge_better(row):
        if not row['有宇宙投放']: return None
        score = 0
        if pd.notna(row['yu_进店率']) and pd.notna(row['zc_进店率']) and row['yu_进店率'] > row['zc_进店率']: score += 1
        if pd.notna(row['yu_ITI']) and pd.notna(row['zc_ITI']) and row['yu_ITI'] > row['zc_ITI']: score += 1
        return score >= 1

    df['宇宙效果好'] = df.apply(judge_better, axis=1)

    def classify(row):
        if not row['有宇宙投放']: return 'push_test'
        elif row['宇宙效果好'] == True: return 'push_scale'
        else: return 'track'

    df['类型'] = df.apply(classify, axis=1)

    type_map = {'push_test': 't1', 'push_scale': 't2', 'track': 't3'}
    result = {'t1': [], 't2': [], 't3': []}
    for _, r in df.sort_values('zc_消耗', ascending=False).iterrows():
        row = {
            '客户': r['客户'],
            '整体消耗': fmt_wan(r['zc_消耗']),
            '宇宙消耗': fmt_wan(r['yu_消耗']) if r['有宇宙投放'] else '未投放',
            '渗透率': f"{r['消耗渗透率']*100:.1f}%" if r['有宇宙投放'] else '-',
            'zc_CTR': fmt_pct(r['zc_CTR']), 'yu_CTR': fmt_pct(r['yu_CTR']) if r['有宇宙投放'] else '-',
            'zc_ITI': fmt_pct(r['zc_ITI']), 'yu_ITI': fmt_pct(r['yu_ITI']) if r['有宇宙投放'] else '-',
            'zc_进店率': fmt_pct(r['zc_进店率']), 'yu_进店率': fmt_pct(r['yu_进店率']) if r['有宇宙投放'] else '-',
            'zc_进店成本': fmt_cost(r['zc_进店成本']), 'yu_进店成本': fmt_cost(r['yu_进店成本']) if r['有宇宙投放'] else '-',
        }
        result[type_map[r['类型']]].append(row)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"类型一(未投放): {len(result['t1'])}个")
    print(f"类型二(效果好投入少): {len(result['t2'])}个")
    print(f"类型三(数据不及整体): {len(result['t3'])}个")
    print(f"结果已保存: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法: python3 classify_clients.py <zc_csv> <yu_csv> <output_json>")
        sys.exit(1)
    classify_clients(sys.argv[1], sys.argv[2], sys.argv[3])
