# -*- coding: utf-8 -*-
"""
保留 v1.7 的「会思考的进化 AI」核心能力（原有功能不丢）：

  - analyze_memory : 智能记忆分析（理解本质 / 根因 / 隐含需求 / 自动修复）
  - predict_risks  : 预测性维护（从历史推断明日风险）
  - generate_report: 进化报告（成长趋势统计）

这里把原 SKILL.md 中的逻辑原样保留为可调用的命令，并让它们读写同一份
「每日日志」（~/.workbuddy/memory/YYYY-MM-DD.md），与 v2.0.0 的记忆底座共存。
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from datetime import date, timedelta

from . import config


# ── 工具 ──────────────────────────────────────────────────────────────────
def safe_read(filepath: str):
    if not os.path.exists(filepath):
        return None
    for enc in ["utf-8", "gbk", "gb2312", "latin1"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
            if enc != "utf-8":
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
            if not content.strip():
                return None
            return content
        except UnicodeDecodeError:
            continue
        except PermissionError:
            return None
    return None


def extract_issues(text: str):
    patterns = [
        r"(?:报错|错误|失败|不行|问题|无法|bug|坑)[：:]?\s*(.+)",
        r"(?:Exception|Error|Failed)[：:]?\s*(.+)",
    ]
    issues = []
    for p in patterns:
        for m in re.findall(p, text, re.IGNORECASE):
            # 去掉前导标点/空白，避免「，提示 token 错误。」这类脏片段
            clean = m.strip().strip("，。；;、, ：: ")
            if clean:
                issues.append(clean)
    return issues


def find_root_cause(issue: str, fix_log: list):
    d = issue.lower()
    if "token" in d or "key" in d:
        recent = [h for h in fix_log if any("token" in f.get("problem", "").lower()
                                            for f in h.get("fixes", []))]
        date_str = recent[-1]["date"] if recent else "未知"
        return "Token 过期或类型错误（上次成功更新: %s）" % date_str
    if "permission" in d or "权限" in d:
        return "系统安全策略限制（执行策略/访问权限未配置）"
    if "module" in d or "import" in d:
        return "Python 环境未安装所需依赖库"
    if "network" in d or "connection" in d:
        return "网络连接不稳定或代理/VPN 设置问题"
    if "文件" in d or "找不到" in d:
        return "文件路径变更或被意外删除"
    return "需要更多上下文分析"


def find_implicit_needs(content: str):
    needs = []
    c = content.lower()
    if "publish" in c or "发布" in c:
        needs.append("发布前自动检查 token 和登录状态")
    if "skillhub" in c and "token" in c:
        needs.append("创建 token 定期刷新提醒")
    return needs


def smart_fix(root_cause: str):
    d = root_cause.lower()
    if "token" in d:
        return {"status": "manual", "cmd": "skillhub auth whoami",
                "msg": "请运行: skillhub auth whoami"}
    if "权限" in d:
        return {"status": "manual", "cmd": "Set-ExecutionPolicy RemoteSigned",
                "msg": "以管理员运行 PowerShell 并执行: Set-ExecutionPolicy RemoteSigned"}
    if "依赖库" in d:
        return {"status": "success", "cmd": "pip install",
                "msg": "可自动安装缺失库"}
    if "网络" in d:
        return {"status": "manual", "cmd": "ping skillhub.cn",
                "msg": "请检查网络连接"}
    return {"status": "logged", "cmd": None, "msg": "已记录，积累后可自动优化"}


def save_fix_log(fix_log_path: str, fixes: list) -> None:
    try:
        logs = []
        if os.path.exists(fix_log_path):
            with open(fix_log_path, "r") as f:
                logs = json.load(f)
        logs.append({"date": date.today().strftime("%Y-%m-%d"), "fixes": fixes})
        with open(fix_log_path, "w") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ── 命令 ──────────────────────────────────────────────────────────────────
def analyze_memory(day: str | None = None, auto_fix: bool = True) -> dict | None:
    today = day or date.today().strftime("%Y-%m-%d")
    today_file = config.daily_log_path(today)
    fix_log_path = str(config.ZWJH_DIR / "fix_log.json")

    if not os.path.exists(today_file):
        print("📭 今日 (%s) 没有记忆文件" % today)
        print("   说「帮我配置 + 设置定时任务」— 一键创建环境")
        print("   说「模拟演示」— 用假数据看 AI 怎么思考")
        return None

    content = safe_read(str(today_file))
    if content is None:
        return None

    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    problems = []
    fix_log = []
    if os.path.exists(fix_log_path):
        try:
            with open(fix_log_path, "r") as f:
                fix_log = json.load(f)
        except Exception:
            fix_log = []

    for p in paragraphs:
        for issue in extract_issues(p):
            root = find_root_cause(issue, fix_log)
            problems.append({"surface": issue, "root": root})

    needs = find_implicit_needs(content)
    fixes = []
    if auto_fix:
        for prob in problems:
            # 关键：把「问题原文」一并写入 fix，否则 predict_risks 无法统计模式
            fx = smart_fix(prob["root"])
            fx["problem"] = prob["surface"]
            fx["root"] = prob["root"]
            fixes.append(fx)

    print("═══════════════════════════════════════════")
    print("  🧠 深度记忆分析报告 (%s)" % today)
    print("═══════════════════════════════════════════")
    ok = sum(1 for f in fixes if f["status"] == "success")
    manual = sum(1 for f in fixes if f["status"] == "manual")
    print("  识别问题: %d | 自动修复: %d | 需操作: %d" % (len(problems), ok, manual))
    print("───────────────────────────────────────────")
    for i, p in enumerate(problems, 1):
        print("  %d. %s" % (i, p["surface"][:40]))
        print("     → %s" % p["root"][:50])
    if needs:
        print("\n  💡 建议: %s" % "; ".join(needs))
    print("\n═══════════════════════════════════════════")

    save_fix_log(fix_log_path, fixes)
    return {"problems": problems, "fixes": fixes}


def predict_risks() -> None:
    fix_log_path = str(config.ZWJH_DIR / "fix_log.json")
    print("═══════════════════════════════════════════")
    print("  🔮 预测性维护报告")
    print("═══════════════════════════════════════════")
    if not os.path.exists(fix_log_path):
        print("  📭 暂无数据 - 先运行几次记忆分析")
        return
    try:
        with open(fix_log_path, "r") as f:
            logs = json.load(f)
    except Exception:
        logs = []
    if not logs:
        print("  📭 暂无历史记录")
        return

    problem_freq = Counter()
    for entry in logs[-7:]:
        for fix in entry.get("fixes", []):
            desc = fix.get("problem", "")
            if "token" in desc.lower() or "key" in desc.lower():
                problem_freq["token_expiry"] += 1
            elif "permission" in desc.lower() or "权限" in desc:
                problem_freq["permission"] += 1
            elif "module" in desc.lower():
                problem_freq["module"] += 1
            elif "network" in desc.lower():
                problem_freq["network"] += 1

    predictions = []
    for ptype, count in problem_freq.most_common(3):
        if count >= 2:
            risk = "高" if count >= 3 else "中"
            predictions.append({"type": ptype, "risk": risk})

    if predictions:
        print("\n  数据量: %d 天" % len(logs))
        print("\n  ⚠️ 预测到 %d 个潜在风险:" % len(predictions))
        for p in predictions:
            print("    [%s] %s" % (p["risk"], p["type"]))
    else:
        print("  ✅ 近期运行稳定，无高风险")
    print("\n═══════════════════════════════════════════")


def generate_report(days: int = 30) -> None:
    fix_log_path = str(config.ZWJH_DIR / "fix_log.json")
    today = date.today()
    if not os.path.exists(fix_log_path):
        print("📭 暂无数据")
        return
    try:
        with open(fix_log_path, "r") as f:
            logs = json.load(f)
    except Exception:
        return

    cutoff = (today - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [l for l in logs if isinstance(l, dict) and l.get("date", "") >= cutoff]
    if not recent:
        print("最近 %d 天无数据" % days)
        return

    total = success = 0
    for log in recent:
        for fix in log.get("fixes", []):
            total += 1
            if fix.get("status") == "success":
                success += 1
    rate = (success / max(total, 1)) * 100
    status = "📈 进步中" if rate > 70 else "📊 稳定" if rate > 50 else "📉 有挑战"

    report = (
        "# 🧬 进化报告 (%s)\n\n"
        "**周期**: %s ~ %s\n\n"
        "## 📊 汇总\n"
        "- 总修复次数: **%d**\n"
        "- 成功自动修复: **%d** (%d%%)\n"
        "- 数据覆盖: **%d** 天\n\n"
        "## 🎯 成长状态\n%s\n"
        % (today.strftime("%Y-%m-%d"),
           (today - timedelta(days=days)).strftime("%Y-%m-%d"),
           today.strftime("%Y-%m-%d"), total, success, rate, len(recent), status)
    )
    print(report)
    report_file = config.MEMORY_DIR / ("evolution_report_%s.md"
                                       % today.strftime("%Y%m%d"))
    try:
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        print("📄 报告已保存: %s" % report_file)
    except Exception:
        pass


def demo() -> None:
    """模拟演示（无真实数据时展示效果）。"""
    fake = (
        "今天 SkillHub 发布失败，提示 token 错误。\n\n"
        "PowerShell 执行策略导致脚本无法运行。\n\n"
        "需要做一个发布前检查清单，避免再忘刷新 token。"
    )
    print("（模拟演示数据）\n")
    paragraphs = [p.strip() for p in fake.split("\n\n") if p.strip()]
    problems = []
    for p in paragraphs:
        for issue in extract_issues(p):
            problems.append({"surface": issue, "root": find_root_cause(issue, [])})
    needs = find_implicit_needs(fake)
    print("═══════════════════════════════════════════")
    print("  🧠 深度记忆分析报告 (模拟)")
    print("═══════════════════════════════════════════")
    for i, p in enumerate(problems, 1):
        print("  %d. %s" % (i, p["surface"][:40]))
        print("     → %s" % p["root"][:50])
    if needs:
        print("\n  💡 建议: %s" % "; ".join(needs))
    print("\n═══════════════════════════════════════════")
