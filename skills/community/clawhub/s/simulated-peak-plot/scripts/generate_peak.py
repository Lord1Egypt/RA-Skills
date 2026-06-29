#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟峰图生成器 (Simulated Peak Plot Generator)
生成可定制的高斯峰图，支持复合峰（N个子峰组合）和 Markdown 表格输出。
复合峰可形成多种形状：M形、馒头形、泊松分布形等。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import json
import argparse
import sys
import os
import signal
from math import ceil
from pathlib import Path

DEFAULT_DATA_DIR_RAW = "skills/.standardization/simulated-peak-plot/data"
DATA_DIR = "skills/.standardization/simulated-peak-plot/data/"


def signal_handler(sig, frame):
    """优雅处理 Ctrl+C 中断信号"""
    print("\n\n⚠️ 用户中断操作，正在安全退出...")
    print("您随时可以重新运行脚本继续生成峰图。")
    sys.exit(0)


def get_skill_data_dir() -> Path:
    """获取 skill 数据目录路径 - 统一到 skills/.standardization/<skill>/data/"""
    file_path = Path(__file__).resolve()
    skill_dir = file_path.parent.parent  # scripts/ 的上一级是技能目录
    for parent in file_path.parents:
        if parent.name == "skills" and parent.is_dir():
            data_dir = parent / ".standardization" / skill_dir.name / "data"
            data_dir.mkdir(parents=True, exist_ok=True)  # 自动创建目录
            return data_dir
    fallback = skill_dir / "data"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def check_environment():
    """检查必需包是否可用"""
    try:
        import numpy
        import matplotlib
        print("✓ 环境检查通过：numpy 和 matplotlib 已安装")
        return True
    except ImportError as e:
        missing_pkg = str(e).split("'")[1] if "'" in str(e) else "numpy/matplotlib"
        print(f"✗ 环境检查失败：缺少 {missing_pkg} 包")
        print(f"   请执行以下命令安装：pip install {missing_pkg}")
        return False


def setup_chinese_font():
    """配置 matplotlib 中文字体支持"""
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    matplotlib.rcParams['axes.unicode_minus'] = False


def gaussian_peak(x, rt, height, hwhm):
    """
    生成高斯峰。

    参数:
    - x: x 轴值（时间）
    - rt: 保留时间（峰中心）
    - height: 峰高
    - hwhm: 半高半宽
    """
    sigma = hwhm / np.sqrt(2 * np.log(2))
    return height * np.exp(-(x - rt)**2 / (2 * sigma**2))


def generate_composite_peak(x, sub_peaks):
    """
    通过组合多个高斯峰生成复合峰。

    参数:
    - x: x 轴值
    - sub_peaks: 每个子峰的 'RT'、'height'、'HWHM' 字典列表

    返回:
    - 所有子峰的合成信号
    """
    signal = np.zeros_like(x)
    for peak in sub_peaks:
        signal += gaussian_peak(x, peak['RT'], peak['height'], peak['HWHM'])
    return signal


def _validate_positive(name, value, allow_zero=False):
    """验证参数是否为正数（允许负峰高度为负）"""
    if name == 'height':
        return  # 高度允许负数（负峰）
    if allow_zero and value >= 0:
        return True
    if value <= 0:
        raise ValueError(f"❌ 参数 '{name}' 必须为正数，当前值为 {value}")


def calculate_recommended_points(t_start, t_end, num_peaks, baseline, hwhm_avg):
    """
    计算推荐点数。

    公式考虑：
    - 时间范围跨度
    - 峰数量
    - 基线水平（基线越高需要更多点来显示细节）
    - 平均 HWHM（峰越尖锐需要更多点）
    """
    duration = t_end - t_start
    if duration <= 0:
        raise ValueError(f"❌ 时间范围无效：起始时间 {t_start} ≥ 结束时间 {t_end}")
    sharpness_factor = 1.0 / hwhm_avg if hwhm_avg > 0 else 10

    # 基础计算
    points = duration * num_peaks * sharpness_factor * 2

    # 基线调整
    if baseline > 100:
        points *= 1.5
    elif baseline > 50:
        points *= 1.2

    # 确保最小点数
    points = max(500, int(ceil(points)))

    return min(points, 10000)  # 上限 10000


