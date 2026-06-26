#!/usr/bin/env python3
"""
子代理配置分析器
Sub-agent Configuration Analyzer

功能：
- 扫描已配置的子代理角色
- 分析模型分布
- 识别能力覆盖
- 提供优化建议

使用方法：
python3 skills/subagent-collaboration/scripts/analyze_subagents.py
"""

import json
import os
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = "/Users/nanlin/.openclaw/workspace"
DOCS_DIR = Path(WORKSPACE) / "docs"
MEMORY_FILE = Path(WORKSPACE) / "MEMORY.md"

# 已知角色配置（从 subagent-roles-v2.md 提取）
KNOWN_ROLES = {
    "国际战略分析师": {"model": "qwen3.5-plus", "category": "战略分析"},
    "商业战略咨询师": {"model": "qwen3.5-plus", "category": "战略分析"},
    "军事战略专家": {"model": "qwen3-coder-plus", "category": "战略分析"},
    "网络安全专家": {"model": "qwen3-coder-plus", "category": "安全技术"},
    "情报分析专家": {"model": "qwen3.5-plus", "category": "安全技术"},
    "资深开发工程师": {"model": "qwen3-coder-plus", "category": "安全技术"},
    "专业律师": {"model": "qwen3.5-plus", "category": "法律经济"},
    "经济制裁专家": {"model": "glm-4.7", "category": "法律经济"},
    "专业人力资源 HRD": {"model": "glm-4.7", "category": "管理服务"},
    "心理咨询师": {"model": "qwen3.5-plus", "category": "管理服务"},
    "生活助理": {"model": "glm-4.7", "category": "管理服务"},
    "健身教练": {"model": "glm-4.7", "category": "健康"},
}

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def analyze_docs():
    """分析 docs 目录中的子代理配置"""
    roles_found = {}
    
    # 读取 subagent-roles-v2.md
    roles_file = DOCS_DIR / "subagent-roles-v2.md"
    if roles_file.exists():
        content = roles_file.read_text(encoding='utf-8')
        
        # 提取角色名称
        for role_name in KNOWN_ROLES.keys():
            if role_name in content:
                roles_found[role_name] = KNOWN_ROLES[role_name]
    
    return roles_found

def analyze_memory():
    """分析 MEMORY.md 中的子代理使用记录"""
    usage_stats = {}
    
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding='utf-8')
        
        # 简单统计：查找 sessions_spawn 相关记录
        # （实际应该更复杂的解析，这里简化处理）
        if "sessions_spawn" in content:
            usage_stats["has_usage"] = True
    
    return usage_stats

def analyze_model_distribution(roles):
    """分析模型分布"""
    model_count = {}
    category_count = {}
    
    for role_name, config in roles.items():
        model = config.get("model", "unknown")
        category = config.get("category", "unknown")
        
        model_count[model] = model_count.get(model, 0) + 1
        category_count[category] = category_count.get(category, 0) + 1
    
    return model_count, category_count

def generate_recommendations(roles, model_dist, category_dist):
    """生成优化建议"""
    recommendations = []
    
    # 检查角色覆盖
    total_roles = len(KNOWN_ROLES)
    configured_roles = len(roles)
    
    if configured_roles < total_roles:
        missing = total_roles - configured_roles
        recommendations.append(f"已配置 {configured_roles}/{total_roles} 个角色，可考虑补充 {missing} 个角色")
    
    # 检查模型分布
    high_cost_models = sum(count for model, count in model_dist.items() 
                          if "max" in model or "coder-plus" in model)
    low_cost_models = sum(count for model, count in model_dist.items() 
                         if "glm-4.7" in model)
    
    if high_cost_models > low_cost_models:
        recommendations.append("高成本模型使用较多，建议简单任务改用 glm-4.7")
    
    # 检查类别平衡
    if len(category_dist) < 3:
        recommendations.append("角色类别较单一，建议覆盖更多领域（战略/技术/法律/管理等）")
    
    # 特定建议
    if "医疗" not in str(category_dist.keys()):
        recommendations.append("可考虑添加医疗顾问角色")
    
    if "法律" not in str(category_dist.keys()):
        recommendations.append("可考虑添加法律顾问角色")
    
    return recommendations

def main():
    print_header("🤖 子代理配置分析器")
    print(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 分析配置
    print_info("扫描子代理配置...")
    roles = analyze_docs()
    
    if roles:
        print_success(f"已配置子代理角色：{len(roles)} 个")
        for role_name, config in roles.items():
            print(f"   - {role_name} ({config['model']})")
    else:
        print_warning("未检测到明确的子代理配置")
        print_info("参考 subagent-roles-v2.md 中的 12 个预定义角色")
    
    # 模型分布
    print_header("📊 模型分布")
    model_dist, category_dist = analyze_model_distribution(roles)
    
    for model, count in sorted(model_dist.items(), key=lambda x: -x[1]):
        print(f"   {model}: {count} 个")
    
    # 类别分布
    print_header("📋 类别分布")
    for category, count in sorted(category_dist.items(), key=lambda x: -x[1]):
        print(f"   {category}: {count} 个")
    
    # 优化建议
    print_header("💡 优化建议")
    recommendations = generate_recommendations(roles, model_dist, category_dist)
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    else:
        print_success("配置良好，无需特别优化")
    
    # 输出 JSON 报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "configured_roles": len(roles),
        "roles": list(roles.keys()),
        "model_distribution": model_dist,
        "category_distribution": category_dist,
        "recommendations": recommendations
    }
    
    output_dir = Path(WORKSPACE) / "analysis" / "subagents"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print_header("📁 报告保存")
    print_success(f"报告已保存：{output_file}")
    
    print("\n")

if __name__ == "__main__":
    main()
