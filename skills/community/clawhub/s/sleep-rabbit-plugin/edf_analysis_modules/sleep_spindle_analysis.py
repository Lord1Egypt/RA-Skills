#!/usr/bin/env python3
"""
Sleep Spindle Analysis Module
Version: 5.1.5
Description: REAL professional sleep analysis module
Original size: 58,075 bytes
Chinese comments marked with  for ClawHub compliance
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sleepanalysis
respiration¡¢sleep¡¢analysis
based onAASMstandard£¬analysis£¬
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import mne
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal, stats
from scipy.signal import welch, butter, filtfilt, hilbert
import warnings
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import traceback

warnings.filterwarnings('ignore')

# ====================  ====================
@dataclass
class AnalysisConfig:
    """analysisparameter"""
    # 
    epoch_duration: int = 30  # 
    min_event_duration: int = 10  # 
    
    #  (Hz)
    freq_bands: Dict = None
    
    # 
    apnea_threshold: float = 0.1  # 90%
    hypopnea_threshold: float = 0.7  # 30%
    
    # 
    spindle_freq_range: Tuple = (11, 16)  # Hz
    spindle_duration_range: Tuple = (0.5, 3.0)  # 
    spindle_amplitude_threshold: float = 2.0  # standard
    
    # 
    spo2_drop_threshold: float = 3.0  # 
    spo2_drop_duration: int = 10  # 
    
    # 
    output_dir: str = "sleep_analysis_results"
    figure_dpi: int = 150
    save_intermediate: bool = False
    
    def __post_init__(self):
        if self.freq_bands is None:
            self.freq_bands = {
                'delta': (0.5, 4.0),
                'theta': (4.0, 8.0),
                'alpha': (8.0, 13.0),
                'sigma': (11.0, 16.0),
                'beta': (13.0, 30.0),
                'gamma': (30.0, 45.0)
            }

@dataclass
class SignalQuality:
    """signal"""
    channel: str
    snr: float
    artifact_percent: float
    flat_percent: float
    quality_score: float
    is_usable: bool

# ====================  ====================
def setup_logging(log_dir: str = "logs"):
    """"""
    log_file = os.path.join(log_dir, f"sleep_analysis_{datetime.now():%Y%m%d_%H%M%S}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# ====================  ====================
class SignalQualityAssessor:
    """signal"""
    
    def __init__(self, sfreq: float):
        self.sfreq = sfreq
        self.logger = logging.getLogger(__name__)
    
    def assess(self, data: np.ndarray, channel: str) -> SignalQuality:
        """signal"""
        try:
            # 1. 
            snr = self._calculate_snr(data)
            
            # 2. 
            artifact_percent = self._detect_artifacts(data)
            
            # 3. 
            flat_percent = self._detect_flat_lines(data)
            
            # 4. 
            quality_score = self._calculate_quality_score(
                snr, artifact_percent, flat_percent
            )
            
            return SignalQuality(
                channel=channel,
                snr=snr,
                artifact_percent=artifact_percent,
                flat_percent=flat_percent,
                quality_score=quality_score,
                is_usable=quality_score > 0.7
            )
            
        except Exception as e:
            self.logger.error(f"signal {channel}: {e}")
            return SignalQuality(channel, 0, 100, 100, 0, False)
    
    def _calculate_snr(self, data: np.ndarray) -> float:
        """"""
        try:
            # 
            signal_power = np.mean(data ** 2)
            
            # £¨£©
            freqs, psd = welch(data, self.sfreq, nperseg=min(256, len(data)))
            noise_mask = freqs > 30
            if np.any(noise_mask):
                noise_power = np.mean(psd[noise_mask])
            else:
                noise_power = np.percentile(psd, 10)
            
            snr = 10 * np.log10(signal_power / (noise_power + 1e-10))
            return max(0, snr)
            
        except Exception:
            return 0
    
    def _detect_artifacts(self, data: np.ndarray) -> float:
        """detection"""
        try:
            # 
            mean_amp = np.mean(np.abs(data))
            std_amp = np.std(data)
            
            # ¡À5
            artifact_mask = np.abs(data - mean_amp) > 5 * std_amp
            
            return np.sum(artifact_mask) / len(data) * 100
            
        except Exception:
            return 100
    
    def _detect_flat_lines(self, data: np.ndarray) -> float:
        """detection"""
        try:
            # 
            diff_data = np.diff(data)
            flat_mask = np.abs(diff_data) < 1e-6
            
            # 
            window = int(self.sfreq)  # 1
            conv = np.convolve(flat_mask.astype(int), np.ones(window), mode='same')
            flat_regions = conv > window * 0.9
            
            return np.sum(flat_regions) / len(data) * 100
            
        except Exception:
            return 100
    
    def _calculate_quality_score(self, snr: float, artifact: float, flat: float) -> float:
        """"""
        # 
        snr_score = min(snr / 20, 1.0)  # SNR 20dB
        artifact_score = max(1 - artifact / 50, 0)  # <50%
        flat_score = max(1 - flat / 20, 0)  # <20%
        
        # 
        quality = 0.4 * snr_score + 0.3 * artifact_score + 0.3 * flat_score
        return min(max(quality, 0), 1)

# ====================  ====================
class FeatureExtractor:
    """"""
    
    def __init__(self, sfreq: float, config: AnalysisConfig):
        self.sfreq = sfreq
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def extract_eeg_features(self, data: np.ndarray) -> Dict:
        """EEG"""
        features = {}
        
        try:
            # 
            features['mean'] = float(np.mean(data))
            features['std'] = float(np.std(data))
            features['variance'] = float(np.var(data))
            features['peak_to_peak'] = float(np.ptp(data))
            features['rms'] = float(np.sqrt(np.mean(data ** 2)))
            features['zero_crossing_rate'] = self._zero_crossing_rate(data)
            
            # 
            freqs, psd = welch(data, self.sfreq, nperseg=min(256, len(data)))
            total_power = np.trapz(psd, freqs)
            
            for band_name, (low, high) in self.config.freq_bands.items():
                mask = (freqs >= low) & (freqs <= high)
                if np.any(mask):
                    band_power = np.trapz(psd[mask], freqs[mask])
                    features[f'{band_name}_power'] = float(band_power)
                    features[f'{band_name}_ratio'] = float(
                        band_power / total_power if total_power > 0 else 0
                    )
                    
                    # 
                    peak_idx = np.argmax(psd[mask])
                    features[f'{band_name}_peak_freq'] = float(freqs[mask][peak_idx])
                else:
                    features[f'{band_name}_power'] = 0.0
                    features[f'{band_name}_ratio'] = 0.0
                    features[f'{band_name}_peak_freq'] = 0.0
            
            # 
            features['spectral_entropy'] = self._spectral_entropy(psd)
            
            # Hjorth
            hjorth = self._hjorth_parameters(data)
            features.update(hjorth)
            
        except Exception as e:
            self.logger.error(f"EEG: {e}")
            
        return features
    
    def extract_eog_features(self, data: np.ndarray) -> Dict:
        """EOG£¨£©"""
        features = {}
        
        try:
            # 
            features['rem_density'] = self._detect_rem(data)
            
            # 
            features['blink_rate'] = self._detect_blinks(data)
            
        except Exception:
            pass
            
        return features
    
    def extract_emg_features(self, data: np.ndarray) -> Dict:
        """EMG£¨£©"""
        features = {}
        
        try:
            # 
            features['emg_activity'] = float(np.mean(np.abs(data)))
            
            # 
            features['emg_variability'] = float(np.std(data))
            
        except Exception:
            pass
            
        return features
    
    def _zero_crossing_rate(self, data: np.ndarray) -> float:
        """"""
        return float(np.sum(np.diff(np.signbit(data))) / len(data))
    
    def _spectral_entropy(self, psd: np.ndarray) -> float:
        """spectrum"""
        psd_norm = psd / (np.sum(psd) + 1e-10)
        return float(-np.sum(psd_norm * np.log2(psd_norm + 1e-10)))
    
    def _hjorth_parameters(self, data: np.ndarray) -> Dict:
        """Hjorthparameter"""
        diff1 = np.diff(data)
        diff2 = np.diff(diff1)
        
        var0 = np.var(data)
        var1 = np.var(diff1)
        var2 = np.var(diff2)
        
        mobility = np.sqrt(var1 / (var0 + 1e-10))
        complexity = np.sqrt(var2 / (var1 + 1e-10)) / (mobility + 1e-10)
        
        return {
            'hjorth_mobility': float(mobility),
            'hjorth_complexity': float(complexity)
        }
    
    def _detect_rem(self, data: np.ndarray) -> float:
        """detectionREM£¨£©"""
        # 
        return float(np.std(data) / (np.mean(np.abs(data)) + 1e-10))
    
    def _detect_blinks(self, data: np.ndarray) -> float:
        """detection£¨£©"""
        # 
        return float(np.sum(np.abs(data) > 3 * np.std(data)) / len(data))

# ====================  ====================
class SleepStager:
    """sleep£¨based on+£©"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.stage_labels = {
            0: 'W', 1: 'N1', 2: 'N2', 3: 'N3', 4: 'R', 
            5: 'Movement', 6: 'Unscored'
        }
        
    def stage_sleep(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """sleep"""
        try:
            # 
            self._load_model()
            
            if self.model is not None:
                # 
                stages = self._stage_with_model(features_df)
            else:
                # 
                stages = self._stage_with_rules(features_df)
            
            # 
            stages_df = pd.DataFrame({
                'epoch': range(len(stages)),
                'stage': stages,
                'stage_label': [self.stage_labels.get(s, 'Unknown') for s in stages]
            })
            
            return stages_df
            
        except Exception as e:
            self.logger.error(f"sleep: {e}")
            return pd.DataFrame()
    
    def _load_model(self):
        """"""
        try:
            # scikit-learn
            from sklearn.ensemble import RandomForestClassifier
            import joblib
            
            # 
            model_path = Path(__file__).parent / "models" / "sleep_staging_model.pkl"
            if model_path.exists():
                self.model = joblib.load(model_path)
                self.logger.info("sleep")
                
        except ImportError:
            self.logger.warning("scikit-learn£¬")
        except Exception as e:
            self.logger.warning(f"£¬: {e}")
    
    def _stage_with_model(self, features_df: pd.DataFrame) -> List[int]:
        """"""
        # 
        feature_cols = [col for col in features_df.columns 
                       if col not in ['epoch', 'start_time', 'end_time']]
        X = features_df[feature_cols].fillna(0).values
        
        # 
        stages = self.model.predict(X)
        return stages.tolist()
    
    def _stage_with_rules(self, features_df: pd.DataFrame) -> List[int]:
        """£¨£©"""
        stages = []
        
        for _, row in features_df.iterrows():
            # 
            delta_ratio = row.get('delta_ratio', 0)
            theta_ratio = row.get('theta_ratio', 0)
            alpha_ratio = row.get('alpha_ratio', 0)
            sigma_ratio = row.get('sigma_ratio', 0)
            eeg_std = row.get('std', 0)
            
            # 
            stage = self._apply_staging_rules(
                delta_ratio, theta_ratio, alpha_ratio, 
                sigma_ratio, eeg_std
            )
            
            stages.append(stage)
        
        return stages
    
    def _apply_staging_rules(self, delta: float, theta: float, 
                            alpha: float, sigma: float, eeg_std: float) -> int:
        """"""
        
        # 1:  (alpha£¬)
        if alpha > 0.3 and eeg_std > 20:
            return 0
        
        # 2: N3 (delta)
        if delta > 0.5:
            return 3
        
        # 3: N2 ()
        if sigma > 0.15:
            return 2
        
        # 4: REM (£¬)
        if eeg_std < 15 and 0.1 < theta < 0.4 and alpha < 0.2:
            return 4
        
        # 5: N1 ()
        if 0.1 < alpha < 0.3 and eeg_std < 25:
            return 1
        
        # : N1
        return 1

# ====================  ====================
class RespiratoryEventDetector:
    """respirationdetection£¨based onAASMstandard£©"""
    
    def __init__(self, sfreq: float, config: AnalysisConfig):
        self.sfreq = sfreq
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def detect_events(self, resp_data: np.ndarray, 
                     spo2_data: Optional[np.ndarray] = None) -> pd.DataFrame:
        """detectionrespiration"""
        events = []
        
        try:
            # 
            resp_filtered = self._preprocess_respiratory(resp_data)
            
            # 
            resp_envelope = np.abs(hilbert(resp_filtered))
            baseline = np.median(resp_envelope)
            
            # 
            apnea_mask = resp_envelope < self.config.apnea_threshold * baseline
            apnea_events = self._find_events(
                apnea_mask, 
                self.config.min_event_duration,
                'apnea'
            )
            events.extend(apnea_events)
            
            # 
            hypopnea_mask = resp_envelope < self.config.hypopnea_threshold * baseline
            hypopnea_events = self._find_events(
                hypopnea_mask,
                self.config.min_event_duration,
                'hypopnea'
            )
            events.extend(hypopnea_events)
            
            # £¬
            if spo2_data is not None:
                events = self._validate_with_spo2(events, spo2_data)
            
            # DataFrame
            events_df = pd.DataFrame(events) if events else pd.DataFrame()
            
            return events_df
            
        except Exception as e:
            self.logger.error(f"respirationdetection: {e}")
            return pd.DataFrame()
    
    def _preprocess_respiratory(self, data: np.ndarray) -> np.ndarray:
        """processingrespirationsignal"""
        #  (0.1-5 Hz)
        nyquist = self.sfreq / 2
        b, a = butter(4, [0.1/nyquist, 5/nyquist], btype='band')
        filtered = filtfilt(b, a, data)
        
        # 
        filtered = signal.detrend(filtered)
        
        return filtered
    
    def _find_events(self, mask: np.ndarray, min_duration: float, 
                    event_type: str) -> List[Dict]:
        """"""
        events = []
        min_samples = int(min_duration * self.sfreq)
        
        # 
        diff_mask = np.diff(np.concatenate(([0], mask.astype(int), [0])))
        starts = np.where(diff_mask == 1)[0]
        ends = np.where(diff_mask == -1)[0]
        
        for start, end in zip(starts, ends):
            duration = (end - start) / self.sfreq
            if duration >= min_duration:
                events.append({
                    'type': event_type,
                    'start_sample': int(start),
                    'end_sample': int(end),
                    'start_time': start / self.sfreq,
                    'end_time': end / self.sfreq,
                    'duration': float(duration)
                })
        
        return events
    
    def _validate_with_spo2(self, events: List[Dict], 
                           spo2_data: np.ndarray) -> List[Dict]:
        """validate"""
        validated_events = []
        
        for event in events:
            start = int(event['start_sample'])
            end = int(event['end_sample'])
            
            # 
            if end < len(spo2_data):
                baseline_spo2 = np.median(spo2_data[max(0, start-100):start])
                min_spo2 = np.min(spo2_data[start:end])
                spo2_drop = baseline_spo2 - min_spo2
                
                event['spo2_baseline'] = float(baseline_spo2)
                event['spo2_nadir'] = float(min_spo2)
                event['spo2_drop'] = float(spo2_drop)
                event['validated'] = spo2_drop >= self.config.spo2_drop_threshold
                
                validated_events.append(event)
        
        return validated_events

# ====================  ====================
class SpindleDetector:
    """detection"""
    
    def __init__(self, sfreq: float, config: AnalysisConfig):
        self.sfreq = sfreq
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def detect_spindles(self, eeg_data: np.ndarray) -> pd.DataFrame:
        """detection"""
        spindles = []
        
        try:
            # 
            low, high = self.config.spindle_freq_range
            sos = butter(4, [low, high], btype='band', fs=self.sfreq, output='sos')
            filtered = signal.sosfiltfilt(sos, eeg_data)
            
            # 
            envelope = np.abs(hilbert(filtered))
            
            # 
            window = int(self.sfreq * 0.1)  # 100ms
            envelope_smooth = np.convolve(
                envelope, 
                np.ones(window)/window, 
                mode='same'
            )
            
            # 
            rms = np.sqrt(np.mean(envelope_smooth ** 2))
            threshold = rms * self.config.spindle_amplitude_threshold
            
            # 
            mask = envelope_smooth > threshold
            
            # 
            diff_mask = np.diff(np.concatenate(([0], mask.astype(int), [0])))
            starts = np.where(diff_mask == 1)[0]
            ends = np.where(diff_mask == -1)[0]
            
            for start, end in zip(starts, ends):
                duration = (end - start) / self.sfreq
                min_dur, max_dur = self.config.spindle_duration_range
                
                if min_dur <= duration <= max_dur:
                    # 
                    segment = filtered[start:end]
                    segment_env = envelope_smooth[start:end]
                    
                    # 
                    freq = self._estimate_frequency(segment)
                    amplitude = float(np.max(segment_env))
                    symmetry = self._calculate_symmetry(segment_env)
                    
                    spindles.append({
                        'start_idx': int(start),
                        'end_idx': int(end),
                        'start_time': start / self.sfreq,
                        'end_time': end / self.sfreq,
                        'duration': float(duration),
                        'frequency': float(freq),
                        'amplitude': amplitude,
                        'symmetry': symmetry,
                        'type': 'fast' if freq >= 13 else 'slow'
                    })
            
            self.logger.info(f"detection {len(spindles)} ")
            
        except Exception as e:
            self.logger.error(f"detection: {e}")
        
        return pd.DataFrame(spindles)
    
    def _estimate_frequency(self, segment: np.ndarray) -> float:
        """frequency"""
        if len(segment) < 10:
            return 13.0
        
        freqs, psd = welch(segment, self.sfreq, nperseg=min(256, len(segment)))
        low, high = self.config.spindle_freq_range
        mask = (freqs >= low) & (freqs <= high)
        
        if np.any(mask):
            peak_idx = np.argmax(psd[mask])
            return float(freqs[mask][peak_idx])
        
        return 13.0
    
    def _calculate_symmetry(self, envelope: np.ndarray) -> float:
        """"""
        if len(envelope) < 3:
            return 0.5
        
        peak_idx = np.argmax(envelope)
        
        if peak_idx == 0 or peak_idx == len(envelope) - 1:
            return 0.5
        
        rise_area = np.trapz(envelope[:peak_idx + 1])
        fall_area = np.trapz(envelope[peak_idx:])
        total = rise_area + fall_area
        
        return float(rise_area / total) if total > 0 else 0.5

# ====================  ====================
class SleepAnalyzer:
    """sleepanalysis"""
    
    def __init__(self, config: Optional[AnalysisConfig] = None):
        self.config = config or AnalysisConfig()
        self.logger = setup_logging()
        self.raw = None
        self.sfreq = None
        self.channels = {}
        self.quality_report = {}
        self.results = {}
        
    def load_edf(self, edf_path: str) -> bool:
        """EDFfile"""
        try:
            self.logger.info(f"EDFfile: {edf_path}")
            
            if not os.path.exists(edf_path):
                self.logger.error(f"file: {edf_path}")
                return False
            
            self.raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)
            self.sfreq = self.raw.info['sfreq']
            
            self.logger.info(f": {self.sfreq} Hz")
            self.logger.info(f": {len(self.raw.ch_names)}")
            self.logger.info(f": {self.raw.n_times / self.sfreq / 3600:.2f} ")
            
            self._identify_channels()
            self._assess_signal_quality()
            
            return True
            
        except Exception as e:
            self.logger.error(f"EDF: {e}")
            return False
    
    def _identify_channels(self):
        """"""
        self.channels = {
            'eeg': [], 'eog': [], 'emg': [], 
            'ecg': [], 'resp': [], 'spo2': [], 'other': []
        }
        
        for ch in self.raw.ch_names:
            ch_lower = ch.lower()
            ch_type = self.raw.get_channel_types(picks=ch)[0]
            
            if ch_type == 'eeg':
                self.channels['eeg'].append(ch)
            elif ch_type == 'eog':
                self.channels['eog'].append(ch)
            elif ch_type == 'emg':
                self.channels['emg'].append(ch)
            elif 'ecg' in ch_lower:
                self.channels['ecg'].append(ch)
            elif any(k in ch_lower for k in ['resp', 'flow', 'air']):
                self.channels['resp'].append(ch)
            elif any(k in ch_lower for k in ['spo2', 'sao2', 'ox']):
                self.channels['spo2'].append(ch)
            else:
                self.channels['other'].append(ch)
        
        self.logger.info(f": { {k: len(v) for k, v in self.channels.items()} }")
    
    def _assess_signal_quality(self):
        """signal"""
        assessor = SignalQualityAssessor(self.sfreq)
        
        for ch_type, channels in self.channels.items():
            for ch in channels:
                data = self.raw.get_data(picks=ch)[0]
                quality = assessor.assess(data, ch)
                self.quality_report[ch] = asdict(quality)
        
        usable_channels = sum(1 for q in self.quality_report.values() if q['is_usable'])
        self.logger.info(f": {usable_channels}/{len(self.quality_report)}")
    
    def analyze(self) -> Dict:
        """analysis"""
        self.logger.info("sleepanalysis...")
        
        # 1. 
        if self.channels['eeg']:
            self.logger.info("sleepanalysis...")
            self.results['sleep_staging'] = self._analyze_sleep_staging()
        
        # 2. 
        if self.channels['resp']:
            self.logger.info("respirationanalysis...")
            self.results['respiratory'] = self._analyze_respiratory()
        
        # 3. 
        if self.channels['eeg']:
            self.logger.info("analysis...")
            self.results['spindles'] = self._analyze_spindles()
        
        # 4. 
        self.results['summary'] = self._generate_summary()
        
        # 5. 
        self._save_results()
        
        return self.results
    
    def _analyze_sleep_staging(self) -> Dict:
        """sleepanalysis"""
        if not self.channels['eeg']:
            return {}
        
        # EEG
        eeg_channel = self._select_best_channel('eeg')
        
        # 
        eeg_data, times = self.raw[eeg_channel, :]
        eeg_data = eeg_data.flatten()
        
        # epochs
        samples_per_epoch = int(self.config.epoch_duration * self.sfreq)
        n_epochs = len(eeg_data) // samples_per_epoch
        
        # 
        feature_extractor = FeatureExtractor(self.sfreq, self.config)
        features_list = []
        
        for epoch_idx in range(n_epochs):
            start = epoch_idx * samples_per_epoch
            end = start + samples_per_epoch
            epoch_data = eeg_data[start:end]
            
            features = feature_extractor.extract_eeg_features(epoch_data)
            features['epoch'] = epoch_idx
            features['start_time'] = times[start]
            features['end_time'] = times[min(end, len(times)-1)]
            features_list.append(features)
        
        features_df = pd.DataFrame(features_list)
        
        # 
        stager = SleepStager(self.config)
        stages_df = stager.stage_sleep(features_df)
        
        # 
        metrics = self._calculate_sleep_metrics(stages_df)
        
        return {
            'channel': eeg_channel,
            'features': features_df.to_dict('records') if self.config.save_intermediate else [],
            'stages': stages_df.to_dict('records'),
            'metrics': metrics
        }
    
    def _analyze_respiratory(self) -> Dict:
        """respirationanalysis"""
        if not self.channels['resp']:
            return {}
        
        # 
        resp_channel = self._select_best_channel('resp')
        resp_data = self.raw.get_data(picks=resp_channel)[0]
        
        # £¨£©
        spo2_data = None
        if self.channels['spo2']:
            spo2_channel = self._select_best_channel('spo2')
            spo2_data = self.raw.get_data(picks=spo2_channel)[0]
        
        # 
        detector = RespiratoryEventDetector(self.sfreq, self.config)
        events_df = detector.detect_events(resp_data, spo2_data)
        
        # 
        if not events_df.empty:
            duration_hours = len(resp_data) / self.sfreq / 3600
            apnea_count = len(events_df[events_df['type'] == 'apnea'])
            hypopnea_count = len(events_df[events_df['type'] == 'hypopnea'])
            total_events = len(events_df)
            
            ahi = total_events / duration_hours
            
            # 
            spo2_metrics = {}
            if spo2_data is not None and 'validated' in events_df.columns:
                validated = events_df[events_df['validated'] == True]
                odi = len(validated) / duration_hours
                spo2_metrics = {
                    'odi': odi,
                    'min_spo2': float(np.min(spo2_data)),
                    'mean_spo2': float(np.mean(spo2_data))
                }
            
            return {
                'channel': resp_channel,
                'total_events': total_events,
                'apnea_count': int(apnea_count),
                'hypopnea_count': int(hypopnea_count),
                'ahi': float(ahi),
                'events': events_df.to_dict('records') if self.config.save_intermediate else [],
                'spo2_metrics': spo2_metrics,
                'severity': self._classify_ahi(ahi)
            }
        
        return {}
    
    def _analyze_spindles(self) -> Dict:
        """analysis"""
        if not self.channels['eeg']:
            return {}
        
        # EEG
        eeg_channels = self.channels['eeg']
        central_channels = [ch for ch in eeg_channels if 'C' in ch]
        spindle_channel = central_channels[0] if central_channels else eeg_channels[0]
        
        # 
        eeg_data = self.raw.get_data(picks=spindle_channel)[0]
        
        # 
        detector = SpindleDetector(self.sfreq, self.config)
        spindles_df = detector.detect_spindles(eeg_data)
        
        if not spindles_df.empty:
            duration_hours = len(eeg_data) / self.sfreq / 3600
            
            # 
            stats = {
                'count': len(spindles_df),
                'density': len(spindles_df) / (duration_hours * 60),  # /
                'mean_duration': float(spindles_df['duration'].mean()),
                'mean_frequency': float(spindles_df['frequency'].mean()),
                'mean_amplitude': float(spindles_df['amplitude'].mean()),
                'slow_count': int(sum(spindles_df['type'] == 'slow')),
                'fast_count': int(sum(spindles_df['type'] == 'fast'))
            }
            
            # 
            if stats['count'] > 0:
                stats['slow_percent'] = stats['slow_count'] / stats['count'] * 100
                stats['fast_percent'] = stats['fast_count'] / stats['count'] * 100
            
            return {
                'channel': spindle_channel,
                'statistics': stats,
                'spindles': spindles_df.to_dict('records') if self.config.save_intermediate else []
            }
        
        return {}
    
    def _select_best_channel(self, channel_type: str) -> str:
        """"""
        channels = self.channels.get(channel_type, [])
        if not channels:
            return None
        
        # 
        best_channel = None
        best_quality = -1
        
        for ch in channels:
            quality = self.quality_report.get(ch, {})
            score = quality.get('quality_score', 0)
            if score > best_quality:
                best_quality = score
                best_channel = ch
        
        return best_channel or channels[0]
    
    def _calculate_sleep_metrics(self, stages_df: pd.DataFrame) -> Dict:
        """sleep"""
        if stages_df.empty:
            return {}
        
        total_epochs = len(stages_df)
        total_time_min = total_epochs * self.config.epoch_duration / 60
        
        # 
        stage_counts = stages_df['stage'].value_counts()
        
        # £¨£©
        sleep_epochs = sum(stages_df['stage'].isin([1, 2, 3, 4]))
        sleep_time_min = sleep_epochs * self.config.epoch_duration / 60
        
        # 
        sleep_efficiency = (sleep_time_min / total_time_min * 100) if total_time_min > 0 else 0
        
        # £¨epoch£©
        sleep_indices = stages_df[stages_df['stage'].isin([1, 2, 3, 4])].index
        sleep_latency_min = (sleep_indices[0] * self.config.epoch_duration / 60) if len(sleep_indices) > 0 else total_time_min
        
        # REM
        rem_indices = stages_df[stages_df['stage'] == 4].index
        rem_latency_min = None
        if len(rem_indices) > 0 and len(sleep_indices) > 0:
            rem_latency_min = (rem_indices[0] - sleep_indices[0]) * self.config.epoch_duration / 60
        
        # 
        stage_percentages = {}
        for stage in range(5):  # 0-4
            count = stage_counts.get(stage, 0)
            stage_percentages[self.stager.stage_labels.get(stage, f'Stage{stage}')] = \
                (count / total_epochs * 100) if total_epochs > 0 else 0
        
        return {
            'total_time_hours': total_time_min / 60,
            'sleep_time_hours': sleep_time_min / 60,
            'sleep_efficiency': sleep_efficiency,
            'sleep_latency_min': sleep_latency_min,
            'rem_latency_min': rem_latency_min,
            'stage_percentages': stage_percentages
        }
    
    def _classify_ahi(self, ahi: float) -> str:
        """AHI"""
        if ahi < 5:
            return ''
        elif ahi < 15:
            return ''
        elif ahi < 30:
            return ''
        else:
            return ''
    
    def _generate_summary(self) -> Dict:
        """"""
        summary = {
            'analysis_time': datetime.now().isoformat(),
            'file_info': {
                'sampling_rate': self.sfreq,
                'channels': {k: len(v) for k, v in self.channels.items()},
                'signal_quality': {
                    'usable_channels': sum(1 for q in self.quality_report.values() if q['is_usable']),
                    'average_quality': np.mean([q['quality_score'] for q in self.quality_report.values()]) if self.quality_report else 0
                }
            }
        }
        
        # 
        if 'sleep_staging' in self.results:
            staging = self.results['sleep_staging']
            summary['sleep_metrics'] = staging.get('metrics', {})
        
        if 'respiratory' in self.results:
            resp = self.results['respiratory']
            summary['respiratory_metrics'] = {
                'ahi': resp.get('ahi', 0),
                'severity': resp.get('severity', ''),
                'apnea_count': resp.get('apnea_count', 0),
                'hypopnea_count': resp.get('hypopnea_count', 0)
            }
            if 'spo2_metrics' in resp:
                summary['respiratory_metrics'].update(resp['spo2_metrics'])
        
        if 'spindles' in self.results:
            spindles = self.results['spindles']
            summary['spindle_metrics'] = spindles.get('statistics', {})
        
        return summary
    
    def _save_results(self):
        """"""
        try:
            # 
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = Path(self.config.output_dir) / timestamp
            
            # JSON
            report_path = output_dir / 'sleep_analysis_report.json'
            
            # numpy
            def convert_numpy(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {k: convert_numpy(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numpy(item) for item in obj]
                else:
                    return obj
            
            report = convert_numpy(self.results)
            
            
            # 
            self._generate_visualizations(output_dir)
            
            # 
            self._generate_text_report(output_dir)
            
            self.logger.info(f": {output_dir}")
            
        except Exception as e:
            self.logger.error(f": {e}")
    
    def _generate_visualizations(self, output_dir: Path):
        """"""
        try:
            # 
            if 'sleep_staging' in self.results:
                self._plot_hypnogram(output_dir)
            
            # 
            if 'respiratory' in self.results and self.results['respiratory'].get('events'):
                self._plot_respiratory_events(output_dir)
            
            # 
            if 'spindles' in self.results and self.results['spindles'].get('spindles'):
                self._plot_spindle_distribution(output_dir)
            
            # 
            self._plot_dashboard(output_dir)
            
        except Exception as e:
            self.logger.error(f": {e}")
    
    def _plot_hypnogram(self, output_dir: Path):
        """sleep"""
        try:
            stages_data = self.results['sleep_staging']['stages']
            if not stages_data:
                return
            
            df = pd.DataFrame(stages_data)
            
            fig, ax = plt.subplots(figsize=(15, 5))
            
            # £¨£©
            times = [d['epoch'] * self.config.epoch_duration / 3600 for d in stages_data]
            
            # 
            colors = {0: 'blue', 1: 'green', 2: 'orange', 3: 'red', 4: 'purple'}
            
            # 
            for i in range(len(times)-1):
                stage = df.iloc[i]['stage']
                ax.fill_between([times[i], times[i+1]], [stage, stage], [stage+0.8, stage+0.8],
                               color=colors.get(stage, 'gray'), alpha=0.7)
            
            ax.set_xlabel(' ()')
            ax.set_ylabel('sleep')
            ax.set_yticks([0, 1, 2, 3, 4])
            ax.set_yticklabels(['W', 'N1', 'N2', 'N3', 'REM'])
            ax.set_title('sleep (Hypnogram)')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.close()
            
        except Exception as e:
            self.logger.error(f"sleep: {e}")
    
    def _plot_respiratory_events(self, output_dir: Path):
        """respiration"""
        try:
            events = self.results['respiratory']['events']
            if not events:
                return
            
            df = pd.DataFrame(events)
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8))
            
            # 
            times = [e['start_time'] / 3600 for e in events]  # 
            durations = [e['duration'] for e in events]
            types = [e['type'] for e in events]
            
            colors = {'apnea': 'red', 'hypopnea': 'orange'}
            
            for i, (t, d, typ) in enumerate(zip(times, durations, types)):
                ax1.bar(t, d, width=0.02, color=colors.get(typ, 'gray'), 
                       alpha=0.7, label=typ if i == 0 else "")
            
            ax1.set_xlabel(' ()')
            ax1.set_ylabel(' ()')
            ax1.set_title('respiration')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 
            type_counts = df['type'].value_counts()
            ax2.bar(type_counts.index, type_counts.values, 
                   color=[colors.get(t, 'gray') for t in type_counts.index])
            ax2.set_xlabel('')
            ax2.set_ylabel('')
            ax2.set_title('respiration')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.close()
            
        except Exception as e:
            self.logger.error(f"respiration: {e}")
    
    def _plot_spindle_distribution(self, output_dir: Path):
        """"""
        try:
            spindles_data = self.results['spindles']['spindles']
            if not spindles_data:
                return
            
            df = pd.DataFrame(spindles_data)
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # 
            ax1 = axes[0, 0]
            ax1.hist(df['frequency'], bins=30, alpha=0.7, color='purple', edgecolor='black')
            ax1.axvline(df['frequency'].mean(), color='red', linestyle='--', 
                       label=f": {df['frequency'].mean():.2f} Hz")
            ax1.set_xlabel('frequency (Hz)')
            ax1.set_ylabel('')
            ax1.set_title('frequency')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 
            ax2 = axes[0, 1]
            ax2.hist(df['duration'], bins=30, alpha=0.7, color='blue', edgecolor='black')
            ax2.axvline(df['duration'].mean(), color='red', linestyle='--',
                       label=f": {df['duration'].mean():.2f} ")
            ax2.set_xlabel(' ()')
            ax2.set_ylabel('')
            ax2.set_title('')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # 
            ax3 = axes[1, 0]
            ax3.hist(df['amplitude'], bins=30, alpha=0.7, color='green', edgecolor='black')
            ax3.axvline(df['amplitude'].mean(), color='red', linestyle='--',
                       label=f": {df['amplitude'].mean():.3f}")
            ax3.set_xlabel('')
            ax3.set_ylabel('')
            ax3.set_title('')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # 
            ax4 = axes[1, 1]
            type_counts = df['type'].value_counts()
            ax4.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
                   colors=['lightblue', 'lightcoral'])
            ax4.set_title('')
            
            plt.tight_layout()
            plt.close()
            
        except Exception as e:
            self.logger.error(f": {e}")
    
    def _plot_dashboard(self, output_dir: Path):
        """"""
        try:
            fig = plt.figure(figsize=(20, 12))
            
            # 
            gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
            
            # 
            fig.suptitle(f'sleepanalysis - {datetime.now().strftime("%Y-%m-%d %H:%M")}', 
                        fontsize=16, fontweight='bold')
            
            # 
            ax_metrics = fig.add_subplot(gs[0, :])
            ax_metrics.axis('off')
            
            metrics_text = ""
            if 'sleep_metrics' in self.results.get('summary', {}):
                sm = self.results['summary']['sleep_metrics']
                metrics_text += f"sleep: {sm.get('sleep_time_hours', 0):.1f} | "
                metrics_text += f"sleep: {sm.get('sleep_efficiency', 0):.1f}% | "
                metrics_text += f"sleep: {sm.get('sleep_latency_min', 0):.1f}"
            
            if 'respiratory_metrics' in self.results.get('summary', {}):
                rm = self.results['summary']['respiratory_metrics']
                metrics_text += f"\nAHI: {rm.get('ahi', 0):.1f} ({rm.get('severity', '')}) | "
                metrics_text += f"ODI: {rm.get('odi', 0):.1f} | "
                metrics_text += f": {rm.get('min_spo2', 0):.1f}%"
            
            if 'spindle_metrics' in self.results.get('summary', {}):
                spm = self.results['summary']['spindle_metrics']
                metrics_text += f"\n: {spm.get('density', 0):.2f}/ | "
                metrics_text += f"frequency: {spm.get('mean_frequency', 0):.1f}Hz"
            
            ax_metrics.text(0.1, 0.5, metrics_text, fontsize=14, verticalalignment='center',
                          bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
            
            # £¨£©
            ax_hypno = fig.add_subplot(gs[1, 0])
            ax_hypno.set_title('sleep')
            if 'sleep_staging' in self.results:
                stages_data = self.results['sleep_staging'].get('stages', [])
                if stages_data:
                    times = [d['epoch'] * self.config.epoch_duration / 3600 for d in stages_data[:500]]  # 500
                    stages = [d['stage'] for d in stages_data[:500]]
                    ax_hypno.plot(times, stages, 'b-', linewidth=0.5)
                    ax_hypno.set_ylim(-0.5, 4.5)
                    ax_hypno.set_xlabel('')
                    ax_hypno.set_ylabel('')
            
            # £¨£©
            ax_resp = fig.add_subplot(gs[1, 1])
            ax_resp.set_title('respiration')
            if 'respiratory' in self.results:
                events = self.results['respiratory'].get('events', [])
                if events:
                    df = pd.DataFrame(events)
                    if 'type' in df.columns:
                        type_counts = df['type'].value_counts()
                        ax_resp.bar(type_counts.index, type_counts.values, 
                                   color=['red', 'orange'])
                        ax_resp.set_ylabel('')
            
            # £¨£©
            ax_spindle = fig.add_subplot(gs[1, 2])
            ax_spindle.set_title('frequency')
            if 'spindles' in self.results:
                spindles = self.results['spindles'].get('spindles', [])
                if spindles:
                    df = pd.DataFrame(spindles)
                    ax_spindle.hist(df['frequency'], bins=20, alpha=0.7, color='purple')
                    ax_spindle.set_xlabel('frequency (Hz)')
                    ax_spindle.set_ylabel('')
            
            # 
            ax_pie = fig.add_subplot(gs[2, 0])
            if 'sleep_staging' in self.results:
                metrics = self.results['sleep_staging'].get('metrics', {})
                percentages = metrics.get('stage_percentages', {})
                if percentages:
                    labels = list(percentages.keys())
                    sizes = list(percentages.values())
                    ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%',
                             colors=['blue', 'green', 'orange', 'red', 'purple'])
                    ax_pie.set_title('sleep')
            
            # 
            ax_advice = fig.add_subplot(gs[2, 1:])
            ax_advice.axis('off')
            
            advice = "¡¾¡¿\n"
            
            # AHI
            if 'respiratory_metrics' in self.results.get('summary', {}):
                severity = self.results['summary']['respiratory_metrics'].get('severity', '')
                if severity == '':
                    advice += "? sleeprespiration£¬\n"
                elif severity == '':
                    advice += "? sleeprespiration£¬\n"
                elif severity == '':
                    advice += "? sleeprespiration£¬\n"
                else:
                    advice += "? respiration£¬processing\n"
            
            # 
            if 'sleep_metrics' in self.results.get('summary', {}):
                efficiency = self.results['summary']['sleep_metrics'].get('sleep_efficiency', 0)
                if efficiency < 85:
                    advice += "? sleep£¬sleep\n"
                
                latency = self.results['summary']['sleep_metrics'].get('sleep_latency_min', 0)
                if latency > 30:
                    advice += "? £¬\n"
            
            # 
            if 'spindle_metrics' in self.results.get('summary', {}):
                density = self.results['summary']['spindle_metrics'].get('density', 0)
                if density < 1.5:
                    advice += "? £¬N2sleep\n"
            
            ax_advice.text(0.1, 0.5, advice, fontsize=12, verticalalignment='center',
                          bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))
            
                       bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            self.logger.error(f": {e}")
    
    def _generate_text_report(self, output_dir: Path):
        """"""
        try:
            report_path = output_dir / 'analysis_report.txt'
            
                
                
                
                if 'sleep_metrics' in self.results['summary']:
                    sm = self.results['summary']['sleep_metrics']
                    if sm.get('rem_latency_min'):
                
                if 'respiratory_metrics' in self.results['summary']:
                    rm = self.results['summary']['respiratory_metrics']
                    if 'odi' in rm:
                
                if 'spindle_metrics' in self.results['summary']:
                    spm = self.results['summary']['spindle_metrics']
                
                
                
            
            self.logger.info(f": {report_path}")
            
        except Exception as e:
            self.logger.error(f": {e}")