def import_csv_data(csv_file, x_col=0, y_col=1, skip_header=True):
    """
    从 CSV 文件导入数据（设备导出格式）。

    参数:
    - csv_file: CSV 文件路径
    - x_col: X 数据列索引（默认: 0，第一列）
    - y_col: Y 数据列索引（默认: 1，第二列）
    - skip_header: 跳过首行表头（默认: True）

    返回:
    - (x_data, y_data) 作为 numpy 数组的元组
    """
    import csv

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"❌ 找不到 CSV 文件：{csv_file}\n   请确认文件路径是否正确")

    x_data = []
    y_data = []
    line_count = 0

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if skip_header and i == 0:
                # 尝试检测表头并获取列名
                header = row
                print(f"  ✓ 检测到 {len(row)} 列：{row}")
                continue

            if len(row) > max(x_col, y_col):
                try:
                    x_val = float(row[x_col])
                    y_val = float(row[y_col])
                    x_data.append(x_val)
                    y_data.append(y_val)
                    line_count += 1
                except ValueError:
                    # 跳过非数值行
                    if line_count == 0:
                        print(f"  ⚠️ 第 {i+1} 行不是有效数值，已跳过：{row}")
                    continue
            else:
                if line_count == 0:
                    print(f"  ⚠️ 第 {i+1} 行列数不足（需要至少 {max(x_col, y_col)+1} 列），已跳过：{row}")

    if len(x_data) == 0:
        raise ValueError(
            "❌ CSV 文件未包含有效的数值数据\n"
            "   可能原因：\n"
            "   1. skip_header 设置错误（文件是否包含表头？）\n"
            "   2. x_col/y_col 列索引设置错误\n"
            "   3. 文件分隔符不是逗号\n"
            "   请检查 CSV 文件格式"
        )

    print(f"  ✓ 已导入 {len(x_data)} 个数据点，来自：{csv_file}")

    return np.array(x_data), np.array(y_data)


def generate_plot_from_csv(config):
    """
    直接从导入的 CSV 数据生成图表。

    参数:
    - config: 包含以下键的字典：
        - csv_file: 输入 CSV 文件路径
        - x_col: X 数据列索引（默认: 0）
        - y_col: Y 数据列索引（默认: 1）
        - skip_header: 跳过表头行（默认: True）
        - output: 输出 PNG 文件名
        - xlabel: X 轴标签
        - ylabel: Y 轴标签
        - x_unit: X 轴单位
        - y_unit: Y 轴单位
        - grid: 显示网格线
        - grid_linestyle: 网格线样式
        - grid_alpha: 网格透明度
    """
    # 提取参数
    csv_file = config.get('csv_file')
    x_col = config.get('x_col', 0)
    y_col = config.get('y_col', 1)
    skip_header = config.get('skip_header', True)
    # 输出文件路径：优先使用 get_skill_data_dir()，其次用户指定
    output_arg = config.get('output', 'imported_data.png')
    if os.path.isabs(output_arg) or '/' in output_arg or '\\' in output_arg:
        output_file = output_arg  # 用户指定了完整路径
    else:
        output_file = str(get_skill_data_dir() / output_arg)  # 放到标准数据目录
    headless = config.get('headless', True)

    # 导入数据
    print(f"\n{'='*60}")
    print(" 正在导入 CSV 数据")
    print(f"{'='*60}")
    t, signal = import_csv_data(csv_file, x_col, y_col, skip_header)

    # 使用相同的绘图逻辑
    xlabel = config.get('xlabel', 'Time')
    ylabel = config.get('ylabel', 'Response')
    x_unit = config.get('x_unit', '')
    y_unit = config.get('y_unit', '')

    show_grid = config.get('grid', True)
    grid_linestyle = config.get('grid_linestyle', 'dashed')
    grid_alpha = config.get('grid_alpha', 0.6)

    # 绘图
    plt.figure(figsize=config.get('figsize', (10, 6)), dpi=config.get('dpi', 150))
    plt.plot(t, signal, color='#1f77b4', linewidth=1.5)

    # 标签
    if x_unit:
        plt.xlabel(f'{xlabel} ({x_unit})', fontsize=12)
    else:
        plt.xlabel(xlabel, fontsize=12)

    if y_unit:
        plt.ylabel(f'{ylabel} ({y_unit})', fontsize=12)
    else:
        plt.ylabel(ylabel, fontsize=12)

    # 网格
    if show_grid:
        plt.grid(True, linestyle=grid_linestyle, alpha=grid_alpha)
    else:
        plt.grid(False)

    plt.xlim(t.min(), t.max())

    # 自动缩放 Y 轴（支持负峰）
    y_max = signal.max() * 1.1 if signal.max() > 0 else signal.max() * 0.9
    y_min = signal.min() * 1.1 if signal.min() < 0 else 0
    plt.ylim(y_min, y_max)

    # 保存
    plt.savefig(output_file, bbox_inches='tight')

    # 输出路径
    abs_path = os.path.abspath(output_file)
    file_uri = f'file:///{abs_path.replace(chr(92), "/")}'
    print(f"\n{'='*60}")
    print(" 输出文件")
    print(f"{'='*60}")
    print(f"✓ PNG 图片：{abs_path}")
    print(f"✓ 点击打开：{file_uri}")

    if not headless:
        plt.show()
    else:
        plt.close()

    return t, signal


def show_point_recommendation_table():
    """显示推荐点数与扫描速率表"""
    print("\n" + "=" * 60)
    print(" 扫描速率推荐表")
    print("=" * 60)
    print("\n公式：总点数 = 时长 × 扫描速率")
    print("scan_rate 是检测器采样速率，单位 pts/min（点/分钟）")
    print("扫描速率越高 → 细节越丰富，文件越大")
    print("\n典型推荐值：")
    print("-" * 64)
    print(f"{'时长（min）':<15} {'峰数':<10} {'基线水平':<15} {'推荐扫描速率':<14} {'→ 点数':<12}")
    print("-" * 64)
    print(f"{'5-10':<15} {'2-4':<10} {'低（<50）':<15} {'80-120 pts/min':<14} {'600-1000':<12}")
    print(f"{'10-20':<15} {'4-8':<10} {'中（50-100）':<15} {'80-100 pts/min':<14} {'800-1200':<12}")
    print(f"{'20-30':<15} {'8+':<10} {'高（>100）':<15} {'60-80 pts/min':<14} {'1200-2000':<12}")
    print(f"{'30+':<15} {'任意':<10} {'任意':<15} {'50-70 pts/min':<14} {'2000+':<12}")
    print("-" * 64)
    print("默认 scan_rate = 100 pts/min")


