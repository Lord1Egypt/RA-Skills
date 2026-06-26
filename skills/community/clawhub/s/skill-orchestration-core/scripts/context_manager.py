#!/usr/bin/env python3
"""
上下文管理器 — 管理 skill 之间的上下文传递和共享

用法:
  python context_manager.py show [project_path]
  python context_manager.py save [project_path]
  python context_manager.py load [project_path]
  python context_manager.py clear [project_path]
  python context_manager.py get <key> [project_path]
  python context_manager.py set <key> <value> [project_path]
  python context_manager.py complete <skill_name> [project_path]
  python context_manager.py status [project_path]
"""

import json
import os
import sys
import gzip
import base64
import fcntl
from datetime import datetime
from pathlib import Path


class ContextManager:
    """管理 skill 编排的上下文数据"""

    def __init__(self, project_path):
        self.project_path = Path(project_path).resolve()
        self.orchestration_dir = self.project_path / ".orchestration"
        self.context_file = self.orchestration_dir / "context.json"
        self._lock_file = self.orchestration_dir / ".context.lock"

        self.context = {
            "project": {
                "name": self.project_path.name,
                "path": str(self.project_path),
                "description": "",
            },
            "state": {
                "currentSkill": None,
                "progress": 0,
                "completedSkills": [],
                "startTime": datetime.now().isoformat(),
            },
            "data": {},
            "config": {
                "contextCompression": True,
                "maxContextSize": 100000,
            },
        }

        self._ensure_dirs()

    def set(self, key, value):
        self.context["data"][key] = value
        self._check_size()

    def get(self, key, default=None):
        return self.context["data"].get(key, default)

    def delete(self, key):
        self.context["data"].pop(key, None)

    def has(self, key):
        return key in self.context["data"]

    def mark_skill_completed(self, skill):
        completed = self.context["state"]["completedSkills"]
        if skill not in completed:
            completed.append(skill)

    def is_skill_completed(self, skill):
        return skill in self.context["state"]["completedSkills"]

    def pass_to(self, skill):
        self.context["state"]["currentSkill"] = skill
        self.context["state"]["progress"] = self._calculate_progress()
        self.save()

    def compress(self):
        raw = json.dumps(self.context, ensure_ascii=False).encode("utf-8")
        compressed = gzip.compress(raw)
        return {
            "version": "1.0",
            "compressed": True,
            "data": base64.b64encode(compressed).decode("ascii"),
            "timestamp": datetime.now().isoformat(),
        }

    def restore(self, compressed):
        if compressed.get("compressed"):
            raw = base64.b64decode(compressed["data"])
            text = gzip.decompress(raw).decode("utf-8")
            self.context = json.loads(text)
        else:
            self.context = compressed

    def save(self):
        self._ensure_dirs()
        with open(self._lock_file, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                with open(self.context_file, "w", encoding="utf-8") as f:
                    json.dump(self.context, f, ensure_ascii=False, indent=2)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    def load(self):
        if not self.context_file.exists():
            return False
        with open(self._lock_file, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_SH)
            try:
                with open(self.context_file, "r", encoding="utf-8") as f:
                    self.context = json.load(f)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)
        return True

    def clear(self):
        self.context["data"] = {}
        self.context["state"] = {
            "currentSkill": None,
            "progress": 0,
            "completedSkills": [],
            "startTime": datetime.now().isoformat(),
        }
        self.save()

    def get_size(self):
        return len(json.dumps(self.context, ensure_ascii=False))

    def get_project_info(self):
        return self.context["project"]

    def get_state(self):
        return self.context["state"]

    def get_all_data(self):
        return dict(self.context["data"])

    def set_project_info(self, info):
        self.context["project"].update(info)

    def get_progress(self):
        return self.context["state"]["progress"]

    def set_progress(self, progress):
        self.context["state"]["progress"] = progress

    def _ensure_dirs(self):
        self.orchestration_dir.mkdir(parents=True, exist_ok=True)

    def _check_size(self):
        size = self.get_size()
        max_size = self.context["config"].get("maxContextSize", 100000)
        if size > max_size:
            print(
                "警告: 上下文大小 ({}) 超过限制 ({})，"
                "建议压缩或清理不必要的数据".format(size, max_size)
            )

    def _calculate_progress(self):
        completed = len(self.context["state"]["completedSkills"])
        total = completed + 1
        return round((completed / total) * 100, 1)


def main():
    args = sys.argv[1:]
    if not args:
        _print_usage()
        return

    command = args[0]

    if command in ("set", "get"):
        key = args[1] if len(args) > 1 else None
        value = " ".join(args[2:]) if len(args) > 2 else None
        project_path = os.getcwd()
    else:
        project_path = args[1] if len(args) > 1 else os.getcwd()
        key = None
        value = None

    ctx = ContextManager(project_path)

    if command == "show":
        ctx.load()
        print(json.dumps(ctx.context, ensure_ascii=False, indent=2))

    elif command == "save":
        ctx.save()
        print("Context saved")

    elif command == "load":
        if ctx.load():
            print("Context loaded")
        else:
            print("No context found")

    elif command == "clear":
        ctx.clear()
        print("Context cleared")

    elif command == "get":
        if not key:
            print("错误: 请提供 key", file=sys.stderr)
            sys.exit(1)
        ctx.load()
        val = ctx.get(key)
        if val is not None:
            print(json.dumps(val, ensure_ascii=False, indent=2))
        else:
            print("Key '{}' not found".format(key))

    elif command == "set":
        if not key or value is None:
            print("错误: 请提供 key 和 value", file=sys.stderr)
            sys.exit(1)
        ctx.load()
        try:
            parsed_value = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            parsed_value = value
        ctx.set(key, parsed_value)
        ctx.save()
        print("Set {}".format(key))

    elif command == "complete":
        skill_name = args[1] if len(args) > 1 else None
        if not skill_name:
            print("错误: 请提供 skill 名称", file=sys.stderr)
            sys.exit(1)
        ctx.load()
        ctx.mark_skill_completed(skill_name)
        ctx.save()
        print("Marked {} as completed".format(skill_name))

    elif command == "status":
        ctx.load()
        state = ctx.get_state()
        project = ctx.get_project_info()
        print("项目: {}".format(project.get("name", "N/A")))
        print("路径: {}".format(project.get("path", "N/A")))
        print("当前Skill: {}".format(state.get("currentSkill", "N/A")))
        print("进度: {}%".format(state.get("progress", 0)))
        completed = state.get("completedSkills", [])
        print("已完成: {}".format(", ".join(completed) if completed else "无"))
        data_keys = list(ctx.context["data"].keys())
        print("数据键: {}".format(", ".join(data_keys) if data_keys else "无"))
        print("上下文大小: {} bytes".format(ctx.get_size()))

    else:
        _print_usage()


def _print_usage():
    print("用法:")
    print("  python context_manager.py show [project_path]")
    print("  python context_manager.py save [project_path]")
    print("  python context_manager.py load [project_path]")
    print("  python context_manager.py clear [project_path]")
    print("  python context_manager.py get <key> [project_path]")
    print("  python context_manager.py set <key> <value> [project_path]")
    print("  python context_manager.py complete <skill_name> [project_path]")
    print("  python context_manager.py status [project_path]")


if __name__ == "__main__":
    main()
