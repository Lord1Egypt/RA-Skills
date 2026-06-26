#!/usr/bin/env python3
"""
流程编排器 — 基于 DESIGN.md 的流程编排，集成 Hermes delegate_task 真正执行 skill

用法:
  python workflow_orchestrator.py parse <DESIGN.md>
  python workflow_orchestrator.py execute <DESIGN.md>
  python workflow_orchestrator.py status <DESIGN.md>
  python workflow_orchestrator.py checkpoint <DESIGN.md> <name>
  python workflow_orchestrator.py restore <DESIGN.md> <name>
  python workflow_orchestrator.py jump <DESIGN.md> <stage_name>
"""

import json
import os
import re
import sys
import fcntl
import shutil
from datetime import datetime
from pathlib import Path

# 尝试导入 PyYAML，没有则用简单解析器
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class WorkflowOrchestrator:
    """基于 DESIGN.md 的流程编排器"""

    # 阶段标题正则：支持中文"阶段 N:"和英文"Stage N:"
    # 只匹配标题行，name取同行内容；body取标题后到下一个同级或更高级标题
    STAGE_HEADING_REGEX = re.compile(
        r'###\s+(?:阶段|Stage)\s+(\d+)\s*[:：]\s*([^\n]+)\n(.*?)(?=\n###|\n##|\Z)',
        re.DOTALL
    )

    # 列表行正则（只匹配 - 开头的Markdown列表，避免与加粗**混淆）
    LIST_LINE_REGEX = re.compile(r'^[ \t]*-[ \t]+(.+?)\s*$', re.MULTILINE)

    def __init__(self, design_path):
        self.design_path = Path(design_path).resolve()
        self.project_path = self.design_path.parent
        self.orchestration_dir = self.project_path / ".orchestration"
        self.state_file = self.orchestration_dir / "state.json"
        self._lock_file = self.orchestration_dir / ".state.lock"
        self.checkpoints_dir = self.orchestration_dir / "checkpoints"

        self.design_content = ""
        self.parsed = {
            "metadata": {},
            "workflow": [],
            "context": {},
            "validation": {},
            "state": {},
        }
        self.state = {
            "currentStage": None,
            "status": "idle",  # idle / running / paused / completed
            "stageResults": {},
            "startTime": None,
            "endTime": None,
        }
        self._ensure_dirs()

    def parse_design(self):
        """解析 DESIGN.md 文件"""
        if not self.design_path.exists():
            raise FileNotFoundError(f"DESIGN.md 不存在: {self.design_path}")

        self.design_content = self.design_path.read_text(encoding="utf-8")
        self._parse_metadata()
        self._parse_workflow()
        self._parse_context()
        self._parse_validation()
        self._parse_state()
        return self.parsed

    def execute(self):
        """执行工作流，输出 [ORCHESTRATE] 指令供 Hermes agent 通过 delegate_task 调度"""
        if not self.parsed["workflow"]:
            self.parse_design()

        self.state["status"] = "running"
        self.state["startTime"] = datetime.now().isoformat()
        self._save_state()

        orchestration_output = []

        for stage in self.parsed["workflow"]:
            stage_num = stage["number"]
            stage_name = stage["name"]

            self.state["currentStage"] = stage_num
            self._save_state()

            print(f"\n[ORCHESTRATE] 阶段 {stage_num}: {stage_name}")

            for skill_name in stage["skills"]:
                print(f"[ORCHESTRATE] → 执行 skill: {skill_name}")
                print(
                    f'[ORCHESTRATE] delegate_task goal: '
                    f'"使用 {skill_name} skill 完成阶段 {stage_num}({stage_name})的任务"'
                )

                # 构造 context 字符串
                context_parts = [
                    f"项目路径={self.project_path}",
                    f"任务列表={stage.get('tasks', [])}",
                    f"期望输出={stage.get('outputs', [])}",
                ]

                # 添加上下文传递信息
                ctx_info = self.parsed["context"].get(skill_name, {})
                if ctx_info:
                    if "input" in ctx_info:
                        print(f"[CONTEXT] {skill_name} 输入: {ctx_info['input']}")
                        context_parts.append(f"输入文件={ctx_info['input']}")
                    if "output" in ctx_info:
                        print(f"[CONTEXT] {skill_name} 输出: {ctx_info['output']}")
                        context_parts.append(f"输出文件={ctx_info['output']}")
                    if "pass_to" in ctx_info:
                        print(f"[CONTEXT] {skill_name} → {ctx_info['pass_to']}")

                print(
                    f'[ORCHESTRATE] delegate_task context: '
                    f'"{", ".join(context_parts)}"'
                )

                # 输出验证规则
                val_rules = self.parsed["validation"].get(skill_name, {})
                if val_rules:
                    print(f"[VALIDATE] {skill_name} 验证规则: {json.dumps(val_rules, ensure_ascii=False)}")

                orchestration_output.append({
                    "stage": stage_num,
                    "stage_name": stage_name,
                    "skill": skill_name,
                    "goal": f"使用 {skill_name} skill 完成阶段 {stage_num}({stage_name})的任务",
                    "context": ", ".join(context_parts),
                    "validation": val_rules,
                })

            self.state["stageResults"][str(stage_num)] = {
                "name": stage_name,
                "status": "orchestrated",
                "skills": stage["skills"],
                "timestamp": datetime.now().isoformat(),
            }
            self._save_state()

        self.state["status"] = "completed"
        self.state["endTime"] = datetime.now().isoformat()
        self.state["currentStage"] = None
        self._save_state()

        print(f"\n[ORCHESTRATE] 工作流编排完成，共 {len(self.parsed['workflow'])} 个阶段")
        return orchestration_output

    def pause(self):
        """暂停工作流"""
        self.state["status"] = "paused"
        self._save_state()
        print("[ORCHESTRATE] 工作流已暂停")

    def resume(self):
        """恢复工作流"""
        self.state["status"] = "running"
        self._save_state()
        print("[ORCHESTRATE] 工作流已恢复")

    def jump_to(self, stage_name):
        """跳转到指定阶段"""
        for stage in self.parsed["workflow"]:
            if stage_name in stage["name"] or str(stage["number"]) == stage_name:
                self.state["currentStage"] = stage["number"]
                self._save_state()
                print(f"[ORCHESTRATE] 跳转到阶段 {stage['number']}: {stage['name']}")
                return
        print(f"[ORCHESTRATE] 未找到阶段: {stage_name}")

    def set_checkpoint(self, name):
        """保存检查点"""
        self._ensure_dirs()
        checkpoint_data = {
            "state": dict(self.state),
            "parsed": dict(self.parsed),
            "timestamp": datetime.now().isoformat(),
        }
        cp_file = self.checkpoints_dir / f"checkpoint-{name}.json"
        with open(cp_file, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        print(f"[CHECKPOINT] 已保存: {name}")

    def restore_checkpoint(self, name):
        """恢复检查点"""
        cp_file = self.checkpoints_dir / f"checkpoint-{name}.json"
        if not cp_file.exists():
            print(f"[CHECKPOINT] 未找到: {name}")
            return False
        with open(cp_file, "r", encoding="utf-8") as f:
            checkpoint_data = json.load(f)
        self.state = checkpoint_data["state"]
        self.parsed = checkpoint_data["parsed"]
        self._save_state()
        print(f"[CHECKPOINT] 已恢复: {name}")
        return True

    def get_status(self):
        """获取当前状态"""
        self._load_state()
        return {
            "design": str(self.design_path),
            "status": self.state.get("status", "idle"),
            "currentStage": self.state.get("currentStage"),
            "stagesCompleted": len(self.state.get("stageResults", {})),
            "totalStages": len(self.parsed.get("workflow", [])),
            "startTime": self.state.get("startTime"),
            "endTime": self.state.get("endTime"),
        }

    # ============================================================
    # 内部解析方法
    # ============================================================

    def _parse_metadata(self):
        """解析 DESIGN.md 头部的 YAML frontmatter"""
        fm_match = re.match(r'^---\s*\n(.*?)\n---', self.design_content, re.DOTALL)
        if fm_match:
            fm_text = fm_match.group(1)
            if HAS_YAML:
                try:
                    self.parsed["metadata"] = yaml.safe_load(fm_text) or {}
                    return
                except yaml.YAMLError:
                    pass
            # 简单解析
            for line in fm_text.strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    self.parsed["metadata"][k.strip()] = v.strip()

    def _parse_workflow(self):
        """解析工作流阶段"""
        for match in self.STAGE_HEADING_REGEX.finditer(self.design_content):
            num = int(match.group(1))
            name = match.group(2).strip()
            body = match.group(3)

            skills = self._extract_list(body, r'\*{0,2}(?:使用的\s*)?[Ss]kills?\*{0,2}[:：]\s*\n((?:[ \t]*-[ \t]+[^\n]+\n)+)')
            tasks = self._extract_list(body, r'\*{0,2}(?:任务|[Tt]asks?)\*{0,2}[:：]\s*\n((?:[ \t]*-[ \t]+[^\n]+\n)+)')
            outputs = self._extract_list(body, r'\*{0,2}(?:输出|[Oo]utputs?)\*{0,2}[:：]\s*\n((?:[ \t]*-[ \t]+[^\n]+\n)+)')

            self.parsed["workflow"].append({
                "number": num,
                "name": name,
                "skills": skills,
                "tasks": tasks,
                "outputs": outputs,
            })

    def _parse_context(self):
        """解析上下文传递配置"""
        ctx_text = self._extract_section("上下文传递|[Cc]ontext")
        if not ctx_text:
            return
        # 去掉可能的 ```yaml 代码块包裹
        ctx_text = re.sub(r'```ya?ml\s*\n?', '', ctx_text)
        ctx_text = re.sub(r'\n?```', '', ctx_text)

        if HAS_YAML:
            try:
                data = yaml.safe_load(ctx_text)
                if isinstance(data, dict) and "context" in data:
                    self.parsed["context"] = data["context"]
                elif isinstance(data, dict):
                    self.parsed["context"] = data
                return
            except yaml.YAMLError:
                pass

        # 简单解析
        self.parsed["context"] = self._simple_yaml_parse(ctx_text)

    def _parse_validation(self):
        """解析质量验证配置"""
        val_text = self._extract_section("质量验证|[Vv]alidation")
        if not val_text:
            return
        val_text = re.sub(r'```ya?ml\s*\n?', '', val_text)
        val_text = re.sub(r'\n?```', '', val_text)

        if HAS_YAML:
            try:
                data = yaml.safe_load(val_text)
                if isinstance(data, dict) and "validation" in data:
                    self.parsed["validation"] = data["validation"]
                elif isinstance(data, dict):
                    self.parsed["validation"] = data
                return
            except yaml.YAMLError:
                pass

        self.parsed["validation"] = self._simple_yaml_parse(val_text)

    def _parse_state(self):
        """解析状态管理配置"""
        state_text = self._extract_section("状态管理|[Ss]tate")
        if not state_text:
            return
        state_text = re.sub(r'```ya?ml\s*\n?', '', state_text)
        state_text = re.sub(r'\n?```', '', state_text)

        if HAS_YAML:
            try:
                data = yaml.safe_load(state_text)
                if isinstance(data, dict) and "state" in data:
                    self.parsed["state"] = data["state"]
                elif isinstance(data, dict):
                    self.parsed["state"] = data
                return
            except yaml.YAMLError:
                pass

        self.parsed["state"] = self._simple_yaml_parse(state_text)

    def _extract_section(self, heading_pattern):
        """从 DESIGN.md 提取指定章节内容"""
        # 匹配 ## 上下文传递 或 ## Context 等
        regex = re.compile(
            rf'##\s+(?:{heading_pattern})\s*\n(.*?)(?=\n##|\Z)',
            re.DOTALL
        )
        match = regex.search(self.design_content)
        return match.group(1).strip() if match else ""

    def _extract_list(self, text, pattern):
        """从阶段文本中提取列表项"""
        match = re.search(pattern, text)
        if not match:
            return []
        items = self.LIST_LINE_REGEX.findall(match.group(1))
        return [item.strip() for item in items]

    def _simple_yaml_parse(self, text):
        """简单 YAML 解析器（无 PyYAML 时的降级方案）"""
        result = {}
        current_key = None
        for line in text.strip().split("\n"):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            # 顶层 key: value
            if not line.startswith(" ") and not line.startswith("\t"):
                if ":" in stripped:
                    k, v = stripped.split(":", 1)
                    current_key = k.strip()
                    v = v.strip()
                    if v and v not in ("", "null", "~"):
                        try:
                            result[current_key] = json.loads(v)
                        except (json.JSONDecodeError, ValueError):
                            result[current_key] = v
                    else:
                        result[current_key] = {}
        return result

    def _ensure_dirs(self):
        self.orchestration_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

    def _save_state(self):
        self._ensure_dirs()
        with open(self._lock_file, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                with open(self.state_file, "w", encoding="utf-8") as f:
                    json.dump(self.state, f, ensure_ascii=False, indent=2)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    def _load_state(self):
        if not self.state_file.exists():
            return False
        with open(self._lock_file, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_SH)
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    self.state = json.load(f)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)
        return True


def main():
    args = sys.argv[1:]
    if not args:
        _print_usage()
        return

    command = args[0]

    if command == "parse":
        design_path = args[1] if len(args) > 1 else None
        if not design_path:
            print("错误: 请提供 DESIGN.md 路径", file=sys.stderr)
            sys.exit(1)
        orch = WorkflowOrchestrator(design_path)
        parsed = orch.parse_design()
        print(json.dumps(parsed, ensure_ascii=False, indent=2))

    elif command == "execute":
        design_path = args[1] if len(args) > 1 else None
        if not design_path:
            print("错误: 请提供 DESIGN.md 路径", file=sys.stderr)
            sys.exit(1)
        orch = WorkflowOrchestrator(design_path)
        orch.parse_design()
        result = orch.execute()
        print(f"\n--- 编排输出 ---")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "status":
        design_path = args[1] if len(args) > 1 else None
        if not design_path:
            print("错误: 请提供 DESIGN.md 路径", file=sys.stderr)
            sys.exit(1)
        orch = WorkflowOrchestrator(design_path)
        if orch._load_state():
            orch.parse_design()
        status = orch.get_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))

    elif command == "checkpoint":
        if len(args) < 3:
            print("错误: 用法: checkpoint <DESIGN.md> <name>", file=sys.stderr)
            sys.exit(1)
        orch = WorkflowOrchestrator(args[1])
        orch.parse_design()
        orch._load_state()
        orch.set_checkpoint(args[2])

    elif command == "restore":
        if len(args) < 3:
            print("错误: 用法: restore <DESIGN.md> <name>", file=sys.stderr)
            sys.exit(1)
        orch = WorkflowOrchestrator(args[1])
        orch.parse_design()
        orch.restore_checkpoint(args[2])

    elif command == "jump":
        if len(args) < 3:
            print("错误: 用法: jump <DESIGN.md> <stage_name>", file=sys.stderr)
            sys.exit(1)
        orch = WorkflowOrchestrator(args[1])
        orch.parse_design()
        orch.jump_to(args[2])

    else:
        _print_usage()


def _print_usage():
    print("用法:")
    print("  python workflow_orchestrator.py parse <DESIGN.md>")
    print("  python workflow_orchestrator.py execute <DESIGN.md>")
    print("  python workflow_orchestrator.py status <DESIGN.md>")
    print("  python workflow_orchestrator.py checkpoint <DESIGN.md> <name>")
    print("  python workflow_orchestrator.py restore <DESIGN.md> <name>")
    print("  python workflow_orchestrator.py jump <DESIGN.md> <stage_name>")


if __name__ == "__main__":
    main()
