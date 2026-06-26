#!/usr/bin/env python3
"""
Procedural Memory: Записывает работающие команды и скрипты
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

from config import PROCEDURAL_FILE

def record_procedure(name: str, command: str, description: str, category: str = "general"):
    """Записывает процедуру."""
    
    procedure = {
        'timestamp': datetime.now().isoformat(),
        'name': name,
        'command': command,
        'description': description,
        'category': category,
        'uses': 0,
        'last_used': None
    }
    
    with open(PROCEDURAL_FILE, 'a') as f:
        f.write(json.dumps(procedure) + '\n')
    
    print(f"✅ Procedure recorded: {name}")
    return procedure


def get_procedures(category: str = None):
    """Получить все процедуры."""
    procedures = []
    if os.path.exists(PROCEDURAL_FILE):
        with open(PROCEDURAL_FILE) as f:
            for line in f:
                try:
                    proc = json.loads(line)
                    if category is None or proc.get('category') == category:
                        procedures.append(proc)
                except:
                    pass
    return procedures


def search_procedure(query: str):
    """Найти процедуру по ключевым словам."""
    procedures = get_procedures()
    query_lower = query.lower()
    
    results = []
    for proc in procedures:
        if (query_lower in proc.get('name', '').lower() or 
            query_lower in proc.get('description', '').lower() or
            query_lower in proc.get('command', '').lower()):
            results.append(proc)
    
    return results


def increment_use(proc_name: str):
    """Увеличить счётчик использования."""
    if not os.path.exists(PROCEDURAL_FILE):
        return
    
    procedures = get_procedures()
    
    with open(PROCEDURAL_FILE, 'w') as f:
        for proc in procedures:
            if proc.get('name') == proc_name:
                proc['uses'] = proc.get('uses', 0) + 1
                proc['last_used'] = datetime.now().isoformat()
            f.write(json.dumps(proc) + '\n')


def init_procedures():
    """Инициализировать базовые процедуры."""
    
    base_procedures = [
        {
            'name': 'run_self_improvement',
            'command': 'python3 scripts/self_improvement_cycle.py',
            'description': 'Запустить цикл самоулучшения',
            'category': 'maintenance'
        },
        {
            'name': 'check_errors',
            'command': 'python3 scripts/topic_selector.py --analyze-only',
            'description': 'Проверить ошибки и получить рекомендации',
            'category': 'maintenance'
        },
    ]
    
    existing = get_procedures()
    if existing:
        return
    
    for proc in base_procedures:
        proc['timestamp'] = datetime.now().isoformat()
        proc['uses'] = 0
        proc['last_used'] = None
        with open(PROCEDURAL_FILE, 'a') as f:
            f.write(json.dumps(proc) + '\n')
    
    print(f"✅ Initialized {len(base_procedures)} base procedures")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        init_procedures()
        print("\nProcedures:")
        for p in get_procedures():
            print(f"  - {p['name']}: {p['description']}")
    elif sys.argv[1] == '--search':
        query = sys.argv[2] if len(sys.argv) > 2 else ''
        results = search_procedure(query)
        print(json.dumps(results, indent=2))
    elif sys.argv[1] == '--category':
        category = sys.argv[2] if len(sys.argv) > 2 else None
        results = get_procedures(category)
        print(json.dumps(results, indent=2))
