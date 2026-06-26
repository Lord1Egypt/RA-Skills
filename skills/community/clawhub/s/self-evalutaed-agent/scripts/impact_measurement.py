#!/usr/bin/env python3
"""
Impact Measurement: Измеряет эффект после выполнения задачи
Универсальная версия - использует config.py
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Add skill directory to path for config import
import sys
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

from config import IMPACT_LOG

def record_impact(task_name: str, metric_before: dict, metric_after: dict, task_type: str = "improvement"):
    """Записывает измерение impact."""
    
    measurement = {
        'timestamp': datetime.now().isoformat(),
        'task_name': task_name,
        'task_type': task_type,
        'before': metric_before,
        'after': metric_after,
        'delta': {
            k: metric_after.get(k, 0) - metric_before.get(k, 0)
            for k in set(list(metric_before.keys()) + list(metric_after.keys()))
        }
    }
    
    with open(IMPACT_LOG, 'a') as f:
        f.write(json.dumps(measurement) + '\n')
    
    print(f"✅ Impact recorded for: {task_name}")
    return measurement


def get_recent_impacts(limit: int = 10):
    """Получить последние измерения."""
    impacts = []
    if os.path.exists(IMPACT_LOG):
        with open(IMPACT_LOG) as f:
            for line in f.readlines()[-limit:]:
                try:
                    impacts.append(json.loads(line))
                except:
                    pass
    return impacts


def summarize_impacts():
    """Сводка по impact за последнее время."""
    impacts = get_recent_impacts(30)
    
    if not impacts:
        return {"total": 0, "message": "No measurements yet"}
    
    by_type = {}
    for imp in impacts:
        t = imp.get('task_type', 'unknown')
        if t not in by_type:
            by_type[t] = {'count': 0, 'improvements': 0, 'regressions': 0}
        
        by_type[t]['count'] += 1
        
        delta = imp.get('delta', {})
        if any(v < 0 for v in delta.values() if isinstance(v, (int, float))):
            by_type[t]['regressions'] += 1
        else:
            by_type[t]['improvements'] += 1
    
    return {
        'total': len(impacts),
        'by_type': by_type,
        'recent': impacts[-5:]
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--summarize':
        result = summarize_impacts()
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == '--record':
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--task', required=True)
        parser.add_argument('--before', required=True)
        parser.add_argument('--after', required=True)
        parser.add_argument('--type', default='improvement')
        args = parser.parse_args(sys.argv[2:])
        
        record_impact(
            args.task,
            json.loads(args.before),
            json.loads(args.after),
            args.type
        )
    else:
        print("Usage:")
        print("  python3 impact_measurement.py --record --task 'name' --before '{}' --after '{}'")
        print("  python3 impact_measurement.py --summarize")
