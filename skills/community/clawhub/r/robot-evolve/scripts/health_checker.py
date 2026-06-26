"""
health_checker.py — robot-evolve 健康检查（直接导入调用）
"""

import os
import sys
from pathlib import Path

# 确保 skills/robot-evolve/scripts 在 path 中
SCRIPT_DIR = Path(__file__).parent
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", SCRIPT_DIR.parent.parent))
sys.path.insert(0, str(SCRIPT_DIR))

def main():
    try:
        from auto_evolve import main as evolve_main
        print("=== Robot-Evolve 健康检查 ===")
        evolve_main()
    except ImportError:
        print("[ERROR] 无法导入 auto_evolve，请检查技能是否正确安装")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 健康检查失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
