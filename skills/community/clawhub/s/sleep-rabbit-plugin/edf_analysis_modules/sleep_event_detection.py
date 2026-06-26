#!/usr/bin/env python3
"""
Sleep Event Detection Module
Version: 5.1.5
Description: REAL professional sleep analysis module
Original size: 56,922 bytes
Chinese comments marked with  for ClawHub compliance
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sleepdetection v3.0
AASM 2.6standard£¬signaldetection
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
from scipy.signal import find_peaks, welch, butter, filtfilt, hilbert
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum
import warnings
import json
from pathlib import Path

warnings.filterwarnings('ignore')

# ====================  ====================
class EventType(Enum):
    """£¨based onAASMstandard£©"""
    APNEA_OBSTRUCTIVE = "respiration"
    APNEA_CENTRAL = "respiration"
    APNEA_MIXED = "respiration"
    HYPOPNEA = ""
    RERA = "respiration"
    PLMS = ""
    AROUSAL = ""
    DESATURATION = ""

class Severity(Enum):
    """"""
    NORMAL = ""
    MILD = ""
    MODERATE = ""
    SEVERE = ""

# ====================  ====================
@dataclass
class AASMConfig:
    """AASMstandardparameter"""
    #  (AASM 2.6)
    APNEA_THRESHOLD: float = 0.1  # ¡Ý90%
    HYPOPNEA_THRESHOLD: float = 0.7  # ¡Ý30%
    MIN_EVENT_DURATION: float = 10.0  # 
    MAX_APNEA_DURATION: float = 120.0  # £¨Cheyne-Stokes£©
    
    # 
    SPO2_DROP_THRESHOLD: float = 3.0  # ¡Ý3%
    SPO2_DROP_DURATION: float = 10.0  # 10
    SPO2_ARTIFACT_THRESHOLD: float = 20.0  # 
    
    # 
    PLMS_MIN_DURATION: float = 0.5  # 
    PLMS_MAX_DURATION: float = 10.0  # 
    PLMS_MIN_INTERVAL: float = 5.0  # 
    PLMS_MAX_INTERVAL: float = 90.0  # 
    PLMS_MIN_SEQUENCE: int = 4  # 4
    
    # 
    AROUSAL_MIN_DURATION: float = 3.0  # 
    AROUSAL_MAX_DURATION: float = 15.0  # 
    AROUSAL_EEG_SHIFT: float = 1.5  # EEGfrequency
    
    # 
    EFFORT_THRESHOLD: float = 0.5  # respiration
    RERA_DURATION: float = 10.0  # 

@dataclass
class SleepEvent:
    """sleep"""
    type: EventType
    start_time: float  # 
    end_time: float    # 
    duration: float    # 
    confidence: float  # 0-1 
    channels_used: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """"""
        return {
            'type': self.type.value,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'confidence': self.confidence,
            'channels_used': self.channels_used,
            'metadata': self.metadata
        }

@dataclass
class RespiratoryEvent(SleepEvent):
    """respiration"""
    airflow_reduction: float = 0.0  # 
    spo2_nadir: float = 100.0  # 
    spo2_drop: float = 0.0  # 
    effort_present: bool = True  # respiration
    desaturation_present: bool = False  # 

@dataclass
class PLMSEvent(SleepEvent):
    """"""
    amplitude: float = 0.0
    interval_to_previous: float = 0.0
    interval_to_next: float = 0.0
    sequence_index: int = 0  # 

@dataclass
class ArousalEvent(SleepEvent):
    """"""
    eeg_frequency_shift: float = 0.0
    emg_increase: float = 0.0
    associated_with_respiratory: bool = False

# ====================  ====================
class SignalQualityAssessor:
    """signal£¨£©"""
    
    def __init__(self, sfreq: float):
        self.sfreq = sfreq
        self.logger = logging.getLogger(__name__)
    
    def assess_respiratory(self, data: np.ndarray) -> Dict:
        """respirationsignal"""
        quality = {}
        
        # 1. 
        baseline = np.polyfit(np.arange(len(data)), data, 1)
        quality['baseline_drift'] = abs(baseline[0]) * len(data) / self.sfreq
        
        # 2. 
        noise_floor = np.percentile(np.abs(data), 10)
        signal_power = np.mean(data ** 2)
        quality['snr'] = 10 * np.log10(signal_power / (noise_floor ** 2 + 1e-10))
        
        # 3. 
        peaks, _ = find_peaks(data, distance=self.sfreq/3)  # 20
        if len(peaks) > 1:
            resp_rates = 60 * self.sfreq / np.diff(peaks)
            quality['resp_rate_mean'] = np.mean(resp_rates)
            quality['resp_rate_std'] = np.std(resp_rates)
            quality['is_physiological'] = (4 <= quality['resp_rate_mean'] <= 40)
        else:
            quality['is_physiological'] = False
        
        # 4. 
        quality['score'] = self._calculate_score(quality)
        
        return quality
    
    def assess_spo2(self, data: np.ndarray) -> Dict:
        """signal"""
        quality = {}
        
        # 1.  (60-100%)
        valid_mask = (data >= 60) & (data <= 100)
        quality['valid_percent'] = np.sum(valid_mask) / len(data) * 100
        
        # 2. £¨£©
        diff_data = np.diff(data)
        artifact_mask = np.abs(diff_data) > self.SPO2_ARTIFACT_THRESHOLD
        quality['artifact_percent'] = np.sum(artifact_mask) / len(diff_data) * 100
        
        # 3. 
        quality['stability'] = 1 - np.std(diff_data) / (np.mean(data) + 1e-10)
        
        # 4. 
        quality['score'] = (
            0.4 * (quality['valid_percent'] / 100) +
            0.3 * (1 - quality['artifact_percent'] / 100) +
            0.3 * quality['stability']
        )
        
        return quality
    
    def _calculate_score(self, quality: Dict) -> float:
        """"""
        score = 0.0
        weights = {'snr': 0.3, 'is_physiological': 0.4, 'baseline_drift': 0.3}
        
        if quality.get('snr', 0) > 20:
            score += weights['snr']
        elif quality.get('snr', 0) > 10:
            score += weights['snr'] * 0.5
        
        if quality.get('is_physiological', False):
            score += weights['is_physiological']
        
        if quality.get('baseline_drift', 100) < 10:
            score += weights['baseline_drift']
        elif quality.get('baseline_drift', 100) < 20:
            score += weights['baseline_drift'] * 0.5
        
        return score

# ====================  ====================
class RespiratoryEventDetector:
    """respirationdetection£¨AASM 2.6standard£©"""
    
    def __init__(self, sfreq: float, config: AASMConfig):
        self.sfreq = sfreq
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def detect_events(self, 
                     airflow: np.ndarray,
                     thorax: Optional[np.ndarray] = None,
                     abdomen: Optional[np.ndarray] = None,
                     spo2: Optional[np.ndarray] = None,
                     position: Optional[np.ndarray] = None) -> List[RespiratoryEvent]:
        """detectionrespiration£¨signal£©"""
        
        events = []
        
        try:
            # 1. 
            airflow_filtered = self._preprocess_airflow(airflow)
            
            # 2. 
            envelope = self._calculate_envelope(airflow_filtered)
            baseline = np.median(envelope)
            
            # 3. £¨£©
            effort = None
            if thorax is not None and abdomen is not None:
                effort = self._calculate_effort(thorax, abdomen)
            
            # 4. 
            candidates = self._find_candidate_events(envelope, baseline)
            
            # 5. 
            for start, end in candidates:
                event = self._validate_event(
                    start, end,
                    airflow_filtered,
                    envelope,
                    effort,
                    spo2,
                    baseline
                )
                
                if event:
                    events.append(event)
            
            # 6. 
            events = self._merge_events(events)
            
            # 7. //
            events = self._classify_by_effort(events, effort)
            
            self.logger.info(f"detection {len(events)} respiration")
            
        except Exception as e:
            self.logger.error(f"respirationdetection: {e}")
            
        return events
    
    def _preprocess_airflow(self, data: np.ndarray) -> np.ndarray:
        """processingrespirationsignal"""
        #  (0.05-5 Hz)
        sos = butter(4, [0.05, 5], btype='band', fs=self.sfreq, output='sos')
        filtered = signal.sosfiltfilt(sos, data)
        
        # 
        filtered = signal.detrend(filtered)
        
        return filtered
    
    def _calculate_envelope(self, data: np.ndarray) -> np.ndarray:
        """respiration"""
        # 
        analytic = hilbert(data)
        envelope = np.abs(analytic)
        
        # £¨£©
        window = int(self.sfreq * 2)  # 2
        window = min(window, len(envelope) // 10)
        if window > 0:
            envelope = np.convolve(envelope, np.ones(window)/window, mode='same')
        
        return envelope
    
    def _calculate_effort(self, thorax: np.ndarray, abdomen: np.ndarray) -> np.ndarray:
        """respiration£¨£©"""
        # 
        sos = butter(4, [0.05, 5], btype='band', fs=self.sfreq, output='sos')
        thorax_f = signal.sosfiltfilt(sos, thorax)
        abdomen_f = signal.sosfiltfilt(sos, abdomen)
        
        # 
        thorax_phase = np.angle(hilbert(thorax_f))
        abdomen_phase = np.angle(hilbert(abdomen_f))
        
        # £¨£©
        phase_diff = np.abs(np.angle(np.exp(1j * (thorax_phase - abdomen_phase))))
        
        # £¨1£¬0£©
        effort_index = 1 - phase_diff / np.pi
        
        return effort_index
    
    def _find_candidate_events(self, envelope: np.ndarray, 
                               baseline: float) -> List[Tuple[int, int]]:
        """"""
        candidates = []
        
        # 
        apnea_mask = envelope < (self.config.APNEA_THRESHOLD * baseline)
        hypopnea_mask = envelope < (self.config.HYPOPNEA_THRESHOLD * baseline)
        
        min_samples = int(self.config.MIN_EVENT_DURATION * self.sfreq)
        
        # 
        def find_regions(mask, min_len):
            regions = []
            start = None
            for i, m in enumerate(mask):
                if m and start is None:
                    start = i
                elif not m and start is not None:
                    if i - start >= min_len:
                        regions.append((start, i))
                    start = None
            if start is not None and len(mask) - start >= min_len:
                regions.append((start, len(mask)))
            return regions
        
        # 
        apnea_candidates = find_regions(apnea_mask, min_samples)
        
        # £¨£©
        hypopnea_candidates = []
        for start, end in find_regions(hypopnea_mask, min_samples):
            # 
            overlap = False
            for a_start, a_end in apnea_candidates:
                if not (end <= a_start or start >= a_end):
                    overlap = True
                    break
            if not overlap:
                hypopnea_candidates.append((start, end))
        
        # 
        candidates.extend([(s, e, 'apnea') for s, e in apnea_candidates])
        candidates.extend([(s, e, 'hypopnea') for s, e in hypopnea_candidates])
        
        return [(s, e) for s, e, _ in candidates]
    
    def _validate_event(self, start: int, end: int,
                       airflow: np.ndarray,
                       envelope: np.ndarray,
                       effort: Optional[np.ndarray],
                       spo2: Optional[np.ndarray],
                       baseline: float) -> Optional[RespiratoryEvent]:
        """validate£¨AASMstandard£©"""
        
        duration = (end - start) / self.sfreq
        
        # 
        if duration > self.config.MAX_APNEA_DURATION:
            return None
        
        # 
        segment_baseline = np.median(envelope[max(0, start-int(self.sfreq*10)):start])
        if segment_baseline < 1e-10:
            segment_baseline = baseline
        
        min_envelope = np.min(envelope[start:end])
        reduction = 1 - (min_envelope / segment_baseline)
        
        # 
        if reduction >= 0.9:
            event_type = EventType.APNEA_OBSTRUCTIVE  # 
        elif reduction >= 0.3:
            event_type = EventType.HYPOPNEA
        else:
            return None
        
        # £¨£©
        spo2_drop = 0
        spo2_nadir = 100
        desaturation_present = False
        
        if spo2 is not None:
            # 30
            search_end = min(end + int(self.sfreq * 30), len(spo2))
            segment_spo2 = spo2[start:search_end]
            
            if len(segment_spo2) > 0:
                spo2_nadir = np.min(segment_spo2)
                spo2_baseline = np.median(spo2[max(0, start-int(self.sfreq*60)):start])
                spo2_drop = spo2_baseline - spo2_nadir
                
                # AASM£º¡Ý3%
                desaturation_present = spo2_drop >= self.config.SPO2_DROP_THRESHOLD
                
                # 
                if event_type == EventType.HYPOPNEA and not desaturation_present:
                    return None
        
        # 
        event = RespiratoryEvent(
            type=event_type,
            start_time=start / self.sfreq,
            end_time=end / self.sfreq,
            duration=duration,
            confidence=self._calculate_confidence(reduction, spo2_drop),
            channels_used=['airflow'],
            metadata={
                'airflow_reduction': reduction,
                'min_envelope': min_envelope,
                'baseline': segment_baseline
            },
            airflow_reduction=reduction,
            spo2_nadir=spo2_nadir,
            spo2_drop=spo2_drop,
            desaturation_present=desaturation_present
        )
        
        return event
    
    def _calculate_confidence(self, reduction: float, spo2_drop: float) -> float:
        """"""
        confidence = 0.5
        
        # 
        if reduction >= 0.9:
            confidence += 0.3
        elif reduction >= 0.5:
            confidence += 0.2
        
        # 
        if spo2_drop >= 4:
            confidence += 0.2
        elif spo2_drop >= 3:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _merge_events(self, events: List[RespiratoryEvent]) -> List[RespiratoryEvent]:
        """"""
        if len(events) < 2:
            return events
        
        merged = []
        current = events[0]
        
        for next_event in events[1:]:
            gap = next_event.start_time - current.end_time
            
            if gap < 5:  # 5
                # 
                current.end_time = next_event.end_time
                current.duration = current.end_time - current.start_time
                # 
                if (next_event.type == EventType.APNEA_OBSTRUCTIVE and 
                    current.type == EventType.HYPOPNEA):
                    current.type = next_event.type
                current.confidence = max(current.confidence, next_event.confidence)
            else:
                merged.append(current)
                current = next_event
        
        merged.append(current)
        return merged
    
    def _classify_by_effort(self, events: List[RespiratoryEvent], 
                           effort: Optional[np.ndarray]) -> List[RespiratoryEvent]:
        """respiration"""
        if effort is None:
            return events
        
        for event in events:
            start_idx = int(event.start_time * self.sfreq)
            end_idx = int(event.end_time * self.sfreq)
            
            if end_idx >= len(effort):
                end_idx = len(effort) - 1
            
            # 
            event_effort = np.mean(effort[start_idx:end_idx])
            pre_event_effort = np.mean(effort[max(0, start_idx-int(self.sfreq*30)):start_idx])
            
            # / -> 
            #  -> 
            if event_effort > pre_event_effort * 0.8:
                if event.type == EventType.APNEA_OBSTRUCTIVE:
                    event.type = EventType.APNEA_OBSTRUCTIVE
                event.metadata['effort_present'] = True
            elif event_effort < pre_event_effort * 0.2:
                if event.type == EventType.APNEA_OBSTRUCTIVE:
                    event.type = EventType.APNEA_CENTRAL
                event.metadata['effort_present'] = False
            else:
                if event.type == EventType.APNEA_OBSTRUCTIVE:
                    event.type = EventType.APNEA_MIXED
                event.metadata['effort_present'] = 'mixed'
        
        return events

# ====================  ====================
class PLMSDetector:
    """detection£¨AASM/WASMstandard£©"""
    
    def __init__(self, sfreq: float, config: AASMConfig):
        self.sfreq = sfreq
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def detect_events(self, emg_data: np.ndarray) -> List[PLMSEvent]:
        """detection"""
        
        movements = []
        
        try:
            # 1. EMG
            emg_filtered = self._preprocess_emg(emg_data)
            
            # 2. 
            lm_events = self._detect_limb_movements(emg_filtered)
            
            if len(lm_events) < self.config.PLMS_MIN_SEQUENCE:
                return []
            
            # 3. 
            sequences = self._find_sequences(lm_events)
            
            # 4. PLMS
            movements = self._mark_plms(lm_events, sequences)
            
            self.logger.info(f"detection {len(movements)} ")
            
        except Exception as e:
            self.logger.error(f"PLMSdetection: {e}")
        
        return movements
    
    def _preprocess_emg(self, data: np.ndarray) -> np.ndarray:
        """processingEMGsignal"""
        #  (10-100 Hz)
        sos = butter(4, [10, 100], btype='band', fs=self.sfreq, output='sos')
        filtered = signal.sosfiltfilt(sos, data)
        
        # 
        rectified = np.abs(filtered)
        
        # £¨£©
        window = int(self.sfreq * 0.1)  # 100ms
        window = min(window, len(rectified) // 100)
        if window > 0:
            smoothed = np.convolve(rectified, np.ones(window)/window, mode='same')
        else:
            smoothed = rectified
        
        return smoothed
    
    def _detect_limb_movements(self, emg_env: np.ndarray) -> List[Dict]:
        """detection"""
        movements = []
        
        # 
        baseline = np.median(emg_env)
        threshold = baseline * 3
        min_duration = int(self.config.PLMS_MIN_DURATION * self.sfreq)
        max_duration = int(self.config.PLMS_MAX_DURATION * self.sfreq)
        
        # 
        above_threshold = emg_env > threshold
        
        # 
        diff = np.diff(np.concatenate(([0], above_threshold.astype(int), [0])))
        starts = np.where(diff == 1)[0]
        ends = np.where(diff == -1)[0]
        
        for start, end in zip(starts, ends):
            duration = (end - start) / self.sfreq
            
            if min_duration <= duration <= max_duration:
                movements.append({
                    'start': start,
                    'end': end,
                    'duration': duration,
                    'amplitude': np.max(emg_env[start:end])
                })
        
        return movements
    
    def _find_sequences(self, movements: List[Dict]) -> List[List[int]]:
        """"""
        if len(movements) < self.config.PLMS_MIN_SEQUENCE:
            return []
        
        sequences = []
        current_sequence = [0]
        
        for i in range(1, len(movements)):
            prev_end = movements[i-1]['end']
            curr_start = movements[i]['start']
            
            interval = (curr_start - prev_end) / self.sfreq
            
            # PLMS
            if (self.config.PLMS_MIN_INTERVAL <= interval <= 
                self.config.PLMS_MAX_INTERVAL):
                current_sequence.append(i)
            else:
                if len(current_sequence) >= self.config.PLMS_MIN_SEQUENCE:
                    sequences.append(current_sequence)
                current_sequence = [i]
        
        # 
        if len(current_sequence) >= self.config.PLMS_MIN_SEQUENCE:
            sequences.append(current_sequence)
        
        return sequences
    
    def _mark_plms(self, movements: List[Dict], 
                  sequences: List[List[int]]) -> List[PLMSEvent]:
        """PLMS"""
        plms_events = []
        
        # PLMS
        for seq_idx, sequence in enumerate(sequences):
            for pos_idx, mov_idx in enumerate(sequence):
                mov = movements[mov_idx]
                
                # 
                interval_to_prev = 0
                if pos_idx > 0:
                    prev_mov = movements[sequence[pos_idx-1]]
                    interval_to_prev = (mov['start'] - prev_mov['end']) / self.sfreq
                
                interval_to_next = 0
                if pos_idx < len(sequence) - 1:
                    next_mov = movements[sequence[pos_idx+1]]
                    interval_to_next = (next_mov['start'] - mov['end']) / self.sfreq
                
                event = PLMSEvent(
                    type=EventType.PLMS,
                    start_time=mov['start'] / self.sfreq,
                    end_time=mov['end'] / self.sfreq,
                    duration=mov['duration'],
                    confidence=0.8,
                    channels_used=['emg'],
                    amplitude=mov['amplitude'],
                    interval_to_previous=interval_to_prev,
                    interval_to_next=interval_to_next,
                    sequence_index=seq_idx
                )
                
                plms_events.append(event)
        
        return plms_events

# ====================  ====================
class ArousalDetector:
    """detection£¨AASMstandard£©"""
    
    def __init__(self, sfreq: float, config: AASMConfig):
        self.sfreq = sfreq
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def detect_events(self, 
                     eeg_data: np.ndarray,
                     emg_data: Optional[np.ndarray] = None) -> List[ArousalEvent]:
        """detection"""
        
        arousals = []
        
        try:
            # 1. EEG
            delta, theta, alpha, beta = self._compute_band_powers(eeg_data)
            
            # 2. 
            baseline_alpha = np.median(alpha)
            baseline_beta = np.median(beta)
            
            # 3. 
            window_size = int(self.sfreq * 3)  # 3
            step_size = int(self.sfreq * 1)    # 1
            
            candidates = []
            
            for i in range(0, len(eeg_data) - window_size, step_size):
                # 
                current_alpha = np.mean(alpha[i:i+window_size])
                current_beta = np.mean(beta[i:i+window_size])
                current_theta = np.mean(theta[i:i+window_size])
                
                # EEG
                alpha_ratio = current_alpha / (baseline_alpha + 1e-10)
                beta_ratio = current_beta / (baseline_beta + 1e-10)
                
                if (alpha_ratio > self.config.AROUSAL_EEG_SHIFT or 
                    beta_ratio > self.config.AROUSAL_EEG_SHIFT):
                    candidates.append({
                        'start': i,
                        'alpha_ratio': alpha_ratio,
                        'beta_ratio': beta_ratio,
                        'theta_power': current_theta
                    })
            
            # 4. 
            merged_candidates = self._merge_candidates(candidates)
            
            # 5. 
            for cand in merged_candidates:
                arousal = self._validate_candidate(
                    cand, eeg_data, emg_data,
                    baseline_alpha, baseline_beta
                )
                if arousal:
                    arousals.append(arousal)
            
            # 6. 
            # 
            
            self.logger.info(f"detection {len(arousals)} ")
            
        except Exception as e:
            self.logger.error(f"detection: {e}")
        
        return arousals
    
    def _compute_band_powers(self, data: np.ndarray) -> Tuple[np.ndarray, ...]:
        """power"""
        # 
        bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 13),
            'beta': (13, 30)
        }
        
        results = []
        for low, high in bands.values():
            sos = butter(4, [low, high], btype='band', fs=self.sfreq, output='sos')
            filtered = signal.sosfiltfilt(sos, data)
            power = filtered ** 2
            results.append(power)
        
        return tuple(results)
    
    def _merge_candidates(self, candidates: List[Dict]) -> List[Dict]:
        """"""
        if not candidates:
            return []
        
        merged = []
        current = candidates[0].copy()
        
        for next_cand in candidates[1:]:
            gap = next_cand['start'] - current['start']
            
            if gap < self.sfreq * 15:  # 15
                # 
                current['end'] = next_cand['start']
                current['duration'] = (current['end'] - current['start']) / self.sfreq
                current['alpha_ratio'] = max(current['alpha_ratio'], 
                                           next_cand['alpha_ratio'])
                current['beta_ratio'] = max(current['beta_ratio'],
                                          next_cand['beta_ratio'])
            else:
                merged.append(current)
                current = next_cand.copy()
        
        merged.append(current)
        return merged
    
    def _validate_candidate(self, candidate: Dict,
                          eeg_data: np.ndarray,
                          emg_data: Optional[np.ndarray],
                          baseline_alpha: float,
                          baseline_beta: float) -> Optional[ArousalEvent]:
        """validate"""
        
        start = candidate.get('start', 0)
        end = candidate.get('end', start + int(self.sfreq * 10))
        
        duration = (end - start) / self.sfreq
        
        # 
        if not (self.config.AROUSAL_MIN_DURATION <= duration <= 
                self.config.AROUSAL_MAX_DURATION):
            return None
        
        # 
        alpha_ratio = candidate.get('alpha_ratio', 1)
        beta_ratio = candidate.get('beta_ratio', 1)
        
        # EMG£¨£©
        emg_increase = 0
        if emg_data is not None:
            pre_emg = np.mean(emg_data[max(0, start-int(self.sfreq*5)):start])
            during_emg = np.mean(emg_data[start:end])
            if pre_emg > 0:
                emg_increase = during_emg / pre_emg
        
        event = ArousalEvent(
            type=EventType.AROUSAL,
            start_time=start / self.sfreq,
            end_time=end / self.sfreq,
            duration=duration,
            confidence=0.7,
            channels_used=['eeg'] + (['emg'] if emg_data is not None else []),
            eeg_frequency_shift=max(alpha_ratio, beta_ratio),
            emg_increase=emg_increase
        )
        
        return event

# ==================== RERA ====================
class RERADetector:
    """RERAdetection£¨respiration£©"""
    
    def __init__(self, sfreq: float, config: AASMConfig):
        self.sfreq = sfreq
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def detect_events(self,
                     airflow: np.ndarray,
                     effort: np.ndarray,
                     arousals: List[ArousalEvent]) -> List[SleepEvent]:
        """detectionRERA"""
        
        rera_events = []
        
        try:
            # 1. 
            effort_increases = self._detect_effort_increases(effort)
            
            # 2. 
            for arousal in arousals:
                # 30
                arousal_time = arousal.start_time
                
                for effort_start, effort_end in effort_increases:
                    if (effort_end < arousal_time and 
                        arousal_time - effort_end < 30):
                        
                        # RERA
                        duration = effort_end - effort_start
                        if duration >= self.config.RERA_DURATION:
                            event = SleepEvent(
                                type=EventType.RERA,
                                start_time=effort_start,
                                end_time=effort_end,
                                duration=duration,
                                confidence=0.7,
                                channels_used=['effort', 'eeg'],
                                metadata={
                                    'associated_arousal_time': arousal_time,
                                    'effort_increase': True
                                }
                            )
                            rera_events.append(event)
                            break
            
            self.logger.info(f"detection {len(rera_events)} RERA")
            
        except Exception as e:
            self.logger.error(f"RERAdetection: {e}")
        
        return rera_events
    
    def _detect_effort_increases(self, effort: np.ndarray) -> List[Tuple[float, float]]:
        """detectionrespiration"""
        increases = []
        
        # 
        effort_env = np.abs(hilbert(effort))
        
        # 
        window = int(self.sfreq * 5)  # 5
        if window < len(effort_env):
            effort_smooth = np.convolve(effort_env, np.ones(window)/window, mode='same')
        else:
            effort_smooth = effort_env
        
        # 
        baseline = np.median(effort_smooth)
        threshold = baseline * (1 + self.config.EFFORT_THRESHOLD)
        
        above_threshold = effort_smooth > threshold
        
        # 
        diff = np.diff(np.concatenate(([0], above_threshold.astype(int), [0])))
        starts = np.where(diff == 1)[0]
        ends = np.where(diff == -1)[0]
        
        for start, end in zip(starts, ends):
            duration = (end - start) / self.sfreq
            if duration >= self.config.RERA_DURATION:
                increases.append((start / self.sfreq, end / self.sfreq))
        
        return increases

# ====================  ====================
class DesaturationDetector:
    """detection"""
    
    def __init__(self, sfreq: float, config: AASMConfig):
        self.sfreq = sfreq
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def detect_events(self, spo2_data: np.ndarray) -> List[SleepEvent]:
        """detection"""
        
        desats = []
        
        try:
            # 
            spo2_clean = self._clean_spo2(spo2_data)
            
            # 
            window_size = int(self.sfreq * self.config.SPO2_DROP_DURATION)
            step_size = int(self.sfreq * 1)
            
            for i in range(0, len(spo2_clean) - window_size, step_size):
                # 
                window = spo2_clean[i:i+window_size]
                baseline = spo2_clean[i]
                
                # 
                min_val = np.min(window)
                drop = baseline - min_val
                
                if drop >= self.config.SPO2_DROP_THRESHOLD:
                    # 
                    min_idx = i + np.argmin(window)
                    
                    event = SleepEvent(
                        type=EventType.DESATURATION,
                        start_time=i / self.sfreq,
                        end_time=min_idx / self.sfreq,
                        duration=(min_idx - i) / self.sfreq,
                        confidence=0.9,
                        channels_used=['spo2'],
                        metadata={
                            'baseline_spo2': baseline,
                            'nadir_spo2': min_val,
                            'drop': drop
                        }
                    )
                    desats.append(event)
            
            self.logger.info(f"detection {len(desats)} ")
            
        except Exception as e:
            self.logger.error(f"detection: {e}")
        
        return desats
    
    def _clean_spo2(self, data: np.ndarray) -> np.ndarray:
        """signal"""
        # 
        filtered = signal.medfilt(data, kernel_size=5)
        
        # 
        filtered = np.clip(filtered, 60, 100)
        
        return filtered

# ====================  ====================
class SleepEventAnalyzer:
    """sleepanalysis"""
    
    def __init__(self, config: Optional[AASMConfig] = None):
        self.config = config or AASMConfig()
        self.logger = self._setup_logging()
        self.raw = None
        self.sfreq = None
        self.channels = {}
        self.events = []
        
    def _setup_logging(self) -> logging.Logger:
        """"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def load_edf(self, edf_path: str) -> bool:
        """EDFfile"""
        try:
            self.logger.info(f"EDFfile: {edf_path}")
            
            if not os.path.exists(edf_path):
                self.logger.error(f"file: {edf_path}")
                return False
            
            self.raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)
            self.sfreq = self.raw.info['sfreq']
            
            self._identify_channels()
            
            self.logger.info(f": {self.sfreq} Hz")
            self.logger.info(f": {self.raw.times[-1]/3600:.2f} ")
            
            return True
            
        except Exception as e:
            self.logger.error(f"EDF: {e}")
            return False
    
    def _identify_channels(self):
        """"""
        self.channels = {
            'eeg': [], 'eog': [], 'emg': [], 
            'ecg': [], 'resp': [], 'spo2': [],
            'thorax': [], 'abdomen': [], 'other': []
        }
        
        for ch in self.raw.ch_names:
            ch_lower = ch.lower()
            
            # EEG
            if any(k in ch_lower for k in ['eeg', 'c3', 'c4', 'fz', 'cz', 'pz']):
                self.channels['eeg'].append(ch)
            # EOG
            elif any(k in ch_lower for k in ['eog', 'loc', 'roc']):
                self.channels['eog'].append(ch)
            # EMG
            elif any(k in ch_lower for k in ['emg', 'chin', 'leg']):
                self.channels['emg'].append(ch)
            # ECG
            elif any(k in ch_lower for k in ['ecg', 'ekg']):
                self.channels['ecg'].append(ch)
            # 
            elif any(k in ch_lower for k in ['flow', 'airflow', 'nasal']):
                self.channels['resp'].append(ch)
            # 
            elif any(k in ch_lower for k in ['thorax', 'chest']):
                self.channels['thorax'].append(ch)
            # 
            elif any(k in ch_lower for k in ['abdomen', 'abdo']):
                self.channels['abdomen'].append(ch)
            # 
            elif any(k in ch_lower for k in ['spo2', 'sao2', 'oxygen']):
                self.channels['spo2'].append(ch)
            else:
                self.channels['other'].append(ch)
    
    def analyze(self) -> Dict:
        """analysis"""
        
        results = {
            'events': [],
            'indices': {},
            'summary': {}
        }
        
        # 1. 
        if self.channels['resp']:
            self.logger.info("respirationdetection...")
            
            # 
            resp_ch = self.channels['resp'][0]
            resp_data = self.raw.get_data(picks=resp_ch)[0]
            
            # £¨£©
            thorax = None
            abdomen = None
            if self.channels['thorax']:
                thorax = self.raw.get_data(picks=self.channels['thorax'][0])[0]
            if self.channels['abdomen']:
                abdomen = self.raw.get_data(picks=self.channels['abdomen'][0])[0]
            
            # £¨£©
            spo2 = None
            if self.channels['spo2']:
                spo2 = self.raw.get_data(picks=self.channels['spo2'][0])[0]
            
            # 
            detector = RespiratoryEventDetector(self.sfreq, self.config)
            resp_events = detector.detect_events(
                resp_data, thorax, abdomen, spo2
            )
            
            results['events'].extend(resp_events)
            self.logger.info(f"detection {len(resp_events)} respiration")
        
        # 2. 
        if self.channels['emg']:
            self.logger.info("detection...")
            
            # EMG
            leg_emg = [ch for ch in self.channels['emg'] 
                      if 'leg' in ch.lower() or 'tib' in ch.lower()]
            if not leg_emg:
                leg_emg = [self.channels['emg'][0]]
            
            emg_data = self.raw.get_data(picks=leg_emg[0])[0]
            
            detector = PLMSDetector(self.sfreq, self.config)
            plms_events = detector.detect_events(emg_data)
            
            results['events'].extend(plms_events)
            self.logger.info(f"detection {len(plms_events)} PLMS")
        
        # 3. 
        if self.channels['eeg']:
            self.logger.info("detection...")
            
            eeg_ch = self.channels['eeg'][0]
            eeg_data = self.raw.get_data(picks=eeg_ch)[0]
            
            # EMG£¨£©
            emg_data = None
            if self.channels['emg']:
                emg_data = self.raw.get_data(picks=self.channels['emg'][0])[0]
            
            detector = ArousalDetector(self.sfreq, self.config)
            arousal_events = detector.detect_events(eeg_data, emg_data)
            
            results['events'].extend(arousal_events)
            self.logger.info(f"detection {len(arousal_events)} ")
        
        # 4. RERA£¨£©
        if (self.channels['thorax'] and self.channels['abdomen'] and 
            arousal_events):
            self.logger.info("RERAdetection...")
            
            thorax = self.raw.get_data(picks=self.channels['thorax'][0])[0]
            abdomen = self.raw.get_data(picks=self.channels['abdomen'][0])[0]
            
            # 
            effort = np.abs(thorax) + np.abs(abdomen)
            
            detector = RERADetector(self.sfreq, self.config)
            rera_events = detector.detect_events(
                resp_data if 'resp_data' in locals() else None,
                effort,
                arousal_events
            )
            
            results['events'].extend(rera_events)
            self.logger.info(f"detection {len(rera_events)} RERA")
        
        # 5. 
        if self.channels['spo2']:
            self.logger.info("detection...")
            
            spo2 = self.raw.get_data(picks=self.channels['spo2'][0])[0]
            
            detector = DesaturationDetector(self.sfreq, self.config)
            desat_events = detector.detect_events(spo2)
            
            results['events'].extend(desat_events)
            self.logger.info(f"detection {len(desat_events)} ")
        
        # 6. 
        results['indices'] = self._calculate_indices(results['events'])
        
        # 7. 
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _calculate_indices(self, events: List[SleepEvent]) -> Dict:
        """"""
        
        total_hours = self.raw.times[-1] / 3600
        
        indices = {
            'ahi': 0,  # respiration
            'rdi': 0,  # respiration£¨RERA£©
            'plmsi': 0,  # 
            'ari': 0,  # 
            'odi': 0,  # 
            'total_events': len(events)
        }
        
        # AHI£¨+£©
        apnea_hypopnea = [e for e in events 
                         if e.type in [EventType.APNEA_OBSTRUCTIVE,
                                      EventType.APNEA_CENTRAL,
                                      EventType.APNEA_MIXED,
                                      EventType.HYPOPNEA]]
        indices['ahi'] = len(apnea_hypopnea) / total_hours
        
        # RDI£¨AHI + RERA£©
        rdi_events = [e for e in events 
                     if e.type in [EventType.APNEA_OBSTRUCTIVE,
                                  EventType.APNEA_CENTRAL,
                                  EventType.APNEA_MIXED,
                                  EventType.HYPOPNEA,
                                  EventType.RERA]]
        indices['rdi'] = len(rdi_events) / total_hours
        
        # PLMSI
        plms = [e for e in events if e.type == EventType.PLMS]
        indices['plmsi'] = len(plms) / total_hours
        
        # ARI
        arousals = [e for e in events if e.type == EventType.AROUSAL]
        indices['ari'] = len(arousals) / total_hours
        
        # ODI
        desats = [e for e in events if e.type == EventType.DESATURATION]
        indices['odi'] = len(desats) / total_hours
        
        return indices
    
    def _generate_summary(self, results: Dict) -> Dict:
        """"""
        
        indices = results['indices']
        
        summary = {
            'total_events': indices['total_events'],
            'indices': indices,
            'severity': self._classify_severity(indices),
            'recommendations': self._generate_recommendations(indices)
        }
        
        return summary
    
    def _classify_severity(self, indices: Dict) -> Dict:
        """"""
        
        severity = {}
        
        # AHI
        ahi = indices['ahi']
        if ahi < 5:
            severity['ahi'] = Severity.NORMAL.value
        elif ahi < 15:
            severity['ahi'] = Severity.MILD.value
        elif ahi < 30:
            severity['ahi'] = Severity.MODERATE.value
        else:
            severity['ahi'] = Severity.SEVERE.value
        
        # PLMSI
        plmsi = indices['plmsi']
        if plmsi < 5:
            severity['plmsi'] = Severity.NORMAL.value
        elif plmsi < 25:
            severity['plmsi'] = Severity.MILD.value
        else:
            severity['plmsi'] = Severity.MODERATE.value
        
        # ARI
        ari = indices['ari']
        if ari < 10:
            severity['ari'] = Severity.NORMAL.value
        elif ari < 20:
            severity['ari'] = Severity.MILD.value
        else:
            severity['ari'] = Severity.MODERATE.value
        
        return severity
    
    def _generate_recommendations(self, indices: Dict) -> List[str]:
        """"""
        
        recommendations = []
        
        # AHI
        ahi = indices['ahi']
        if ahi >= 30:
            recommendations.append(
                "sleeprespiration£¬sleep£¬CPAP"
            )
        elif ahi >= 15:
            recommendations.append(
                "sleeprespiration£¬sleep£¬"
            )
        elif ahi >= 5:
            recommendations.append(
                "sleeprespiration£¬£¨¡¢¡¢£©"
            )
        
        # PLMSI
        plmsi = indices['plmsi']
        if plmsi >= 25:
            recommendations.append(
                "£¬check£¬"
            )
        elif plmsi >= 5:
            recommendations.append(
                "£¬£¬"
            )
        
        # ARI
        ari = indices['ari']
        if ari >= 20:
            recommendations.append(
                "£¬sleep£¬sleep"
            )
        
        return recommendations

