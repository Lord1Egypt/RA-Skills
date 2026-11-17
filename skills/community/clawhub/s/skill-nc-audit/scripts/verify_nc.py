#!/usr/bin/env python3
"""
不符合项验证跟踪脚本
功能:更新不符合项验证状态,记录验证人和验证结果
"""
import json
import argparse
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent.parent / "assets" / "nc_data.json"

# 状态流转定义
STATUS_FLOW = {
    "open": ["in_progress", "closed"],
    "in_progress": ["verified", "open"],
    "verified": ["closed", "in_progress"],
    "closed": []
}

def load_data():
    """加载数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"non_conformances": []}

def save_data(data):
    """保存数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def validate_transition(current_status, new_status):
    """验证状态流转是否合法"""
    if new_status not in STATUS_FLOW:
        return False, f"无效状态: {new_status}"
    
    allowed = STATUS_FLOW.get(current_status, [])
    if new_status not in allowed and new_status != current_status:
        return False, f"不允许的状态转换: {current_status} -> {new_status}"
    
    return True, "状态转换有效"

def update_verification(nc_id, status, verifier=None, result=None):
    """更新验证状态"""
    data = load_data()
    
    # 查找不符合项
    nc = None
    for item in data['non_conformances']:
        if item['id'] == nc_id:
            nc = item
            break
    
    if not nc:
        return {"status": "error", "message": f"未找到不符合项: {nc_id}"}
    
    # 验证状态转换
    current_status = nc['verification']['status']
    is_valid, msg = validate_transition(current_status, status)
    
    if not is_valid:
        return {"status": "error", "message": msg}
    
    # 更新验证信息
    nc['verification']['status'] = status
    
    if verifier:
        nc['verification']['verifier'] = verifier
    
    if result:
        nc['verification']['result'] = result
        nc['verification']['verified_at'] = datetime.now().strftime("%Y-%m-%d")
    
    save_data(data)
    
    return {
        "status": "success",
        "message": f"状态已更新: {current_status} -> {status}",
        "nc_id": nc_id,
        "new_status": status,
        "verifier": nc['verification']['verifier'],
        "result": nc['verification']['result']
    }

def verify(args):
    """验证跟踪"""
    if not args.nc_id:
        result = {"status": "error", "message": "必须提供--nc-id参数"}
        print(json.dumps(result, ensure_ascii=False))
        return result
    
    # 确定新状态
    new_status = args.status if args.status else "in_progress"
    
    result = update_verification(
        nc_id=args.nc_id,
        status=new_status,
        verifier=args.verifier,
        result=args.result
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result

def get_statistics():
    """获取验证状态统计"""
    data = load_data()
    stats = {
        "total": len(data['non_conformances']),
        "by_status": {"open": 0, "in_progress": 0, "verified": 0, "closed": 0},
        "by_category": {"major": 0, "minor": 0, "observation": 0}
    }
    
    for nc in data['non_conformances']:
        status = nc['verification']['status']
        category = nc['category']
        
        if status in stats['by_status']:
            stats['by_status'][status] += 1
        if category in stats['by_category']:
            stats['by_category'][category] += 1
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='验证跟踪')
    parser.add_argument('--nc-id', required=True, help='不符合项ID')
    parser.add_argument('--status', choices=['open', 'in_progress', 'verified', 'closed'],
                        help='新状态(默认in_progress)')
    parser.add_argument('--verifier', help='验证人')
    parser.add_argument('--result', help='验证结果')
    
    args = parser.parse_args()
    verify(args)

if __name__ == "__main__":
    main()
