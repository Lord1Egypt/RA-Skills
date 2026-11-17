#!/usr/bin/env python3
"""
不符合项查询脚本
功能:按条件筛选和展示不符合项列表
"""
import json
import argparse
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "assets" / "nc_data.json"

def load_data():
    """加载数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"non_conformances": []}

def filter_nc(data, args):
    """筛选不符合项"""
    results = data.get('non_conformances', [])
    
    if args.status:
        results = [nc for nc in results if nc['verification']['status'] == args.status]
    
    if args.clause:
        results = [nc for nc in results if args.clause in nc['clause']]
    
    if args.category:
        results = [nc for nc in results if nc['category'] == args.category]
    
    if args.audit_id:
        results = [nc for nc in results if nc['audit_info']['audit_id'] == args.audit_id]
    
    if args.nc_id:
        results = [nc for nc in results if nc['id'] == args.nc_id]
    
    return results

def format_nc(nc, verbose=False):
    """格式化输出"""
    if verbose:
        return f"""
ID: {nc['id']}
标题: {nc['title']}
条款: {nc['clause']}
类别: {nc['category']}
描述: {nc['description']}
证据: {', '.join(nc['evidence']) if nc['evidence'] else '无'}
根本原因: {nc['root_cause'] or '未填写'}
纠正措施: {nc['corrective_action'] or '未填写'}
验证状态: {nc['verification']['status']}
验证人: {nc['verification']['verifier'] or '未分配'}
验证结果: {nc['verification']['result'] or '待验证'}
审核ID: {nc['audit_info']['audit_id'] or '未关联'}
审核日期: {nc['audit_info']['audit_date']}
创建时间: {nc['created_at'][:10]}
"""
    else:
        status_icon = {'open': '○', 'in_progress': '◐', 'verified': '◓', 'closed': '●'}
        icon = status_icon.get(nc['verification']['status'], '○')
        return f"{icon} [{nc['id']}] {nc['clause']} | {nc['category']:10} | {nc['title'][:40]}"

def list_nc(args):
    """列出不符合项"""
    data = load_data()
    results = filter_nc(data, args)
    
    if not results:
        result = {"status": "success", "message": "未找到符合条件的记录", "count": 0, "items": []}
        print(json.dumps(result, ensure_ascii=False))
        return result
    
    output = []
    for nc in results:
        output.append(format_nc(nc, verbose=args.verbose))
    
    result = {
        "status": "success",
        "count": len(results),
        "items": results,
        "summary": "\n".join(output)
    }
    
    if args.verbose:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"\n{'='*70}")
        print(f"共找到 {len(results)} 条不符合项:")
        print(f"{'='*70}")
        for line in output:
            print(line)
        print(f"{'='*70}")
    
    return result

def main():
    parser = argparse.ArgumentParser(description='查询不符合项')
    parser.add_argument('--status', choices=['open', 'in_progress', 'verified', 'closed'],
                        help='按验证状态筛选')
    parser.add_argument('--clause', help='按条款编号筛选(支持模糊匹配)')
    parser.add_argument('--category', choices=['major', 'minor', 'observation'],
                        help='按类别筛选')
    parser.add_argument('--audit-id', help='按审核ID筛选')
    parser.add_argument('--nc-id', help='按不符合项ID精确筛选')
    parser.add_argument('--verbose', action='store_true', help='详细输出(JSON格式)')
    
    args = parser.parse_args()
    list_nc(args)

if __name__ == "__main__":
    main()
