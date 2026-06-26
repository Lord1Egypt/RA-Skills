#!/usr/bin/env python3
"""
子代理安全配置检查器
Sub-agent Security Configuration Checker

功能：
- 检查子代理配置是否符合 RSG v2.2.0 规则
- 检测 openclaw-120 至 openclaw-139 共 20 条规则
- 生成安全检查报告

使用方法：
python3 skills/subagent-collaboration/scripts/security_check.py --input workflow.json
"""

import json
import argparse
import re
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = "/Users/nanlin/.openclaw/workspace"

# RSG v2.2.0 子代理监控规则定义
RSG_SUBAGENT_RULES = {
    "openclaw-120": {
        "name": "子代理无超时限制",
        "severity": "MEDIUM",
        "check": lambda agent: "timeoutSeconds" not in agent and "runTimeoutSeconds" not in agent,
        "message": "未设置超时限制"
    },
    "openclaw-121": {
        "name": "子代理超长超时",
        "severity": "HIGH",
        "check": lambda agent: (agent.get("timeoutSeconds") or agent.get("runTimeoutSeconds") or 0) > 1000,
        "message": "超时时间超过 1000 秒"
    },
    "openclaw-122": {
        "name": "子代理无清理策略",
        "severity": "LOW",
        "check": lambda agent: "cleanup" not in agent,
        "message": "未指定 cleanup 策略"
    },
    "openclaw-123": {
        "name": "子代理继承工作目录风险",
        "severity": "MEDIUM",
        "check": lambda agent: any(pattern in str(agent.get("cwd", "")) 
                                   for pattern in ["/Users", "/home", "~", "/"]),
        "message": "cwd 指向敏感目录"
    },
    "openclaw-124": {
        "name": "子代理沙箱绕过",
        "severity": "HIGH",
        "check": lambda agent: agent.get("sandbox") == "inherit",
        "message": "使用 sandbox=\"inherit\" 可能绕过安全限制"
    },
    "openclaw-125": {
        "name": "子代理 ACP 会话恢复滥用",
        "severity": "HIGH",
        "check": lambda agent: (agent.get("runtime") == "acp" and 
                               len(agent.get("resumeSessionId", "")) > 20),
        "message": "ACP 会话恢复使用长 session ID"
    },
    "openclaw-126": {
        "name": "子代理附件过大",
        "severity": "MEDIUM",
        "check": lambda agent: any(att.get("size", 0) > 10240 
                                   for att in agent.get("attachments", [])),
        "message": "附件大小超过 10KB"
    },
    "openclaw-127": {
        "name": "子代理附件过多",
        "severity": "MEDIUM",
        "check": lambda agent: len(agent.get("attachments", [])) > 5,
        "message": "附件数量超过 5 个"
    },
    "openclaw-128": {
        "name": "子代理流式输出到父会话",
        "severity": "MEDIUM",
        "check": lambda agent: (agent.get("streamTo") == "parent" and 
                               agent.get("mode") == "session"),
        "message": "持久化子代理流式输出到父会话"
    },
    "openclaw-129": {
        "name": "子代理递归生成",
        "severity": "CRITICAL",
        "check": lambda agent: "sessions_spawn" in agent.get("task", ""),
        "message": "任务包含 sessions_spawn，可能导致递归生成"
    },
    "openclaw-130": {
        "name": "子代理高成本模型",
        "severity": "LOW",
        "check": lambda agent: any(model in (agent.get("model") or "") 
                                   for model in ["qwen3-max", "glm-5", "kimi-k2.5"]),
        "message": "使用高成本模型"
    },
    "openclaw-131": {
        "name": "子代理无标签标识",
        "severity": "LOW",
        "check": lambda agent: "label" not in agent or not agent["label"],
        "message": "未设置 label 标识"
    },
    "openclaw-132": {
        "name": "子代理敏感任务",
        "severity": "HIGH",
        "check": lambda agent: any(pattern in (agent.get("task") or "").lower() 
                                   for pattern in ["memory_", "config.", "gateway.", "secret", "password", "token"]),
        "message": "任务涉及敏感操作（记忆/配置/凭据）"
    },
    "openclaw-133": {
        "name": "子代理网络访问",
        "severity": "MEDIUM",
        "check": lambda agent: any(pattern in (agent.get("task") or "").lower() 
                                   for pattern in ["web_fetch", "web_search", "browser", "curl", "wget"]),
        "message": "任务包含网络访问"
    },
    "openclaw-134": {
        "name": "子代理文件写入",
        "severity": "MEDIUM",
        "check": lambda agent: any(pattern in (agent.get("task") or "").lower() 
                                   for pattern in ["write", "create", "delete"]) and ".md" in (agent.get("task") or ""),
        "message": "任务涉及文件写入"
    },
    "openclaw-135": {
        "name": "子代理命令执行",
        "severity": "CRITICAL",
        "check": lambda agent: any(pattern in (agent.get("task") or "").lower() 
                                   for pattern in ["exec", "sudo", "rm -rf", "chmod"]),
        "message": "任务包含命令执行"
    },
    "openclaw-136": {
        "name": "子代理会话历史访问",
        "severity": "HIGH",
        "check": lambda agent: "sessions_history" in (agent.get("task") or "").lower(),
        "message": "任务涉及会话历史访问"
    },
    "openclaw-137": {
        "name": "子代理跨会话消息",
        "severity": "HIGH",
        "check": lambda agent: "sessions_send" in (agent.get("task") or "").lower(),
        "message": "任务涉及跨会话消息"
    },
    "openclaw-138": {
        "name": "子代理工具调用",
        "severity": "MEDIUM",
        "check": lambda agent: any(pattern in (agent.get("task") or "").lower() 
                                   for pattern in ["message", "gateway", "cron", "nodes", "canvas"]),
        "message": "任务涉及高权限工具调用"
    },
    "openclaw-139": {
        "name": "子代理并发数过多",
        "severity": "HIGH",
        "check": lambda agents: len(agents) > 3 if isinstance(agents, list) else False,
        "message": "并发子代理数量超过 3 个",
        "is_batch_check": True
    }
}

SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
SEVERITY_COLORS = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🔵"
}

def load_workflow(input_path):
    """加载工作流配置文件"""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{input_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_agent(agent, rule_id, rule):
    """检查单个代理是否符合规则"""
    try:
        if rule.get("is_batch_check"):
            return False  # 批量检查单独处理
        return rule["check"](agent)
    except Exception as e:
        return False

def check_batch(agents, rule_id, rule):
    """批量检查规则"""
    try:
        if rule.get("is_batch_check"):
            return rule["check"](agents)
        return False
    except Exception as e:
        return False

def run_security_check(workflow):
    """执行安全检查"""
    agents = workflow.get("agents", [])
    violations = []
    passed = []
    
    # 单个代理检查
    for agent in agents:
        agent_violations = []
        
        for rule_id, rule in RSG_SUBAGENT_RULES.items():
            if rule.get("is_batch_check"):
                continue
            
            if check_agent(agent, rule_id, rule):
                agent_violations.append({
                    "rule_id": rule_id,
                    "rule_name": rule["name"],
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "agent_label": agent.get("label", "unknown")
                })
        
        if not agent_violations:
            passed.append(agent.get("label", "unknown"))
        
        violations.extend(agent_violations)
    
    # 批量检查
    for rule_id, rule in RSG_SUBAGENT_RULES.items():
        if rule.get("is_batch_check"):
            if check_batch(agents, rule_id, rule):
                violations.append({
                    "rule_id": rule_id,
                    "rule_name": rule["name"],
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "agent_label": "all"
                })
    
    return violations, passed

def generate_report(workflow, violations, passed):
    """生成安全检查报告"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "task": workflow.get("task", "unknown"),
        "mode": workflow.get("mode", "unknown"),
        "total_agents": len(workflow.get("agents", [])),
        "violations": violations,
        "passed_agents": passed,
        "summary": {
            "CRITICAL": len([v for v in violations if v["severity"] == "CRITICAL"]),
            "HIGH": len([v for v in violations if v["severity"] == "HIGH"]),
            "MEDIUM": len([v for v in violations if v["severity"] == "MEDIUM"]),
            "LOW": len([v for v in violations if v["severity"] == "LOW"])
        },
        "passed": len(violations) == 0
    }
    
    return report

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def main():
    parser = argparse.ArgumentParser(description="子代理安全配置检查器")
    parser.add_argument("--input", type=str, required=True, help="工作流配置文件路径")
    parser.add_argument("--output", type=str, help="报告输出路径")
    parser.add_argument("--quiet", action="store_true", help="安静模式，只输出结果")
    
    args = parser.parse_args()
    
    if not args.quiet:
        print_header("🛡️  RSG v2.2.0 子代理安全检查")
        print(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 加载工作流
    try:
        workflow = load_workflow(args.input)
        if not args.quiet:
            print_info(f"加载工作流：{workflow.get('task', 'unknown')[:50]}...")
    except Exception as e:
        print_error(f"加载失败：{e}")
        return 1
    
    # 执行检查
    if not args.quiet:
        print_info(f"检查 {len(workflow.get('agents', []))} 个子代理配置...")
    
    violations, passed = run_security_check(workflow)
    report = generate_report(workflow, violations, passed)
    
    # 输出结果
    if not args.quiet:
        print_header("📊 检查结果")
        
        if report["passed"]:
            print_success("安全检查通过！")
            print(f"\n✅ 通过检查的子代理：{len(passed)} 个")
        else:
            print_error(f"发现 {len(violations)} 个安全问题")
            
            # 按严重程度分组
            for severity in SEVERITY_ORDER:
                severity_violations = [v for v in violations if v["severity"] == severity]
                if severity_violations:
                    print(f"\n{SEVERITY_COLORS[severity]} {severity} ({len(severity_violations)}个):")
                    for v in severity_violations:
                        print(f"   - [{v['rule_id']}] {v['rule_name']}")
                        print(f"     代理：{v['agent_label']}")
                        print(f"     问题：{v['message']}")
    
    # 保存报告
    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = Path(WORKSPACE) / "security_reports" / "subagents"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"security_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    if not args.quiet:
        print_header("📁 报告保存")
        print_success(f"报告已保存：{output_path}")
        
        # 输出修复建议
        if violations:
            print_header("💡 修复建议")
            
            critical_count = report["summary"]["CRITICAL"]
            high_count = report["summary"]["HIGH"]
            
            if critical_count > 0:
                print_error(f"紧急：{critical_count} 个严重问题必须修复")
                print("   - 移除递归生成（openclaw-129）")
                print("   - 移除命令执行（openclaw-135）")
            
            if high_count > 0:
                print_warning(f"重要：{high_count} 个高风险问题建议修复")
                print("   - 设置合理超时时间（≤300 秒）")
                print("   - 使用 sandbox=\"require\"")
                print("   - 避免敏感任务委托给子代理")
            
            print("\n通用建议：")
            print("   - 始终设置 label 标识")
            print("   - 设置 cleanup=\"delete\" 自动清理")
            print("   - 简单任务使用低成本模型（glm-4.7）")
            print("   - 控制并发数≤3 个")
    
    # 返回状态码
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    exit(main())
