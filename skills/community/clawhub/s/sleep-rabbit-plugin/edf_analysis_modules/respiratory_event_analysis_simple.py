#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
呼吸事件详细分析脚本 - 简化版（避免Unicode问题）
基于AASM标准进行专业的呼吸事件分析
"""

import os
import sys
import mne
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal, stats, interpolate
import warnings
import json
warnings.filterwarnings('ignore')

def respiratory_event_analysis(edf_path):
    """进行呼吸事件详细分析"""
    
    print("=" * 70)
    print("呼吸事件详细分析报告")
    print("=" * 70)
    print(f"分析文件: {edf_path}")
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not os.path.exists(edf_path):
        print("错误: 文件不存在!")
        return None
    
    try:
        # 1. 加载EDF文件（使用preload=False避免内存问题）
        print("[1/12] 加载EDF文件...")
        raw = mne.io.read_raw_edf(edf_path, preload=False, verbose=False)
        
        # 2. 识别呼吸相关通道
        print("[2/12] 识别呼吸相关通道...")
        
        channel_info = {
            'respiratory': [],
            'spo2': [],
            'ecg': [],
            'thoracic': [],
            'abdominal': []
        }
        
        # 自动识别通道类型
        for ch_name in raw.ch_names:
            ch_name_lower = ch_name.lower()
            if any(keyword in ch_name_lower for keyword in ['resp', 'flow', 'airflow', 'nasal', 'oro-nasal']):
                channel_info['respiratory'].append(ch_name)
            elif any(keyword in ch_name_lower for keyword in ['spo2', 'sao2', 'oxi', 'oxygen']):
                channel_info['spo2'].append(ch_name)
            elif any(keyword in ch_name_lower for keyword in ['ecg', 'ekg', 'electrocardiogram']):
                channel_info['ecg'].append(ch_name)
            elif any(keyword in ch_name_lower for keyword in ['thor', 'chest', 'rib']):
                channel_info['thoracic'].append(ch_name)
            elif any(keyword in ch_name_lower for keyword in ['abd', 'abdominal', 'belly']):
                channel_info['abdominal'].append(ch_name)
        
        print(f"   识别到呼吸通道: {channel_info['respiratory']}")
        print(f"   识别到血氧通道: {channel_info['spo2']}")
        print(f"   识别到心电通道: {channel_info['ecg']}")
        
        if not channel_info['respiratory']:
            print("错误: 未找到呼吸通道!")
            return None
        
        # 3. 提取呼吸信号（使用分块处理避免内存问题）
        print("[3/12] 提取呼吸信号...")
        resp_channel = channel_info['respiratory'][0]
        sfreq = raw.info['sfreq']
        
        # 获取数据长度但不加载所有数据
        n_samples = raw.n_times
        duration_hours = n_samples / (sfreq * 3600)
        
        print(f"   采样频率: {sfreq} Hz")
        print(f"   数据长度: {n_samples:,} 样本")
        print(f"   记录时长: {duration_hours:.2f} 小时")
        
        # 对于大文件，使用分块处理
        print(f"   文件较大，使用分块处理...")
        
        # 定义分块大小（例如1小时的数据）
        chunk_size_samples = int(3600 * sfreq)  # 1小时
        n_chunks = int(np.ceil(n_samples / chunk_size_samples))
        
        print(f"   分为 {n_chunks} 个数据块处理")
        
        # 4. 呼吸信号预处理（分块进行）
        print("[4/12] 呼吸信号预处理（分块）...")
        
        # 带通滤波 (0.1-5 Hz，对应呼吸频率)
        nyquist = sfreq / 2
        lowcut = 0.1  # 对应6次/分钟
        highcut = 5.0  # 对应300次/分钟
        
        # 设计带通滤波器
        b, a = signal.butter(4, [lowcut/nyquist, highcut/nyquist], btype='band')
        
        # 存储处理后的数据
        resp_envelope_chunks = []
        all_events = []
        
        # 分块处理数据
        for chunk_idx in range(min(n_chunks, 24)):  # 最多处理24小时
            start_sample = chunk_idx * chunk_size_samples
            end_sample = min((chunk_idx + 1) * chunk_size_samples, n_samples)
            
            if chunk_idx % 4 == 0 or chunk_idx == min(n_chunks, 24) - 1:
                print(f"      处理数据块 {chunk_idx + 1}/{min(n_chunks, 24)}")
            
            # 提取当前数据块
            resp_data_chunk = raw.get_data(
                picks=resp_channel,
                start=start_sample,
                stop=end_sample
            )[0]
            
            # 滤波处理
            resp_filtered_chunk = signal.filtfilt(b, a, resp_data_chunk)
            
            # 计算呼吸包络
            resp_envelope_chunk = np.abs(signal.hilbert(resp_filtered_chunk))
            resp_envelope_chunks.append((start_sample, end_sample, resp_envelope_chunk))
            
            # 在当前数据块中检测事件
            chunk_events = detect_events_in_chunk(
                resp_envelope_chunk, start_sample, sfreq,
                baseline_amplitude=np.median(resp_envelope_chunk)
            )
            all_events.extend(chunk_events)
        
        # 合并所有事件
        events = merge_chunk_events(all_events, sfreq)
        
        # 5. 呼吸事件检测已完成（通过分块处理）
        print("[5/12] 呼吸事件检测完成（分块处理）...")
        
        # 统计事件数量
        apnea_count = len([e for e in events if e['type'] == '呼吸暂停'])
        hypopnea_count = len([e for e in events if e['type'] == '低通气'])
        total_events = len(events)
        
        print(f"   检测到呼吸暂停事件: {apnea_count} 个")
        print(f"   检测到低通气事件: {hypopnea_count} 个")
        print(f"   总事件数: {total_events} 个")
        
        # 6. 计算关键指标
        print("[6/12] 计算关键指标...")
        
        # AHI (呼吸暂停低通气指数)
        ahi = total_events / duration_hours
        
        # 事件持续时间统计
        apnea_durations = [e['duration_sec'] for e in events if e['type'] == '呼吸暂停']
        hypopnea_durations = [e['duration_sec'] for e in events if e['type'] == '低通气']
        
        # 事件时间分布
        event_times = [e['start_time'] / 3600 for e in events]  # 转换为小时
        
        # 7. 血氧分析 (如有SpO2通道)
        spo2_analysis = {}
        
        if channel_info['spo2']:
            print("[7/12] 血氧饱和度分析...")
            spo2_channel = channel_info['spo2'][0]
            
            # 只分析第一小时的数据（避免内存问题）
            spo2_data = raw.get_data(
                picks=spo2_channel,
                start=0,
                stop=min(chunk_size_samples, n_samples)
            )[0]
            
            # 计算血氧下降事件 (≥3%持续≥10秒)
            spo2_baseline = np.median(spo2_data)
            spo2_drop_threshold = spo2_baseline - 3  # 下降3%
            
            # 检测血氧下降事件
            spo2_drop_mask = spo2_data < spo2_drop_threshold
            
            # 标记连续区域函数
            def find_continuous_regions(mask, min_duration):
                regions = []
                start = None
                for i, value in enumerate(mask):
                    if value and start is None:
                        start = i
                    elif not value and start is not None:
                        if i - start >= min_duration:
                            regions.append((start, i))
                        start = None
                if start is not None and len(mask) - start >= min_duration:
                    regions.append((start, len(mask)))
                return regions
            
            spo2_drop_regions = find_continuous_regions(spo2_drop_mask, 10 * sfreq)
            
            # ODI (氧减指数) - 基于第一小时数据估算
            odi = len(spo2_drop_regions)  # 第一小时的事件数
            
            # 最低血氧饱和度
            min_spo2 = np.min(spo2_data)
            
            spo2_analysis = {
                'odi': odi,
                'min_spo2': min_spo2,
                'baseline_spo2': spo2_baseline,
                'drop_events': len(spo2_drop_regions)
            }
            
            print(f"   ODI指数: {odi:.1f} 次/小时（基于第一小时估算）")
            print(f"   最低血氧: {min_spo2:.1f}%")
        
        # 8. 严重程度分级
        print("[8/12] 严重程度分级...")
        
        severity = "正常"
        if ahi < 5:
            severity = "正常"
        elif ahi < 15:
            severity = "轻度睡眠呼吸暂停"
        elif ahi < 30:
            severity = "中度睡眠呼吸暂停"
        else:
            severity = "重度睡眠呼吸暂停"
        
        # 9. 生成报告
        print("[9/12] 生成分析报告...")
        
        report = {
            'file_info': {
                'path': edf_path,
                'duration_hours': duration_hours,
                'sampling_rate': sfreq,
                'channels': channel_info
            },
            'events': {
                'total': total_events,
                'apnea_count': apnea_count,
                'hypopnea_count': hypopnea_count,
                'apnea_durations': apnea_durations,
                'hypopnea_durations': hypopnea_durations,
                'event_times': event_times
            },
            'metrics': {
                'ahi': ahi,
                'severity': severity,
                'avg_apnea_duration': np.mean(apnea_durations) if apnea_durations else 0,
                'avg_hypopnea_duration': np.mean(hypopnea_durations) if hypopnea_durations else 0
            },
            'spo2_analysis': spo2_analysis,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 10. 保存报告
        print("[10/12] 保存分析结果...")
        
        # 创建输出目录
        output_dir = os.path.join(os.path.dirname(edf_path), 'respiratory_analysis')
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存JSON报告
        report_path = os.path.join(output_dir, 'respiratory_analysis_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 保存文本报告
        txt_report_path = os.path.join(output_dir, 'respiratory_analysis_summary.txt')
        with open(txt_report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("呼吸事件详细分析报告\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"分析文件: {edf_path}\n")
            f.write(f"分析时间: {report['timestamp']}\n")
            f.write(f"记录时长: {duration_hours:.2f} 小时\n\n")
            
            f.write("关键指标:\n")
            f.write(f"  AHI指数: {ahi:.1f} 事件/小时\n")
            f.write(f"  严重程度: {severity}\n")
            f.write(f"  总事件数: {total_events} 个\n")
            f.write(f"  呼吸暂停: {apnea_count} 个\n")
            f.write(f"  低通气: {hypopnea_count} 个\n")
            
            if apnea_durations:
                f.write(f"  平均呼吸暂停时长: {np.mean(apnea_durations):.1f} 秒\n")
            if hypopnea_durations:
                f.write(f"  平均低通气时长: {np.mean(hypopnea_durations):.1f} 秒\n")
            
            if spo2_analysis:
                f.write("\n血氧分析:\n")
                f.write(f"  ODI指数: {spo2_analysis['odi']:.1f} 次/小时\n")
                f.write(f"  最低血氧: {spo2_analysis['min_spo2']:.1f}%\n")
                f.write(f"  基线血氧: {spo2_analysis['baseline_spo2']:.1f}%\n")
            
            f.write("\n临床建议:\n")
            if ahi < 5:
                f.write("  呼吸事件在正常范围内，无需特殊干预。\n")
                f.write("  建议保持健康生活方式，定期监测。\n")
            elif ahi < 15:
                f.write("  轻度睡眠呼吸暂停，建议生活方式干预。\n")
                f.write("  建议：减重、侧卧睡眠、避免酒精和镇静剂。\n")
                f.write("  建议6-12个月后复查。\n")
            elif ahi < 30:
                f.write("  中度睡眠呼吸暂停，建议医疗评估。\n")
                f.write("  建议咨询睡眠专科医生，考虑睡眠监测。\n")
                f.write("  可能需要CPAP治疗。\n")
            else:
                f.write("  重度睡眠呼吸暂停，需要立即医疗干预。\n")
                f.write("  强烈建议咨询睡眠专科医生。\n")
                f.write("  可能需要CPAP治疗或其他干预措施。\n")
                f.write("  注意驾驶和工作安全风险。\n")
            
            f.write(f"\n输出文件: {report_path}\n")
            f.write("=" * 70 + "\n")
        
        print("[11/12] 分析完成!")
        print()
        print("=" * 70)
        print("呼吸事件分析结果摘要")
        print("=" * 70)
        print(f"AHI指数: {ahi:.1f} 事件/小时")
        print(f"严重程度: {severity}")
        print(f"总事件数: {total_events} 个")
        print(f"  呼吸暂停: {apnea_count} 个")
        print(f"  低通气: {hypopnea_count} 个")
        
        if spo2_analysis:
            print(f"ODI指数: {spo2_analysis['odi']:.1f} 次/小时")
            print(f"最低血氧: {spo2_analysis['min_spo2']:.1f}%")
        
        print(f"输出目录: {output_dir}")
        print("=" * 70)
        
        return report
        
    except Exception as e:
        print(f"分析过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def detect_events_in_chunk(resp_envelope, chunk_start_sample, sfreq, baseline_amplitude):
    """在单个数据块中检测呼吸事件"""
    events = []
    
    # 检测呼吸暂停 (气流停止≥10秒)
    apnea_threshold = 0.1 * baseline_amplitude  # 气流下降90%
    apnea_min_duration = 10 * sfreq  # 10秒
    
    # 检测低通气 (气流下降≥30%持续≥10秒)
    hypopnea_threshold = 0.7 * baseline_amplitude  # 气流下降30%
    hypopnea_min_duration = 10 * sfreq  # 10秒
    
    # 寻找低于阈值的时间段
    apnea_mask = resp_envelope < apnea_threshold
    hypopnea_mask = resp_envelope < hypopnea_threshold
    
    # 标记连续区域
    def find_continuous_regions(mask, min_duration):
        regions = []
        start = None
        for i, value in enumerate(mask):
            if value and start is None:
                start = i
            elif not value and start is not None:
                if i - start >= min_duration:
                    regions.append((start, i))
                start = None
        if start is not None and len(mask) - start >= min_duration:
            regions.append((start, len(mask)))
        return regions
    
    # 检测呼吸暂停事件
    apnea_regions = find_continuous_regions(apnea_mask, apnea_min_duration)
    for start, end in apnea_regions:
        duration_sec = (end - start) / sfreq
        events.append({
            'type': '呼吸暂停',
            'start_sample': chunk_start_sample + start,
            'end_sample': chunk_start_sample + end,
            'duration_sec': duration_sec,
            'start_time': (chunk_start_sample + start) / sfreq,
            'end_time': (chunk_start_sample + end) / sfreq
        })
    
    # 检测低通气事件 (排除与呼吸暂停重叠的部分)
    hypopnea_regions = find_continuous_regions(hypopnea_mask, hypopnea_min_duration)
    for start, end in hypopnea_regions:
        # 检查是否与呼吸暂停重叠
        overlap = False
        for apnea_start, apnea_end in apnea_regions:
            if not (end <= apnea_start or start >= apnea_end):
                overlap = True
                break
        
        if not overlap:
            duration_sec = (end - start) / sfreq
            events.append({
                'type': '低通气',
                'start_sample': chunk_start_sample + start,
                'end_sample': chunk_start_sample + end,
                'duration_sec': duration_sec,
                'start_time': (chunk_start_sample + start) / sfreq,
                'end_time': (chunk_start_sample + end) / sfreq
            })
    
    return events

def merge_chunk_events(all_events, sfreq):
    """合并跨数据块的连续事件"""
    if not all_events:
        return []
    
    # 按开始时间排序
    sorted_events = sorted(all_events, key=lambda x: x['start_sample'])
    
    merged_events = []
    current_event = None
    
    for event in sorted_events:
        if current_event is None:
            current_event = event.copy()
        else:
            # 检查是否连续（间隔小于5秒）
            gap = event['start_sample'] - current_event['end_sample']
            same_type = event['type'] == current_event['type']
            
            if gap < 5 * sfreq and same_type:
                # 合并事件
                current_event['end_sample'] = event['end_sample']
                current_event['duration_sec'] = (current_event['end_sample'] - current_event['start_sample']) / sfreq
                current_event['end_time'] = current_event['end_sample'] / sfreq
            else:
                # 保存当前事件，开始新事件
                merged_events.append(current_event)
                current_event = event.copy()
    
    # 添加最后一个事件
    if current_event:
        merged_events.append(current_event)
    
    return merged_events

def main():
    """主函数"""
    # 设置编码以支持中文
    import sys
    import io
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if len(sys.argv) > 1:
        edf_path = sys.argv[1]
    else:
        # 默认使用测试文件
        edf_path = r"D:\openclaw\AISleepGen\data\edf\SC4001E0-PSG.edf"
    
    print("眠小兔呼吸事件分析系统启动...")
    result = respiratory_event_analysis(edf_path)
    
    if result:
        print("分析成功完成!")
    else:
        print("分析失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()