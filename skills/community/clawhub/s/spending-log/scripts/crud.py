#!/usr/bin/env python3
"""支出记录数据操作（增删改查）"""

import json
import argparse
import os
import time
import uuid
try:
    import fcntl
except ImportError:
    fcntl = None
from datetime import datetime

from module import CATEGORIES, load_data


def save_data(filepath, expenses):
    """写入临时文件再 rename，带文件锁防止并发写入"""
    lock_path = filepath + '.lock'
    lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    try:
        if fcntl:
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
        tmp_path = filepath + '.tmp'
        with open(tmp_path, 'w') as f:
            json.dump(expenses, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, filepath)
    finally:
        if fcntl:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)
        try:
            os.unlink(lock_path)
        except OSError:
            pass


def add_record(filepath, amount, category, description, date=None):
    """新增记录"""
    # 校验
    if float(amount) <= 0:
        print(json.dumps({'error': '金额必须为正数'}, ensure_ascii=False))
        return None
    if category not in CATEGORIES:
        print(json.dumps({'error': f'分类无效，可选: {", ".join(CATEGORIES)}'}, ensure_ascii=False))
        return None
    if date:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print(json.dumps({'error': '日期格式应为 YYYY-MM-DD'}, ensure_ascii=False))
            return None

    expenses = load_data(filepath)
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    ts = int(time.time() * 1000)
    record = {
        'id': uuid.uuid4().hex[:16],
        'amount': round(float(amount), 2),
        'category': category,
        'description': description,
        'date': date,
        'timestamp': ts
    }
    expenses.append(record)
    save_data(filepath, expenses)
    print(json.dumps(record, ensure_ascii=False))
    return record


def find_records(filepath, id=None, description=None, category=None, date=None, amount=None, recent=None):
    """查找记录，返回JSON列表"""
    expenses = load_data(filepath)
    results = []

    if id:
        results = [e for e in expenses if e['id'] == id]
    else:
        for e in expenses:
            match = True
            if description and description not in e.get('description', ''):
                match = False
            if category and e.get('category') != category:
                match = False
            if date and e.get('date') != date:
                match = False
            if amount is not None and abs(e.get('amount', 0) - float(amount)) > 0.001:
                match = False
            if match:
                results.append(e)
        # 默认按时间倒序
        results = sorted(results, key=lambda x: x['timestamp'], reverse=True)
        if recent:
            results = results[:recent]

    print(json.dumps(results, ensure_ascii=False))
    return results


def edit_record(filepath, record_id, amount=None, category=None, description=None, date=None):
    """修改记录"""
    expenses = load_data(filepath)

    found = None
    for e in expenses:
        if e['id'] == record_id:
            found = e
            break

    if not found:
        print(json.dumps({'error': f'未找到ID为 {record_id} 的记录'}, ensure_ascii=False))
        return None

    old = dict(found)
    errors = []
    
    if amount is not None:
        if float(amount) <= 0:
            errors.append('金额必须为正数')
        else:
            found['amount'] = round(float(amount), 2)
    if category is not None:
        if category and category not in CATEGORIES:
            errors.append(f'分类无效，可选: {", ".join(CATEGORIES)}')
        elif category:
            found['category'] = category
    if description is not None:
        found['description'] = description
    if date is not None:
        try:
            datetime.strptime(date, '%Y-%m-%d')
            found['date'] = date
        except ValueError:
            errors.append('日期格式应为 YYYY-MM-DD')
    
    if errors:
        # 回滚：整体替换而非逐 key 恢复
        found.clear()
        found.update(old)
        print(json.dumps({'error': '; '.join(errors)}, ensure_ascii=False))
        return None

    if found == old:
        print(json.dumps({'error': '没有做任何修改'}, ensure_ascii=False))
        return None

    save_data(filepath, expenses)
    print(json.dumps({'old': old, 'new': found}, ensure_ascii=False))
    return found


def delete_record(filepath, record_id):
    """删除记录"""
    expenses = load_data(filepath)
    before = len(expenses)
    expenses = [e for e in expenses if e['id'] != record_id]
    after = len(expenses)

    if before == after:
        print(json.dumps({'error': f'未找到ID为 {record_id} 的记录'}, ensure_ascii=False))
        return False

    save_data(filepath, expenses)
    print(json.dumps({'deleted': record_id}, ensure_ascii=False))
    return True


def main():
    parser = argparse.ArgumentParser(description='支出记录数据操作（增删改查）')
    parser.add_argument('--file', default='data/expenses.json', help='数据文件路径')

    sub = parser.add_subparsers(dest='command', required=True)

    # 新增
    add_p = sub.add_parser('add', help='新增记录')
    add_p.add_argument('--amount', type=float, required=True, help='金额')
    add_p.add_argument('--category', required=True, help='分类')
    add_p.add_argument('--description', required=True, help='描述')
    add_p.add_argument('--date', help='日期 YYYY-MM-DD（默认今天）')

    # 查找
    find_p = sub.add_parser('find', help='查找记录')
    find_p.add_argument('--id', help='按ID精确匹配')
    find_p.add_argument('--description', help='按描述模糊匹配')
    find_p.add_argument('--category', help='按分类精确匹配')
    find_p.add_argument('--date', help='按日期精确匹配')
    find_p.add_argument('--amount', type=float, help='按金额精确匹配')
    find_p.add_argument('--recent', type=int, help='最近N条（可与其它条件组合）')

    # 修改
    edit_p = sub.add_parser('edit', help='修改记录')
    edit_p.add_argument('--id', required=True, help='记录ID')
    edit_p.add_argument('--amount', type=float, help='新金额')
    edit_p.add_argument('--category', help='新分类')
    edit_p.add_argument('--description', help='新描述')
    edit_p.add_argument('--date', help='新日期 YYYY-MM-DD')

    # 删除
    del_p = sub.add_parser('delete', help='删除记录')
    del_p.add_argument('--id', required=True, help='记录ID')

    args = parser.parse_args()

    if args.command == 'add':
        add_record(args.file, args.amount, args.category, args.description, args.date)
    elif args.command == 'find':
        find_records(args.file, id=args.id, description=args.description,
                     category=args.category, date=args.date, amount=args.amount, recent=args.recent)
    elif args.command == 'edit':
        edit_record(args.file, args.id, amount=args.amount, category=args.category,
                    description=args.description, date=args.date)
    elif args.command == 'delete':
        delete_record(args.file, args.id)


if __name__ == '__main__':
    main()