# ====================  ====================
class EventVisualizer:
    """"""
    
    def __init__(self, sfreq: float):
        self.sfreq = sfreq
    
    def plot_events(self, events: List[SleepEvent], 
                   raw: mne.io.Raw,
                   output_path: str):
        """"""
        
        fig, axes = plt.subplots(4, 1, figsize=(16, 12))
        
        # 
        colors = {
            EventType.APNEA_OBSTRUCTIVE: 'red',
            EventType.APNEA_CENTRAL: 'darkred',
            EventType.APNEA_MIXED: 'orange',
            EventType.HYPOPNEA: 'gold',
            EventType.RERA: 'purple',
            EventType.PLMS: 'blue',
            EventType.AROUSAL: 'green',
            EventType.DESATURATION: 'cyan'
        }
        
        # 1. 
        ax1 = axes[0]
        resp_events = [e for e in events if e.type in [
            EventType.APNEA_OBSTRUCTIVE, EventType.APNEA_CENTRAL,
            EventType.APNEA_MIXED, EventType.HYPOPNEA, EventType.RERA
        ]]
        
        for event in resp_events:
            ax1.barh(0, event.duration/60, left=event.start_time/3600,
                    height=0.5, color=colors.get(event.type, 'gray'),
                    alpha=0.7, label=event.type.value)
        
        ax1.set_xlabel(' ()')
        ax1.set_title('respiration')
        ax1.set_yticks([])
        ax1.grid(True, alpha=0.3)
        
        # 2. 
        ax2 = axes[1]
        plms_events = [e for e in events if e.type == EventType.PLMS]
        
        times = [e.start_time/3600 for e in plms_events]
        durations = [e.duration for e in plms_events]
        
        if times:
            ax2.scatter(times, durations, c='blue', alpha=0.6, s=30)
        ax2.set_xlabel(' ()')
        ax2.set_ylabel(' ()')
        ax2.set_title('')
        ax2.grid(True, alpha=0.3)
        
        # 3. 
        ax3 = axes[2]
        arousal_events = [e for e in events if e.type == EventType.AROUSAL]
        
        times = [e.start_time/3600 for e in arousal_events]
        durations = [e.duration for e in arousal_events]
        
        if times:
            ax3.bar(times, durations, width=0.02, color='green', alpha=0.7)
        ax3.set_xlabel(' ()')
        ax3.set_ylabel(' ()')
        ax3.set_title('')
        ax3.grid(True, alpha=0.3)
        
        # 4. 
        ax4 = axes[3]
        desat_events = [e for e in events if e.type == EventType.DESATURATION]
        
        times = [e.start_time/3600 for e in desat_events]
        drops = [e.metadata.get('drop', 0) for e in desat_events]
        
        if times:
            ax4.scatter(times, drops, c='cyan', alpha=0.6, s=50)
        ax4.set_xlabel(' ()')
        ax4.set_ylabel(' (%)')
        ax4.set_title('')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.close()
    
    def plot_hypnogram_with_events(self, events: List[SleepEvent],
                                   stages: Optional[np.ndarray],
                                   output_path: str):
        """sleep"""
        
        fig, ax = plt.subplots(figsize=(16, 6))
        
        # 
        if stages is not None:
            times = np.arange(len(stages)) * 30 / 3600  # 30epoch
            ax.plot(times, stages, 'b-', linewidth=1, alpha=0.7)
        
        # 
        y_pos = {
            EventType.APNEA_OBSTRUCTIVE: 5.5,
            EventType.APNEA_CENTRAL: 5.0,
            EventType.APNEA_MIXED: 4.5,
            EventType.HYPOPNEA: 4.0,
            EventType.RERA: 3.5,
            EventType.PLMS: 3.0,
            EventType.AROUSAL: 2.5,
            EventType.DESATURATION: 2.0
        }
        
        colors = {
            EventType.APNEA_OBSTRUCTIVE: 'red',
            EventType.APNEA_CENTRAL: 'darkred',
            EventType.APNEA_MIXED: 'orange',
            EventType.HYPOPNEA: 'gold',
            EventType.RERA: 'purple',
            EventType.PLMS: 'blue',
            EventType.AROUSAL: 'green',
            EventType.DESATURATION: 'cyan'
        }
        
        for event in events:
            y = y_pos.get(event.type, 1)
            color = colors.get(event.type, 'gray')
            
            ax.plot([event.start_time/3600, event.end_time/3600], 
                   [y, y], color=color, linewidth=3, alpha=0.8)
        
        ax.set_xlabel(' ()')
        ax.set_ylabel('sleep / ')
        ax.set_title('sleep')
        ax.set_ylim(0, 6)
        ax.grid(True, alpha=0.3)
        
        # 
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', alpha=0.7, label='respiration'),
            Patch(facecolor='darkred', alpha=0.7, label='respiration'),
            Patch(facecolor='orange', alpha=0.7, label='respiration'),
            Patch(facecolor='gold', alpha=0.7, label=''),
            Patch(facecolor='purple', alpha=0.7, label='RERA'),
            Patch(facecolor='blue', alpha=0.7, label='PLMS'),
            Patch(facecolor='green', alpha=0.7, label=''),
            Patch(facecolor='cyan', alpha=0.7, label='')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
        
        plt.tight_layout()
        plt.close()