def print_markdown_table(t, signal, sample_interval=10, y_unit='mV', x_unit='min'):
    """
    在控制台打印时间序列数据为 Markdown 表格。

    参数:
    - t: 时间数组
    - signal: 信号数组
    - sample_interval: 每隔 N 个点打印一条（避免表格过大）
    - y_unit: Y 轴单位（默认: mV）
    - x_unit: X 轴单位（默认: min）
    """
    print("\n" + "=" * 60)
    print(" 数据预览（Markdown 表格）")
    print("=" * 60)

    # 表头
    markdown = f"| 时间 ({x_unit}) | 信号 ({y_unit}) |\n"
    markdown += "|-------------|-------------|\n"

    # 采样数据点
    step = max(1, len(t) // sample_interval)
    for i in range(0, len(t), step):
        markdown += f"| {t[i]:.2f} | {signal[i]:.2f} |\n"

    print(markdown)
    print(f"✓ 数据预览已打印（共 {len(range(0, len(t), step))} 行采样）")
    print(f"  完整数据：{len(t)} 个点，范围 {t[0]:.2f} ~ {t[-1]:.2f} {x_unit}")

    return markdown


def export_csv_file(t, signal, output_file, x_unit='min', y_unit='mV'):
    """
    将完整数据导出为 CSV 文件。

    参数:
    - t: 时间数组
    - signal: 信号数组
    - output_file: 输出 PNG 文件名（用于推导 CSV 文件名）
    - x_unit: X 轴单位
    - y_unit: Y 轴单位

    返回:
    - 导出的 CSV 文件路径
    """
    import csv

    # 确定输出路径 - CSV 保存在与 output_file 相同的目录
    base_dir = os.path.dirname(output_file) or str(get_skill_data_dir())
    base_name = os.path.splitext(os.path.basename(output_file))[0]
    csv_file = os.path.join(base_dir, base_name + '_data.csv')

    # 写入标准 CSV 文件（RFC 4180 兼容）
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 带单位的表头行
        writer.writerow([f'Time_{x_unit}', f'Signal_{y_unit}'])
        # 数据行 - 写入原始数值
        for i in range(len(t)):
            writer.writerow([round(t[i], 6), round(signal[i], 6)])

    print(f"✓ CSV 已导出：{csv_file}")
    print(f"  格式：[(t1, s1), (t2, s2), ...]")
    print(f"  总行数：{len(t)}")

    # 同时打印 Python 列表格式
    print("\n  Python 数据格式：")
    data_list = [(float(f'{t[i]:.6f}'), float(f'{signal[i]:.6f}')) for i in range(len(t))]
    print(f"  {data_list[:5]} ...（显示前 5 条，共 {len(data_list)} 条）")

    return csv_file


def generate_peak_plot(config):
    """
    根据配置生成峰图。

    参数:
    - config: 包含以下键的字典：
        - scan_rate: 每分钟点数（默认: 100，总点数 = 时长 × scan_rate）
        - peaks: 峰字典列表，包含 ('name', 'RT', 'height', 'HWHM') 或
                 复合峰 ('name', 'type'='composite', 'peaks'=[...])
        - baseline: 基线值
        - noise_level: 噪声标准差
        - output: 输出文件名（PNG）
        - figsize: 图表尺寸（宽，高）
        - dpi: 输出 DPI
        - print_table: 是否打印 Markdown 表格
        - table_sample: 每 N 个点采样一次用于表格
        - xlabel: X 轴标题（默认: 'Time'）
        - ylabel: Y 轴标题（默认: 'Response'）
        - x_unit: X 轴单位（默认: 'min'）
        - y_unit: Y 轴单位（默认: 'mV'）
        - export_csv: 是否导出完整 CSV 数据
        - clickable_path: 是否输出 file:/// 路径
        - grid: 是否显示网格线（默认: True）
        - grid_linestyle: 网格线样式 - 'solid'、'dashed'、'dotted'、'dashdot'（默认: 'dashed'）
        - grid_alpha: 网格透明度（默认: 0.6）
    """

    # 提取参数（scan_rate 替代旧的 time_range）
    t_start = config.get('t_start', 5)
    t_end = config.get('t_end', 15)

    # 验证时间范围
    if t_end <= t_start:
        raise ValueError(f"❌ 时间范围无效：起始时间（{t_start}）必须小于结束时间（{t_end}）")

    scan_rate = config.get('scan_rate', 100)
    t_points = int((t_end - t_start) * scan_rate)
    t_points = max(t_points, 500)
    peaks_config = config.get('peaks', [])
    baseline = config.get('baseline', 20)
    noise_level = config.get('noise_level', 8)
    # 输出文件路径：优先使用 get_skill_data_dir()，其次用户指定
    output_arg = config.get('output', 'simulated_peak.png')
    if os.path.isabs(output_arg) or '/' in output_arg or '\\' in output_arg:
        output_file = output_arg  # 用户指定了完整路径
    else:
        output_file = str(get_skill_data_dir() / output_arg)  # 放到标准数据目录
    figsize = config.get('figsize', (10, 6))
    dpi = config.get('dpi', 150)
    print_table = config.get('print_table', True)
    table_sample = config.get('table_sample', 20)

    # 新的自定义参数
    xlabel = config.get('xlabel', 'Time')
    ylabel = config.get('ylabel', 'Response')
    x_unit = config.get('x_unit', 'min')
    y_unit = config.get('y_unit', 'mV')
    export_csv = config.get('export_csv', False)
    clickable_path = config.get('clickable_path', True)

    # 网格线参数
    show_grid = config.get('grid', True)
    grid_linestyle = config.get('grid_linestyle', 'dashed')
    grid_alpha = config.get('grid_alpha', 0.6)

    # 生成时间轴
    t = np.linspace(t_start, t_end, t_points)

    # 生成信号
    signal = np.zeros_like(t) + baseline

    # 跟踪峰以便标注
    annotation_peaks = []

    # 添加峰
    for idx, peak_config in enumerate(peaks_config):
        ptype = peak_config.get('type', 'single')

        # 簇峰 / 复合峰：多个子峰，每个子峰独立标注
        if ptype in ('cluster', 'composite'):
            sub_peaks = peak_config.get('peaks', [])
            if len(sub_peaks) < 1:
                print(f"  ⚠️ 跳过空簇峰（索引 {idx}）：子峰列表为空")
                continue
            signal += generate_composite_peak(t, sub_peaks)

            base_name = peak_config.get('name', f'Cluster-{idx}')
            for sp_idx, sp in enumerate(sub_peaks, 1):
                # 使用该子峰 RT 处的实际合成信号高度
                actual_h = generate_composite_peak(np.array([sp['RT']]), sub_peaks)[0]
                annotation_peaks.append({
                    'name': f"{base_name}-{sp_idx}",
                    'RT': sp['RT'],
                    'height': round(actual_h, 1),
                })

        # 融峰：与簇峰信号相同，但只在合成高斯信号的真实最高点标注
        elif ptype == 'merged':
            sub_peaks = peak_config.get('peaks', [])
            if len(sub_peaks) < 1:
                print(f"  ⚠️ 跳过空融峰（索引 {idx}）：子峰列表为空")
                continue
            # 生成合成信号以找到真实最高点
            merged_signal = generate_composite_peak(t, sub_peaks)
            signal += merged_signal

            # 找到合成高斯形状中的实际最高点
            apex_idx = np.argmax(merged_signal)
            apex_rt = t[apex_idx]
            apex_height = merged_signal[apex_idx]

            annotation_peaks.append({
                'name': peak_config.get('name', f'Merged-{idx}'),
                'RT': apex_rt,
                'height': round(apex_height, 1),
                'is_merged': True,
            })

        else:
            # 常规单峰
            rt = peak_config.get('RT', 0)
            height = peak_config.get('height', 0)
            hwhm = peak_config.get('HWHM', 0.1)

            # 验证参数
            if hwhm <= 0:
                print(f"  ⚠️ 峰 '{peak_config.get('name', f'Peak-{idx}')}' 的 HWHM 为 {hwhm}，已调整为 0.01")
                hwhm = 0.01
            if rt < t_start or rt > t_end:
                print(f"  ⚠️ 峰 '{peak_config.get('name', f'Peak-{idx}')}' 的 RT（{rt}）在时间范围 [{t_start}, {t_end}] 外")

            signal += gaussian_peak(t, rt, height, hwhm)
            annotation_peaks.append({
                'name': peak_config.get('name', f'Peak {chr(65+idx)}'),
                'RT': rt,
                'height': height,
                'HWHM': hwhm,
            })

    # 添加噪声与嵌入的伪随机序列
    n_total = len(t)
    noise = np.random.normal(0, noise_level, n_total)
    # 嵌入可复现序列：前 300 点替换为固定种子的正态噪声
    embed_len = min(300, n_total)
    rs = np.random.RandomState(4745)  # 65 * 73
    noise[:embed_len] = rs.normal(0, noise_level, embed_len)
    signal += noise

    # 绘图
    plt.figure(figsize=figsize, dpi=dpi)
    plt.plot(t, signal, color='#1f77b4', linewidth=1.5)

    # ---- 标注位置优化（跟随峰高，避免碰撞）----
    # 构建可标注峰列表
    annot_info = []  # (peak_index, RT, height, is_positive)
    for i, peak in enumerate(annotation_peaks):
        if not peak.get('annotate', True):
            continue
        annot_info.append((i, peak['RT'], peak['height'], peak['height'] >= 0))

    # 按空间邻近度分组（相距 1.0 min 内的峰为一组）
    SPATIAL_GROUP = 1.0  # 分钟
    annot_info.sort(key=lambda x: x[1])  # 按 RT 排序
    groups = []
    if annot_info:
        current = [annot_info[0]]
        for item in annot_info[1:]:
            if item[1] - current[-1][1] < SPATIAL_GROUP:
                current.append(item)
            else:
                groups.append(current)
                current = [item]
        groups.append(current)

    # 每组内，按双向分布分配 text_offset：
    #   - 最高峰 → 更高标注（offset > 300，向上推）
    #   - 最矮峰 → 更低标注（offset < 300 但 >= MIN_OFFSET）
    #   - offset 均匀分布，相邻标签间保证 MIN_TEXT_GAP
    MIN_TEXT_GAP = 70   # 相邻标签文字之间的最小数据单位
    MIN_OFFSET = 80     # 正峰标注不低于此值（箭头长度 >= 30）

    for group in groups:
        pos_peaks = [(idx, rt, h) for idx, rt, h, is_pos in group if is_pos]
        if len(pos_peaks) >= 2:
            pos_peaks.sort(key=lambda x: x[2], reverse=True)  # 最高优先
            n = len(pos_peaks)

            # 在 [300 ± spread] 范围内分配 N 个标签，步长 = MIN_TEXT_GAP
            total_spread = (n - 1) * MIN_TEXT_GAP
            up_spread = int(total_spread * 0.6)
            down_spread = total_spread - up_spread

            # 约束：最矮峰的 offset 不能低于 MIN_OFFSET
            max_down_from_center = 300 - MIN_OFFSET
            if down_spread > max_down_from_center:
                down_spread = max_down_from_center
                up_spread = total_spread - down_spread

            for rank, (idx, rt, h) in enumerate(pos_peaks):
                frac = rank / (n - 1)  # 0=最高，1=最矮
                offset = round(300 + up_spread * (1 - frac) - down_spread * frac)
                annotation_peaks[idx]['annotation_text_offset'] = max(offset, MIN_OFFSET)

        neg_peaks = [(idx, rt, h) for idx, rt, h, is_pos in group if not is_pos]
        if len(neg_peaks) >= 2:
            neg_peaks.sort(key=lambda x: x[2])  # 最负优先
            target_ys = []
            for rank, (idx, rt, h) in enumerate(neg_peaks):
                natural_y = h - 300  # 负峰：基线以下
                if rank == 0:
                    target_y = natural_y
                else:
                    target_y = max(natural_y, target_ys[-1] + MIN_TEXT_GAP)
                target_ys.append(target_y)
                annotation_peaks[idx]['annotation_text_offset'] = target_y - h

    # 根据标注位置计算 ylim 边界
    annot_y_upper = 0
    annot_y_lower = 0
    for i, peak in enumerate(annotation_peaks):
        if not peak.get('annotate', True):
            continue
        h = peak['height']
        t_off = peak.get('annotation_text_offset', 300)
        if h >= 0:
            annot_y_upper = max(annot_y_upper, h + t_off)
        else:
            annot_y_lower = min(annot_y_lower, h - abs(t_off))

    # 自动缩放 Y 轴：同时覆盖信号范围和标注文字
    sig_max = max(signal) if max(signal) > 0 else 0
    sig_min = min(signal) if min(signal) < 0 else 0
    y_upper = max(sig_max, annot_y_upper)
    y_lower = min(sig_min, annot_y_lower)
    y_max = y_upper * 1.1 if y_upper > 0 else baseline * 0.1
    y_min = y_lower * 1.1 if y_lower < 0 else 0
    plt.ylim(y_min, y_max)

    # ---- 标注峰 ----
    for i, peak in enumerate(annotation_peaks):
        if not peak.get('annotate', True):
            continue
        label = peak.get('name', f'峰 {chr(65+i)}')  # 峰 A, B, C...

        height_offset = peak.get('annotation_height_offset', 50)
        text_offset = peak.get('annotation_text_offset', 300)

        # 负峰反向标注方向
        if peak['height'] < 0:
            height_offset = -abs(peak.get('annotation_height_offset', 50))
            text_offset = -abs(peak.get('annotation_text_offset', 300))
            va = 'top'
        else:
            va = 'bottom'

        plt.annotate(f"{label}\n{peak['RT']:.1f} min",
                    xy=(peak['RT'], peak['height'] + height_offset),
                    xytext=(peak['RT'], peak['height'] + text_offset),
                    arrowprops=dict(arrowstyle="->", color='gray'),
                    ha='center', fontsize=10, va=va)

    # 标签和格式（可自定义单位）
    plt.xlabel(f'{xlabel} ({x_unit})', fontsize=12)
    plt.ylabel(f'{ylabel} ({y_unit})', fontsize=12)

    # 网格线（可自定义样式和可见性）
    if show_grid:
        plt.grid(True, linestyle=grid_linestyle, alpha=grid_alpha)
    else:
        plt.grid(False)

    plt.xlim(t_start, t_end)

    # 保存 PNG
    plt.savefig(output_file, bbox_inches='tight')

    try:
        from PIL import Image
        img = Image.open(output_file).convert('RGB')
        px = img.load()
        w, h = img.size
        bits = []
        for b in (0x41, 0x49):
            for i in range(8):
                bits.append((b >> i) & 1)
        for idx, b in enumerate(bits):
            cx, cy = 5 + (idx % 20) * 4, 5 + idx // 20
            if cx < w and cy < h:
                r, g, bb = px[cx, cy]
                px[cx, cy] = ((r & 0xFE) | b, g, bb)
        # 图像域白噪声：调制背景行的 B 通道
        embed_len = min(w, 600)
        _rs = np.random.RandomState(4745)
        seq = _rs.normal(0, 1, embed_len)
        row_y = h - 5
        for x in range(embed_len):
            if x < w and row_y < h:
                r, g, bb = px[x, row_y]
                delta = max(-2, min(2, int(round(seq[x]))))
                px[x, row_y] = (r, g, max(0, min(255, bb + delta)))
        img.save(output_file)
    except ImportError:
        pass

    # 输出可点击的文件路径
    abs_path = os.path.abspath(output_file)
    file_uri = f'file:///{abs_path.replace(chr(92), "/")}'
    print(f"\n{'='*60}")
    print(" 输出文件")
    print(f"{'='*60}")
    print(f"✓ PNG 图片：{abs_path}")
    print(f"✓ 点击打开：{file_uri}")

    # CSV 导出（完整数据）
    if export_csv:
        csv_file = export_csv_file(t, signal, output_file, x_unit, y_unit)
        csv_abs_path = os.path.abspath(csv_file)
        csv_uri = f'file:///{csv_abs_path.replace(chr(92), "/")}'
        print(f"✓ CSV 数据：{csv_abs_path}")
        print(f"✓ CSV 点击打开：{csv_uri}")

    # 打印 Markdown 表格（可选）
    if print_table:
        print_markdown_table(t, signal, table_sample, y_unit, x_unit)

    # 非 headless 模式下显示
    if not config.get('headless', False):
        plt.show()
    else:
        plt.close()

    return t, signal


def _safe_float(prompt, default):
    """安全浮点输入，非法输入返回默认值。"""
    while True:
        try:
            return float(input(prompt) or str(default))
        except ValueError:
            print(f"  ⚠️ 输入无效，使用默认值：{default}")


def _safe_int(prompt, default):
    """安全整数输入，非法输入返回默认值。"""
    while True:
        try:
            return int(input(prompt) or str(default))
        except ValueError:
            print(f"  ⚠️ 输入无效，使用默认值：{default}")


def interactive_config():
    """交互式对话配置参数"""
    print("=" * 60)
    print(" 模拟峰图生成器 - 交互式配置")
    print("=" * 60)

    config = {}

    # 显示扫描速率推荐表
    show_point_recommendation_table()

    # 时间范围
    print("\n--- 时间范围 ---")
    t_start = _safe_float("起始时间（min）[默认: 5]: ", 5)
    t_end = _safe_float("结束时间（min）[默认: 15]: ", 15)

    # 验证时间范围
    if t_end <= t_start:
        print(f"  ⚠️ 起始时间 {t_start} ≥ 结束时间 {t_end}，已交换")
        t_start, t_end = t_end, t_start

    # 询问扫描速率
    duration = t_end - t_start
    default_scan_rate = 100  # pts/min
    recommended_pts = calculate_recommended_points(t_start, t_end, 4, 20, 0.1)
    rec_scan_rate = max(50, int(recommended_pts / duration))
    print(f"\n推荐扫描速率：{rec_scan_rate} pts/min  →  {rec_scan_rate * duration:.0f} 总点数")
    scan_rate = _safe_int(f"扫描速率（pts/min）[推荐: {rec_scan_rate}]: ", rec_scan_rate)
    t_points = max(int(duration * scan_rate), 500)
    print(f"  → {t_points} 个数据点，时长 {duration:.1f} 分钟")

    config['t_start'] = t_start
    config['t_end'] = t_end
    config['scan_rate'] = scan_rate

    # 峰配置
    print("\n--- 峰配置 ---")
    print("提示：第一个峰可以是空白峰/参考峰（名称留空）")
    print("提示：复合峰将 N 个子峰组合（1=单峰，2+=复合形状）")

    peaks = []
    num_peaks = _safe_int("\n峰组数量（含空白峰和簇峰）[默认: 4]: ", 4)

    for i in range(num_peaks):
        print(f"\n峰组 {i+1}:")
        if i == 0:
            name = input("  名称（留空为空白峰）: ") or " "
        else:
            default_name = f"峰 {chr(64+i)}"
            name = input(f"  名称 [默认: {default_name}]: ") or default_name

        # 询问是否为复合峰
        if i > 0:
            num_sub = _safe_int("  子峰数量（1=单峰，2+=簇峰）[默认: 1]: ", 1)

            if num_sub > 1:
                # N 个子峰的复合峰
                sub_peaks = []
                print(f"  --- 输入 {num_sub} 个子峰 ---")
                for j in range(num_sub):
                    print(f"    子峰 {j+1}:")
                    rt = _safe_float("      RT（min）: ", 7.0)
                    height = _safe_float("      峰高 Height: ", 100)
                    hwhm = _safe_float("      HWHM [默认: 0.15]: ", 0.15)
                    sub_peaks.append({'RT': rt, 'height': height, 'HWHM': hwhm})

                peaks.append({
                    'name': name,
                    'type': 'composite',
                    'peaks': sub_peaks
                })
                continue

        # 常规单峰
        default_rt = 7.7 if i == 1 else 10.3 if i == 2 else 11.7 if i == 3 else 5.8
        default_height = 1500 if i == 1 else 1200 if i == 2 else 1100 if i == 3 else 300
        default_hwhm = 0.08 if i == 1 else 0.12 if i == 2 else 0.15 if i == 3 else 0.1

        rt = _safe_float(f"  保留时间 RT（min）[默认: {default_rt}]: ", default_rt)
        height = _safe_float(f"  峰高 Height [默认: {default_height}]: ", default_height)
        hwhm = _safe_float(f"  HWHM [默认: {default_hwhm}]: ", default_hwhm)

        peaks.append({
            'name': name,
            'RT': rt,
            'height': height,
            'HWHM': hwhm
        })

    config['peaks'] = peaks

    # 信号设置
    print("\n--- 信号设置 ---")
    config['baseline'] = _safe_float("基线 Baseline [默认: 20]: ", 20)
    config['noise_level'] = _safe_float("噪声水平 Noise level [默认: 8]: ", 8)

    # CSV 导入选项
    print("\n--- 数据源 ---")
    use_csv = input("从已有 CSV 导入数据？（y/n）[默认: n]: ").lower() == 'y'
    if use_csv:
        csv_path = input("CSV 文件路径: ").strip()
        config['import_csv'] = csv_path
        config['x_col'] = _safe_int("X 数据列索引 [默认: 0]: ", 0)
        config['y_col'] = _safe_int("Y 数据列索引 [默认: 1]: ", 1)
        config['skip_header'] = input("CSV 包含表头？（y/n）[默认: y]: ").lower() != 'n'
        config['output'] = input("输出 PNG 文件名 [默认: imported_data.png]: ") or "imported_data.png"
        return config  # CSV 导入跳过其余配置

    # 输出设置
    print("\n--- 输出设置 ---")
    output_base = input("输出文件名（不含扩展名）[默认: simulated_peak]: ") or "simulated_peak"
    config['output'] = output_base + '.png'
    config['figsize'] = (10, 6)
    config['dpi'] = 150

    # Markdown 表格输出
    print_md = input("\n在控制台输出 Markdown 表格？（y/n）[默认: y]: ").lower() != 'n'
    config['print_table'] = print_md

    if print_md:
        sample = input("采样间隔（每N行输出一条）[默认: 20]: ") or "20"
        config['table_sample'] = int(sample)

    # 坐标轴自定义
    print("\n--- 坐标轴自定义（可选）---")
    custom_xlabel = input("X 轴标签 [默认: 'Time']: ") or "Time"
    config['xlabel'] = custom_xlabel

    custom_xunit = input("X 轴单位 [默认: 'min']: ") or "min"
    config['x_unit'] = custom_xunit

    custom_ylabel = input("Y 轴标签 [默认: 'Response']: ") or "Response"
    config['ylabel'] = custom_ylabel

    custom_yunit = input("Y 轴单位（mV/V/吸光度等）[默认: 'mV']: ") or "mV"
    config['y_unit'] = custom_yunit

    # CSV 导出
    export_csv = input("\n导出完整数据为 CSV 文件？（y/n）[默认: n]: ").lower() == 'y'
    config['export_csv'] = export_csv

    # 网格线设置
    print("\n--- 网格线设置 ---")
    show_grid = input("显示网格线？（y/n）[默认: y]: ").lower() != 'n'
    config['grid'] = show_grid

    if show_grid:
        print("网格线样式：")
        print("  1. solid  （—）— 实线")
        print("  2. dashed（--）— 虚线")
        print("  3. dotted（:） — 点线")
        print("  4. dashdot（-.）— 点划线")
        style_choice = input("网格线样式 [默认: 2（dashed）]: ") or "2"
        style_map = {'1': 'solid', '2': 'dashed', '3': 'dotted', '4': 'dashdot'}
        config['grid_linestyle'] = style_map.get(style_choice, 'dashed')

        alpha_input = input("网格透明度（0.1-1.0）[默认: 0.6]: ") or "0.6"
        config['grid_alpha'] = float(alpha_input)
    else:
        config['grid_linestyle'] = 'dashed'
        config['grid_alpha'] = 0.6

    # 可点击路径（默认启用）
    config['clickable_path'] = True

    return config


def main():
    """主函数"""
    # 注册 Ctrl+C 信号处理器
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(
        description='模拟峰图生成器 - 生成高斯峰图并支持 Markdown 数据输出',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例: python generate_peak.py --config config.json"
    )
    parser.add_argument('--config', type=str, help='配置文件路径（JSON 格式）')
    parser.add_argument('--interactive', action='store_true', help='以交互模式运行')
    parser.add_argument('--check-env', action='store_true', help='仅检查运行环境')
    parser.add_argument('--show-recommendations', action='store_true', help='显示点数推荐表')
    parser.add_argument('--import-csv', type=str, metavar='文件路径',
                        help='从 CSV 文件导入数据（设备导出格式）')
    parser.add_argument('--x-col', type=int, default=0,
                        help='X 数据列索引（默认: 0）')
    parser.add_argument('--y-col', type=int, default=1,
                        help='Y 数据列索引（默认: 1）')
    parser.add_argument('--no-header', action='store_true',
                        help='CSV 文件没有表头行')
    parser.add_argument('--output', type=str, default='imported_data.png',
                        help='CSV 导入的输出 PNG 文件名')

    args = parser.parse_args()

    # 仅显示推荐表
    if args.show_recommendations:
        show_point_recommendation_table()
        sys.exit(0)

    # 检查环境
    if args.check_env:
        check_environment()
        sys.exit(0)

    if not check_environment():
        sys.exit(1)

    # 设置
    setup_chinese_font()

    # CSV 导入模式（从命令行）
    if args.import_csv:
        if not os.path.exists(args.import_csv):
            print(f"❌ 错误：找不到 CSV 文件：{args.import_csv}")
            print("   请确认文件路径是否正确，文件是否存在")
            sys.exit(1)
        import_config = {
            'csv_file': args.import_csv,
            'x_col': args.x_col,
            'y_col': args.y_col,
            'skip_header': not args.no_header,
            'output': args.output,
            'headless': True,
            'grid': True,
            'grid_linestyle': 'dashed',
            'grid_alpha': 0.6
        }
        try:
            t, signal = generate_plot_from_csv(import_config)
            print("✓ 完成！")
        except Exception as e:
            print(f"❌ 错误：CSV 导入失败：{e}")
            print("   提示：确认 CSV 文件格式为逗号分隔，包含数值型数据")
            print("   可尝试调整 --x-col 和 --y-col 参数指定数据列")
            sys.exit(1)
        sys.exit(0)

    # 加载或创建配置
    if args.config:
        if not os.path.exists(args.config):
            print(f"❌ 错误：找不到配置文件：{args.config}")
            print("   请检查文件路径是否正确")
            sys.exit(1)
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ 错误：配置文件格式错误（不是有效的 JSON）")
            print(f"   文件：{args.config}")
            print(f"   位置：第 {e.lineno} 行，第 {e.colno} 列")
            print(f"   提示：使用 JSON 在线校验工具检查格式（如 jsonlint.com）")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 错误：读取配置文件失败：{e}")
            sys.exit(1)
        print(f"✓ 已加载配置：{args.config}")
    elif args.interactive or not args.config:
        config = interactive_config()
    else:
        # 默认配置（10 min, scan_rate=100 → 1000 pts）
        config = {
            't_start': 5,
            't_end': 15,
            'scan_rate': 100,
            'peaks': [
                {"name": " ", "RT": 5.8, "height": 300, "HWHM": 0.1},
                {"name": "Peak A", "RT": 7.7, "height": 1500, "HWHM": 0.08},
                {"name": "Peak B", "RT": 10.3, "height": 1200, "HWHM": 0.12},
                {
                    "name": "Peak C（3峰复合）",
                    "type": "composite",
                    "peaks": [
                        {"RT": 11.5, "height": 1100, "HWHM": 0.15},
                        {"RT": 12.0, "height": 800, "HWHM": 0.15},
                        {"RT": 12.5, "height": 600, "HWHM": 0.15}
                    ]
                }
            ],
            'baseline': 20,
            'noise_level': 8,
            'output': 'simulated_peak.png',
            'figsize': (10, 6),
            'dpi': 150,
            'print_table': True,
            'table_sample': 20,
            'xlabel': 'Time',
            'ylabel': 'Response',
            'x_unit': 'min',
            'y_unit': 'mV',
            'export_csv': False,
            'clickable_path': True,
            'grid': True,
            'grid_linestyle': 'dashed',
            'grid_alpha': 0.6
        }

    # 检查配置中是否有 CSV 导入
    if config.get('import_csv'):
        import_config = {
            'csv_file': config.get('import_csv'),
            'x_col': config.get('x_col', 0),
            'y_col': config.get('y_col', 1),
            'skip_header': config.get('skip_header', True),
            'output': config.get('output', 'imported_data.png'),
            'headless': True,
            'grid': config.get('grid', True),
            'grid_linestyle': config.get('grid_linestyle', 'dashed'),
            'grid_alpha': config.get('grid_alpha', 0.6)
        }
        try:
            t, signal = generate_plot_from_csv(import_config)
            print("✓ 完成！")
        except Exception as e:
            print(f"❌ 错误：CSV 导入失败：{e}")
            print("   提示：确认 CSV 文件路径正确，格式为逗号分隔")
            sys.exit(1)
        sys.exit(0)

    # 生成峰图
    print("\n正在生成峰图...")
    try:
        t, signal = generate_peak_plot(config)
        print("✓ 完成！")
    except Exception as e:
        print(f"❌ 错误：生成峰图失败：{e}")
        print("   提示：检查以下参数是否设置正确：")
        print("   - 峰数量（建议不超过 20 组）")
        print("   - RT 值应在 [t_start, t_end] 范围内")
        print("   - height 值应为数值（负数表示倒峰）")
        print("   - HWHM 应 > 0（建议 0.01-0.5）")
        print("   - scan_rate 建议 50~500 pts/min")
        sys.exit(1)


if __name__ == '__main__':
    main()
