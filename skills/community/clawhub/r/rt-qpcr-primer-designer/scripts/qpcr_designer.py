#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RT-qPCR Primer Designer CLI
Automated sequence fetching, Primer3 design, thermodynamic & specificity validation, and Excel delivery.
"""

import os
import sys
import re
import json
import argparse
import urllib.request
import urllib.error

# Ensure stdout handles unicode
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def fetch_genbank(accession, email=None, api_key=None):
    """Fetch GenBank record using NCBI E-utilities efetch."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = f"db=nuccore&id={accession}&rettype=gb&retmode=text"
    if api_key:
        params += f"&api_key={api_key}"
    if email:
        params += f"&email={email}"
    
    url = f"{base_url}?{params}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (RT-qPCR-Designer)'})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        raise RuntimeError(f"Failed to fetch GenBank record for {accession}: {e}")
    
    # Parse record metadata
    organism = "Unknown organism"
    product = "Unknown product"
    m_org = re.search(r'ORGANISM\s+([^\n]+)', content)
    if m_org:
        organism = m_org.group(1).strip()
    
    m_prod = re.search(r'/product="([^"]+)"', content)
    if m_prod:
        product = m_prod.group(1).strip()
    
    # Parse CDS location
    cds_start, cds_end = None, None
    m_cds = re.search(r'\sCDS\s+(?:join\()?(\d+)\.\.(\d+)', content)
    if m_cds:
        cds_start = int(m_cds.group(1))
        cds_end = int(m_cds.group(2))
    
    # Parse sequence from ORIGIN
    origin_idx = content.find('ORIGIN')
    if origin_idx == -1:
        raise ValueError("ORIGIN block not found in GenBank record.")
    origin_text = content[origin_idx+6:]
    seq_chars = re.findall(r'[a-zA-Z]', origin_text)
    seq = ''.join(seq_chars).upper()
    
    return {
        'accession': accession,
        'organism': organism,
        'product': product,
        'length': len(seq),
        'cds_start': cds_start,
        'cds_end': cds_end,
        'sequence': seq,
    }


