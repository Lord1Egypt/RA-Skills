#!/usr/bin/env python3
"""
企业安全审计模块 - Phase 1
钓鱼邮件识别 + 密码策略审计

用法:
  python3 enterprise_audit.py phishing --url "https://suspicious-site.com" --sender "admin@g00gle.com"
  python3 enterprise_audit.py password-policy --input policy.json
  python3 enterprise_audit.py full-audit --email user@example.com --sender "support@paypa1.com"
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from urllib.parse import urlparse


# ============================================================
# 钓鱼邮件识别
# ============================================================

# 常见品牌域名（用于lookalike检测）
BRAND_DOMAINS = {
    "google": ["google.com", "gmail.com"],
    "microsoft": ["microsoft.com", "outlook.com", "office.com"],
    "apple": ["apple.com", "icloud.com"],
    "amazon": ["amazon.com", "aws.amazon.com"],
    "paypal": ["paypal.com"],
    "alipay": ["alipay.com"],
    "wechat": ["wechat.com", "weixin.qq.com"],
    "taobao": ["taobao.com"],
    "jd": ["jd.com"],
    "dji": ["dji.com"],
    "bytedance": ["bytedance.com"],
    "feishu": ["feishu.cn"],
    "dingtalk": ["dingtalk.com"],
    "baidu": ["baidu.com"],
}

# 可疑URL特征模式
SUSPICIOUS_URL_PATTERNS = [
    (r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "IP直连URL", "high"),
    (r"https?://[a-z0-9-]+\.(xyz|top|club|win|click|download|stream|gq|ml|cf|ga|tk)", "高风险TLD域名", "high"),
    (r"https?://[a-z0-9-]*-(login|secure|verify|update|confirm|account|signin)[a-z0-9-]*\.", "关键词伪装域名", "high"),
    (r"https?://bit\.ly|t\.co|tinyurl|ow\.ly|is\.gd", "短链接（可能隐藏真实URL）", "medium"),
    (r"https?://[a-z0-9-]+\.weebly\.com|\.wordpress\.com|\.wix\.com|\.blogspot\.com", "免费建站平台", "medium"),
    (r"https?://[a-z0-9-]+\.(ru|cn|br|in)/[a-z0-9-]+-(secure|login|verify)", "非主流国家域名+安全关键词", "medium"),
]

# 钓鱼邮件正文特征
PHISHING_BODY_PATTERNS = [
    (r"urgent.{0,20}(action|required|attention)", "紧急行动要求", "high"),
    (r"(suspend|关闭|冻结|停用).{0,30}(account|账号|账户)", "账号威胁", "high"),
    (r"(click|点击).{0,20}(link|link|链接).{0,30}(verify|验证|confirm|确认)", "点击验证链接", "high"),
    (r"(congratulations|恭喜).{0,30}(won|中奖|prize|奖金)", "中奖诈骗", "medium"),
    (r"(password|密码).{0,20}(expire|过期|expir)", "密码过期威胁", "high"),
    (r"(wire|transfer|汇款|转账).{0,30}(immediately|立即|urgent|紧急)", "紧急转账要求", "high"),
]


def detect_lookalike_domain(sender_domain):
    """检测仿冒品牌域名"""
    domain_lower = sender_domain.lower().replace("www.", "")
    parts = domain_lower.split(".")
    if len(parts) < 2:
        return None

    root = parts[0]
    alerts = []

    # 视觉混淆字符替换后匹配品牌
    visual_map = {"0": "o", "1": "l", "3": "e", "5": "s", "7": "t", "9": "g",
                  "l": "i", "rn": "m", "nn": "m", "ii": "ll"}
    normalized = root
    for old, new in visual_map.items():
        normalized = normalized.replace(old, new)

    for brand, domains in BRAND_DOMAINS.items():
        for brand_domain in domains:
            brand_root = brand_domain.split(".")[0]
            if normalized == brand_root and domain_lower not in domains:
                alerts.append({
                    "brand": brand,
                    "real_domain": domains[0],
                    "fake_domain": domain_lower,
                    "type": "视觉混淆域名",
                    "risk": "high"
                })
            # Levenshtein距离=1的相似域名
            elif len(root) == len(brand_root) and _levenshtein(root, brand_root) == 1:
                if domain_lower not in domains:
                    alerts.append({
                        "brand": brand,
                        "real_domain": domains[0],
                        "fake_domain": domain_lower,
                        "type": "拼写近似域名",
                        "risk": "high"
                    })

    return alerts if alerts else None


def _levenshtein(s1, s2):
    """计算Levenshtein编辑距离"""
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


def analyze_phishing(url=None, sender=None, body=None):
    """综合钓鱼邮件分析"""
    findings = []
    risk_score = 0  # 0=安全, 1-30=低风险, 31-60=中风险, 61-100=高风险

    # 1. URL分析
    if url:
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split("/")[0]

            for pattern, desc, level in SUSPICIOUS_URL_PATTERNS:
                if re.search(pattern, url, re.IGNORECASE):
                    score = 30 if level == "high" else 15
                    risk_score += score
                    findings.append({
                        "category": "URL特征",
                        "finding": desc,
                        "detail": f"匹配URL: {url}",
                        "risk": level,
                        "score": score
                    })

            # HTTPS检查
            if parsed.scheme == "http":
                risk_score += 10
                findings.append({
                    "category": "URL特征",
                    "finding": "非HTTPS连接",
                    "detail": f"URL使用不安全的HTTP协议",
                    "risk": "medium",
                    "score": 10
                })
        except Exception as e:
            findings.append({"category": "URL分析", "finding": f"解析失败: {e}", "risk": "low", "score": 0})

    # 2. 发件人域名分析
    if sender:
        sender_domain = sender.split("@")[-1] if "@" in sender else sender
        lookalike = detect_lookalike_domain(sender_domain)
        if lookalike:
            for alert in lookalike:
                risk_score += 35
                findings.append({
                    "category": "仿冒域名",
                    "finding": alert["type"],
                    "detail": f"仿冒品牌: {alert['brand']} (真实: {alert['real_domain']}, 仿冒: {alert['fake_domain']})",
                    "risk": alert["risk"],
                    "score": 35
                })

    # 3. 正文分析
    if body:
        for pattern, desc, level in PHISHING_BODY_PATTERNS:
            if re.search(pattern, body, re.IGNORECASE):
                score = 20 if level == "high" else 10
                risk_score += score
                findings.append({
                    "category": "正文特征",
                    "finding": desc,
                    "detail": f"匹配钓鱼话术: {desc}",
                    "risk": level,
                    "score": score
                })

    # 风险等级
    risk_score = min(risk_score, 100)
    if risk_score >= 61:
        verdict = "🔴 高风险 - 极可能是钓鱼邮件"
    elif risk_score >= 31:
        verdict = "🟡 中风险 - 存在可疑特征，需人工核实"
    elif risk_score >= 10:
        verdict = "🟠 低风险 - 有轻微可疑点，建议留意"
    else:
        verdict = "🟢 安全 - 未发现明显钓鱼特征"

    return {
        "risk_score": risk_score,
        "verdict": verdict,
        "findings": findings,
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


# ============================================================
# 密码策略审计
# ============================================================

# 中国等保2.0 / ISO 27001 密码策略基线
POLICY_BASELINE = {
    "min_length": {"required": 8, "recommended": 12, "standard": "等保2.0 / ISO 27001"},
    "complexity": {
        "require_upper": True,
        "require_lower": True,
        "require_digit": True,
        "require_special": True,
        "standard": "等保2.0 三级要求"
    },
    "max_age_days": {"required": 90, "recommended": 60, "standard": "ISO 27001 A.9.4.3"},
    "history_count": {"required": 3, "recommended": 5, "standard": "CIS Control 16"},
    "lockout_threshold": {"required": 5, "recommended": 3, "standard": "等保2.0 / NIST SP 800-63B"},
    "lockout_duration_min": {"required": 30, "recommended": 60, "standard": "等保2.0"},
}


def audit_password_policy(policy_data):
    """审计密码策略合规性"""
    results = []
    compliance_score = 100

    # 最小长度
    min_len = policy_data.get("min_length", 0)
    if min_len >= POLICY_BASELINE["min_length"]["recommended"]:
        status = "✅ 合规（推荐级）"
        deduction = 0
    elif min_len >= POLICY_BASELINE["min_length"]["required"]:
        status = "🟡 合规（最低级，建议提升）"
        deduction = 10
    else:
        status = f"🔴 不合规（要求≥{POLICY_BASELINE['min_length']['required']}，当前{min_len}）"
        deduction = 25
    compliance_score -= deduction
    results.append({
        "item": "最小密码长度",
        "value": f"{min_len}字符",
        "required": f"≥{POLICY_BASELINE['min_length']['required']}",
        "recommended": f"≥{POLICY_BASELINE['min_length']['recommended']}",
        "status": status,
        "deduction": deduction,
        "standard": POLICY_BASELINE["min_length"]["standard"]
    })

    # 复杂度
    complexity = policy_data.get("complexity", {})
    comp_items = [
        ("require_upper", "大写字母", complexity.get("require_upper", False)),
        ("require_lower", "小写字母", complexity.get("require_lower", False)),
        ("require_digit", "数字", complexity.get("require_digit", False)),
        ("require_special", "特殊字符", complexity.get("require_special", False)),
    ]
    missing = []
    for key, label, enabled in comp_items:
        required = POLICY_BASELINE["complexity"][key]
        if required and not enabled:
            missing.append(label)
    if not missing:
        results.append({
            "item": "密码复杂度",
            "value": "全部启用",
            "required": "4项全启用",
            "status": "✅ 合规",
            "deduction": 0,
            "standard": POLICY_BASELINE["complexity"]["standard"]
        })
    else:
        deduction = len(missing) * 10
        compliance_score -= deduction
        results.append({
            "item": "密码复杂度",
            "value": f"缺少: {', '.join(missing)}",
            "required": "4项全启用",
            "status": f"🔴 不合规（缺少{len(missing)}项）",
            "deduction": deduction,
            "standard": POLICY_BASELINE["complexity"]["standard"]
        })

    # 密码最大使用期限
    max_age = policy_data.get("max_age_days", 0)
    if max_age == 0:
        status = "🔴 不合规（密码永不过期）"
        deduction = 20
    elif max_age <= POLICY_BASELINE["max_age_days"]["recommended"]:
        status = "✅ 合规（推荐级）"
        deduction = 0
    elif max_age <= POLICY_BASELINE["max_age_days"]["required"]:
        status = "🟡 合规（最低级）"
        deduction = 5
    else:
        status = f"🔴 不合规（要求≤{POLICY_BASELINE['max_age_days']['required']}天，当前{max_age}天）"
        deduction = 20
    compliance_score -= deduction
    results.append({
        "item": "密码最大使用期限",
        "value": f"{max_age}天" if max_age > 0 else "永不过期",
        "required": f"≤{POLICY_BASELINE['max_age_days']['required']}天",
        "recommended": f"≤{POLICY_BASELINE['max_age_days']['recommended']}天",
        "status": status,
        "deduction": deduction,
        "standard": POLICY_BASELINE["max_age_days"]["standard"]
    })

    # 密码历史记录
    history = policy_data.get("history_count", 0)
    if history >= POLICY_BASELINE["history_count"]["recommended"]:
        deduction = 0
        status = "✅ 合规（推荐级）"
    elif history >= POLICY_BASELINE["history_count"]["required"]:
        deduction = 5
        status = "🟡 合规（最低级）"
    else:
        deduction = 15
        status = f"🔴 不合规（要求≥{POLICY_BASELINE['history_count']['required']}，当前{history}）"
    compliance_score -= deduction
    results.append({
        "item": "密码历史记录",
        "value": f"记住{history}次",
        "required": f"≥{POLICY_BASELINE['history_count']['required']}次",
        "status": status,
        "deduction": deduction,
        "standard": POLICY_BASELINE["history_count"]["standard"]
    })

    # 锁定阈值
    lockout = policy_data.get("lockout_threshold", 0)
    if lockout == 0:
        deduction = 20
        status = "🔴 不合规（无锁定策略）"
    elif lockout <= POLICY_BASELINE["lockout_threshold"]["recommended"]:
        deduction = 0
        status = "✅ 合规（推荐级）"
    elif lockout <= POLICY_BASELINE["lockout_threshold"]["required"]:
        deduction = 5
        status = "🟡 合规（最低级）"
    else:
        deduction = 10
        status = f"🟠 偏松（推荐≤{POLICY_BASELINE['lockout_threshold']['recommended']}次）"
    compliance_score -= deduction
    results.append({
        "item": "账户锁定阈值",
        "value": f"{lockout}次失败后锁定" if lockout > 0 else "无锁定",
        "required": f"≤{POLICY_BASELINE['lockout_threshold']['required']}次",
        "status": status,
        "deduction": deduction,
        "standard": POLICY_BASELINE["lockout_threshold"]["standard"]
    })

    compliance_score = max(compliance_score, 0)

    if compliance_score >= 80:
        grade = "合规"
        emoji = "🟢"
    elif compliance_score >= 60:
        grade = "基本合规"
        emoji = "🟡"
    elif compliance_score >= 40:
        grade = "部分合规"
        emoji = "🟠"
    else:
        grade = "不合规"
        emoji = "🔴"

    return {
        "compliance_score": compliance_score,
        "grade": f"{emoji} {grade}",
        "results": results,
        "audited_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "standard": "等保2.0 / ISO 27001 / NIST SP 800-63B"
    }


# ============================================================
# 报告生成
# ============================================================

def generate_phishing_report(result):
    """生成钓鱼分析报告"""
    lines = [
        "🎣 钓鱼邮件分析报告",
        "━" * 30,
        "",
        f"📊 风险评分：{result['risk_score']}/100",
        f"📋 判定结果：{result['verdict']}",
        f"🕐 分析时间：{result['analyzed_at']}",
        "",
    ]
    if result["findings"]:
        lines.append("🔍 发现的风险特征：")
        for i, f in enumerate(result["findings"], 1):
            lines.append(f"  {i}. [{f['risk'].upper()}] {f['finding']}")
            lines.append(f"     详情：{f['detail']}")
            lines.append(f"     加分：+{f['score']}")
    else:
        lines.append("✅ 未发现明显钓鱼特征")

    lines.extend(["", "💡 建议："])
    if result["risk_score"] >= 61:
        lines.append("  🔴 请勿点击任何链接或下载附件！")
        lines.append("  🔴 将此邮件转发给IT安全团队处理")
        lines.append("  🔴 如已点击，立即修改相关账号密码")
    elif result["risk_score"] >= 31:
        lines.append("  🟡 暂勿操作，联系发件人确认邮件真实性")
        lines.append("  🟡 不要通过邮件中的链接登录任何账号")
    else:
        lines.append("  🟢 邮件看起来正常，但仍建议保持警惕")

    return "\n".join(lines)


def generate_policy_report(result):
    """生成密码策略审计报告"""
    lines = [
        "🔐 密码策略合规审计报告",
        "━" * 30,
        "",
        f"📊 合规评分：{result['grade']}（{result['compliance_score']}/100）",
        f"📋 审计标准：{result['standard']}",
        f"🕐 审计时间：{result['audited_at']}",
        "",
        "📋 审计详情：",
    ]
    for r in result["results"]:
        lines.append(f"")
        lines.append(f"  ▸ {r['item']}")
        lines.append(f"    当前值：{r['value']}")
        lines.append(f"    要求：{r['required']}")
        if "recommended" in r:
            lines.append(f"    推荐：{r['recommended']}")
        lines.append(f"    状态：{r['status']}")
        lines.append(f"    依据：{r['standard']}")

    lines.extend(["", "💡 改进建议："])
    for r in result["results"]:
        if "🔴" in r["status"] or "🟠" in r["status"]:
            lines.append(f"  • {r['item']}：请按标准要求调整（{r['required']}）")

    return "\n".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="企业安全审计工具")
    subparsers = parser.add_subparsers(dest="command", help="审计模块")

    # 钓鱼检测子命令
    phish_parser = subparsers.add_parser("phishing", help="钓鱼邮件识别")
    phish_parser.add_argument("--url", help="可疑URL")
    phish_parser.add_argument("--sender", help="发件人邮箱")
    phish_parser.add_argument("--body", help="邮件正文（用引号包裹）")

    # 密码策略审计子命令
    policy_parser = subparsers.add_parser("password-policy", help="密码策略合规审计")
    policy_parser.add_argument("--input", help="密码策略JSON文件路径")
    policy_parser.add_argument("--min-length", type=int, default=0, help="最小密码长度")
    policy_parser.add_argument("--max-age", type=int, default=0, help="密码最大使用天数")
    policy_parser.add_argument("--history", type=int, default=0, help="密码历史记录次数")
    policy_parser.add_argument("--lockout", type=int, default=0, help="账户锁定阈值")

    # 综合审计子命令
    full_parser = subparsers.add_parser("full-audit", help="综合安全审计")
    full_parser.add_argument("--email", help="邮箱地址（用于泄露检查）")
    full_parser.add_argument("--url", help="可疑URL")
    full_parser.add_argument("--sender", help="发件人邮箱")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "phishing":
        if not any([args.url, args.sender, args.body]):
            print("⚠️ 请提供至少一个参数: --url, --sender, --body")
            return
        result = analyze_phishing(url=args.url, sender=args.sender, body=args.body)
        print(generate_phishing_report(result))

    elif args.command == "password-policy":
        policy_data = {}
        if args.input:
            try:
                with open(args.input, "r", encoding="utf-8") as f:
                    policy_data = json.load(f)
            except Exception as e:
                print(f"⚠️ 读取策略文件失败: {e}")
                return
        else:
            policy_data = {
                "min_length": args.min_length,
                "max_age_days": args.max_age,
                "history_count": args.history,
                "lockout_threshold": args.lockout,
                "complexity": {
                    "require_upper": True,
                    "require_lower": True,
                    "require_digit": True,
                    "require_special": False,
                }
            }
        result = audit_password_policy(policy_data)
        print(generate_policy_report(result))

    elif args.command == "full-audit":
        lines = ["🏢 企业综合安全审计报告", "━" * 40, ""]

        if args.url or args.sender:
            lines.append("━━ 钓鱼邮件分析 ━━")
            result = analyze_phishing(url=args.url, sender=args.sender)
            lines.append(generate_phishing_report(result))
            lines.append("")

        print("\n".join(lines))


if __name__ == "__main__":
    main()
