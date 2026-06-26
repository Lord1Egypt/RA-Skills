#!/usr/bin/env python3
"""端到端测试：验证 skill-orchestration-core 三个脚本协同工作"""
import json
import sys
sys.path.insert(0, '.')

from workflow_orchestrator import WorkflowOrchestrator
from context_manager import ContextManager
from output_validator import OutputValidator

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
skill_dir = os.path.dirname(script_dir)
design_path = os.path.join(skill_dir, 'templates/example-project/DESIGN.md')
project_path = os.path.join(skill_dir, 'templates/example-project/')

print('=== 1. 解析 DESIGN.md ===')
orch = WorkflowOrchestrator(design_path)
parsed = orch.parse_design()
print(f'  阶段数: {len(parsed["workflow"])}')
for s in parsed["workflow"]:
    print(f'    阶段{s["number"]}: {s["name"]} -> skills={s["skills"]}')
print(f'  上下文规则: {len(parsed["context"])} skills')
print(f'  验证规则: {len(parsed["validation"])} skills')

print('\n=== 2. 上下文管理 ===')
ctx = ContextManager(project_path)
ctx.save()
ctx.set('requirements', {'features': ['用户注册', '登录', '权限管理']})
ctx.mark_skill_completed('writing-plans')
ctx.pass_to('test-driven-development')
print(f'  进度: {ctx.get_progress()}%')
print(f'  已完成: {ctx.get_state()["completedSkills"]}')

print('\n=== 3. Checkpoint/Restore ===')
orch._load_state()
orch.set_checkpoint('after_stage1')
print(f'  保存checkpoint: after_stage1')
ok = orch.restore_checkpoint('after_stage1')
print(f'  恢复checkpoint: {ok}')

print('\n=== 4. 输出验证 ===')
v = OutputValidator(project_path)
v.load_from_design(design_path)
v.validate_all()
print(f'  writing-plans: {v.results["writing-plans"]["valid"]}')
print(f'  test-driven-development: {v.results["test-driven-development"]["valid"]}')
print(f'  requesting-code-review: {v.results["requesting-code-review"]["valid"]}')

print('\n=== 5. 状态查询 ===')
status = orch.get_status()
print(f'  status={status["status"]}, stagesCompleted={status["stagesCompleted"]}')

print('\n=== 端到端测试完成 ===')