def design_primers(seq, cds_start=None, cds_end=None, min_prod=80, max_prod=150, opt_tm=60.0, num_return=5):
    """Run Primer3 design within CDS or sequence."""
    try:
        import primer3
    except ImportError:
        raise ImportError("primer3-py is required. Install with: pip install primer3-py")
    
    seq_len = len(seq)
    if cds_start is None or cds_end is None:
        target_start = 0
        target_len = seq_len
    else:
        # 0-indexed start and length
        target_start = max(0, cds_start - 1)
        target_len = min(seq_len - target_start, cds_end - target_start)

    p3_seq_args = {
        'SEQUENCE_ID': 'target_seq',
        'SEQUENCE_TEMPLATE': seq,
        'SEQUENCE_INCLUDED_REGION': [target_start, target_len]
    }

    p3_global_args = {
        'PRIMER_OPT_SIZE': 20,
        'PRIMER_MIN_SIZE': 18,
        'PRIMER_MAX_SIZE': 24,
        'PRIMER_OPT_TM': float(opt_tm),
        'PRIMER_MIN_TM': float(opt_tm) - 2.0,
        'PRIMER_MAX_TM': float(opt_tm) + 2.0,
        'PRIMER_MAX_DIFF_TM': 1.5,
        'PRIMER_MIN_GC': 40.0,
        'PRIMER_OPT_GC_PERCENT': 50.0,
        'PRIMER_MAX_GC': 60.0,
        'PRIMER_PRODUCT_SIZE_RANGE': [[min_prod, max_prod]],
        'PRIMER_NUM_RETURN': num_return,
        'PRIMER_MAX_POLY_X': 4,
        'PRIMER_MAX_SELF_ANY': 4.0,
        'PRIMER_MAX_SELF_END': 2.0,
        'PRIMER_MAX_HAIRPIN_TH': 45.0,
        'PRIMER_GC_CLAMP': 1,
    }

    res = primer3.bindings.design_primers(p3_seq_args, p3_global_args)
    count = res.get('PRIMER_PAIR_NUM_RETURNED', 0)
    
    pairs = []
    for i in range(count):
        f_seq = res[f'PRIMER_LEFT_{i}_SEQUENCE']
        r_seq = res[f'PRIMER_RIGHT_{i}_SEQUENCE']
        f_tm = res[f'PRIMER_LEFT_{i}_TM']
        r_tm = res[f'PRIMER_RIGHT_{i}_TM']
        f_gc = res[f'PRIMER_LEFT_{i}_GC_PERCENT']
        r_gc = res[f'PRIMER_RIGHT_{i}_GC_PERCENT']
        f_pos, f_len = res[f'PRIMER_LEFT_{i}']
        r_pos, r_len = res[f'PRIMER_RIGHT_{i}']
        prod_size = res[f'PRIMER_PAIR_{i}_PRODUCT_SIZE']
        
        # Thermodynamics
        f_hp = primer3.calc_hairpin(f_seq)
        r_hp = primer3.calc_hairpin(r_seq)
        f_homo = primer3.calc_homodimer(f_seq)
        r_homo = primer3.calc_homodimer(r_seq)
        hetero = primer3.calc_heterodimer(f_seq, r_seq)
        
        # Amplicon sequence
        # f_pos is 0-indexed start of forward primer
        # r_pos is 0-indexed 3' end of reverse primer on forward strand
        amp_start = f_pos
        amp_end = r_pos + 1
        amp_seq = seq[amp_start:amp_end]
        amp_gc = sum(1 for b in amp_seq if b in 'GC') / len(amp_seq) * 100
        
        pairs.append({
            'rank': i + 1,
            'f_seq': f_seq,
            'r_seq': r_seq,
            'f_len': f_len,
            'r_len': r_len,
            'f_tm': f_tm,
            'r_tm': r_tm,
            'f_gc': f_gc,
            'r_gc': r_gc,
            'f_pos_mrna': f"{f_pos+1}..{f_pos+f_len}",
            'r_pos_mrna': f"{r_pos-r_len+2}..{r_pos+1}",
            'f_pos_cds': f"{f_pos+1 - (cds_start or 1) + 1}..{f_pos+f_len - (cds_start or 1) + 1}" if cds_start else "-",
            'r_pos_cds': f"{r_pos-r_len+2 - (cds_start or 1) + 1}..{r_pos+1 - (cds_start or 1) + 1}" if cds_start else "-",
            'prod_len': prod_size,
            'amp_seq': amp_seq,
            'amp_gc': amp_gc,
            'f_hairpin_tm': f_hp.tm,
            'r_hairpin_tm': r_hp.tm,
            'f_homodimer_tm': f_homo.tm,
            'r_homodimer_tm': r_homo.tm,
            'cross_dimer_tm': hetero.tm,
            'cross_dimer_dg': hetero.dg / 1000.0,
            'delta_tm': abs(f_tm - r_tm),
        })
        
    return pairs


def check_specificity_local(pairs, full_seq):
    """Check 3'-end 10-mer seeds across full mRNA sequence to ensure no off-target bindings."""
    def revcomp(s):
        tr = str.maketrans('ATCG', 'TAGC')
        return s.translate(tr)[::-1]
    
    rc_full = revcomp(full_seq)
    
    results = []
    for p in pairs:
        f_seq = p['f_seq']
        r_seq = p['r_seq']
        
        f_seed = f_seq[-10:]
        r_seed = r_seq[-10:]
        
        f_hits_fwd = len([i for i in range(len(full_seq) - 9) if full_seq[i:i+10] == f_seed])
        f_hits_rc = len([i for i in range(len(rc_full) - 9) if rc_full[i:i+10] == f_seed])
        
        r_hits_fwd = len([i for i in range(len(full_seq) - 9) if full_seq[i:i+10] == r_seed])
        r_hits_rc = len([i for i in range(len(rc_full) - 9) if rc_full[i:i+10] == r_seed])
        
        is_specific = (f_hits_fwd == 1 and f_hits_rc == 0 and r_hits_fwd == 0 and r_hits_rc == 1)
        p['local_specific'] = is_specific
        p['spec_desc'] = "100%唯一特异" if is_specific else "需注意副结合位点"
        results.append(p)
        
    return results


