#!/usr/bin/env python3
"""
Sleep Staging Fixed Module
Version: 5.1.5
Description: REAL professional sleep analysis module
Original size: 14,635 bytes
Chinese comments marked with  for ClawHub compliance
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sleepanalysis
£¬Unscored
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
from scipy import signal
import warnings
import json
warnings.filterwarnings('ignore')

def analyze_sleep_stages(edf_path):
    """sleepanalysis"""
    
    print("=" * 70)
    print("sleepanalysis")
    print("=" * 70)
    print(f"file: {edf_path}")
    print(f": {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 1. 
        print("[1/6] EDFfile...")
        raw = mne.io.read_raw_edf(edf_path, preload=False, verbose=False)
        
        sfreq = raw.info['sfreq']
        n_samples = raw.n_times
        duration_hours = n_samples / (sfreq * 3600)
        
        print(f"   : {duration_hours:.1f}")
        print(f"   : {sfreq}Hz")
        print(f"   : {len(raw.ch_names)}")
        
        # 2. 
        print("[2/6] sleep...")
        
        # 
        print("   :")
        for i, ch in enumerate(raw.ch_names[:10]):  # 10
            print(f"     {i+1}. {ch}")
        if len(raw.ch_names) > 10:
            print(f"    ... {len(raw.ch_names)-10}")
        
        # 
        eeg_chans = []
        eog_chans = []
        emg_chans = []
        resp_chans = []
        
        for ch in raw.ch_names:
            ch_lower = ch.lower()
            if 'eeg' in ch_lower:
                eeg_chans.append(ch)
            elif 'eog' in ch_lower:
                eog_chans.append(ch)
            elif 'emg' in ch_lower:
                emg_chans.append(ch)
            elif 'resp' in ch_lower:
                resp_chans.append(ch)
        
        print(f"   EEG: {eeg_chans}")
        print(f"   EOG: {eog_chans}")
        print(f"   EMG: {emg_chans}")
        print(f"   respiration: {resp_chans}")
        
        # 3. 
        if eeg_chans:
            analysis_channel = eeg_chans[0]
            print(f"   EEGanalysis: {analysis_channel}")
        elif resp_chans:
            analysis_channel = resp_chans[0]
            print(f"   respirationanalysis: {analysis_channel}")
        else:
            print("   : analysis!")
            return None
        
        # 4. 
        print("[3/6] analysisdata...")
        
        # 30epoch£¨£©
        epoch_sec = 30
        epoch_samples = int(epoch_sec * sfreq)
        total_epochs = int(n_samples / epoch_samples)
        
        print(f"   epoch: {total_epochs} ({epoch_sec})")
        
        # £¨10epoch£¬£©
        sample_rate = 20
        sampled_epochs = []
        
        for epoch_idx in range(0, total_epochs, sample_rate):
            start = epoch_idx * epoch_samples
            end = min((epoch_idx + 1) * epoch_samples, n_samples)
            
            if epoch_idx % 200 == 0:
                print(f"      processingepoch {epoch_idx}/{total_epochs}")
            
            # 
            data = raw.get_data(picks=analysis_channel, start=start, stop=end)[0]
            
            if len(data) < epoch_samples * 0.8:  # data80%£¬
                continue
            
            # 
            features = calculate_epoch_features(data, sfreq, epoch_idx, start/sfreq)
            sampled_epochs.append(features)
        
        print(f"   analysis: {len(sampled_epochs)}epoch")
        
        # 5. 
        print("[4/6] sleep...")
        
        sleep_stages = []
        for features in sampled_epochs:
            stage = classify_sleep_stage_fixed(features)
            sleep_stages.append(stage)
        
        # 
        stage_counts = {}
        for stage in sleep_stages:
            label = get_stage_label(stage)
            stage_counts[label] = stage_counts.get(label, 0) + 1
        
        total = len(sleep_stages)
        print("   sleep:")
        for label, count in stage_counts.items():
            percentage = (count / total) * 100
            print(f"     {label}: {count} ({percentage:.1f}%)")
        
        # 6. 
        print("[5/6] ...")
        
        # 
        sleep_metrics = calculate_sleep_metrics(sleep_stages, sampled_epochs)
        
        report = {
            'file_info': {
                'path': edf_path,
                'duration_hours': round(duration_hours, 2),
                'sampling_rate': sfreq,
                'analysis_channel': analysis_channel,
                'total_epochs': total_epochs,
                'sampled_epochs': len(sampled_epochs)
            },
            'sleep_stages': {
                'counts': stage_counts,
                'percentages': {k: round((v/total)*100, 1) for k, v in stage_counts.items()},
                'raw_stages': sleep_stages
            },
            'sleep_metrics': sleep_metrics,
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 7. 
        print("[6/6] ...")
        
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'analysis_outputs', 'sleep_staging_fixed')
        
        # JSON
        report_path = os.path.join(output_dir, 'sleep_staging_report.json')
        
        # 
        txt_path = os.path.join(output_dir, 'sleep_staging_summary.txt')
        create_text_report(report, txt_path)
        
        # 
        create_visualizations(sleep_stages, sampled_epochs, output_dir)
        
        print()
        print("=" * 70)
        print("analysis!")
        print(f": {output_dir}")
        print("=" * 70)
        
        return report
        
    except Exception as e:
        print(f": {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def calculate_epoch_features(data, sfreq, epoch_idx, start_time):
    """epoch"""
    
    # 
    mean_amp = np.mean(np.abs(data))
    std_amp = np.std(data)
    
    # £¨£©
    def band_power(data, sfreq, low, high):
        from scipy.signal import welch
        freqs, psd = welch(data, sfreq, nperseg=min(256, len(data)))
        mask = (freqs >= low) & (freqs <= high)
        return np.mean(psd[mask]) if np.any(mask) else 0
    
    delta_power = band_power(data, sfreq, 0.5, 4)
    theta_power = band_power(data, sfreq, 4, 8)
    alpha_power = band_power(data, sfreq, 8, 13)
    sigma_power = band_power(data, sfreq, 11, 16)
    beta_power = band_power(data, sfreq, 13, 30)
    
    # 
    total_power = delta_power + theta_power + alpha_power + sigma_power + beta_power + 1e-10
    
    features = {
        'epoch_idx': epoch_idx,
        'start_time': start_time,
        'mean_amplitude': mean_amp,
        'std_amplitude': std_amp,
        'delta_ratio': delta_power / total_power,
        'theta_ratio': theta_power / total_power,
        'alpha_ratio': alpha_power / total_power,
        'sigma_ratio': sigma_power / total_power,
        'beta_ratio': beta_power / total_power,
        'total_power': total_power
    }
    
    return features

def classify_sleep_stage_fixed(features):
    """sleep"""
    
    mean_amp = features['mean_amplitude']
    alpha_ratio = features['alpha_ratio']
    delta_ratio = features['delta_ratio']
    sigma_ratio = features['sigma_ratio']
    
    # 
    debug = False
    
    if debug:
        print(f"  : amp={mean_amp:.3f}, alpha={alpha_ratio:.3f}, delta={delta_ratio:.3f}, sigma={sigma_ratio:.3f}")
    
    # 1: 
    if mean_amp < 1.0:  # 
        if debug: print("   -> Unscored ()")
        return 7  # Unscored
    
    # 2: Alpha
    if alpha_ratio > 0.3:  # Alpha
        if debug: print("   -> Wake (Alpha)")
        return 0  # Wake
    
    # 3: Delta
    if delta_ratio > 0.4:  # Delta
        if debug: print("   -> N3 (Delta)")
        return 3  # N3
    
    # 4: SigmaN2
    if 0.1 < sigma_ratio < 0.3:  # Sigma
        if debug: print("   -> N2 (Sigma)")
        return 2  # N2
    
    # 5: +AlphaREM
    if mean_amp < 50 and 0.05 < alpha_ratio < 0.2:
        if debug: print("   -> REM ()")
        return 4  # REM
    
    # : N1£¨£©
    if debug: print("   -> N1 ()")
    return 1  # N1

def get_stage_label(stage_code):
    """"""
    labels = {
        0: 'Wake',
        1: 'N1',
        2: 'N2',
        3: 'N3',
        4: 'REM',
        5: 'N4',
        6: 'Movement',
        7: 'Unscored'
    }
    return labels.get(stage_code, 'Unknown')

def calculate_sleep_metrics(stages, epochs):
    """sleep"""
    
    if not stages:
        return {
            'total_sleep_time_hours': 0,
            'sleep_efficiency_percent': 0,
            'sleep_latency_minutes': 0,
            'rem_latency_minutes': None,
            'wake_percent': 0,
            'n1_percent': 0,
            'n2_percent': 0,
            'n3_percent': 0,
            'rem_percent': 0
        }
    
    # 
    stage_counts = {}
    for stage in stages:
        label = get_stage_label(stage)
        stage_counts[label] = stage_counts.get(label, 0) + 1
    
    total = len(stages)
    
    # 
    percentages = {}
    for label, count in stage_counts.items():
        percentages[label] = round((count / total) * 100, 1)
    
    # £¨epoch 30£©
    sleep_epochs = total - stage_counts.get('Wake', 0) - stage_counts.get('Unscored', 0)
    total_sleep_time = sleep_epochs * 30  # 
    
    # 
    total_time = total * 30  # 
    sleep_efficiency = (total_sleep_time / total_time) * 100 if total_time > 0 else 0
    
    # £¨Wake/Unscored£©
    sleep_latency = 0
    for i, stage in enumerate(stages):
        if stage not in [0, 7]:  # WakeUnscored
            sleep_latency = i * 30 / 60  # 
            break
    
    # REM
    rem_latency = None
    for i, stage in enumerate(stages):
        if stage == 4:  # REM
            # 
            first_sleep = None
            for j in range(i):
                if stages[j] not in [0, 7]:
                    first_sleep = j
                    break
            
            if first_sleep is not None:
                rem_latency = (i - first_sleep) * 30 / 60  # 
            break
    
    return {
        'total_sleep_time_hours': round(total_sleep_time / 3600, 2),
        'sleep_efficiency_percent': round(sleep_efficiency, 1),
        'sleep_latency_minutes': round(sleep_latency, 1),
        'rem_latency_minutes': round(rem_latency, 1) if rem_latency else None,
        'wake_percent': percentages.get('Wake', 0),
        'n1_percent': percentages.get('N1', 0),
        'n2_percent': percentages.get('N2', 0),
        'n3_percent': percentages.get('N3', 0),
        'rem_percent': percentages.get('REM', 0),
        'unscored_percent': percentages.get('Unscored', 0)
    }

def create_text_report(report, output_path):
    """"""
    
    try:
            
            
            metrics = report['sleep_metrics']
            
            if metrics['rem_latency_minutes']:
            else:
            
            for stage, percent in report['sleep_stages']['percentages'].items():
            
            
            
        
        print(f"   : {output_path}")
        
    except Exception as e:
        print(f"   : {str(e)}")

def create_visualizations(stages, epochs, output_dir):
    """"""
    
    try:
        if not stages:
            return
        
        # 1. 
        times = [e['start_time'] / 3600 for e in epochs]  # 
        stage_labels = [get_stage_label(s) for s in stages]
        
        # 
        colors = {
            'Wake': '#FF6B6B',
            'N1': '#4ECDC4',
            'N2': '#45

