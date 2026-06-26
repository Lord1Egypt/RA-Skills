#!/usr/bin/env python3
"""
Sleep Staging Analysis Module
Version: 5.1.5
Description: REAL professional sleep analysis module
Original size: 27,599 bytes
Chinese comments marked with  for ClawHub compliance
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sleepanalysis
analysisEDFfilesleep£¨Wake, N1, N2, N3, REM£©
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
import warnings
import json
warnings.filterwarnings('ignore')

def sleep_staging_analysis(edf_path):
    """sleepanalysis"""
    
    print("=" * 70)
    print("sleepanalysis")
    print("=" * 70)
    print(f"analysisfile: {edf_path}")
    print(f"analysis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not os.path.exists(edf_path):
        print(": file!")
        return None
    
    try:
        # 1. EDF
        print("[1/8] EDFfile...")
        raw = mne.io.read_raw_edf(edf_path, preload=False, verbose=False)
        
        # 
        sfreq = raw.info['sfreq']
        n_samples = raw.n_times
        duration_hours = n_samples / (sfreq * 3600)
        
        print(f"   frequency: {sfreq} Hz")
        print(f"   data: {n_samples:,} ")
        print(f"   : {duration_hours:.2f} ")
        
        # 2. EEG£¨£©
        print("[2/8] EEG...")
        
        eeg_channels = []
        eog_channels = []
        emg_channels = []
        
        for ch_name in raw.ch_names:
            ch_name_lower = ch_name.lower()
            if any(keyword in ch_name_lower for keyword in ['eeg', 'c3', 'c4', 'cz', 'f3', 'f4', 'fz', 'o1', 'o2', 'pz']):
                eeg_channels.append(ch_name)
            elif any(keyword in ch_name_lower for keyword in ['eog', 'loc', 'roc']):
                eog_channels.append(ch_name)
            elif any(keyword in ch_name_lower for keyword in ['emg', 'chin']):
                emg_channels.append(ch_name)
        
        print(f"   EEG: {eeg_channels}")
        print(f"   EOG: {eog_channels}")
        print(f"   EMG: {emg_channels}")
        
        if not eeg_channels:
            print(": standardEEG£¬...")
            # 
            for ch_name in raw.ch_names:
                if 'EEG' in ch_name.upper() or 'C' in ch_name or 'F' in ch_name or 'O' in ch_name or 'P' in ch_name:
                    eeg_channels.append(ch_name)
            
            if not eeg_channels:
                print(": EEGsleep!")
                return None
        
        # 3. EEG£¨£©
        print("[3/8] EEGdata£¨processing£©...")
        
        # £¨30£©
        chunk_size_samples = int(1800 * sfreq)  # 30
        n_chunks = int(np.ceil(n_samples / chunk_size_samples))
        
        print(f"    {n_chunks} dataprocessing")
        
        # 30epoch
        all_features = []
        epoch_times = []
        
        # 30epoch£¨£©
        epoch_duration = 30  # 
        epoch_samples = int(epoch_duration * sfreq)
        
        # 4. £¨ - £©
        print("[4/8] sleep...")
        
        # EEG
        eeg_channel = eeg_channels[0]
        
        # epoch
        total_epochs = int(n_samples / epoch_samples)
        print(f"   epoch: {total_epochs} ({epoch_duration}epoch)")
        
        # £¨10epoch£¬£©
        sample_rate = 10
        sampled_epochs = []
        
        for epoch_idx in range(0, total_epochs, sample_rate):
            start_sample = epoch_idx * epoch_samples
            end_sample = min((epoch_idx + 1) * epoch_samples, n_samples)
            
            if epoch_idx % 100 == 0 or epoch_idx == total_epochs - 1:
                print(f"      processingepoch {epoch_idx + 1}/{total_epochs}")
            
            # epoch
            epoch_data = raw.get_data(
                picks=eeg_channel,
                start=start_sample,
                stop=end_sample
            )[0]
            
            if len(epoch_data) < epoch_samples * 0.5:  # data£¬
                continue
            
            # £¨£©
            features = {
                'epoch_idx': epoch_idx,
                'start_time': start_sample / sfreq,
                'end_time': end_sample / sfreq,
                'mean_amplitude': np.mean(np.abs(epoch_data)),
                'std_amplitude': np.std(epoch_data),
                'delta_power': _calculate_band_power(epoch_data, sfreq, 0.5, 4),
                'theta_power': _calculate_band_power(epoch_data, sfreq, 4, 8),
                'alpha_power': _calculate_band_power(epoch_data, sfreq, 8, 13),
                'sigma_power': _calculate_band_power(epoch_data, sfreq, 11, 16),  # 
                'beta_power': _calculate_band_power(epoch_data, sfreq, 13, 30),
                'gamma_power': _calculate_band_power(epoch_data, sfreq, 30, 45)
            }
            
            sampled_epochs.append(features)
        
        # 5. £¨£©
        print("[5/8] sleep...")
        
        # 
        sleep_stages = []
        stage_labels = []
        
        for features in sampled_epochs:
            stage = _classify_sleep_stage(features)
            sleep_stages.append(stage)
            stage_labels.append(_get_stage_label(stage))
        
        # 6. 
        print("[6/8] sleep...")
        
        # 
        unique_stages, stage_counts = np.unique(sleep_stages, return_counts=True)
        total_epochs_sampled = len(sleep_stages)
        
        stage_percentages = {}
        for stage, count in zip(unique_stages, stage_counts):
            percentage = (count / total_epochs_sampled) * 100
            stage_percentages[_get_stage_label(stage)] = round(percentage, 1)
        
        # 
        sleep_continuity = _calculate_sleep_continuity(sleep_stages, sampled_epochs)
        
        # 7. 
        print("[7/8] analysis...")
        
        report = {
            'file_info': {
                'path': edf_path,
                'duration_hours': round(duration_hours, 2),
                'sampling_rate': sfreq,
                'eeg_channel': eeg_channel,
                'total_epochs': total_epochs,
                'sampled_epochs': total_epochs_sampled
            },
            'sleep_structure': {
                'stage_percentages': stage_percentages,
                'total_sleep_time_hours': round(sleep_continuity['total_sleep_time'] / 3600, 2),
                'sleep_efficiency': round(sleep_continuity['sleep_efficiency'] * 100, 1),
                'sleep_latency_minutes': round(sleep_continuity['sleep_latency'] / 60, 1),
                'wake_after_sleep_onset_minutes': round(sleep_continuity['wake_after_sleep_onset'] / 60, 1),
                'rem_latency_minutes': round(sleep_continuity['rem_latency'] / 60, 1) if sleep_continuity['rem_latency'] else None
            },
            'stage_details': {
                'sampled_stages': sleep_stages,
                'stage_labels': stage_labels,
                'epoch_features': sampled_epochs
            },
            'analysis_notes': 'analysisbased on¡£sleepEEG/EOG/EMG¡£',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 8. 
        print("[8/8] analysis...")
        
        # 
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'analysis_outputs', 'sleep_staging_analysis')
        
        # JSON
        report_path = os.path.join(output_dir, 'sleep_staging_report.json')
        
        # 
        _create_sleep_histogram(sleep_stages, sampled_epochs, output_dir)
        
        # 
        _create_text_report(report, output_dir)
        
        print()
        print("=" * 70)
        print("sleepanalysis!")
        print("=" * 70)
        print(f": {output_dir}")
        
        return report
        
    except Exception as e:
        print(f"analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def _calculate_band_power(self, signal, sfreq, low_freq, high_freq):
    """power£¨£©"""
    from scipy import signal as sp_signal
    
    # 
    nyquist = sfreq / 2
    b, a = sp_signal.butter(4, [low_freq/nyquist, high_freq/nyquist], btype='band')
    
    # 
    filtered = sp_signal.filtfilt(b, a, signal)
    
    # 
    power = np.mean(filtered ** 2)
    return power

def _classify_sleep_stage(self, features):
    """based onsleep£¨£©"""
    
    # 
    alpha_ratio = features['alpha_power'] / (features['delta_power'] + 1e-10)
    delta_ratio = features['delta_power'] / (features['alpha_power'] + 1e-10)
    sigma_ratio = features['sigma_power'] / (features['theta_power'] + 1e-10)
    
    # 
    if features['mean_amplitude'] < 10:  # data
        return 7  # 
    
    # alphaN1
    if alpha_ratio > 0.5:
        return 0  # Wake
    
    # delta£¨N3£©
    elif delta_ratio > 2.0:
        return 3  # N3
    
    # sigma£¨£©N2
    elif 0.3 < sigma_ratio < 1.5:
        return 2  # N2
    
    # REM
    elif features['mean_amplitude'] < 30 and 0.1 < alpha_ratio < 0.3:
        return 4  # REM
    
    # N1£¨£©
    else:
        return 1  # N1

def _get_stage_label(self, stage_code):
    """sleep"""
    stage_labels = {
        0: 'Wake',
        1: 'N1',
        2: 'N2', 
        3: 'N3',
        4: 'REM',
        5: 'N4',  # standard£¬N3
        6: 'Movement',
        7: 'Unscored'
    }
    return stage_labels.get(stage_code, 'Unknown')

def _calculate_sleep_continuity(self, sleep_stages, epoch_features):
    """sleep"""
    
    if not sleep_stages:
        return {
            'total_sleep_time': 0,
            'sleep_efficiency': 0,
            'sleep_latency': 0,
            'wake_after_sleep_onset': 0,
            'rem_latency': None
        }
    
    # £¨Wake£©
    first_sleep_idx = None
    for i, stage in enumerate(sleep_stages):
        if stage != 0:  # Wake
            first_sleep_idx = i
            break
    
    # REM
    first_rem_idx = None
    for i, stage in enumerate(sleep_stages):
        if stage == 4:  # REM
            first_rem_idx = i
            break
    
    # 
    total_epochs = len(sleep_stages)
    sleep_epochs = len([s for s in sleep_stages if s != 0])  # Wakesleep
    
    # epoch 30
    epoch_duration = 30
    
    total_sleep_time = sleep_epochs * epoch_duration
    total_recording_time = total_epochs * epoch_duration
    
    sleep_efficiency = total_sleep_time / total_recording_time if total_recording_time > 0 else 0
    
    # £¨£©
    sleep_latency = first_sleep_idx * epoch_duration if first_sleep_idx is not None else total_recording_time
    
    # REM£¨REM£©
    rem_latency = None
    if first_sleep_idx is not None and first_rem_idx is not None and first_rem_idx > first_sleep_idx:
        rem_latency = (first_rem_idx - first_sleep_idx) * epoch_duration
    
    # £¨£©
    # Wake
    wake_after_sleep = 0
    if first_sleep_idx is not None:
        for i in range(first_sleep_idx, len(sleep_stages)):
            if sleep_stages[i] == 0:
                wake_after_sleep += epoch_duration
    
    return {
        'total_sleep_time': total_sleep_time,
        'sleep_efficiency': sleep_efficiency,
        'sleep_latency': sleep_latency,
        'wake_after_sleep_onset': wake_after_sleep,
        'rem_latency': rem_latency
    }

def _create_sleep_histogram(self, sleep_stages, epoch_features, output_dir):
    """sleep"""
    
    if not sleep_stages:
        return
    
    try:
        # 
        stage_labels = [self._get_stage_label(s) for s in sleep_stages]
        times = [feat['start_time'] / 3600 for feat in epoch_features]  # 
        
        # 
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # 1. 
        colors = {'Wake': 'gray', 'N1': 'blue', 'N2': 'green', 'N3': 'red', 'REM': 'purple'}
        stage_colors = [colors.get(label, 'black') for label in stage_labels]
        
        ax1.bar(times, [1] * len(times), color=stage_colors, width=0.02)
        ax1.set_xlabel(' ()')
        ax1.set_ylabel('sleep')
        ax1.set_title('sleep')
        ax1.set_ylim(0, 1.2)
        
        # 
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, label=label) 
                          for label, color in colors.items()]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        # 2. 
        unique_labels, counts = np.unique(stage_labels, return_counts=True)
        ax2.pie(counts, labels=unique_labels, autopct='%1.1f%%', 
                colors=[colors.get(label, 'gray') for label in unique_labels])
        ax2.set_title('sleep')
        
        plt.tight_layout()
        plot_path = os.path.join(output_dir, 'sleep_staging_histogram.png')
        plt.close()
        
        print(f"   sleep: {plot_path}")
        
    except Exception as e:
        print(f"   : {str(e)}")

def _create_text_report(self, report, output_dir):
    """"""
    
    try:
        txt_path = os.path.join(output_dir, 'sleep_staging_summary.txt')
        
            
            
            
            if report['sleep_structure']['rem_latency_minutes']:
            else:
            
            for stage, percentage in report['sleep_structure']['stage_percentages'].items():
            
            
            
        
        print(f"   : {txt_path}")
        
    except Exception as e:
        print(f"   : {str(e)}")

def main():
    """function"""
    # 
    import sys
    import io
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if len(sys.argv) > 1:
        edf_path = sys.argv[1]
    else:
        edf_path = r"D:\openclaw\AISleepGen\data\edf\SC4001E0-PSG.edf"
    
    print("sleepanalysis...")
    
    # 
    analyzer = SleepStagingAnalyzer()
    result = analyzer.sleep_staging_analysis(edf_path)
    
    if result:
        print("analysis!")
    else:
        print("analysis!")
        sys.exit(1)

class SleepStagingAnalyzer:
    """sleepanalysis"""
    
    def __init__(self):
        pass
    
    # 
    def sleep_staging_analysis(self, edf_path):
        # 
        # £¬
        return sleep_staging_analysis(edf_path)
    
    def _calculate_band_power(self, signal, sfreq, low_freq, high_freq):
        return _calculate_band_power(signal, sfreq, low_freq, high_freq)
    
    def _classify_sleep_stage(self, features):
        return _classify_sleep_stage(features)
    
    def _get_stage_label(self, stage_code):
        return _get_stage_label(stage_code)
    
    def _calculate_sleep_continuity(self, sleep_stages, epoch_features):
        return _calculate_sleep_continuity(sleep_stages, epoch_features)
    
    def _create_sleep_histogram(self, sleep_stages, epoch_features, output_dir):
        return _create_sleep_histogram(sleep_stages, epoch_features, output_dir)
    
    def _create_text_report(self, report, output_dir):
        return _create_text_report(report, output_dir)

# £¨£©
def _calculate_band_power(signal, sfreq, low_freq, high_freq):
    """power£¨£©"""
    from scipy import signal as sp_signal
    
    # 
    nyquist = sfreq / 2
    b, a = sp_signal.butter(4, [low_freq/nyquist, high_freq/nyquist], btype='band')
    
    # 
    filtered = sp_signal.filtfilt(b, a, signal)
    
    # 
    power = np.mean(filtered ** 2)
    return power

def _classify_sleep_stage(features):
    """based onsleep£¨£©"""
    
    # 
    alpha_ratio = features['alpha_power'] / (features['delta_power'] + 1e-10)
    delta_ratio = features['delta_power'] / (features['alpha_power'] + 1e-10)
    sigma_ratio = features['sigma_power'] / (features['theta_power'] + 1e-10)
    
    # 
    if features['mean_amplitude'] < 10:  # data
        return 7  # 
    
    # alphaN1
    if alpha_ratio > 0.5:
        return 0  # Wake
    
    # delta£¨N3£©
    elif delta_ratio > 2.0:
        return 3  # N3
    
    # sigma£¨£©N2
    elif 0.3 < sigma_ratio < 1.5:
        return 2  # N2
    
    # REM
    elif features['mean_amplitude'] < 30 and 0.1 < alpha_ratio < 0.3:
        return 4  # REM
    
    # N1£¨£©
    else:
        return 1  # N1

def _get_stage_label(stage_code):
    """sleep"""
    stage_labels = {
        0: 'Wake',
        1: 'N1',
        2: 'N2', 
        3: 'N3',
        4: 'REM',
        5: 'N4',  # standard£¬N3
        6: 'Movement',
        7: 'Unscored'
    }
    return stage_labels.get(stage_code, 'Unknown')

def _calculate_sleep_continuity(sleep_stages, epoch_features):
    """sleep"""
    
    if not sleep_stages:
        return {
            'total_sleep_time': 0,
            'sleep_efficiency': 0,
            'sleep_latency': 0,
            'wake_after_sleep_onset': 0,
            'rem_latency': None
        }
    
    # £¨Wake£©
    first_sleep_idx = None
    for i, stage in enumerate(sleep_stages):
        if stage != 0:  # Wake
            first_sleep_idx = i
            break
    
    # REM
    first_rem_idx = None
    for i, stage in enumerate(sleep_stages):
        if stage == 4:  # REM
            first_rem_idx = i
            break
    
    # 
    total_epochs = len(sleep_stages)
    sleep_epochs = len([s for s in sleep_stages if s != 0])  # Wakesleep
    
    # epoch 30
    epoch_duration = 30
    
    total_sleep_time = sleep_epochs * epoch_duration
    total_recording_time = total_epochs * epoch_duration
    
    sleep_efficiency = total_sleep_time / total_recording_time if total_recording_time > 0 else 0
    
    # £¨£©
    sleep_latency = first_sleep_idx * epoch_duration if first_sleep_idx is not None else total_recording_time
    
    # REM£¨REM£©
    rem_latency = None
    if first_sleep_idx is not None and first_rem_idx is not None and first_rem_idx > first_sleep_idx:
        rem_latency = (first_rem_idx - first_sleep_idx) * epoch_duration
    
    # £¨£©
    # Wake
    wake_after_sleep = 0
    if first_sleep_idx is not None:
        for i in range(first_sleep_idx, len(sleep_stages)):
            if sleep_stages[i] == 0:
                wake_after_sleep += epoch_duration
    
    return {
        'total_sleep_time': total_sleep_time,
        'sleep_efficiency': sleep_efficiency,
        'sleep_latency': sleep_latency,
        'wake_after_sleep_onset': wake_after_sleep,
        'rem_latency': rem_latency
    }

def _create_sleep_histogram(sleep_stages, epoch_features, output_dir):
    """sleep"""
    
    if not sleep_stages:
        return
    
    try:
        # 
        stage_labels = [_get_stage_label(s) for s in sleep_stages]
        times = [feat['start_time'] / 3600 for feat in epoch_features]  # 
        
        # 
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # 1. 
        colors = {'Wake': 'gray', 'N1': 'blue', 'N2': 'green', 'N3': 'red', 'REM': 'purple'}
        stage_colors = [colors.get(label, 'black') for label in stage_labels]
        
        ax1.bar(times, [1] * len(times), color=stage_colors, width=0.02)
        ax1.set_xlabel(' ()')
        ax1.set_ylabel('sleep')
        ax1.set_title('sleep')
        ax1.set_ylim(0, 1.2)
        
        # 
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, label=label) 
                          for label, color in colors.items()]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        # 2. 
        unique_labels, counts = np.unique(stage_labels, return_counts=True)
        ax2.pie(counts, labels=unique_labels, autopct='%1.1f%%', 
                colors=[colors.get(label, 'gray') for label in unique_labels])
        ax2.set_title('sleep')
        
        plt.tight_layout()
        plot_path = os.path.join(output_dir, 'sleep_staging_histogram.png')
        plt.close()
        
        print(f"   sleep: {plot_path}")
        
    except Exception as e:
        print(f"   : {str(e)}")

def _create_text_report(report, output_dir):
    """"""
    
    try:
        txt_path = os.path.join(output_dir, 'sleep_staging_summary.txt')
        
            
            
            
            if report['sleep_structure']['rem_latency_minutes']:
            else:
            
            for stage, percentage in report['sleep_structure']['stage_percentages'].items():
            
            
            
        
        print(f"   : {txt_path}")
        
    except Exception as e:
        print(f"   : {str(e)}")

if __name__ == "__main__":
    main()

