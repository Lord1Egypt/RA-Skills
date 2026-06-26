#!/usr/bin/env python3
"""
Whoop Data Processor - Self-contained version
"""
import json
import os
from datetime import datetime

# Get skill directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(SKILL_DIR, 'data')
OUTPUT_DIR = os.path.join(SKILL_DIR, 'data', 'processed')

def process_cycles(data):
    records = data.get('records', [])
    processed = []
    
    for r in records:
        score = r.get('score', {})
        start = r.get('start', '')
        
        # Convert UTC to date
        if start:
            date = start[:10]
        else:
            date = 'Unknown'
        
        processed.append({
            'date': date,
            'strain': score.get('strain', 0),
            'kilojoules': score.get('kilojoule', 0),
            'avg_hr': score.get('average_heart_rate', 0),
            'max_hr': score.get('max_heart_rate', 0),
            'distance': score.get('distance_meter', 0) / 1000 if score.get('distance_meter') else 0
        })
    
    return processed

def process_sleep(data):
    records = data.get('records', [])
    processed = []
    
    for r in records:
        score = r.get('score', {})
        stage = score.get('stage_summary', {})
        start = r.get('start', '')
        
        if start:
            date = start[:10]
        else:
            date = 'Unknown'
        
        # Check if nap
        nap = r.get('nap', False)
        
        in_bed_ms = stage.get('total_in_bed_time_milli', 0)
        in_bed_hours = in_bed_ms / 3600000 if in_bed_ms else 0
        
        processed.append({
            'date': date,
            'nap': nap,
            'total_in_bed_hours': round(in_bed_hours, 1),
            'sleep_performance': score.get('sleep_performance_percentage', 0),
            'sleep_efficiency': score.get('sleep_efficiency_percentage', 0),
            'respiratory_rate': score.get('respiratory_rate', 0),
            'light_sleep_hours': round(stage.get('total_light_sleep_time_milli', 0) / 3600000, 1),
            'deep_sleep_hours': round(stage.get('total_slow_wave_sleep_time_milli', 0) / 3600000, 1),
            'rem_sleep_hours': round(stage.get('total_rem_sleep_time_milli', 0) / 3600000, 1),
            'disturbances': stage.get('disturbance_count', 0)
        })
    
    return processed

def process_recovery(data):
    records = data.get('records', [])
    processed = []
    
    for r in records:
        score = r.get('score', {})
        sleep_id = r.get('sleep_id', '')
        
        # Get date from sleep record
        date = 'Unknown'
        if sleep_id:
            for s in data.get('sleep_records', []):
                if s.get('id') == sleep_id:
                    start = s.get('start', '')
                    if start:
                        date = start[:10]
                    break
        
        processed.append({
            'date': date,
            'recovery_score': score.get('recovery_score', 0),
            'hrv': round(score.get('hrv_rmssd_milli', 0), 1),
            'rhr': score.get('resting_heart_rate', 0),
            'spo2': score.get('spo2_percentage', 0),
            'skin_temp': round(score.get('skin_temp_celsius', 0), 1)
        })
    
    return processed

def main():
    # Ensure output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load raw data
    cycles_file = os.path.join(DATA_DIR, 'cycles_raw.json')
    sleep_file = os.path.join(DATA_DIR, 'sleep_raw.json')
    recovery_file = os.path.join(DATA_DIR, 'recovery_raw.json')
    
    try:
        with open(cycles_file) as f:
            cycles_data = json.load(f)
        cycles = process_cycles(cycles_data)
    except Exception as e:
        print(f"Error processing cycles: {e}")
        cycles = []
    
    try:
        with open(sleep_file) as f:
            sleep_data = json.load(f)
        sleep = process_sleep(sleep_data)
    except Exception as e:
        print(f"Error processing sleep: {e}")
        sleep = []
    
    try:
        with open(recovery_file) as f:
            recovery_data = json.load(f)
        recovery = process_recovery(recovery_data)
    except Exception as e:
        print(f"Error processing recovery: {e}")
        recovery = []
    
    # Save processed data
    output = {
        'processed': {
            'cycles': cycles,
            'sleep': sleep,
            'recovery': recovery
        },
        'generated_at': datetime.now().isoformat()
    }
    
    output_file = os.path.join(OUTPUT_DIR, 'latest.json')
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Data processed and saved!")
    print(f"📊 Recovery records: {len(recovery)}")
    print(f"📊 Sleep records: {len(sleep)}")
    print(f"📊 Cycle records: {len(cycles)}")

if __name__ == '__main__':
    main()