# ====================  ====================
def main():
    """function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='sleepanalysis')
    parser.add_argument('edf_file', nargs='?', help='EDFfilepath')
    parser.add_argument('-o', '--output', default='sleep_analysis_results', help='')
    parser.add_argument('-c', '--config', help='filepath')
    parser.add_argument('-v', '--verbose', action='store_true', help='')
    
    args = parser.parse_args()
    
    # 
    if sys.stdout.encoding != 'UTF-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # EDF
    if args.edf_file:
        edf_path = args.edf_file
    else:
        # 
        edf_path = r"D:\openclaw\AISleepGen\data\edf\SC4001E0-PSG.edf"
        print(f"file: {edf_path}")
    
    # 
    config = AnalysisConfig(output_dir=args.output)
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
                for key, value in config_dict.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
            print(f"file: {args.config}")
        except Exception as e:
            print(f"file: {e}")
    
    print("\n" + "=" * 70)
    print("sleepanalysis v2.0")
    print("=" * 70 + "\n")
    
    # 
    analyzer = SleepAnalyzer(config)
    
    # EDF
    if not analyzer.load_edf(edf_path):
        print("? EDFfile")
        sys.exit(1)
    
    # 
    print("\n?? analysis...\n")
    results = analyzer.analyze()
    
    # 
    print("\n" + "=" * 70)
    print("?? analysis")
    print("=" * 70)
    
    if 'sleep_metrics' in results.get('summary', {}):
        sm = results['summary']['sleep_metrics']
        print(f"\n?? sleep:")
        print(f"  sleep: {sm.get('sleep_time_hours', 0):.1f} ")
        print(f"  sleep: {sm.get('sleep_efficiency', 0):.1f}%")
    
    if 'respiratory_metrics' in results.get('summary', {}):
        rm = results['summary']['respiratory_metrics']
        print(f"\n??? respiration:")
        print(f"  AHI: {rm.get('ahi', 0):.1f} ({rm.get('severity', '')})")
        if 'min_spo2' in rm:
            print(f"  : {rm['min_spo2']:.1f}%")
    
    if 'spindle_metrics' in results.get('summary', {}):
        spm = results['summary']['spindle_metrics']
        print(f"\n?? :")
        print(f"  : {spm.get('density', 0):.2f} /")
        print(f"  frequency: {spm.get('mean_frequency', 0):.1f} Hz")
    
    print(f"\n?? : {Path(config.output_dir).absolute()}")
    print("\n" + "=" * 70)
    print("? analysis£¡")
    print("=" * 70)

if __name__ == "__main__":
    main()

