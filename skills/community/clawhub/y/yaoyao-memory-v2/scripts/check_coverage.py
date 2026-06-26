#!/usr/bin/env python3
"""检查向量覆盖率"""
import subprocess
import json
from pathlib import Path


from paths import VEC_EXT, VECTORS_DB

def check_coverage():
    # 检查数据库文件是否存在
    if not Path(VECTORS_DB).exists():
        print(f"⚠️  向量数据库不存在: {VECTORS_DB}")
        print("   请先运行 memory.py sync-start 初始化")
        return None
    
    result = subprocess.run(
        f'sqlite3 -cmd ".load {VEC_EXT}" "{VECTORS_DB}" '
        f'"SELECT COUNT(*) FROM l1_records; SELECT COUNT(*) FROM l1_vec; '
        f'SELECT COUNT(*) FROM l0_conversations; SELECT COUNT(*) FROM l0_vec;"',
        shell=True, capture_output=True, text=True,
        timeout=30  # 超时保护
    )
    
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 4:
            l1_records = int(lines[0])
            l1_vec = int(lines[1])
            l0_conversations = int(lines[2])
            l0_vec = int(lines[3])
            
            l1_coverage = 100.0 * l1_vec / max(l1_records, 1)
            l0_coverage = 100.0 * l0_vec / max(l0_conversations, 1)
            
            return {
                "l1_records": l1_records,
                "l1_vec": l1_vec,
                "l1_coverage": round(l1_coverage, 1),
                "l0_conversations": l0_conversations,
                "l0_vec": l0_vec,
                "l0_coverage": round(l0_coverage, 1)
            }
    
    return None

if __name__ == "__main__":
    import datetime
    print(f"向量覆盖率检查 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    result = check_coverage()
    if result:
        print(f"L1 覆盖率: {result['l1_coverage']}%")
        print(f"L0 覆盖率: {result['l0_coverage']}%")
    else:
        print("检查失败")
