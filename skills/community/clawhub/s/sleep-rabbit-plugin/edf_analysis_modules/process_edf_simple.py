#!/usr/bin/env python3
"""
Simple EDF Processing Module - REAL EDF Analysis
Version: 5.1.5
Description: Real EDF file processing with MNE-Python integration
"""

import os
import sys
from datetime import datetime

def process_edf_simple(file_path):
    """
    Real EDF file processing function
    
    Args:
        file_path: Path to EDF file
        
    Returns:
        Dictionary with real EDF analysis results
    """
    try:
        # Check EDF file
        if not os.path.exists(file_path):
            return {"error": f"EDF file not found: {file_path}", "status": "error"}
        
        print("=" * 70)
        print("REAL EDF Processing - AISleepGen 5.1.5")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"File: {file_path}")
        print("=" * 70)
        
        # Try to import MNE for real EDF processing
        try:
            import mne
            import numpy as np
            
            # Load EDF file
            raw = mne.io.read_raw_edf(file_path, preload=True)
            
            # Get basic information
            info = {
                "status": "real_analysis",
                "method": "mne_edf_processing",
                "version": "5.1.5",
                "file_size_bytes": os.path.getsize(file_path),
                "channels": raw.info['nchan'],
                "sampling_frequency": raw.info['sfreq'],
                "duration_seconds": raw.times[-1],
                "channel_names": raw.ch_names[:10],  # First 10 channels
                "file_type": "EDF"
            }
            
            # Add some basic analysis if file is not too large
            if raw.info['nchan'] > 0 and len(raw.times) > 0:
                # Get first channel data for basic stats
                channel_data = raw.get_data(picks=0)[0]
                info["data_statistics"] = {
                    "samples": len(channel_data),
                    "mean": float(np.mean(channel_data)),
                    "std": float(np.std(channel_data)),
                    "min": float(np.min(channel_data)),
                    "max": float(np.max(channel_data))
                }
            
            return info
            
        except ImportError:
            # MNE not available, return basic file info
            return {
                "status": "real_analysis",
                "method": "basic_edf_processing",
                "version": "5.1.5",
                "file_size_bytes": os.path.getsize(file_path),
                "file_type": "EDF",
                "note": "MNE-Python not installed. Install with: pip install mne numpy scipy",
                "recommendation": "For full EDF analysis, install required packages"
            }
            
    except Exception as e:
        return {"error": f"EDF processing error: {str(e)}", "status": "error"}

# For backward compatibility
if __name__ == "__main__":
    # Test if run directly
    if len(sys.argv) > 1:
        result = process_edf_simple(sys.argv[1])
        import json
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python process_edf_simple.py <edf-file>")
        print("Example: python process_edf_simple.py data/sample.edf")