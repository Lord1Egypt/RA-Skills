#!/usr/bin/env python3
"""
Auto-Trigger: Запускает Self-Improvement при обнаружении ошибок
Универсальная версия - использует config.py
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Add skill directory to path for config import
import sys
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

from config import (
    ERROR_LOG, TRIGGER_LOG, SELF_IMPROVEMENT_CMD, 
    WORKSPACE, SCRIPTS_DIR
)

def check_and_trigger():
    """Проверяет есть ли новые ошибки и запускает Self-Improvement если нужно."""
    
    # Читаем последние ошибки
    if not os.path.exists(ERROR_LOG):
        print(f"No errors log found at {ERROR_LOG}")
        return {"triggered": False, "reason": "no_error_log"}
    
    with open(ERROR_LOG) as f:
        lines = f.readlines()
    
    if not lines:
        return {"triggered": False, "reason": "no_errors"}
    
    # Читаем когда последний раз запускали
    last_trigger = None
    if os.path.exists(TRIGGER_LOG):
        with open(TRIGGER_LOG) as f:
            data = json.load(f)
            last_trigger = data.get('last_trigger')
    
    # Проверяем новые ошибки
    new_errors = []
    for line in lines:
        try:
            err = json.loads(line)
            err_time = err.get('timestamp', '')
            if last_trigger and err_time <= last_trigger:
                continue
            new_errors.append(err)
        except:
            pass
    
    if not new_errors:
        return {"triggered": False, "reason": "no_new_errors"}
    
    # Есть новые ошибки - запускаем Self-Improvement
    print(f"Found {len(new_errors)} new errors! Triggering Self-Improvement...")
    
    # Используем абсолютный путь
    script_path = os.path.join(SCRIPTS_DIR, 'self_improvement_cycle.py')
    
    try:
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=WORKSPACE
        )
        
        # Записываем время последнего запуска
        with open(TRIGGER_LOG, 'w') as f:
            json.dump({
                'last_trigger': datetime.now().isoformat(),
                'errors_count': len(new_errors),
                'result': 'success' if result.returncode == 0 else 'failed'
            }, f, indent=2)
        
        return {
            "triggered": True,
            "reason": f"{len(new_errors)} new errors",
            "result": result.returncode
        }
        
    except Exception as e:
        return {"triggered": False, "error": str(e)}


if __name__ == "__main__":
    result = check_and_trigger()
    print(json.dumps(result, indent=2))
