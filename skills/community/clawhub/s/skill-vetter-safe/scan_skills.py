#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全审核标准_自动化 v1.1
作者: 系统安全策略
原始版本，兼容 Windows 路径
"""
import os
import json
import re
from datetime import datetime

# 跨平台处理：自动检测 OS
if os.name == "nt":
    SKILLS_DIR = r"C:\Users\Administrator\.claude\skills"
else:
    SKILLS_DIR = os.path.join(os.path.expanduser("~"), ".claude", "skills")
    # 如果 ~/.claude/skills 不存在，尝试 /workspace/skills
    if not os.path.isdir(SKILLS_DIR):
        SKILLS_DIR = "/workspace/skills"

REPORT_FILE = os.path.join(SKILLS_DIR, "技能安全审计报告.json")

# 可疑关键词列表
SUSPICIOUS_KEYWORDS = [
    "eval", "exec", "os.system",
    "subprocess", "requests.get", "urllib",
    "open('http", "socket"
]


def scan_skill(file_path):
    """扫描单个文件，返回风险评估结果"""
    result = {
        "文件名": os.path.basename(file_path),
        "路径": file_path,
        "风险评分": 100,
        "风险等级": "🟢 安全",
        "风险点": [],
        "建议": "允许安装"
    }

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # 检测可疑关键词
        for kw in SUSPICIOUS_KEYWORDS:
            if kw in content:
                result["风险点"].append(f"包含可疑关键词: {kw}")
                result["风险评分"] -= 20

        # 降低分数判定权限异常、外部访问
        if re.search(
            r"(sudo|chmod|chown|root|network|socket)",
            content, re.IGNORECASE
        ):
            result["风险点"].append("可能请求高权限或网络访问")
            result["风险评分"] -= 20

        # 风险等级判断
        score = result["风险评分"]

        if score <= 30:
            result["风险等级"] = "🔴 禁止"
            result["建议"] = "禁止安装"
        elif score <= 70:
            result["风险等级"] = "🟡 谨慎"
            result["建议"] = "谨慎安装，建议沙箱运行"

        # 自动补充最后扫描时间
        result["扫描时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        result["风险点"].append(f"扫描失败: {str(e)}")
        result["风险评分"] = 0
        result["风险等级"] = "🔴 禁止"
        result["建议"] = "禁止安装"

    return result


def main():
    report = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        for file in files:
            if file.endswith((".py", ".json", ".js")):
                file_path = os.path.join(root, file)
                result = scan_skill(file_path)
                report.append(result)

    # 输出报告
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

    # 打印摘要
    total = len(report)
    safe = len([r for r in report if r["风险等级"] == "🟢 安全"])
    caution = len([r for r in report if r["风险等级"] == "🟡 谨慎"])
    danger = len([r for r in report if r["风险等级"] == "🔴 禁止"])

    print(f"=" * 40)
    print(f"技能安全审计报告")
    print(f"=" * 40)
    print(f"扫描目录: {SKILLS_DIR}")
    print(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"合计文件: {total}")
    print(f"🟢 安全:   {safe}")
    print(f"🟡 谨慎:   {caution}")
    print(f"🔴 禁止:   {danger}")
    print(f"=" * 40)
    print(f"报告已生成: {REPORT_FILE}")


if __name__ == "__main__":
    main()
