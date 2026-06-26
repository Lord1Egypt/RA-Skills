#!/usr/bin/env python3
"""
Analyze music tracks for beat detection and sync transitions.

Uses librosa for beat detection to synchronize video transitions
with music rhythm.

Requirements:
    pip install librosa

Usage:
    python music-sync.py music.mp3 --output beats.json
    python music-sync.py music.mp3 --find-peaks --count 10
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import librosa
    import numpy as np
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False


def check_librosa():
    """Check if librosa is installed."""
    if not HAS_LIBROSA:
        print("Error: librosa not installed. Run: pip install librosa")
        return False
    return True


def analyze_beats(audio_path: str, sr: int = 22050, verbose: bool = False) -> dict:
    """Analyze audio file for beats and tempo."""
    if not check_librosa():
        return None
    
    if verbose:
        print(f"Loading: {audio_path}")
    
    # Load audio
    y, sr = librosa.load(audio_path, sr=sr)
    duration = len(y) / sr
    
    if verbose:
        print(f"Duration: {duration:.2f}s")
        print("Detecting beats...")
    
    # Beat detection
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    
    # Convert beat frames to time
    beat_times = librosa.frames_to_time(beats, sr=sr)
    
    # Get tempo (BPM)
    if isinstance(tempo, np.ndarray):
        tempo = float(tempo[0]) if len(tempo) > 0 else 120.0
    else:
        tempo = float(tempo)
    
    if verbose:
        print(f"Tempo: {tempo:.1f} BPM")
        print(f"Beats detected: {len(beat_times)}")
    
    return {
        "duration": duration,
        "tempo": round(tempo, 1),
        "beats": beat_times.tolist(),
        "sample_rate": sr
    }


def find_peaks(audio_path: str, count: int = 10, verbose: bool = False) -> list:
    """Find energy peaks in audio for highlight moments."""
    if not check_librosa():
        return []
    
    y, sr = librosa.load(audio_path)
    
    # Compute RMS energy
    rms = librosa.feature.rms(y=y)[0]
    
    # Find peaks
    from scipy.signal import find_peaks as scipy_find_peaks
    peaks, _ = scipy_find_peaks(rms, height=rms.mean(), distance=sr//2)
    
    # Convert to times and sort by energy
    peak_times = librosa.frames_to_time(peaks, sr=sr)
    peak_energies = rms[peaks]
    
    # Get top peaks by energy
    if len(peak_times) > count:
        sorted_indices = np.argsort(peak_energies)[-count:]
        peak_times = peak_times[sorted_indices]
        peak_energies = peak_energies[sorted_indices]
    
    # Sort by time
    sorted_by_time = sorted(zip(peak_times, peak_energies), key=lambda x: x[0])
    
    if verbose:
        print(f"Found {len(sorted_by_time)} energy peaks:")
        for i, (t, e) in enumerate(sorted_by_time, 1):
            print(f"  {i}. {t:.2f}s (energy: {e:.3f})")
    
    return [{"time": float(t), "energy": float(e)} for t, e in sorted_by_time]


def generate_transition_points(beats: list, duration: float, 
                                num_transitions: int = 5,
                                min_gap: float = 2.0) -> list:
    """Generate evenly distributed transition points aligned to beats."""
    if not beats:
        return []
    
    # Calculate ideal spacing
    intervals = []
    current_start = 0
    
    for i in range(num_transitions):
        # Find nearest beat after ideal time
        ideal_time = (i + 1) * (duration / (num_transitions + 1))
        nearest_beat = min(beats, key=lambda b: abs(b - ideal_time))
        
        if nearest_beat > current_start + min_gap:
            intervals.append(nearest_beat)
            current_start = nearest_beat
    
    return intervals


def sync_video_to_beats(video_path: str, beats: list, 
                        output_path: str,
                        transition_style: str = "cut",
                        verbose: bool = False) -> bool:
    """Create video synced to beats using FFmpeg."""
    
    if transition_style == "cut":
        # Hard cut at each beat
        # This is complex - would need to split and concatenate
        pass
    elif transition_style == "fade":
        # Fade transition at each beat
        pass
    elif transition_style == "zoom":
        # Zoom/beat drop effect
        pass
    
    # For MVP, just save beat data for manual use
    if verbose:
        print("Beat sync data saved. Use transition_points in video editor.")
    
    return True


def analyze_track(input_path: str, output_path: str = None,
                  find_peaks: bool = False, peak_count: int = 10,
                  verbose: bool = False) -> dict:
    """Full analysis of music track."""
    
    # Beat analysis
    beat_data = analyze_beats(input_path, verbose=verbose)
    
    if not beat_data:
        return None
    
    result = {
        "file": input_path,
        "duration": beat_data["duration"],
        "tempo": beat_data["tempo"],
        "beats": beat_data["beats"],
        "sample_rate": beat_data["sample_rate"]
    }
    
    # Peak finding
    if find_peaks:
        peaks = find_peaks(input_path, count=peak_count, verbose=verbose)
        result["energy_peaks"] = peaks
        result["transition_points"] = generate_transition_points(
            beat_data["beats"], 
            beat_data["duration"],
            num_transitions=peak_count
        )
    
    # Generate beat intervals for common use cases
    result["beat_interval"] = 60.0 / beat_data["tempo"]  # Time per beat
    result["bar_interval"] = result["beat_interval"] * 4  # 4 beats per bar
    
    # Common edit points
    result["suggested_cuts"] = []
    beats = beat_data["beats"]
    bar_len = 4
    
    for i in range(bar_len, len(beats) - bar_len, bar_len):
        if i + bar_len < len(beats):
            result["suggested_cuts"].append({
                "start": beats[i - bar_len],
                "end": beats[i],
                "bars": 1
            })
    
    # Save to file if requested
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        if verbose:
            print(f"Analysis saved to: {output_path}")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Analyze music for beat-synced transitions")
    parser.add_argument("input", help="Input audio file")
    parser.add_argument("--output", "-o", help="Output analysis JSON")
    parser.add_argument("--find-peaks", "-p", action="store_true", 
                        help="Find energy peaks")
    parser.add_argument("--peak-count", "-c", type=int, default=10,
                        help="Number of peaks to find")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    if not check_librosa():
        sys.exit(1)
    
    output_path = args.output or str(Path(args.input).with_suffix('.json'))
    
    result = analyze_track(
        args.input, output_path,
        find_peaks=args.find_peaks,
        peak_count=args.peak_count,
        verbose=args.verbose
    )
    
    if not result:
        sys.exit(1)
    
    if args.verbose:
        print(f"\nTrack Summary:")
        print(f"  Duration: {result['duration']:.2f}s")
        print(f"  Tempo: {result['tempo']:.1f} BPM")
        print(f"  Beat interval: {result['beat_interval']:.3f}s")
        print(f"  Beats: {len(result['beats'])}")
        if 'energy_peaks' in result:
            print(f"  Energy peaks: {len(result['energy_peaks'])}")
    
    sys.exit(0)


if __name__ == "__main__":
    main()