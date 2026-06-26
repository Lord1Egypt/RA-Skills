#!/usr/bin/env python3
"""
Skill Composer - 编排多个 OpenClaw 技能成自动化工作流
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class WorkflowStep:
    """工作流步骤"""
    def __init__(self, step_data: Dict, step_index: int):
        self.name = step_data.get('name', f'Step {step_index+1}')
        self.skill = step_data['skill']
        self.args = step_data.get('args', [])
        self.output = step_data.get('output')  # 输出引用名
        self.condition = step_data.get('if')   # 条件表达式
        self.status = 'pending'
        self.output_path = None  # 实际输出路径

    def __str__(self):
        return f"{self.name}: {self.skill} {' '.join(self.args)}"

class Workflow:
    """工作流"""
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.name = 'Untitled Workflow'
        self.steps: List[WorkflowStep] = []
        self.continue_on_error = False
        self.variables = {}  # 变量存储：{output_name: path}
        self.base_dir = self.filepath.parent

    def load(self):
        """加载并解析 YAML"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        self.name = data.get('name', self.name)
        self.continue_on_error = data.get('continue-on-error', False)

        steps_data = data.get('steps', [])
        for idx, step_data in enumerate(steps_data):
            step = WorkflowStep(step_data, idx)
            self.steps.append(step)

    def interpolate(self, args: List[str]) -> List[str]:
        """替换参数中的变量 {{var}}"""
        result = []
        for arg in args:
            # 简单的变量插值
            for var_name, var_value in self.variables.items():
                placeholder = f"{{{{{var_name}}}}}"  # {{var}}
                if isinstance(arg, str) and placeholder in arg:
                    arg = arg.replace(placeholder, var_value)
            result.append(arg)
        return result

    def evaluate_condition(self, condition: str, step: WorkflowStep) -> bool:
        """评估条件表达式（简化版）"""
        if not condition:
            return True
        # 简单的状态检查：{{step_name.status}} == 'success'
        for var_name, var_value in self.variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            if placeholder in condition:
                condition = condition.replace(placeholder, str(var_value))
        # 安全评估
        try:
            return eval(condition, {"__builtins__": {}})
        except:
            return True  # 默认执行

    def exec_skill(self, skill: str, args: List[str]) -> tuple:
        """执行一个技能"""
        cmd = ['claw', 'skill', 'exec', skill] + args
        print(f"  ▶️  Executing: {skill}")
        print(f"     Args: {args}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                return 'success', result.stdout
            else:
                return 'failed', result.stderr
        except subprocess.TimeoutExpired:
            return 'timeout', 'Execution timed out'
        except Exception as e:
            return 'error', str(e)

    def run(self):
        """运行工作流"""
        print(f"🚀 Running workflow: {self.name}")
        print(f"📁 File: {self.filepath}")
        print(f"📊 Total steps: {len(self.steps)}")
        print()

        for idx, step in enumerate(self.steps, 1):
            print(f"🔹 Step {idx}/{len(self.steps)}: {step.name}")

            # 检查条件
            if not self.evaluate_condition(step.condition, step):
                print(f"  ⏭️  Skipped (condition not met)")
                step.status = 'skipped'
                continue

            # 插值参数
            args = self.interpolate(step.args)

            # 执行
            status, output = self.exec_skill(step.skill, args)
            step.status = status

            if status == 'success':
                print(f"  ✅ Success")
                # 记录输出路径（如果定义了output）
                if step.output:
                    # 假设输出是最后一个参数指定的路径（简化）
                    # 实际应该解析技能的返回信息
                    self.variables[step.output] = args[-1] if args else '.'
            else:
                print(f"  ❌ Failed: {output}")
                if not self.continue_on_error:
                    print(f"\n⛔ Workflow stopped at step {idx}")
                    break

            print()

        # 总结
        self.summary()

    def preview(self):
        """预览工作流"""
        print(f"👀 Previewing workflow: {self.name}")
        print(f"📁 File: {self.filepath}")
        print(f"📊 Total steps: {len(self.steps)}")
        print()
        for idx, step in enumerate(self.steps, 1):
            args = self.interpolate(step.args)
            print(f"{idx}. {step.name}")
            print(f"   Skill: {step.skill}")
            print(f"   Args: {args}")
            if step.output:
                print(f"   Output var: {step.output}")
            print()

    def validate(self) -> bool:
        """验证工作流语法"""
        print(f"🔍 Validating workflow: {self.filepath}")
        errors = []

        # 检查必需字段
        for step in self.steps:
            if not step.skill:
                errors.append(f"Step '{step.name}' missing 'skill' field")
            if not step.args and step.args != []:
                errors.append(f"Step '{step.name}' has invalid 'args'")

        if errors:
            print("❌ Validation failed:")
            for err in errors:
                print(f"  - {err}")
            return False
        else:
            print("✅ Workflow is valid!")
            return True

    def summary(self):
        """输出总结"""
        print("="*50)
        print("📋 Workflow Summary")
        print("="*50)
        success_count = sum(1 for s in self.steps if s.status == 'success')
        failed_count = sum(1 for s in self.steps if s.status == 'failed')
        skipped_count = sum(1 for s in self.steps if s.status == 'skipped')

        for step in self.steps:
            status_icon = {'success': '✅', 'failed': '❌', 'skipped': '⏭️', 'pending': '⏳'}.get(step.status, '❓')
            print(f"  {status_icon} {step.name} ({step.status})")

        print()
        print(f"✅ Success: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"⏭️  Skipped: {skipped_count}")
        print("="*50)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  composer.py run <workflow.yaml>")
        print("  composer.py preview <workflow.yaml>")
        print("  composer.py validate <workflow.yaml>")
        print("  composer.py examples")
        sys.exit(1)

    command = sys.argv[1]
    workflow_file = sys.argv[2] if len(sys.argv) > 2 else None

    base_dir = Path(__file__).parent.parent

    if command == 'examples':
        examples_dir = base_dir / 'examples'
        if examples_dir.exists():
            print("📚 Example Workflows:")
            for ex in examples_dir.glob('*.yaml'):
                print(f"  - {ex.name}")
                with open(ex, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('# '):
                        print(f"    {first_line[2:]}")
        else:
            print("ℹ️  No examples directory found.")
        return

    if not workflow_file:
        print("❌ Workflow file is required")
        sys.exit(1)

    workflow_path = Path(workflow_file)
    if not workflow_path.exists():
        print(f"❌ Workflow file not found: {workflow_file}")
        sys.exit(1)

    workflow = Workflow(workflow_path)
    workflow.load()

    if command == 'run':
        workflow.run()
    elif command == 'preview':
        workflow.preview()
    elif command == 'validate':
        workflow.validate()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()