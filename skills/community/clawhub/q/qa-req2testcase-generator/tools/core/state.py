#!/usr/bin/env python3
"""
core/state.py — 任务状态管理 + Gate Pass + Truncation Guard
"""

import os
import time
import subprocess

from .constants import STEPS, SKILL_VERSION
from .utils import _read_json, _write_json, _ensure_dir
from .security import _verify_gate_hmac


class TaskState:
    """任务状态管理器"""

    def __init__(self, data_dir=None, task_id=None):
        self.task_id = task_id
        self.data_dir = data_dir
        self.state_path = os.path.join(data_dir, "orchestrator_state.json") if data_dir else None
        self.state = self._load()

    def _load(self):
        if self.state_path and os.path.exists(self.state_path):
            try:
                return _read_json(self.state_path)
            except Exception:
                pass
        return {
            "task_id": self.task_id,
            "data_dir": self.data_dir,
            "skill_dir": "",
            "current_step": None,
            "completed_steps": [],
            "current_phase": 1,
            "requirement_file": "",
            "skill_version": SKILL_VERSION,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "updated_at": None,
        }

    def save(self):
        if self.state_path:
            self.state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
            _write_json(self.state_path, self.state)

    def mark_complete(self, step):
        if step not in self.state["completed_steps"]:
            self.state["completed_steps"].append(step)
        self.state["current_step"] = step
        self.save()

    def is_complete(self, step):
        return step in self.state["completed_steps"]

    def is_completed(self, step):
        """Alias for is_complete"""
        return self.is_complete(step)

    def get_next_step(self):
        for step in STEPS:
            if step not in self.state["completed_steps"]:
                return step
        return None


def check_gate(data_dir, step, task_id):
    """V3.2.6: 检查指定步骤的gate pass是否存在、task_id一致、且HMAC签名有效"""
    gp_path = os.path.join(data_dir, "gates", f"{step}.pass.json")
    if not os.path.exists(gp_path):
        return False, f"{step}.pass.json不存在"
    try:
        gp = _read_json(gp_path)
        if gp.get("task_id") != task_id:
            return False, f"task_id不匹配: {gp.get('task_id')} != {task_id}"
        hmac_ok, hmac_msg = _verify_gate_hmac(gp, task_id)
        if not hmac_ok:
            return False, f"{step}: {hmac_msg}"
        return True, "OK"
    except Exception:
        return False, f"{step}.pass.json读取失败"


def run_truncation_guard(skill_dir, data_dir, task_id, step, revision=1):
    """调用truncation_guard.py进行四级校验+auto-mv"""
    tmp_path = os.path.join(data_dir, f"{step.lower()}_output.tmp.json")
    guard_script = os.path.join(skill_dir, "tools", "truncation_guard.py")

    if not os.path.exists(guard_script):
        return False, "truncation_guard.py不存在"
    if not os.path.exists(tmp_path):
        return False, f"{tmp_path}不存在"

    cmd = [
        "python3", guard_script,
        "--file", tmp_path,
        "--step", step,
        "--data-dir", data_dir,
        "--task-id", task_id,
        "--revision", str(revision),
        "--auto-mv"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if result.returncode == 0:
        return True, result.stdout.strip()
    else:
        return False, f"exit={result.returncode}: {result.stderr.strip() or result.stdout.strip()}"
