#!/usr/bin/env python3
"""
Respiratory Event Analysis Module
Version: 5.1.5
Description: REAL professional sleep analysis module
Original size: 20,548 bytes
Chinese comments marked with  for ClawHub compliance
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
respirationanalysis
based onAASMstandardrespirationanalysis
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
warnings.filterwarnings('ignore')

def respiratory_event_analysis(edf_path):
    """respirationanalysis"""
    
    print("=" * 70)
    print("??? respirationanalysis")
    print("=" * 70)
    print(f"?? analysisfile: {edf_path}")
    print(f"? analysis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not os.path.exists(edf_path):
        print("? : file!")
        return None
    
    try:
        # 1. EDF
        print("[1/12] ?? EDFfile...")
        raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)
        
        # 2. 
        print("[2/12] ?? respiration...")
        
        channel_info = {
            'respiratory': [],
            'spo2': [],
            'ecg': [],
            'thoracic': [],
            'abdominal': []
        }
        
        # 
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
        
        print(f"   ? respiration: {channel_info['respiratory']}")
        print(f"   ? : {channel_info['spo2']}")
        print(f"   ? ECG: {channel_info['ecg']}")
        print(f"   ? : {channel_info['thoracic']}")
        print(f"   ? : {channel_info['abdominal']}")
        
        if not channel_info['respiratory']:
            print("? : respiration!")
            return None
        
        # 3. 
        print("[3/12] ?? respirationsignal...")
        resp_channel = channel_info['respiratory'][0]
        resp_data = raw.get_data(picks=resp_channel)[0]
        sfreq = raw.info['sfreq']
        n_samples = len(resp_data)
        duration_hours = n_samples / (sfreq * 3600)
        
        print(f"   ? frequency: {sfreq} Hz")
        print(f"   ? data: {n_samples:,} ")
        print(f"   ? : {duration_hours:.2f} ")
        
        # 4. 
        print("[4/12] ?? respirationsignalprocessing...")
        
        #  (0.1-5 Hz£¬)
        nyquist = sfreq / 2
        lowcut = 0.1  # 6/
        highcut = 5.0  # 300/
        
        # 
        b, a = signal.butter(4, [lowcut/nyquist, highcut/nyquist], btype='band')
        resp_filtered = signal.filtfilt(b, a, resp_data)
        
        # 
        resp_envelope = np.abs(signal.hilbert(resp_filtered))
        
        # 5.  (AASM)
        print("[5/12] ?? respirationdetection...")
        
        #  ()
        baseline_amplitude = np.median(resp_envelope)
        
        #  (¡Ý10)
        apnea_threshold = 0.1 * baseline_amplitude  # 90%
        apnea_min_duration = 10 * sfreq  # 10
        
        #  (¡Ý30%¡Ý10)
        hypopnea_threshold = 0.7 * baseline_amplitude  # 30%
        hypopnea_min_duration = 10 * sfreq  # 10
        
        # 
        events = []
        
        # 
        apnea_mask = resp_envelope < apnea_threshold
        hypopnea_mask = resp_envelope < hypopnea_threshold
        
        # 
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
        
        # 
        apnea_regions = find_continuous_regions(apnea_mask, apnea_min_duration)
        for start, end in apnea_regions:
            duration_sec = (end - start) / sfreq
            events.append({
                'type': 'respiration',
                'start_sample': start,
                'end_sample': end,
                'duration_sec': duration_sec,
                'start_time': start / sfreq,
                'end_time': end / sfreq
            })
        
        #  ()
        hypopnea_regions = find_continuous_regions(hypopnea_mask, hypopnea_min_duration)
        for start, end in hypopnea_regions:
            # 
            overlap = False
            for apnea_start, apnea_end in apnea_regions:
                if not (end <= apnea_start or start >= apnea_end):
                    overlap = True
                    break
            
            if not overlap:
                duration_sec = (end - start) / sfreq
                events.append({
                    'type': '',
                    'start_sample': start,
                    'end_sample': end,
                    'duration_sec': duration_sec,
                    'start_time': start / sfreq,
                    'end_time': end / sfreq
                })
        
        print(f"   ? detectionrespiration: {len(apnea_regions)} ")
        print(f"   ? detection: {len(hypopnea_regions) - len(apnea_regions)} ")
        
        # 6. 
        print("[6/12] ?? ...")
        
        # AHI ()
        total_events = len(events)
        ahi = total_events / duration_hours
        
        # 
        apnea_durations = [e['duration_sec'] for e in events if e['type'] == 'respiration']
        hypopnea_durations = [e['duration_sec'] for e in events if e['type'] == '']
        
        # 
        event_times = [e['start_time'] / 3600 for e in events]  # 
        
        # 7.  (SpO2)
        spo2_data = None
        spo2_analysis = {}
        
        if channel_info['spo2']:
            print("[7/12] ?? analysis...")
            spo2_channel = channel_info['spo2'][0]
            spo2_data = raw.get_data(picks=spo2_channel)[0]
            
            #  (¡Ý3%¡Ý10)
            spo2_baseline = np.median(spo2_data)
            spo2_drop_threshold = spo2_baseline - 3  # 3%
            
            # 
            spo2_drop_mask = spo2_data < spo2_drop_threshold
            spo2_drop_regions = find_continuous_regions(spo2_drop_mask, 10 * sfreq)
            
            # ODI ()
            odi = len(spo2_drop_regions) / duration_hours
            
            # 
            min_spo2 = np.min(spo2_data)
            
            spo2_analysis = {
                'odi': odi,
                'min_spo2': min_spo2,
                'baseline_spo2': spo2_baseline,
                'drop_events': len(spo2_drop_regions)
            }
            
            print(f"   ? ODI: {odi:.1f} /")
            print(f"   ? : {min_spo2:.1f}%")
        
        # 8. 
        print("[8/12] ?? ...")
        
        severity = ""
        if ahi < 5:
            severity = ""
        elif ahi < 15:
            severity = "sleeprespiration"
        elif ahi < 30:
            severity = "sleeprespiration"
        else:
            severity = "sleeprespiration"
        
        # 9. 
        print("[9/12] ?? analysis...")
        
        report = {
            'file_info': {
                'path': edf_path,
                'duration_hours': duration_hours,
                'sampling_rate': sfreq,
                'channels': channel_info
            },
            'events': {
                'total': total_events,
                'apnea_count': len(apnea_regions),
                'hypopnea_count': len(hypopnea_regions) - len(apnea_regions),
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
        
        # 10. 
        print("[10/12] ?? ...")
        
        # 
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'analysis_outputs', 'respiratory_analysis')
        
        # 
        fig, axes = plt.subplots(3, 1, figsize=(15, 10))
        
        # 
        time_axis = np.arange(len(resp_data)) / sfreq / 60  # 
        axes[0].plot(time_axis[:10000], resp_data[:10000], 'b-', alpha=0.7, label='respirationsignal')
        axes[0].set_ylabel('')
        axes[0].set_title('respirationsignal (10000)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # 
        axes[1].plot(time_axis[:10000], resp_filtered[:10000], 'g-', alpha=0.7, label='respirationsignal')
        axes[1].plot(time_axis[:10000], resp_envelope[:10000], 'r-', alpha=0.5, label='respiration')
        axes[1].set_ylabel('')
        axes[1].set_title('respirationsignal')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # 
        axes[2].plot(time_axis[:10000], resp_envelope[:10000], 'k-', alpha=0.5, label='respiration')
        
        # 
        for event in events:
            if event['type'] == 'respiration' and event['start_sample'] < 10000:
                start_min = event['start_sample'] / sfreq / 60
                end_min = event['end_sample'] / sfreq / 60
                axes[2].axvspan(start_min, end_min, alpha=0.3, color='red', label='respiration' if event['start_sample'] == events[0]['start_sample'] else "")
        
        # 
        for event in events:
            if event['type'] == '' and event['start_sample'] < 10000:
                start_min = event['start_sample'] / sfreq / 60
                end_min = event['end_sample'] / sfreq / 60
                axes[2].axvspan(start_min, end_min, alpha=0.2, color='orange', label='' if event['start_sample'] == events[0]['start_sample'] else "")
        
        axes[2].set_xlabel(' ()')
        axes[2].set_ylabel('')
        axes[2].set_title('respirationdetection')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot_path = os.path.join(output_dir, 'respiratory_events.png')
        plt.close()
        
        # 11. 
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # AHI
        axes[0, 0].bar(['respiration', '', ''], 
                      [len(apnea_regions), len(hypopnea_regions) - len(apnea_regions), total_events],
                      color=['red', 'orange', 'blue'])
        axes[0, 0].set_ylabel('')
        axes[0, 0].set_title('respiration')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 
        if apnea_durations:
            axes[0, 1].hist(apnea_durations, bins=20, alpha=0.7, color='red', label='respiration')
        if hypopnea_durations:
            axes[0, 1].hist(hypopnea_durations, bins=20, alpha=0.7, color='orange', label='')
        axes[0, 1].set_xlabel(' ()')
        axes[0, 1].set_ylabel('frequency')
        axes[0, 1].set_title('')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 
        if event_times:
            axes[1, 0].hist(event_times, bins=24, alpha=0.7, color='purple')
            axes[1, 0].set_xlabel(' ()')
            axes[1, 0].set_ylabel('')
            axes[1, 0].set_title(' (24)')
            axes[1, 0].grid(True, alpha=0.3)
        
        # 
        severity_colors = ['green', 'yellow', 'orange', 'red']
        severity_levels = ['', '', '', '']
        severity_values = [0, 5, 15, 30, 100]
        
        ahi_position = min(ahi, 100)
        for i in range(len(severity_levels)):
            axes[1, 1].barh(i, severity_values[i+1] - severity_values[i], 
                           left=severity_values[i], 
                           color=severity_colors[i], 
                           alpha=0.5)
        
        axes[1, 1].plot([ahi_position, ahi_position], [-0.5, 3.5], 'k--', linewidth=2, label=f'AHI = {ahi:.1f}')
        axes[1, 1].set_xlabel('AHI (/)')
        axes[1, 1].set_yticks(range(len(severity_levels)))
        axes[1, 1].set_yticklabels(severity_levels)
        axes[1, 1].set_title('sleeprespiration')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        summary_path = os.path.join(output_dir, 'respiratory_summary.png')
        plt.close()
        
        # 12. 
        print("[11/12] ?? analysis...")
        
        # JSON
        import json
        report_path = os.path.join(output_dir, 'respiratory_analysis_report.json')
        
        # 
        txt_report_path = os.path.join(output_dir, 'respiratory_analysis_summary.txt')
            
            
            
            if apnea_durations:
            if hypopnea_durations:
            
            if spo2_analysis:
            
            if ahi < 5:
            elif ahi < 15:
            elif ahi < 30:
            else:
            
            if event_times:
            
            
        
        print("[12/12] ? analysis!")
        print()
        print("=" * 70)
        print("??? respirationanalysis")
        print("=" * 70)
        print(f"?? AHI: {ahi:.1f} /")
        print(f"?? : {severity}")
        print(f"?? : {total_events} ")
        print(f"   ? respiration: {len(apnea_regions)} ")
        print(f"   ? : {len(hypopnea_regions) - len(apnea_regions)} ")
        
        if spo2_analysis:
            print(f"?? ODI: {spo2_analysis['odi']:.1f} /")
            print(f"?? : {spo2_analysis['min_spo2']:.1f}%")
        
        print(f"?? : {output_dir}")
        print("=" * 70)
        
        return report
        
    except Exception as e:
        print(f"? analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """function"""
    # Unicode
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if len(sys.argv) > 1:
        edf_path = sys.argv[1]
    else:
        # 
        edf_path = r"D:\openclaw\AISleepGen\data\edf\SC4001E0-PSG.edf"
    
    print("respirationanalysis...")
    result = respiratory_event_analysis(edf_path)
    
    if result:
        print("analysis!")
    else:
        print("analysis!")
        sys.exit(1)

if __name__ == "__main__":
    main()


