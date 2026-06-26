import sys, os
from pathlib import Path

# 动态添加脚本路径
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

# 读取配置
try:
    from config import WORKSPACE, DEFAULT_TARGET_SKILL_DIR
    ROBOT_EVOLVE_DIR = DEFAULT_TARGET_SKILL_DIR
except ImportError:
    WORKSPACE = Path(os.environ.get(
        "OPENCLAW_WORKSPACE",
        os.path.join(os.path.expanduser("~"), ".jvs", "workspace")
    ))
    ROBOT_EVOLVE_DIR = WORKSPACE / "skills" / "robot-evolve"

from state_manager import init_state
try:
    init_state('robot-evolve', '3.0.4')
    print('State initialized')
except Exception as e:
    print(f'State check: {e}')

from skill_scheduler import run_from_skill_dir, format_cycle_report
result = run_from_skill_dir(ROBOT_EVOLVE_DIR, max_edits=6)
print(format_cycle_report(result))
