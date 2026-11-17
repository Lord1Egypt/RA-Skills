#!/usr/bin/env python3
"""
validate_theme_consistency.py — 主题一致性 JSON 校验脚本

使用方法：
    python3 validate_theme_consistency.py < checklist.json

输入：一个符合 theme-consistency-checklist.md 格式的 JSON 文件（通过 stdin 或文件）
输出：校验结果报告（通过/不通过 + 问题清单）

检查项：
1. 一句话定题答案是否为双核心
2. 标题与正文是否一致
3. 开头与结尾是否呼应
4. 是否存在偏离段落
5. 读者预期是否一致
"""

import json
import sys


def load_input():
    """从 stdin 或命令行参数读取 JSON"""
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            return json.load(f)
    return json.load(sys.stdin)


def validate(data):
    """运行所有校验规则，返回问题清单"""
    issues = []
    suggestions = []

    # === 检查1：一句话定题 ===
    answer = data.get("一句话定题", {})
    my_answer = answer.get("我的答案", "")
    has_and = answer.get("答案中是否出现'和/以及/同时/也'", False)
    verdict = answer.get("判定", "")

    if my_answer and has_and:
        issues.append(f"🔴 双核心风险：一句话定题答案出现'和'类连接词")
        issues.append(f"   → 你的答案：'{my_answer}'")
        suggestions.append(f"   → 建议：拆成两篇文章，或删掉一个核心主题")

    if verdict == "双核心":
        issues.append(f"🔴 判定为双核心，必须处理")
    elif verdict == "立意不明":
        issues.append(f"🔴 立意不明，建议作者重新定调")
    elif verdict == "尾巴多余":
        issues.append(f"🟡 结尾有偏离尾巴，建议删除或合并")

    # === 检查2：双核心诊断 ===
    diag = data.get("双核心诊断", {})
    if diag.get("是否存在双核心", False):
        conclusion = diag.get("结论", "")
        causal = diag.get("两个核心是否有因果关系", False)
        perceived = diag.get("如果有因果，读者是否能明显感知到", True)

        if conclusion == "必须拆分":
            issues.append(f"🔴 两个核心必须拆分")
        elif conclusion == "可合并" and causal and not perceived:
            issues.append(f"🟡 两个核心有因果但读者感知不到，需要加过渡桥")
            suggestions.append(f"   → 建议：在转换点加1-2句过渡，让读者知道你为什么跳话题")

    # === 检查3：偏离检查 ===
    drift = data.get("偏离检查", {})
    title_match = drift.get("标题与正文：标题是否准确预告了全文主题", True)
    ending_match = drift.get("开头与结尾：结尾是否回扣了开头承诺的核心", True)
    has_drift = drift.get("收尾段：是否存在与主题无关的尾巴", False)

    if not title_match:
        issues.append(f"🔴 标题与正文主题不一致")
    if not ending_match:
        issues.append(f"🔴 结尾没有回扣开头承诺的核心主题")
    if has_drift:
        drift_desc = drift.get("偏离段描述", "")
        issues.append(f"🟡 存在与主题无关的段落：{drift_desc}")
        action = drift.get("建议行动", "")
        suggestions.append(f"   → 建议行动：{action}")

    # === 检查4：读者预期 ===
    expectation = data.get("读者预期管理", {})
    consistent = expectation.get("预期与实际是否一致", True)
    if not consistent:
        issues.append(f"🔴 读者预期与实际内容不一致")
        expected = expectation.get("读者读完第一节后的预期", "")
        actual = expectation.get("实际后半篇的内容", "")
        suggestions.append(f"   → 预期：{expected}")
        suggestions.append(f"   → 实际：{actual}")

    return issues, suggestions


def summarize(issues, suggestions):
    """生成报告"""
    if not issues:
        return "✅ 主题一致性检查通过"

    report = f"⚠️ 发现 {len(issues)} 个问题：\n\n"
    for i, issue in enumerate(issues, 1):
        report += f"{issue}\n"

    if suggestions:
        report += "\n📎 建议：\n"
        for s in suggestions:
            report += f"{s}\n"

    return report


def main():
    try:
        data = load_input()
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误：{e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ 文件未找到：{e}", file=sys.stderr)
        sys.exit(1)

    issues, suggestions = validate(data)
    report = summarize(issues, suggestions)
    print(report)

    if issues:
        sys.exit(1)  # exit code 1 = has issues


if __name__ == "__main__":
    main()