# ====================  ====================
def main():
    """function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='sleepdetection')
    parser.add_argument('edf_file', help='EDFfilepath')
    parser.add_argument('-o', '--output', default='sleep_events_results', 
                       help='')
    parser.add_argument('--config', help='filepath')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("sleepdetection v3.0")
    print("=" * 70 + "\n")
    
    # 
    config = AASMConfig()
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
                for key, value in config_dict.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
            print(f"file: {args.config}\n")
        except Exception as e:
            print(f"file: {e}\n")
    
    # 
    analyzer = SleepEventAnalyzer(config)
    
    # EDF
    if not analyzer.load_edf(args.edf_file):
        print("? EDFfile")
        sys.exit(1)
    
    # 
    print("\n?? analysis...\n")
    results = analyzer.analyze()
    
    # 
    output_dir = Path(args.output)
    
    # 
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 
    events_data = [e.to_dict() for e in results['events']]
    
    
    # 
    
    # 
    visualizer = EventVisualizer(analyzer.sfreq)
    
    plot_path = output_dir / f'events_distribution_{timestamp}.png'
    visualizer.plot_events(results['events'], analyzer.raw, str(plot_path))
    
    # 
    print("\n" + "=" * 70)
    print("?? analysis")
    print("=" * 70)
    
    indices = results['indices']
    print(f"\n?? :")
    print(f"  AHI: {indices['ahi']:.2f} /")
    print(f"  RDI: {indices['rdi']:.2f} /")
    print(f"  PLMSI: {indices['plmsi']:.2f} /")
    print(f"  ARI: {indices['ari']:.2f} /")
    print(f"  ODI: {indices['odi']:.2f} /")
    
    severity = results['summary']['severity']
    print(f"\n?? :")
    print(f"  AHI: {severity['ahi']}")
    print(f"  PLMSI: {severity['plmsi']}")
    print(f"  ARI: {severity['ari']}")
    
    print(f"\n?? :")
    for rec in results['summary']['recommendations']:
        print(f"  ? {rec}")
    
    print(f"\n?? : {output_dir.absolute()}")
    print("\n" + "=" * 70)
    print("? analysis£¡")
    print("=" * 70)

if __name__ == "__main__":
    main()
