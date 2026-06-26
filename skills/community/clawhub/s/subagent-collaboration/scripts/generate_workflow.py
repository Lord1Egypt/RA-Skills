#!/usr/bin/env python3
"""
协作流程生成器
Collaboration Workflow Generator

功能：
- 根据任务描述自动推荐协作模式
- 生成子代理配置
- 输出可执行代码

使用方法：
python3 skills/subagent-collaboration/scripts/generate_workflow.py --task "任务描述" --mode auto
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = "/Users/nanlin/.openclaw/workspace"

# 协作模式定义
COLLABORATION_MODES = {
    "parallel": {
        "name": "并行协作",
        "description": "多领域专家同时分析，主代理汇总",
        "best_for": "多领域综合分析",
        "agent_count": "3-5 个",
        "estimated_time": "3-5 分钟"
    },
    "serial": {
        "name": "串行协作",
        "description": "任务有依赖关系，按顺序执行",
        "best_for": "工作流任务",
        "agent_count": "2-4 个",
        "estimated_time": "5-10 分钟"
    },
    "hierarchical": {
        "name": "分层协作",
        "description": "超大型任务，多层分解",
        "best_for": "超大型项目",
        "agent_count": "5-10 个",
        "estimated_time": "10-20 分钟"
    },
    "competition": {
        "name": "竞争协作",
        "description": "多方案对比择优",
        "best_for": "方案对比择优",
        "agent_count": "3-5 个",
        "estimated_time": "5-8 分钟"
    },
    "consultation": {
        "name": "专家会诊",
        "description": "疑难问题多专家意见",
        "best_for": "疑难问题会诊",
        "agent_count": "4-6 个",
        "estimated_time": "5-8 分钟"
    },
    "relay": {
        "name": "接力协作",
        "description": "长文本/长任务分段处理",
        "best_for": "长流程处理",
        "agent_count": "3-5 个",
        "estimated_time": "8-15 分钟"
    }
}

# 任务类型到协作模式的映射
TASK_PATTERNS = {
    "分析": "parallel",
    "评估": "parallel",
    "对比": "competition",
    "选择": "competition",
    "开发": "serial",
    "创建": "serial",
    "制定": "hierarchical",
    "规划": "hierarchical",
    "诊断": "consultation",
    "排查": "consultation",
    "整理": "relay",
    "撰写": "relay",
    "报告": "relay"
}

# 预定义子代理角色模板
AGENT_TEMPLATES = {
    "market-analysis": {
        "label": "market-analysis",
        "task_template": "分析市场规模、竞争格局、市场趋势",
        "model": "bailian/qwen3.5-plus",
        "timeoutSeconds": 180
    },
    "tech-analysis": {
        "label": "tech-analysis",
        "task_template": "评估技术壁垒、创新能力、技术风险",
        "model": "bailian/qwen3-coder-plus",
        "timeoutSeconds": 180
    },
    "finance-analysis": {
        "label": "finance-analysis",
        "task_template": "分析财务状况、盈利能力、财务风险",
        "model": "bailian/glm-4.7",
        "timeoutSeconds": 180
    },
    "team-analysis": {
        "label": "team-analysis",
        "task_template": "评估团队背景、执行能力、人员风险",
        "model": "bailian/qwen3.5-plus",
        "timeoutSeconds": 180
    },
    "geo-analysis": {
        "label": "geo-analysis",
        "task_template": "分析地缘政治格局、国际关系",
        "model": "bailian/qwen3.5-plus",
        "timeoutSeconds": 300
    },
    "military-analysis": {
        "label": "military-analysis",
        "task_template": "分析军事能力对比、战争风险",
        "model": "bailian/qwen3-coder-plus",
        "timeoutSeconds": 300
    },
    "economic-analysis": {
        "label": "economic-analysis",
        "task_template": "分析经济影响、制裁效果",
        "model": "bailian/glm-4.7",
        "timeoutSeconds": 300
    },
    "security-analysis": {
        "label": "security-analysis",
        "task_template": "分析网络安全威胁、攻击溯源",
        "model": "bailian/qwen3-coder-plus",
        "timeoutSeconds": 300
    },
    "requirements": {
        "label": "requirements",
        "task_template": "分析用户需求，列出功能清单",
        "model": "bailian/qwen3.5-plus",
        "timeoutSeconds": 120
    },
    "architecture": {
        "label": "architecture",
        "task_template": "设计系统架构、技术方案",
        "model": "bailian/qwen3-coder-plus",
        "timeoutSeconds": 180
    },
    "implementation": {
        "label": "implementation",
        "task_template": "编写代码实现功能",
        "model": "bailian/qwen3-coder-plus",
        "timeoutSeconds": 300
    },
    "code-review": {
        "label": "code-review",
        "task_template": "审查代码质量、安全性、性能",
        "model": "bailian/qwen3-coder-plus",
        "timeoutSeconds": 180
    },
    "synthesizer": {
        "label": "synthesizer",
        "task_template": "汇总各方意见，生成综合报告",
        "model": "bailian/qwen3-max",
        "timeoutSeconds": 300
    }
}

def recommend_mode(task_description):
    """根据任务描述推荐协作模式"""
    # 关键词匹配
    for keyword, mode in TASK_PATTERNS.items():
        if keyword in task_description:
            return mode
    
    # 默认返回并行协作
    return "parallel"

def generate_agents(task_description, mode):
    """根据任务和模式生成子代理配置"""
    agents = []
    
    if mode == "parallel":
        # 并行模式：多领域专家
        agents = [
            AGENT_TEMPLATES["market-analysis"].copy(),
            AGENT_TEMPLATES["tech-analysis"].copy(),
            AGENT_TEMPLATES["finance-analysis"].copy(),
            AGENT_TEMPLATES["team-analysis"].copy()
        ]
        for agent in agents:
            agent["task"] = f"针对任务\"{task_description}\"，{agent['task_template']}"
    
    elif mode == "serial":
        # 串行模式：工作流
        agents = [
            AGENT_TEMPLATES["requirements"].copy(),
            AGENT_TEMPLATES["architecture"].copy(),
            AGENT_TEMPLATES["implementation"].copy(),
            AGENT_TEMPLATES["code-review"].copy()
        ]
        agents[0]["task"] = f"针对任务\"{task_description}\"，{agents[0]['task_template']}"
        for i in range(1, len(agents)):
            agents[i]["task"] = f"基于上一步结果，{agents[i]['task_template']}"
    
    elif mode == "competition":
        # 竞争模式：多方案
        agents = [
            {
                "label": "plan-a-aggressive",
                "task": f"针对任务\"{task_description}\"，设计方案 A：激进策略",
                "model": "bailian/qwen3-max",
                "timeoutSeconds": 300
            },
            {
                "label": "plan-b-conservative",
                "task": f"针对任务\"{task_description}\"，设计方案 B：保守策略",
                "model": "bailian/qwen3-max",
                "timeoutSeconds": 300
            },
            {
                "label": "plan-c-balanced",
                "task": f"针对任务\"{task_description}\"，设计方案 C：平衡策略",
                "model": "bailian/qwen3-max",
                "timeoutSeconds": 300
            }
        ]
    
    elif mode == "consultation":
        # 会诊模式：多专家
        agents = [
            {
                "label": "db-expert",
                "task": f"从数据库角度诊断问题：{task_description}",
                "model": "bailian/qwen3-coder-plus",
                "timeoutSeconds": 180
            },
            {
                "label": "network-expert",
                "task": f"从网络角度诊断问题：{task_description}",
                "model": "bailian/qwen3-coder-plus",
                "timeoutSeconds": 180
            },
            {
                "label": "code-expert",
                "task": f"从代码角度诊断问题：{task_description}",
                "model": "bailian/qwen3-coder-plus",
                "timeoutSeconds": 180
            },
            {
                "label": "infra-expert",
                "task": f"从基础设施角度诊断问题：{task_description}",
                "model": "bailian/qwen3-coder-plus",
                "timeoutSeconds": 180
            }
        ]
    
    elif mode == "relay":
        # 接力模式：分段处理
        agents = [
            {
                "label": "researcher",
                "task": f"收集与\"{task_description}\"相关的最新资料",
                "model": "bailian/qwen3.5-plus",
                "timeoutSeconds": 300
            },
            {
                "label": "organizer",
                "task": "整理收集的资料，分类归纳",
                "model": "bailian/qwen3.5-plus",
                "timeoutSeconds": 180
            },
            {
                "label": "analyst",
                "task": "基于整理的资料撰写分析报告",
                "model": "bailian/qwen3.5-plus",
                "timeoutSeconds": 300
            },
            {
                "label": "editor",
                "task": "润色报告，提升可读性",
                "model": "bailian/qwen3.5-plus",
                "timeoutSeconds": 120
            }
        ]
    
    elif mode == "hierarchical":
        # 分层模式：协调员 + 子任务
        agents = [
            {
                "label": "coordinator",
                "task": f"针对任务\"{task_description}\"，制定总体计划并分解为子任务",
                "model": "bailian/qwen3.5-plus",
                "timeoutSeconds": 180,
                "cleanup": "keep"
            }
        ]
        # 子任务由协调员生成，这里预留位置
    
    # 添加安全配置
    for agent in agents:
        if "sandbox" not in agent:
            agent["sandbox"] = "require"
        if "cleanup" not in agent:
            agent["cleanup"] = "delete"
    
    return agents

def generate_code(workflow):
    """生成可执行的 JavaScript 代码"""
    mode = workflow["mode"]
    agents = workflow["agents"]
    
    code_lines = [
        "// 自动生成的多子代理协作代码",
        f"// 协作模式：{mode}",
        f"// 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "const results = await Promise.all(["
    ]
    
    for agent in agents:
        code_lines.append("  sessions_spawn({")
        code_lines.append(f"    task: \"{agent['task']}\",")
        code_lines.append(f"    label: \"{agent['label']}\",")
        code_lines.append(f"    model: \"{agent['model']}\",")
        code_lines.append(f"    timeoutSeconds: {agent['timeoutSeconds']},")
        code_lines.append(f"    sandbox: \"{agent['sandbox']}\",")
        code_lines.append(f"    cleanup: \"{agent['cleanup']}\"")
        code_lines.append("  }),")
    
    code_lines.append("]);")
    code_lines.append("")
    code_lines.append("// 汇总结果")
    code_lines.append("const finalReport = await sessions_spawn({")
    code_lines.append("  task: `汇总以下结果：${JSON.stringify(results)}`,")
    code_lines.append("  label: \"synthesizer\",")
    code_lines.append("  model: \"bailian/qwen3-max\",")
    code_lines.append("  timeoutSeconds: 300,")
    code_lines.append("  sandbox: \"require\",")
    code_lines.append("  cleanup: \"delete\"")
    code_lines.append("});")
    
    return "\n".join(code_lines)

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def main():
    parser = argparse.ArgumentParser(description="协作流程生成器")
    parser.add_argument("--task", type=str, required=True, help="任务描述")
    parser.add_argument("--mode", type=str, default="auto", 
                       choices=["auto", "parallel", "serial", "hierarchical", 
                               "competition", "consultation", "relay"],
                       help="协作模式（auto=自动推荐）")
    parser.add_argument("--output", type=str, help="输出文件路径")
    
    args = parser.parse_args()
    
    print_header("🤖 协作流程生成器")
    print(f"任务：{args.task}")
    
    # 推荐模式
    if args.mode == "auto":
        recommended_mode = recommend_mode(args.task)
        print_info(f"自动推荐协作模式：{COLLABORATION_MODES[recommended_mode]['name']}")
    else:
        recommended_mode = args.mode
        print_info(f"使用指定模式：{COLLABORATION_MODES[recommended_mode]['name']}")
    
    # 显示模式信息
    mode_info = COLLABORATION_MODES[recommended_mode]
    print(f"\n模式说明：{mode_info['description']}")
    print(f"适用场景：{mode_info['best_for']}")
    print(f"子代理数：{mode_info['agent_count']}")
    print(f"预计耗时：{mode_info['estimated_time']}")
    
    # 生成子代理配置
    print_header("📋 生成子代理配置")
    agents = generate_agents(args.task, recommended_mode)
    
    for i, agent in enumerate(agents, 1):
        print(f"\n{i}. {agent['label']}")
        print(f"   任务：{agent['task'][:50]}...")
        print(f"   模型：{agent['model']}")
        print(f"   超时：{agent['timeoutSeconds']}秒")
        print(f"   沙箱：{agent['sandbox']}")
        print(f"   清理：{agent['cleanup']}")
    
    # 生成工作流
    workflow = {
        "task": args.task,
        "mode": recommended_mode,
        "mode_name": mode_info["name"],
        "generated_at": datetime.now().isoformat(),
        "agents": agents,
        "estimated_time": mode_info["estimated_time"],
        "safety_check": "pending"
    }
    
    # 生成代码
    print_header("💻 生成代码")
    code = generate_code(workflow)
    print(code)
    
    # 保存输出
    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = Path(WORKSPACE) / "workflows" / "subagents"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, ensure_ascii=False, indent=2)
    
    print_header("📁 保存结果")
    print_success(f"工作流已保存：{output_path}")
    
    # 同时保存代码文件
    code_path = output_path.with_suffix('.js')
    with open(code_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print_success(f"代码已保存：{code_path}")
    
    print("\n")

if __name__ == "__main__":
    main()