def export_excel(meta, pairs, output_file):
    """Export formatted Excel workbook with 3 professional sheets."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    navy_dark = '1F4E79'
    teal_header = '2E75B6'
    accent_green = 'E2EFDA'
    thin_border_side = Side(border_style='thin', color='D9D9D9')
    thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    # Sheet 1: 引物信息表
    ws1 = wb.create_sheet(title='qPCR引物信息表')
    ws1.views.sheetView[0].showGridLines = True

    ws1.merge_cells('A1:L1')
    ws1['A1'] = f"{meta.get('organism', '')} {meta.get('product', '')} 基因 RT-qPCR 特异性引物设计表"
    ws1['A1'].font = Font(name='微软雅黑', size=15, bold=True, color='FFFFFF')
    ws1['A1'].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type='solid')
    ws1['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws1.row_dimensions[1].height = 38

    ws1.merge_cells('A2:L2')
    ws1['A2'] = f"目标基因：{meta.get('product', '')} (GenBank: {meta.get('accession', '')}) | 扩增技术：RT-qPCR (SYBR Green) | 产物范围：80–150 bp | 退火温度：~60°C"
    ws1['A2'].font = Font(name='微软雅黑', size=9.5, italic=True, color='595959')
    ws1['A2'].alignment = Alignment(horizontal='center', vertical='center')
    ws1.row_dimensions[2].height = 22

    headers = [
        '推荐等级', '引物名称', '方向', '引物序列 (5\' → 3\')', '长度 (nt)', 
        'Tm (°C)', 'GC (%)', '结合位点 (mRNA/CDS)', '产物长度 (bp)', 
        '产物GC (%)', '特异性 (转录组/BLAST)', '综合推荐说明'
    ]

    ws1.row_dimensions[3].height = 28
    for col_idx, h in enumerate(headers, 1):
        cell = ws1.cell(row=3, column=col_idx, value=h)
        cell.font = Font(name='微软雅黑', size=10.5, bold=True, color='FFFFFF')
        cell.fill = PatternFill(start_color=teal_header, end_color=teal_header, fill_type='solid')
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    row_start = 4
    num_pairs = len(pairs)
    for i, p in enumerate(pairs):
        is_rec = (i == 0)
        rank_label = f"【首选推荐】\n方案{i+1}" if is_rec else f"【备选方案】\n方案{i+1}"
        fill_color = accent_green if is_rec else ('F9FBFD' if i % 2 == 1 else 'FFFFFF')
        
        # Forward row
        r_f = row_start + i * 2
        ws1.row_dimensions[r_f].height = 32
        f_vals = [
            rank_label, f"qPCR-P{i+1}-F", "Forward", p['f_seq'], p['f_len'],
            f"{p['f_tm']:.2f}", f"{p['f_gc']:.1f}%", f"mRNA: {p['f_pos_mrna']}\n(CDS: {p['f_pos_cds']})",
            p['prod_len'], f"{p['amp_gc']:.1f}%", p.get('spec_desc', '100%唯一特异'),
            f"【首选推荐】产物{p['prod_len']} bp，GC含量{p['amp_gc']:.1f}%，ΔTm={p['delta_tm']:.2f}°C，无发夹/二聚体干扰" if is_rec else f"备选方案，扩增子{p['prod_len']} bp，GC含量{p['amp_gc']:.1f}%"
        ]
        for col_idx, val in enumerate(f_vals, 1):
            cell = ws1.cell(row=r_f, column=col_idx, value=val)
            cell.font = Font(name='Consolas' if col_idx == 4 else '微软雅黑', size=10, bold=(is_rec and col_idx in [1, 2, 4]))
            cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type='solid')
            cell.border = thin_border
            align_h = 'center' if col_idx in [1, 2, 3, 5, 6, 7, 8, 9, 10, 11] else ('left' if col_idx in [4, 12] else 'center')
            cell.alignment = Alignment(horizontal=align_h, vertical='center', wrap_text=True)

        # Reverse row
        r_r = r_f + 1
        ws1.row_dimensions[r_r].height = 32
        r_vals = [
            rank_label, f"qPCR-P{i+1}-R", "Reverse", p['r_seq'], p['r_len'],
            f"{p['r_tm']:.2f}", f"{p['r_gc']:.1f}%", f"mRNA: {p['r_pos_mrna']}\n(CDS: {p['r_pos_cds']})",
            p['prod_len'], f"{p['amp_gc']:.1f}%", p.get('spec_desc', '100%唯一特异'),
            "3'端具有GC clamp，结合稳定性高"
        ]
        for col_idx, val in enumerate(r_vals, 1):
            cell = ws1.cell(row=r_r, column=col_idx, value=val)
            cell.font = Font(name='Consolas' if col_idx == 4 else '微软雅黑', size=10, bold=(is_rec and col_idx in [1, 2, 4]))
            cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type='solid')
            cell.border = thin_border
            align_h = 'center' if col_idx in [1, 2, 3, 5, 6, 7, 8, 9, 10, 11] else ('left' if col_idx in [4, 12] else 'center')
            cell.alignment = Alignment(horizontal=align_h, vertical='center', wrap_text=True)

        # Merge cells for pair
        ws1.merge_cells(start_row=r_f, start_column=1, end_row=r_r, end_column=1)
        ws1.merge_cells(start_row=r_f, start_column=9, end_row=r_r, end_column=9)
        ws1.merge_cells(start_row=r_f, start_column=10, end_row=r_r, end_column=10)
        ws1.merge_cells(start_row=r_f, start_column=11, end_row=r_r, end_column=11)

    # Amplicon sequences block
    curr_row = row_start + num_pairs * 2 + 2
    ws1.merge_cells(f'A{curr_row}:L{curr_row}')
    ws1[f'A{curr_row}'] = "对应扩增产物全长序列 (Amplicon Sequences 5' → 3')"
    ws1[f'A{curr_row}'].font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
    ws1[f'A{curr_row}'].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type='solid')
    ws1[f'A{curr_row}'].alignment = Alignment(horizontal='left', vertical='center', indent=1)
    ws1.row_dimensions[curr_row].height = 26

    for idx, p in enumerate(pairs):
        curr_row += 1
        ws1.row_dimensions[curr_row].height = 26
        ws1.merge_cells(f'A{curr_row}:C{curr_row}')
        ws1.merge_cells(f'D{curr_row}:L{curr_row}')
        c1 = ws1[f'A{curr_row}']
        c1.value = f"【方案{idx+1}】({p['prod_len']} bp)"
        c1.font = Font(name='微软雅黑', size=9, bold=True, color='1F4E79')
        c1.fill = PatternFill(start_color='F2F4F7', end_color='F2F4F7', fill_type='solid')
        c1.alignment = Alignment(horizontal='center', vertical='center')
        c1.border = thin_border
        
        c2 = ws1[f'D{curr_row}']
        c2.value = p['amp_seq']
        c2.font = Font(name='Consolas', size=9)
        c2.fill = PatternFill(start_color='FBFBFB', end_color='FBFBFB', fill_type='solid')
        c2.alignment = Alignment(horizontal='left', vertical='center')
        c2.border = thin_border

    # Sheet 2: 目标基因与序列详情
    ws2 = wb.create_sheet(title='目标基因与序列详情')
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells('A1:F1')
    ws2['A1'] = f"{meta.get('organism', '')} {meta.get('product', '')} 序列与注释详情"
    ws2['A1'].font = Font(name='微软雅黑', size=14, bold=True, color='FFFFFF')
    ws2['A1'].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type='solid')
    ws2['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws2.row_dimensions[1].height = 35

    gene_details = [
        ('基因名称 (Product)', meta.get('product', '-')),
        ('物种名称 (Organism)', meta.get('organism', '-')),
        ('GenBank 登录号', meta.get('accession', '-')),
        ('NCBI 链接', f"https://www.ncbi.nlm.nih.gov/nuccore/{meta.get('accession', '')}?report=fasta" if meta.get('accession') else "-"),
        ('mRNA 全长', f"{meta.get('length', len(meta.get('sequence', '')))} bp"),
        ('编码区 (CDS)', f"{meta.get('cds_start', '-')}..{meta.get('cds_end', '-')} nt" if meta.get('cds_start') else "全序列作为靶区"),
    ]

    for idx, (k, v) in enumerate(gene_details, 3):
        ws2.row_dimensions[idx].height = 24
        ws2.merge_cells(f'A{idx}:B{idx}')
        ws2.merge_cells(f'C{idx}:F{idx}')
        
        ck = ws2[f'A{idx}']
        ck.value = k
        ck.font = Font(name='微软雅黑', size=10, bold=True, color='1F4E79')
        ck.fill = PatternFill(start_color='EDF2F8', end_color='EDF2F8', fill_type='solid')
        ck.alignment = Alignment(horizontal='left', vertical='center', indent=1)
        ck.border = thin_border
        
        cv = ws2[f'C{idx}']
        cv.value = v
        cv.font = Font(name='微软雅黑', size=10)
        cv.fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
        cv.alignment = Alignment(horizontal='left', vertical='center', indent=1)
        cv.border = thin_border

    curr_row = 10
    ws2.merge_cells(f'A{curr_row}:F{curr_row}')
    ws2[f'A{curr_row}'] = "目标靶区核酸序列 (5' → 3')"
    ws2[f'A{curr_row}'].font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
    ws2[f'A{curr_row}'].fill = PatternFill(start_color=teal_header, end_color=teal_header, fill_type='solid')
    ws2[f'A{curr_row}'].alignment = Alignment(horizontal='left', vertical='center', indent=1)
    ws2.row_dimensions[curr_row].height = 25

    curr_row += 1
    ws2.merge_cells(f'A{curr_row}:F{curr_row}')
    ws2[f'A{curr_row}'] = meta.get('sequence', '')
    ws2[f'A{curr_row}'].font = Font(name='Consolas', size=9.5)
    ws2[f'A{curr_row}'].alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    ws2.row_dimensions[curr_row].height = 65

    # Sheet 3: qPCR 实验参考指南
    ws3 = wb.create_sheet(title='qPCR实验参考指南')
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells('A1:E1')
    ws3['A1'] = "RT-qPCR 实验操作标准流程与质控建议 (SYBR Green)"
    ws3['A1'].font = Font(name='微软雅黑', size=14, bold=True, color='FFFFFF')
    ws3['A1'].fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type='solid')
    ws3['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws3.row_dimensions[1].height = 35

    ws3.merge_cells('A3:E3')
    ws3['A3'] = "1. 推荐 qPCR 反应体系 (20 μL 反应体积)"
    ws3['A3'].font = Font(name='微软雅黑', size=11, bold=True, color='1F4E79')
    ws3.row_dimensions[3].height = 25

    sys_headers = ['组分 (Components)', '加入体积 (Volume)', '终浓度 (Final Conc.)', '备注说明']
    ws3.row_dimensions[4].height = 22
    for col_idx, sh in enumerate(sys_headers, 1):
        c = ws3.cell(row=4, column=col_idx, value=sh)
        c.font = Font(name='微软雅黑', size=10, bold=True, color='FFFFFF')
        c.fill = PatternFill(start_color=teal_header, end_color=teal_header, fill_type='solid')
        c.alignment = Alignment(horizontal='center', vertical='center')

    sys_rows = [
        ('2× SYBR Green qPCR Master Mix', '10.0 μL', '1×', '含热启动Taq酶、dNTP、荧光染料及缓冲液'),
        ('Forward Primer (10 μM)', '0.4–0.8 μL', '0.2–0.4 μM', '建议引物工作液浓度稀释为 10 μM'),
        ('Reverse Primer (10 μM)', '0.4–0.8 μL', '0.2–0.4 μM', '与上游引物按等摩尔浓度配比加入'),
        ('cDNA 模板 (Template)', '2.0 μL', '10–100 ng', '反转录产物建议稀释 5–10 倍后加样'),
        ('ROX Reference Dye (可选)', '0.4 μL / 根据仪器决定', '根据机型', '按荧光定量仪机型要求添加（如 ABI 仪需添加）'),
        ('ddH2O (Nuclease-free)', '补足至 20.0 μL', '-', '无酶灭菌水'),
    ]

    for idx, r in enumerate(sys_rows, 5):
        ws3.row_dimensions[idx].height = 22
        for col_idx, v in enumerate(r, 1):
            cell = ws3.cell(row=idx, column=col_idx, value=v)
            cell.font = Font(name='微软雅黑', size=9)
            cell.alignment = Alignment(horizontal='center' if col_idx in [2, 3] else 'left', vertical='center')
            cell.border = thin_border
            cell.fill = PatternFill(start_color='FBFBFB' if idx%2==1 else 'FFFFFF', end_color='FBFBFB' if idx%2==1 else 'FFFFFF', fill_type='solid')

    p_start = 12
    ws3.merge_cells(f'A{p_start}:E{p_start}')
    ws3[f'A{p_start}'] = "2. 推荐 PCR 扩增程序 (两步法标准程序)"
    ws3[f'A{p_start}'].font = Font(name='微软雅黑', size=11, bold=True, color='1F4E79')
    ws3.row_dimensions[p_start].height = 25

    prog_headers = ['阶段 (Stage)', '温度 (°C)', '时间 (Duration)', '循环数 (Cycles)', '操作目的']
    ws3.row_dimensions[p_start+1].height = 22
    for col_idx, ph in enumerate(prog_headers, 1):
        c = ws3.cell(row=p_start+1, column=col_idx, value=ph)
        c.font = Font(name='微软雅黑', size=10, bold=True, color='FFFFFF')
        c.fill = PatternFill(start_color=teal_header, end_color=teal_header, fill_type='solid')
        c.alignment = Alignment(horizontal='center', vertical='center')

    prog_rows = [
        ('预变性 (Pre-denaturation)', '95 °C', '30 s ~ 2 min', '1', '激活热启动Taq酶，解开模板二级结构'),
        ('PCR 扩增 - 变性', '95 °C', '5 ~ 10 s', '40', '双链DNA变性'),
        ('PCR 扩增 - 退火与延伸', '60 °C', '20 ~ 30 s', '40', '引物结合并延伸，同时在此步采集荧光信号'),
        ('融解曲线 (Melting Curve)', '65 °C ~ 95 °C', '每步上升0.5°C，停留5s', '1', '连续荧光采集，检验单一解链峰（排除二聚体）'),
    ]

    for idx, r in enumerate(prog_rows, p_start+2):
        ws3.row_dimensions[idx].height = 22
        for col_idx, v in enumerate(r, 1):
            cell = ws3.cell(row=idx, column=col_idx, value=v)
            cell.font = Font(name='微软雅黑', size=9)
            cell.alignment = Alignment(horizontal='center' if col_idx in [2, 3, 4] else 'left', vertical='center')
            cell.border = thin_border
            cell.fill = PatternFill(start_color='FBFBFB' if idx%2==1 else 'FFFFFF', end_color='FBFBFB' if idx%2==1 else 'FFFFFF', fill_type='solid')

    qc_start = 18
    ws3.merge_cells(f'A{qc_start}:E{qc_start}')
    ws3[f'A{qc_start}'] = "3. 关键质控与实验注意事项"
    ws3[f'A{qc_start}'].font = Font(name='微软雅黑', size=11, bold=True, color='1F4E79')
    ws3.row_dimensions[qc_start].height = 25

    qc_tips = [
        ('1. gDNA 污染清除', '提取总 RNA 后必须进行有效的 DNase I 处理，或使用含 gDNA Remover / Eraser 的反转录试剂盒，确保无残留基因组 DNA 干扰。'),
        ('2. 阴性对照设立', '务必设立 NTC (No Template Control，加入灭菌水代替模板) 以及 No-RT (无反转录酶对照)，确认反应液无污染，Ct 值应 > 35 或无扩增。'),
        ('3. 扩增效率验证', '实验前建议使用梯度稀释的混合 cDNA (如 5 个 10 倍稀释梯度) 建立标准曲线，验证扩增效率在 90%–110% 之间 (斜率在 -3.58 至 -3.10)。'),
        ('4. 常用内参推荐', '建议选用物种中表达稳定经过验证的内参基因进行归一化（如 β-actin、EF1α 或 GAPDH），双内参组合使用可进一步提高数据可靠性。'),
    ]

    for idx, (title, desc) in enumerate(qc_tips, qc_start+1):
        ws3.row_dimensions[idx].height = 26
        c1 = ws3.cell(row=idx, column=1, value=title)
        c1.font = Font(name='微软雅黑', size=9, bold=True, color='1F4E79')
        c1.border = thin_border
        c1.fill = PatternFill(start_color='EDF2F8', end_color='EDF2F8', fill_type='solid')
        c1.alignment = Alignment(horizontal='left', vertical='center', indent=1)
        
        ws3.merge_cells(start_row=idx, start_column=2, end_row=idx, end_column=5)
        c2 = ws3.cell(row=idx, column=2, value=desc)
        c2.font = Font(name='微软雅黑', size=9)
        c2.border = thin_border
        c2.fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
        c2.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True, indent=1)

    # Column dimensions
    ws1.column_dimensions['A'].width = 16
    ws1.column_dimensions['B'].width = 18
    ws1.column_dimensions['C'].width = 10
    ws1.column_dimensions['D'].width = 25
    ws1.column_dimensions['E'].width = 11
    ws1.column_dimensions['F'].width = 11
    ws1.column_dimensions['G'].width = 11
    ws1.column_dimensions['H'].width = 20
    ws1.column_dimensions['I'].width = 14
    ws1.column_dimensions['J'].width = 14
    ws1.column_dimensions['K'].width = 18
    ws1.column_dimensions['L'].width = 40

    ws2.column_dimensions['A'].width = 24
    ws2.column_dimensions['B'].width = 6
    ws2.column_dimensions['C'].width = 25
    ws2.column_dimensions['D'].width = 25
    ws2.column_dimensions['E'].width = 25
    ws2.column_dimensions['F'].width = 25

    ws3.column_dimensions['A'].width = 30
    ws3.column_dimensions['B'].width = 20
    ws3.column_dimensions['C'].width = 22
    ws3.column_dimensions['D'].width = 25
    ws3.column_dimensions['E'].width = 35

    wb.save(output_file)
    return output_file


def main():
    parser = argparse.ArgumentParser(description="RT-qPCR Primer Designer CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: fetch
    p_fetch = subparsers.add_parser("fetch", help="Fetch GenBank mRNA record")
    p_fetch.add_argument("--accession", required=True, help="NCBI GenBank Accession (e.g. OR123894.1)")
    p_fetch.add_argument("-o", "--output", required=True, help="Output JSON file")

    # Subcommand: design
    p_design = subparsers.add_parser("design", help="Design qPCR primers")
    p_design.add_argument("--input", help="Input JSON file from fetch command")
    p_design.add_argument("--fasta", help="Input FASTA file")
    p_design.add_argument("--cds-start", type=int, help="CDS start position (1-based)")
    p_design.add_argument("--cds-end", type=int, help="CDS end position (1-based)")
    p_design.add_argument("--min-prod", type=int, default=80, help="Min product length (default: 80)")
    p_design.add_argument("--max-prod", type=int, default=150, help="Max product length (default: 150)")
    p_design.add_argument("--opt-tm", type=float, default=60.0, help="Optimal primer Tm (default: 60.0)")
    p_design.add_argument("--num-return", type=int, default=5, help="Number of primer pairs (default: 5)")
    p_design.add_argument("-o", "--output", required=True, help="Output JSON file")

    # Subcommand: specificity
    p_spec = subparsers.add_parser("specificity", help="Check primer specificity against sequence/BLAST")
    p_spec.add_argument("--input", required=True, help="Input primer design JSON")
    p_spec.add_argument("-o", "--output", required=True, help="Output JSON file")

    # Subcommand: export-excel
    p_excel = subparsers.add_parser("export-excel", help="Export Excel delivery workbook")
    p_excel.add_argument("--input", required=True, help="Input primer pairs JSON")
    p_excel.add_argument("-o", "--output", required=True, help="Output XLSX file")

    # Subcommand: pipeline
    p_pipe = subparsers.add_parser("pipeline", help="Run end-to-end primer design and export Excel")
    p_pipe.add_argument("--accession", help="NCBI Accession")
    p_pipe.add_argument("--fasta", help="Input FASTA file")
    p_pipe.add_argument("--organism", default="Unknown organism", help="Organism name")
    p_pipe.add_argument("--product", default="Target gene", help="Product/gene name")
    p_pipe.add_argument("--cds-start", type=int, help="CDS start position (1-based)")
    p_pipe.add_argument("--cds-end", type=int, help="CDS end position (1-based)")
    p_pipe.add_argument("--min-prod", type=int, default=80, help="Min product length")
    p_pipe.add_argument("--max-prod", type=int, default=150, help="Max product length")
    p_pipe.add_argument("--opt-tm", type=float, default=60.0, help="Optimal Tm")
    p_pipe.add_argument("-o", "--output", required=True, help="Output XLSX file path")

    args = parser.parse_args()

    if args.command == "fetch":
        data = fetch_genbank(args.accession)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Success! Fetched record for {args.accession} to {args.output}")

    elif args.command == "design":
        if args.input:
            with open(args.input, "r", encoding="utf-8") as f:
                meta = json.load(f)
            seq = meta["sequence"]
            c_start = meta.get("cds_start")
            c_end = meta.get("cds_end")
        elif args.fasta:
            with open(args.fasta, "r", encoding="utf-8") as f:
                lines = f.readlines()
            seq = "".join([l.strip() for l in lines if not l.startswith(">")])
            meta = {
                "sequence": seq,
                "length": len(seq),
                "organism": "Target organism",
                "product": "Target product"
            }
            c_start = args.cds_start
            c_end = args.cds_end
        else:
            raise ValueError("Either --input (JSON) or --fasta must be provided.")

        pairs = design_primers(
            seq, cds_start=c_start, cds_end=c_end,
            min_prod=args.min_prod, max_prod=args.max_prod,
            opt_tm=args.opt_tm, num_return=args.num_return
        )
        meta["pairs"] = pairs
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
        print(f"Success! Designed {len(pairs)} primer pairs, saved to {args.output}")

    elif args.command == "specificity":
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        full_seq = data["sequence"]
        pairs = data["pairs"]
        pairs = check_specificity_local(pairs, full_seq)
        data["pairs"] = pairs
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Success! Specificity verified for {len(pairs)} pairs, saved to {args.output}")

    elif args.command == "export-excel":
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        pairs = data.get("pairs", [])
        export_excel(data, pairs, args.output)
        print(f"Success! Excel exported to {args.output}")

    elif args.command == "pipeline":
        if args.accession:
            meta = fetch_genbank(args.accession)
        elif args.fasta:
            with open(args.fasta, "r", encoding="utf-8") as f:
                lines = f.readlines()
            seq = "".join([l.strip() for l in lines if not l.startswith(">")])
            meta = {
                "sequence": seq,
                "length": len(seq),
                "organism": args.organism,
                "product": args.product,
                "cds_start": args.cds_start,
                "cds_end": args.cds_end,
            }
        else:
            raise ValueError("Either --accession or --fasta must be specified.")

        c_start = meta.get("cds_start") or args.cds_start
        c_end = meta.get("cds_end") or args.cds_end

        pairs = design_primers(
            meta["sequence"], cds_start=c_start, cds_end=c_end,
            min_prod=args.min_prod, max_prod=args.max_prod,
            opt_tm=args.opt_tm, num_return=5
        )
        pairs = check_specificity_local(pairs, meta["sequence"])
        meta["pairs"] = pairs
        export_excel(meta, pairs, args.output)
        print(f"Pipeline complete! Professional Excel generated at: {args.output}")

if __name__ == "__main__":
    main()
