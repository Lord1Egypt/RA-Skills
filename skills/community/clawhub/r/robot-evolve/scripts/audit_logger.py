#!/usr/bin/env python3
# audit_logger.py
# 适配 ocean-evolve safety-matrix.json 的审计脚本
# L1 执行后告知（本身不危险，主要用于记录）

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# === 配置路径 ===
SKILL_DIR = Path(__file__).parent.parent
MATRIX_PATH = SKILL_DIR / "safety-matrix.json"
MEMORY_DIR = Path.home() / ".openclaw" / "memory" / "evolution"

# === 加载安全矩阵 ===
def load_matrix():
    if not MATRIX_PATH.exists():
        raise FileNotFoundError(f"safety-matrix.json not found at {MATRIX_PATH}")
    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# === 查询操作等级（O(1) 查询） ===
def query_level(operation_name):
    """返回 (level, action, note)"""
    matrix = load_matrix()
    
    # 1. 先查 absoluteBans（最快匹配）
    for ban in matrix.get("absoluteBans", []):
        # forbiddenActions 是字符串数组，检查操作是否命中
        if operation_name in ban.get("forbiddenActions", []):
            return "L3", "TEMP_AUTH_REQUIRED", ban.get("note", "绝对红线")
        # 检查 forbiddenFields
        for field in ban.get("forbiddenFields", []):
            if field in operation_name:
                return "L3", "TEMP_AUTH_REQUIRED", ban.get("note", "绝对红线")
    
    # 2. 在 categories 中精确匹配
    for cat in matrix.get("categories", []):
        for rule in cat.get("rules", []):
            if rule["operation"] == operation_name:
                level = rule["level"]
                note = rule.get("note", "")
                if level == "L3":
                    return level, "TEMP_AUTH_REQUIRED", note
                elif level == "L2":
                    return level, "ASK", note
                elif level == "L1":
                    return level, "EXEC_NOTIFY", note
                else:  # L0
                    return level, "EXEC", note
    
    # 3. 未知操作走默认（L2 + 询问）
    return matrix.get("defaultLevel", "L2"), "ASK", "未在矩阵中定义的操作"

# === 审计日志写入（按月归档） ===
def write_log(level, op_type, target, changes, reason, result, user_reply=None):
    now = datetime.now()
    year_month = now.strftime("%Y-%m")
    log_file = MEMORY_DIR / f"{year_month}.md"
    
    # 确保目录存在
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    
    # 构建日志条目
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""
## [{timestamp}] 操作记录
- **等级**: {level}
- **操作类型**: {op_type}
- **目标**: {target}
- **修改内容**: {changes}
- **原因**: {reason}
- **用户回复**: {user_reply if user_reply else 'N/A'}
- **执行结果**: {result}
"""
    # 追加写入
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry.strip() + "\n")
    
    print(f"[AUDIT] L{level} 操作已记录 -> {log_file.name}")

# === 主逻辑 ===
def main():
    if len(sys.argv) < 2:
        print("用法: python audit_logger.py <操作名称> [详情]")
        print("示例: python audit_logger.py 'pip install' 'install pyautogui 1.4.11'")
        print()
        print("操作等级说明:")
        print("  L0 - 无需告知，可直接执行")
        print("  L1 - 执行后告知")
        print("  L2 - 必须请示用户")
        print("  L3 - 禁止/需临时授权")
        sys.exit(0)
    
    operation = sys.argv[1]
    detail = sys.argv[2] if len(sys.argv) > 2 else ""
    
    level, action, note = query_level(operation)
    
    # 输出结果供 shell 脚本解析
    # 格式: level|action|note
    print(f"{level}|{action}|{note}")
    
    # 如果需要执行后告知（L0/L1），自动记录（用户确认后）
    if action in ("EXEC", "EXEC_NOTIFY") and "--dry-run" not in sys.argv:
        # 这里只是打印提示，实际记录由调用方在确认成功后调用
        pass

def notify_and_log(operation_name, op_type, target, changes, reason, user_reply=None):
    """执行后告知 + 写入日志（call this after successful execution）"""
    level, _, note = query_level(operation_name)
    write_log(
        level=level,
        op_type=op_type,
        target=target,
        changes=changes,
        reason=reason,
        result="成功",
        user_reply=user_reply
    )

# === 命令行入口 ===
if __name__ == "__main__":
    main()