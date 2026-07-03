#!/usr/bin/env python3
"""
CSV 账本行校验器

校验单行数据是否符合「日期,类型,金额,分类,描述,账户」格式。
用于写入前拦截垃圾数据、读取时过滤无效行。

用法:
    python validate_line.py "2026-06-17,支出,22.00,餐饮,牛肉面,建设银行(5422)"
    echo $?   # 0=合法, 1=非法
"""

import csv
import re
import sys

VALID_TYPES = {"收入", "支出"}

def validate_line(line: str) -> tuple:
    """校验一行是否为合法交易记录。
    
    Returns:
        (is_valid: bool, reason: str)
    """
    line = line.strip()
    
    # 空行
    if not line:
        return False, "空行"
    
    # 注释行
    if line.startswith('#'):
        return False, "注释行"
    
    # 余额行
    if line.startswith('余额,'):
        return False, "余额定义行"
    
    # 解析 CSV 字段
    parts = next(csv.reader([line]), None)
    if not parts or len(parts) < 6:
        return False, f"字段不足（需6列，实际{len(parts) if parts else 0}列）"
    
    date_str, txn_type, amount_str, category, description, account = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
    
    # 校验日期格式 YYYY-MM-DD
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return False, f"日期格式非法：{date_str}"
    
    # 尝试解析日期是否真实存在
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False, f"日期不存在：{date_str}"
    
    # 校验类型
    if txn_type not in VALID_TYPES:
        return False, f"类型非法：{txn_type}（须为 收入/支出）"
    
    # 校验金额
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, f"金额必须为正数：{amount}"
    except ValueError:
        return False, f"金额非法：{amount_str}"
    
    # 分类和描述不能为空
    if not category.strip():
        return False, "分类为空"
    if not description.strip():
        return False, "描述为空"
    if not account.strip():
        return False, "账户为空"
    
    return True, "OK"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python validate_line.py \"CSV行\"")
        sys.exit(1)
    
    is_valid, reason = validate_line(sys.argv[1])
    if is_valid:
        print(f"✅ {reason}")
        sys.exit(0)
    else:
        print(f"❌ {reason}")
        sys.exit(1)
