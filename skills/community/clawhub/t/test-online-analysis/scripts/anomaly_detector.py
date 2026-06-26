#!/usr/bin/env python3
"""
Anomaly Detector for Online Analysis Skill
Real-time anomaly detection from data streams
"""

import numpy as np
from typing import List, Dict, Any
from datetime import datetime
from collections import deque

class AnomalyDetector:
    def __init__(self, window_size: int = 100, threshold: float = 3.0):
        self.window_size = window_size
        self.threshold = threshold
        self.data_window = deque(maxlen=window_size)
        self.baseline_mean = None
        self.baseline_std = None
        self.anomalies = []
    
    def update_baseline(self) -> None:
        """Update baseline statistics from current window"""
        if len(self.data_window) < self.window_size // 2:
            return
        
        numeric_data = [x for x in self.data_window if isinstance(x, (int, float))]
        if numeric_data:
            self.baseline_mean = np.mean(numeric_data)
            self.baseline_std = np.std(numeric_data)
    
    def add_data_point(self, value: Any, metadata: Dict = None) -> Dict[str, Any]:
        """Add a single data point and check for anomalies"""
        self.data_window.append(value)
        self.update_baseline()
        
        anomaly = None
        if isinstance(value, (int, float)) and self.baseline_mean is not None and self.baseline_std > 0:
            z_score = abs((value - self.baseline_mean) / self.baseline_std)
            if z_score > self.threshold:
                anomaly = {
                    'timestamp': datetime.now().isoformat(),
                    'value': value,
                    'expected_mean': self.baseline_mean,
                    'expected_std': self.baseline_std,
                    'z_score': z_score,
                    'severity': 'high' if z_score > 5 else 'medium' if z_score > 4 else 'low',
                    'metadata': metadata or {}
                }
                self.anomalies.append(anomaly)
        
        return anomaly
    
    def analyze_batch(self, data: List[Any]) -> List[Dict[str, Any]]:
        """Analyze a batch of data points"""
        batch_anomalies = []
        for point in data:
            anomaly = self.add_data_point(point)
            if anomaly:
                batch_anomalies.append(anomaly)
        return batch_anomalies
    
    def get_anomalies(self, severity: str = None) -> List[Dict[str, Any]]:
        """Get all detected anomalies, optionally filtered by severity"""
        if severity:
            return [a for a in self.anomalies if a['severity'] == severity]
        return self.anomalies
    
    def generate_report(self) -> str:
        """Generate anomaly report in markdown format"""
        md = "# Anomaly Detection Report\n\n"
        md += f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md += f"Total data points processed: {len(self.data_window)}\n"
        md += f"Total anomalies detected: {len(self.anomalies)}\n\n"
        
        if self.anomalies:
            md += "## Anomalies\n\n"
            md += "| Timestamp | Value | Expected Mean | Z-Score | Severity |\n"
            md += "|-----------|-------|---------------|---------|----------|\n"
            
            for anomaly in sorted(self.anomalies, key=lambda x: x['z_score'], reverse=True):
                md += f"| {anomaly['timestamp']} | {anomaly['value']} | {anomaly['expected_mean']:.2f} | {anomaly['z_score']:.2f} | {anomaly['severity']} |\n"
        
        return md

if __name__ == "__main__":
    import sys
    import json
    
    detector = AnomalyDetector()
    
    if len(sys.argv) < 2:
        # Generate test data
        test_data = np.random.normal(100, 10, 200).tolist()
        test_data[50] = 200  # Anomaly
        test_data[150] = 50   # Anomaly
        
        anomalies = detector.analyze_batch(test_data)
        print(detector.generate_report())
    else:
        with open(sys.argv[1], 'r') as f:
            if sys.argv[1].endswith('.json'):
                data = json.load(f)
            else:
                data = [float(line.strip()) for line in f if line.strip()]
        
        anomalies = detector.analyze_batch(data)
        print(detector.generate_report())
