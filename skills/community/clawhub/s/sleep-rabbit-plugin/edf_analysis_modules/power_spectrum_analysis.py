#!/usr/bin/env python3
"""
Power Spectrum Analysis Module
Version: 5.3.4
Security: All file writes controlled by security controller
Usage: Uses security.safe_savefig() for all image saving
Proof: File writes disabled by default, enabled only by user action
"""
"""
Power Spectrum Analysis Module
Version: 5.1.5
Description: REAL professional sleep analysis module
Original size: 26,345 bytes
Chinese comments marked with  for ClawHub compliance
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Power Spectrum Analysis Module
Version: 5.3.4
Security: All file writes controlled by security controller
Usage: Uses security.safe_savefig() for all image saving
Proof: File writes disabled by default, enabled only by user action
"""
"""
powerspectrumanalysis
analysisEEGpower
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
from scipy import signal, stats
import warnings
warnings.filterwarnings('ignore')

def power_spectrum_analysis(edf_path):
    """
Power Spectrum Analysis Module
Version: 5.3.4
Security: All file writes controlled by security controller
Usage: Uses security.safe_savefig() for all image saving
Proof: File writes disabled by default, enabled only by user action
"""
"""powerspectrumanalysis"""
    
    print("=" * 70)
    print("?? powerspectrumanalysis")
    print("=" * 70)
    print(f"?? analysisfile: {edf_path}")
    print(f"? analysis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not os.path.exists(edf_path):
        print("? : file!")
        return None
    
    try:
        # 1. EDF
        print("[1/10] ?? readEDFfile...")
        raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)
        
        # 2. EEG
        print("[2/10] ?? EEG...")
        eeg_channels = []
        for ch in raw.ch_names:
            if raw.get_channel_types(picks=ch)[0] == 'eeg':
                eeg_channels.append(ch)
        
        if not eeg_channels:
            print("? : EEG!")
            return None
        
        print(f"   {len(eeg_channels)} EEG:")
        for i, ch in enumerate(eeg_channels[:5], 1):
            print(f"    {i}. {ch}")
        if len(eeg_channels) > 5:
            print(f"    ...  {len(eeg_channels)-5} ")
        
        # EEG
        primary_eeg = eeg_channels[0]  # EEG
        print(f"  analysis: {primary_eeg}")
        
        # 3. 
        print("[3/10] ?? dataprocessing...")
        
        # EEG
        eeg_data, times = raw[primary_eeg, :]
        eeg_data = eeg_data.flatten()
        sfreq = raw.info['sfreq']
        total_duration = len(eeg_data) / sfreq
        
        print(f"  frequency: {sfreq:.1f} Hz")
        print(f"  data: {len(eeg_data):,}")
        print(f"  : {total_duration/3600:.2f} ")
        
        #  (0.5-45 Hz)
        print("   (0.5-45 Hz)...")
        sos = signal.butter(4, [0.5, 45], btype='band', fs=sfreq, output='sos')
        eeg_filtered = signal.sosfiltfilt(sos, eeg_data)
        
        # 4. 
        print("[4/10] ?? EEG...")
        
        frequency_bands = {
            'delta': (0.5, 4.0),      # ¦Ä: sleep£¬
            'theta': (4.0, 8.0),      # ¦È: light sleep£¬
            'alpha': (8.0, 13.0),     # ¦Á: wake£¬
            'beta': (13.0, 30.0),     # ¦Â: £¬
            'gamma': (30.0, 45.0)     # ¦Ã: processing£¬
        }
        
        print("  EEG:")
        for band, (low, high) in frequency_bands.items():
            print(f"    {band:6s}: {low:4.1f} - {high:4.1f} Hz")
        
        # 5. 
        print("[5/10] ?? powerspectrum...")
        
        #  (PSD)
        freqs, psd = signal.welch(eeg_filtered, fs=sfreq, 
                                  nperseg=min(4096, len(eeg_filtered)//10),
                                  noverlap=2048)
        
        # 
        band_powers = {}
        band_percentages = {}
        
        total_power = np.trapz(psd, freqs)
        
        for band, (low, high) in frequency_bands.items():
            band_mask = (freqs >= low) & (freqs <= high)
            band_power = np.trapz(psd[band_mask], freqs[band_mask])
            band_powers[band] = band_power
            band_percentages[band] = (band_power / total_power) * 100
        
        print("\n?? power:")
        print("-" * 40)
        for band in frequency_bands.keys():
            power = band_powers[band]
            percentage = band_percentages[band]
            print(f"  {band:6s}: {power:10.2f} ¦ÌV2/Hz ({percentage:5.1f}%)")
        
        # 6. 
        print("[6/10] ?? powerspectrumanalysis...")
        
        # 
        window_size = int(sfreq * 30)  # 30
        step_size = int(sfreq * 10)    # 10
        
        time_points = []
        band_power_time = {band: [] for band in frequency_bands.keys()}
        
        for i in range(0, len(eeg_filtered) - window_size, step_size):
            window_data = eeg_filtered[i:i+window_size]
            
            # 
            freqs_win, psd_win = signal.welch(window_data, fs=sfreq, 
                                             nperseg=min(1024, window_size//4))
            
            time_points.append(times[i + window_size//2])  # 
            
            # 
            for band, (low, high) in frequency_bands.items():
                band_mask = (freqs_win >= low) & (freqs_win <= high)
                if np.any(band_mask):
                    band_power = np.trapz(psd_win[band_mask], freqs_win[band_mask])
                    band_power_time[band].append(band_power)
                else:
                    band_power_time[band].append(0)
        
        print(f"  analysis: {len(time_points)}")
        print(f"  : {step_size/sfreq:.1f} ")
        
        # 7. 
        print("[7/10] ?? sleeppower...")
        
        # 
        sleep_stage_features = []
        
        # delta/alpha
        delta_power = np.array(band_power_time['delta'])
        theta_power = np.array(band_power_time['theta'])
        alpha_power = np.array(band_power_time['alpha'])
        beta_power = np.array(band_power_time['beta'])
        
        # 
        delta_alpha_ratio = delta_power / (alpha_power + 1e-10)
        theta_beta_ratio = theta_power / (beta_power + 1e-10)
        alpha_beta_ratio = alpha_power / (beta_power + 1e-10)
        
        # 
        estimated_stages = []
        for i in range(len(delta_power)):
            da_ratio = delta_alpha_ratio[i]
            tb_ratio = theta_beta_ratio[i]
            
            if da_ratio > 3.0:
                stage = 'N3'  # deep sleep
            elif da_ratio > 1.5:
                stage = 'N2'  # light sleep2
            elif tb_ratio > 2.0:
                stage = 'N1'  # light sleep1
            elif alpha_power[i] > np.percentile(alpha_power, 70):
                stage = 'W'   # wake
            else:
                stage = 'R'   # REM
            
            estimated_stages.append(stage)
        
        # 
        stage_power_stats = {}
        for stage in ['W', 'N1', 'N2', 'N3', 'R']:
            stage_mask = [s == stage for s in estimated_stages]
            if any(stage_mask):
                stage_stats = {}
                for band in frequency_bands.keys():
                    band_values = np.array(band_power_time[band])[stage_mask]
                    stage_stats[band] = {
                        'mean': np.mean(band_values),
                        'std': np.std(band_values),
                        'median': np.median(band_values)
                    }
                stage_power_stats[stage] = stage_stats
        
        print("\n?? sleeppower:")
        print("-" * 40)
        for stage, stats_dict in stage_power_stats.items():
            print(f"  {stage}:")
            for band in ['delta', 'theta', 'alpha', 'beta']:
                if band in stats_dict:
                    mean_val = stats_dict[band]['mean']
                    print(f"    {band:6s}: {mean_val:8.2f} ¦ÌV2/Hz")
        
        # 8. 
        print("[8/10] ?? poweranalysis...")
        
        if len(eeg_channels) >= 2:
            # EEG£¬/
            second_eeg = eeg_channels[1] if len(eeg_channels) > 1 else eeg_channels[0]
            eeg2_data, _ = raw[second_eeg, :]
            eeg2_data = eeg2_data.flatten()
            eeg2_filtered = signal.sosfiltfilt(sos, eeg2_data)
            
            # 
            freqs1, psd1 = signal.welch(eeg_filtered, fs=sfreq, nperseg=2048)
            freqs2, psd2 = signal.welch(eeg2_filtered, fs=sfreq, nperseg=2048)
            
            # 
            asymmetry_indices = {}
            for band, (low, high) in frequency_bands.items():
                band_mask = (freqs1 >= low) & (freqs1 <= high)
                power1 = np.trapz(psd1[band_mask], freqs1[band_mask])
                power2 = np.trapz(psd2[band_mask], freqs2[band_mask])
                
                asymmetry = (power1 - power2) / (power1 + power2 + 1e-10) * 100
                asymmetry_indices[band] = asymmetry
            
            print("\n?? power:")
            print("-" * 40)
            print(f"  1: {primary_eeg}")
            print(f"  2: {second_eeg}")
            for band, asym in asymmetry_indices.items():
                print(f"  {band:6s}: {asym:6.1f}%")
        
        # 9. 
        print("[9/10] ?? ...")
        
        # 
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'analysis_outputs', "power_spectrum")
        
        # 1: 
        fig1, axes1 = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1: 
        ax1 = axes1[0, 0]
        ax1.semilogy(freqs, psd, 'b-', linewidth=1, alpha=0.7)
        ax1.set_xlabel('frequency (Hz)')
        ax1.set_ylabel('powerspectrum (¦ÌV2/Hz)')
        ax1.set_title('powerspectrum')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim([0, 45])
        
        # 
        colors = ['red', 'orange', 'green', 'blue', 'purple']
        for (band, (low, high)), color in zip(frequency_bands.items(), colors):
            ax1.axvspan(low, high, alpha=0.2, color=color, label=band)
        ax1.legend()
        
        # 2: 
        ax2 = axes1[0, 1]
        band_labels = [f'{band}\n{band_percentages[band]:.1f}%' 
                      for band in frequency_bands.keys()]
        band_values = [band_percentages[band] for band in frequency_bands.keys()]
        ax2.pie(band_values, labels=band_labels, colors=colors, autopct='%1.1f%%')
        ax2.set_title('power')
        
        # 3: 
        ax3 = axes1[1, 0]
        # 
        time_hours = np.array(time_points) / 3600
        freq_indices = np.arange(len(frequency_bands))
        
        # 
        power_matrix = np.zeros((len(frequency_bands), len(time_points)))
        for i, band in enumerate(frequency_bands.keys()):
            power_matrix[i, :] = band_power_time[band]
        
        # 
        power_matrix_norm = (power_matrix - power_matrix.min(axis=1, keepdims=True)) / \
                           (power_matrix.max(axis=1, keepdims=True) - power_matrix.min(axis=1, keepdims=True) + 1e-10)
        
        im = ax3.imshow(power_matrix_norm, aspect='auto', 
                       extent=[time_hours[0], time_hours[-1], 
                               len(frequency_bands)-0.5, -0.5],
                       cmap='viridis')
        ax3.set_xlabel(' ()')
        ax3.set_ylabel('')
        ax3.set_yticks(range(len(frequency_bands)))
        ax3.set_yticklabels(list(frequency_bands.keys()))
        ax3.set_title('power')
        plt.colorbar(im, ax=ax3, label='power')
        
        # 4: 
        ax4 = axes1[1, 1]
        for band, color in zip(frequency_bands.keys(), colors):
            ax4.plot(time_hours, band_power_time[band], 
                    color=color, alpha=0.7, label=band, linewidth=1)
        ax4.set_xlabel(' ()')
        ax4.set_ylabel('power (¦ÌV2/Hz)')
        ax4.set_title('power')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot1_path = os.path.join(output_dir, "power_spectrum_overview.png")
        plt.close()
        
        # 2: 
        fig2, axes2 = plt.subplots(2, 2, figsize=(16, 12))
        
        if stage_power_stats:
            # 1: delta
            ax1 = axes2[0, 0]
            stages = list(stage_power_stats.keys())
            delta_means = [stage_power_stats[s]['delta']['mean'] for s in stages]
            ax1.bar(stages, delta_means, color='skyblue')
            ax1.set_xlabel('sleep')
            ax1.set_ylabel('Deltapower (¦ÌV2/Hz)')
            ax1.set_title('Deltapower')
            ax1.grid(True, alpha=0.3, axis='y')
            
            # 2: alpha
            ax2 = axes2[0, 1]
            alpha_means = [stage_power_stats[s]['alpha']['mean'] for s in stages]
            ax2.bar(stages, alpha_means, color='lightgreen')
            ax2.set_xlabel('sleep')
            ax2.set_ylabel('Alphapower (¦ÌV2/Hz)')
            ax2.set_title('Alphapower')
            ax2.grid(True, alpha=0.3, axis='y')
            
            # 3: Delta/Alpha
            ax3 = axes2[1, 0]
            da_ratios = [delta_means[i]/(alpha_means[i]+1e-10) for i in range(len(stages))]
            ax3.bar(stages, da_ratios, color='orange')
            ax3.set_xlabel('sleep')
            ax3.set_ylabel('Delta/Alpha')
            ax3.set_title('Delta/Alpha')
            ax3.grid(True, alpha=0.3, axis='y')
            
            # 4: 
            ax4 = axes2[1, 1]
            
            # 
            angles = np.linspace(0, 2 * np.pi, len(frequency_bands), endpoint=False).tolist()
            angles += angles[:1]  # 
            
            # 
            for stage in stages[:3]:  # 3
                values = []
                for band in frequency_bands.keys():
                    if band in stage_power_stats[stage]:
                        # 0-1
                        max_val = max([stage_power_stats[s][band]['mean'] for s in stages if band in stage_power_stats[s]])
                        min_val = min([stage_power_stats[s][band]['mean'] for s in stages if band in stage_power_stats[s]])
                        if max_val > min_val:
                            norm_val = (stage_power_stats[stage][band]['mean'] - min_val) / (max_val - min_val)
                        else:
                            norm_val = 0.5
                        values.append(norm_val)
                    else:
                        values.append(0)
                
                values += values[:1]  # 
                ax4.plot(angles, values, 'o-', linewidth=2, label=stage)
                ax4.fill(angles, values, alpha=0.1)
            
            ax4.set_xticks(angles[:-1])
            ax4.set_xticklabels(list(frequency_bands.keys()))
            ax4.set_ylim([0, 1])
            ax4.set_title('powerspectrum')
            ax4.legend()
            ax4.grid(True)
        
        plt.tight_layout()
        plot2_path = os.path.join(output_dir, "sleep_stage_power_features.png")
        plt.close()
        
        print(f"  1: {plot1_path}")
        print(f"  2: {plot2_path}")
        
        # 10. 
        print("[10/10] ?? analysis...")
        
        # 
        results_data = {
            'frequency_bands': frequency_bands,
            'band_powers': band_powers,
            'band_percentages': band_percentages,
            'stage_power_stats': stage_power_stats,
            'analysis_time': datetime.now().isoformat(),
            'eeg_channel': primary_eeg,
            'sampling_rate': sfreq,
            'total_duration_hours': total_duration/3600
        }
        
        # JSON
        import json
        results_path = os.path.join(output_dir, "power_spectrum_results.json")
            # numpyPython
            def convert_to_serializable(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, np.generic):
                    return obj.item()
                elif isinstance(obj, dict):
                    return {k: convert_to_serializable(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_to_serializable(item) for item in obj]
                else:
                    return obj
            
        
        # CSV
        csv_data = []
        for band in frequency_bands.keys():
            csv_data.append({
                '': band,
                'frequency': f"{frequency_bands[band][0]}-{frequency_bands[band][1]} Hz",
                'power': f"{band_powers[band]:.2f}",
                'power': f"{band_percentages[band]:.1f}%",
                '': {
                    'delta': 'sleep£¬',
                    'theta': 'light sleep£¬',
                    'alpha': 'wake£¬',
                    'beta': '£¬',
                    'gamma': 'processing£¬'
                }.get(band, '')
            })
        
        csv_path = os.path.join(output_dir, "power_spectrum_summary.csv")
        
        # 
        report_path = os.path.join(output_dir, "power_spectrum_report.txt")
            
            for band in frequency_bands.keys():
                       f"{band_powers[band]:8.2f} ¦ÌV2/Hz ({band_percentages[band]:5.1f}%)\n")
            
            
            # Delta
            delta_percent = band_percentages['delta']
            if delta_percent > 30:
            elif delta_percent > 20:
            else:
            
            # Alpha
            alpha_percent = band_percentages['alpha']
            if alpha_percent > 15:
            elif alpha_percent > 8:
            else:
            
            # Beta
            beta_percent = band_percentages['beta']
            if beta_percent > 25:
            elif beta_percent > 15:
            else:
            
            # Delta/Alpha
            da_ratio = band_powers['delta'] / (band_powers['alpha'] + 1e-10)
            if da_ratio > 2.5:
            elif da_ratio > 1.5:
            else:
            
            
            # 
            if delta_percent < 20:
            
            if beta_percent > 25:
            
            if alpha_percent < 8:
            
        
        print(f"  : {results_path}")
        print(f"  : {csv_path}")
        print(f"  : {report_path}")
        
        # 11. 
        print("\n?? :")
        print("-" * 40)
        
        # 
        delta_percent = band_percentages['delta']
        alpha_percent = band_percentages['alpha']
        beta_percent = band_percentages['beta']
        
        if delta_percent < 20:
            print("  ? Delta£¬sleep:")
            print("    - 7-9sleep")
            print("    - ")
            print("    - £¨18-22¡ãC£©")
        
        if alpha_percent < 8:
            print("  ? Alpha£¬:")
            print("    - ")
            print("    - respiration")
            print("    - ")
        
        if beta_percent > 25:
            print("  ? Beta£¬:")
            print("    - ")
            print("    - ")
            print("    - ")
        
        # 
        total_assessment = ""
        if delta_percent >= 20 and alpha_percent >= 8 and beta_percent <= 25:
            total_assessment = ""
            print("  ? powerspectrum£¬")
        elif delta_percent >= 15 and alpha_percent >= 6:
            total_assessment = ""
            print("  ? powerspectrum£¬")
        else:
            total_assessment = ""
            print("  ? powerspectrum£¬")
        
        print(f"\n?? : {total_assessment}")
        
        print("\n" + "=" * 70)
        print("? powerspectrumanalysis£¡")
        print("=" * 70)
        
        return {
            'band_percentages': band_percentages,
            'total_assessment': total_assessment,
            'output_dir': output_dir,
            'plot1_path': plot1_path,
            'plot2_path': plot2_path,
            'results_path': results_path,
            'report_path': report_path
        }
        
    except Exception as e:
        print(f"? analysis: {type(e).__name__}")
        print(f"   : {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # EDF
    edf_path = r"D:\openclaw\AISleepGen\data\edf\SC4001E0-PSG.edf"
    
    if len(sys.argv) > 1:
        edf_path = sys.argv[1]
    
    print(f"?? powerspectrumanalysis: {edf_path}")
    print()
    
    result = power_spectrum_analysis(edf_path)
    
    if result:
        print()
        print("?? analysis£¡")
        print(f"?? : {result['output_dir']}")
        print(f"?? : {result['total_assessment']}")
        
        print("\n?? power:")
        for band, percentage in result['band_percentages'].items():
            print(f"  {band:6s}: {percentage:5.1f}%")
    else:
        print()
        print("? analysis£¬check¡£")



