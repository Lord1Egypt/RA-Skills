# -*- coding: utf-8 -*-
"""Phase 2 完整功能测试（当 trajectories_demo.json 不存在时）"""
import sys
import io
import os
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

from rollout_result import make_rollout_result, RolloutResult
from trajectory_loader import (
    load_from_session_state,
    save_rollout_result,
    save_rollout_results,
    load_rollout_from_json,
)
from session_state_parser import parse_session_state

# 动态获取工作区路径
try:
    from config import WORKSPACE
except ImportError:
    WORKSPACE = Path(os.environ.get(
        "OPENCLAW_WORKSPACE",
        os.path.join(os.path.expanduser("~"), ".jvs", "workspace")
    ))
session_path = WORKSPACE / "SESSION-STATE.md"

# 1. 测试 parse_session_state
print("=== 1. parse_session_state() ===")
parsed = parse_session_state(session_path)
print(f"timestamp : {parsed['timestamp']}")
print(f"task_type : {parsed['task_type']}")
print(f"tasks     : {len(parsed['active_tasks'])} 条")
print(f"corrections: {len(parsed['corrections'])} 条")
print(f"failures  : {len(parsed['failures_detected'])} 条")

# 2. 测试 detect_failures
print()
print("=== 2. detect_failures() ===")
rollouts = load_from_session_state(session_path)
print(f"检测到 {len(rollouts)} 条失败轨迹")
for r in rollouts:
    print(f"  {r.summary()}")

# 3. 模拟一个 trajectories_demo.json 并测试 load_rollout_from_json
print()
print("=== 3. 模拟 trajectories_demo.json ===")
demo_path = str(WORKSPACE / "temp" / "rollouts" / "trajectories_demo.json")
os.makedirs(os.path.dirname(demo_path), exist_ok=True)

demo_data = [
    {
        "id": "rollout_20260603_demo001",
        "skill_id": "robot-evolve",
        "task_type": "tool_use",
        "task_description": "执行 cargo check 编译检查",
        "user_message": "帮我检查沧渊项目的 Rust 编译",
        "predicted_answer": "cargo check 执行成功",
        "reference_answer": "cargo check -p cangyuan --message-format=short",
        "hard": 0.0,
        "soft": 0.4,
        "fail_reason": "cargo check 报错：cannot find crate for 'tokio'",
        "feedback": "你漏了依赖声明",
        "timestamp": "2026-06-03T00:30:00",
        "metadata": {"round": 3},
    },
    {
        "id": "rollout_20260603_demo002",
        "skill_id": "brain",
        "task_type": "decision",
        "task_description": "判断是否应该记录用户偏好",
        "user_message": "先生喜欢什么风格的表格？",
        "predicted_answer": "黑白灰主题色",
        "reference_answer": "黑白灰主题色（简约干净）",
        "hard": 1.0,
        "soft": 0.9,
        "fail_reason": None,
        "feedback": None,
        "timestamp": "2026-06-03T00:35:00",
        "metadata": {},
    },
]
with open(demo_path, 'w', encoding='utf-8') as f:
    import json
    json.dump(demo_data, f, ensure_ascii=False, indent=2)
print(f"创建模拟文件: {demo_path}")

# 4. 加载模拟文件
print()
print("=== 4. load_rollout_from_json() ===")
results = load_rollout_from_json(demo_path)
print(f"加载到 {len(results)} 条 RolloutResult:")
for r in results:
    print(f"  {r.summary()}")

# 5. 测试 save_rollout_result
print()
print("=== 5. save_rollout_result() ===")
saved_paths = save_rollout_results(results, output_dir=str(WORKSPACE / "temp" / "rollouts"))
for p in saved_paths:
    print(f"  已保存: {p}")

# 6. 验证文件内容
print()
print("=== 6. 验证保存的文件 ===")
for p in saved_paths:
    if os.path.exists(p):
        size = os.path.getsize(p)
        print(f"  {os.path.basename(p)}: {size} bytes")
