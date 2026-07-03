#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
loop_branch_renderer.py  v1.20.0
为 chain_executor.py 提供 loop / branch 步骤的 AI 指令渲染能力。
独立文件，避免修改 58KB 的 chain_executor.py。
"""

def render_step(step, step_num, indent=0, verbose=True):
    """
    渲染单个步骤（递归支持 skill / loop / branch）。
    返回渲染后的多行字符串列表。
    """
    lines = []
    prefix = "  " * indent
    sub_prefix = "  " * (indent + 1)

    step_type = step.get("type", "skill")

    if step_type == "skill":
        skill = step.get("skill_name", "")
        sname = step.get("step_name", "")
        action = step.get("action", "")
        ms = " ★" if step.get("failure_mode", {}).get("is_milestone") else ""
        lines.append(f"{prefix}{step_num}. [{skill}] {sname}{ms} — {action}")

        if verbose:
            if step.get("detail"):
                lines.append(f"{sub_prefix}详情: {step['detail']}")
            if step.get("condition"):
                lines.append(f"{sub_prefix}条件: {step['condition']}")
            if step.get("input_vars"):
                import json
                lines.append(f"{sub_prefix}输入: {json.dumps(step['input_vars'], ensure_ascii=False)}")
            if step.get("output_vars"):
                import json
                lines.append(f"{sub_prefix}输出: {json.dumps(step['output_vars'], ensure_ascii=False)}")

    elif step_type == "loop":
        loop = step.get("loop", {})
        mode = loop.get("mode", "for_each")
        max_iter = loop.get("max_iterations", 10)
        if mode == "for_each":
            items = loop.get("items", "")
            loop_var = loop.get("loop_variable", "item")
            lines.append(f"{prefix}[循环 for-each] 遍历 {items}，变量名 {loop_var}，最多 {max_iter} 次")
        else:  # while
            cond = loop.get("while_condition", "")
            lines.append(f"{prefix}[循环 while] 条件 {cond}，最多 {max_iter} 次")

        for i, sub in enumerate(loop.get("steps", [])):
            sub_lines = render_step(sub, f"{step_num}.{i+1}", indent + 1, verbose=verbose)
            lines.extend(sub_lines)

    elif step_type == "branch":
        branch = step.get("branch", {})
        cond = branch.get("condition", "")
        lines.append(f"{prefix}[分支] 条件: {cond}")

        if_steps = branch.get("if_steps", [])
        if if_steps:
            lines.append(f"{prefix}  IF TRUE:")
            for i, sub in enumerate(if_steps):
                sub_lines = render_step(sub, f"{step_num}.{i+1}", indent + 2, verbose=verbose)
                lines.extend(sub_lines)

        else_steps = branch.get("else_steps", [])
        if else_steps:
            lines.append(f"{prefix}  ELSE:")
            for i, sub in enumerate(else_steps):
                sub_lines = render_step(sub, f"{step_num}.{i+1}", indent + 2, verbose=verbose)
                lines.extend(sub_lines)

    return lines

def render_plan_with_loop_branch(plan, verbose=True):
    """
    接收 build_execution_plan() 生成的 plan，
    返回带 loop/branch 渲染的完整 AI 执行指令字符串。
    """
    import json

    lines = []
    lines.append(f"【执行调用链】{plan.get('chain_name', '')}")
    lines.append(f"{'='*70}")
    lines.append(f"📌 目的: {plan.get('description', '')}")
    lines.append(f"📝 意图: {plan.get('user_intent', '')}")
    lines.append(f"📐 总步骤: {plan.get('total_steps', 0)}")
    lines.append(f"🔄 默认重试: 最多{plan.get('default_max_retries', 3)}次")

    if plan.get("missing_skills"):
        lines.append(f"\n⚠️ 缺失技能（请先安装）: {', '.join(set(plan['missing_skills']))}")

    lines.append(f"\n{'─'*70}")
    lines.append("执行步骤:")

    step_num = 0
    for group in plan.get("execution_groups", []):
        if group.get("can_parallel"):
            lines.append(f"\n  ⚡ 并行组 {group['group_index']}:")
        for step in group.get("steps", []):
            step_num += 1
            sub_lines = render_step(step, step_num, indent=1, verbose=verbose)
            lines.extend(sub_lines)

    if plan.get("variable_flow"):
        lines.append(f"\n{'─'*70}")
        lines.append("变量传递链:")
        for vf in plan["variable_flow"]:
            lines.append(f"  步骤{vf['from_step']}({vf['from_step_name']}) → 输出: {vf['outputs']}")

    return "\n".join(lines)

if __name__ == "__main__":
    # 自测
    test_plan = {
        "chain_name": "测试链",
        "description": "测试 loop/branch 渲染",
        "user_intent": "测试",
        "total_steps": 3,
        "default_max_retries": 3,
        "missing_skills": [],
        "execution_groups": [
            {
                "group_index": 1,
                "can_parallel": False,
                "steps": [
                    {
                        "step_index": 1,
                        "type": "loop",
                        "step_name": "批量处理",
                        "loop": {
                            "mode": "for_each",
                            "items": "{{file_list}}",
                            "loop_variable": "f",
                            "max_iterations": 5,
                            "steps": [
                                {"type": "skill", "step_name": "处理文件", "skill_name": "file-ops", "action": "处理单个文件"}
                            ]
                        },
                        "failure_mode": {"on_exhaust": "ask", "is_milestone": False}
                    },
                    {
                        "step_index": 2,
                        "type": "branch",
                        "step_name": "按环境部署",
                        "branch": {
                            "condition": "{{env}} == 'prod'",
                            "if_steps": [
                                {"type": "skill", "step_name": "生产部署", "skill_name": "deploy", "action": "部署到生产"}
                            ],
                            "else_steps": [
                                {"type": "skill", "step_name": "预发部署", "skill_name": "deploy", "action": "部署到预发"}
                            ]
                        },
                        "failure_mode": {"on_exhaust": "abort", "is_milestone": True}
                    }
                ]
            }
        ],
        "variable_flow": []
    }

    result = render_plan_with_loop_branch(test_plan)
    print(result)
