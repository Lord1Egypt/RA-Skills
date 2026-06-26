#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


def read_status(status_file: str) -> Dict[str, Any]:
    if not os.path.exists(status_file):
        return {}
    
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def write_status(status_file: str, status: Dict[str, Any]) -> bool:
    try:
        os.makedirs(os.path.dirname(status_file), exist_ok=True)
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False


def get_last_fetch_time(status: Dict[str, Any], data_type: str) -> Optional[str]:
    data_info = status.get(data_type, {})
    return data_info.get('last_fetch_time')


def update_fetch_time(status: Dict[str, Any], data_type: str, fetch_time: str, fetch_count: int = 0) -> Dict[str, Any]:
    if data_type not in status:
        status[data_type] = {
            'fetch_count': 0,
            'last_fetch_count': 0
        }
    
    status[data_type]['last_fetch_time'] = fetch_time
    status[data_type]['fetch_count'] = status[data_type].get('fetch_count', 0) + 1
    status[data_type]['last_fetch_count'] = fetch_count
    
    return status


def calculate_date_range(
    status: Dict[str, Any], 
    data_type: str, 
    default_years: int = 3
) -> Dict[str, str]:
    today = datetime.now()
    default_start = (today - timedelta(days=default_years * 365)).strftime('%Y%m%d')
    default_end = today.strftime('%Y%m%d')
    
    last_fetch_time = get_last_fetch_time(status, data_type)
    
    if not last_fetch_time:
        return {
            'start_date': default_start,
            'end_date': default_end,
            'is_incremental': False
        }
    
    try:
        last_date = datetime.strptime(last_fetch_time, '%Y-%m-%d %H:%M:%S')
        start_date = (last_date + timedelta(days=1)).strftime('%Y%m%d')
        
        if start_date > default_end:
            return {
                'start_date': default_end,
                'end_date': default_end,
                'is_incremental': True
            }
        
        return {
            'start_date': start_date,
            'end_date': default_end,
            'is_incremental': True
        }
    except ValueError:
        return {
            'start_date': default_start,
            'end_date': default_end,
            'is_incremental': False
        }


def init_status_structure() -> Dict[str, Any]:
    return {
        'market': {
            'last_fetch_time': None,
            'fetch_count': 0,
            'last_fetch_count': 0
        },
        'north_flow': {
            'last_fetch_time': None,
            'fetch_count': 0,
            'last_fetch_count': 0
        },
        'lhb': {
            'last_fetch_time': None,
            'fetch_count': 0,
            'last_fetch_count': 0
        },
        'sentiment': {
            'last_fetch_time': None,
            'fetch_count': 0,
            'last_fetch_count': 0
        },
        'financial': {
            'last_fetch_time': None,
            'fetch_count': 0,
            'last_fetch_count': 0
        }
    }


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print(json.dumps({'error': '缺少参数'}))
        sys.exit(1)
    
    action = sys.argv[1]
    input_data = sys.stdin.read()
    params = json.loads(input_data) if input_data else {}
    
    status_file = params.get('status_file', 'config/fetch_status.json')
    
    if action == 'read':
        status = read_status(status_file)
        print(json.dumps(status, ensure_ascii=False))
    
    elif action == 'get_last_time':
        status = read_status(status_file)
        data_type = params.get('data_type')
        last_time = get_last_fetch_time(status, data_type)
        print(json.dumps({'last_fetch_time': last_time}, ensure_ascii=False))
    
    elif action == 'update_time':
        status = read_status(status_file)
        data_type = params.get('data_type')
        fetch_time = params.get('fetch_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        fetch_count = params.get('fetch_count', 0)
        
        status = update_fetch_time(status, data_type, fetch_time, fetch_count)
        success = write_status(status_file, status)
        print(json.dumps({'success': success}, ensure_ascii=False))
    
    elif action == 'calculate_range':
        status = read_status(status_file)
        data_type = params.get('data_type')
        default_years = params.get('default_years', 3)
        
        date_range = calculate_date_range(status, data_type, default_years)
        print(json.dumps(date_range, ensure_ascii=False))
    
    elif action == 'init':
        status = init_status_structure()
        success = write_status(status_file, status)
        print(json.dumps({'success': success}, ensure_ascii=False))
    
    else:
        print(json.dumps({'error': '未知的操作类型'}))
        sys.exit(1)
