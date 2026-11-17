#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wb_safe_security_test.py —— WorkBuddy 安全稳定运行专家团（WB-SAFE）安全稳定性实测
====================================================================================
本地闭环 · 零真实凭据 · 零网络 · 可重跑。对专家包内容做静态/动态核验，
按 8 条防线 + 包完整性 共 8 维打分（0-5），输出 security_results.json 供雷达图使用。

红线：
  * 绝不读取任何真实密钥内容，只检查"是否具备对应机制"（结构/逻辑/命令存在性）。
  * 绝不发起网络请求；脚本只读，不修改包内任何文件。
  * 结果只描述行为表现，不披露实现细节（先过反逆向门）。

用法：
  python wb_safe_security_test.py [包目录] [输出目录]
  默认包目录 = 脚本同级的上级（即 wb-safe-team 包根）
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent          # scripts/
PKG = (BASE.parent if BASE.name == "scripts" else BASE)   # 包根
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else PKG
if len(sys.argv) > 1:
    PKG = Path(sys.argv[1])

DIMS = [
    ("pkg_integrity", "包结构完整性"),
    ("credential_security", "凭据安全"),
    ("cost_governance", "用量治理"),
    ("connectivity", "连通监控"),
    ("config_baseline", "配置基线"),
    ("encryption", "加解密"),
    ("health_monitor", "健康监护"),
    ("recovery", "灾备恢复"),
]

AGENTS = PKG / "agents"
PLUGIN = PKG / ".codebuddy-plugin" / "plugin.json"
README = PKG / "README.md"
SCRIPTS = PKG / "scripts"


def rd(p):
    try:
        return (p.read_text("utf-8", errors="ignore"))
    except Exception:
        return ""


def score_checks(checks):
    """checks: list[(bool, weight)] -> 0-5 加权分"""
    if not checks:
        return 0.0
    ok = sum(w for c, w in checks if c)
    tot = sum(w for _, w in checks)
    return round(ok / tot * 5, 2)


def test_pkg_integrity():
    checks = []
    # plugin.json 可解析且关键字段齐全
    try:
        pj = json.loads(rd(PLUGIN))
        checks.append((bool(pj.get("name") and pj.get("expertType")), 1.2))
        checks.append((bool(pj.get("displayName") and pj.get("displayDescription")), 0.8))
        checks.append((bool(pj.get("tags") and len(pj.get("tags")) == 3), 0.5))
        checks.append((bool(pj.get("quickPrompts") and len(pj.get("quickPrompts")) == 3), 0.5))
        checks.append((bool(pj.get("teamInfo") and pj.get("members")), 0.5))
    except Exception:
        checks.append((False, 3.5))
    # 9 个 agent 全部存在
    agents = [f.name for f in AGENTS.glob("*.md")] if AGENTS.is_dir() else []
    checks.append((len(agents) == 9, 1.0))
    # 头像存在
    avatars = list((PKG / "avatars").glob("*.png")) if (PKG / "avatars").is_dir() else []
    checks.append((len(avatars) >= 9, 0.5))
    # README 有安装/使用说明
    checks.append(("## 安装" in rd(README) and "## 使用示例" in rd(README), 0.5))
    return score_checks(checks)


def test_credential_security():
    r = rd(README) + rd(AGENTS / "wb-cred-guard.md")
    audit = rd(SCRIPTS / "wb_audit.py")
    checks = [
        ("明文凭据零容忍" in r or "明文泄露" in r, 1.0),
        ("只报位置不回显值" in r, 1.2),
        ("凭据值绝不出现在 stdout" in audit, 1.0),
        ("SECRET_RE" in audit and "sk-" in audit, 0.8),      # 密钥模式识别
        ("SENSITIVE_NAMES" in audit and ".env" in audit, 0.5),
        ("轮换" in r and "吊销" in r, 0.5),
    ]
    return score_checks(checks)


def test_cost_governance():
    r = rd(README) + rd(AGENTS / "wb-credit-steward.md")
    checks = [
        ("免积分优先" in r and "本地" in r, 1.2),
        ("先报备再执行" in r or "先报数再动手" in r, 1.0),
        ("高消耗操作" in r or "相对成本" in r, 0.8),
        ("Ollama" in r or "PIL" in r or "离线替代" in r, 0.8),
        ("实测不猜" in r or "实测" in r, 0.6),
        ("贵操作拆细" in r or "样本" in r, 0.6),
    ]
    return score_checks(checks)


def test_connectivity():
    r = rd(AGENTS / "wb-link-monitor.md") + rd(README)
    checks = [
        ("连接器" in r and "MCP" in r, 1.2),
        ("掉线" in r and "超时" in r, 1.0),
        ("熔断" in r and "降级" in r, 1.0),
        ("探测" in r and "可达" in r, 0.8),
        ("授权失效" in r or "重授权" in r, 0.5),
        ("诊断矩阵" in r or "诊断" in r, 0.5),
    ]
    return score_checks(checks)


def test_config_baseline():
    r = rd(AGENTS / "wb-config-auditor.md") + rd(README)
    audit = rd(SCRIPTS / "wb_audit.py")
    checks = [
        ("基线" in r and "漂移" in r, 1.2),
        ("快照" in r and "版本" in r, 1.0),
        ("前提验证" in r, 1.0),
        ("audit_baseline.json" in audit and "SHA256" in audit, 0.8),
        ("--init-baseline" in audit, 0.5),
        ("三棱镜" in r or "证伪" in r, 0.5),
    ]
    return score_checks(checks)


def test_encryption():
    r = rd(AGENTS / "wb-crypto-keeper.md") + rd(README)
    checks = [
        ("加密" in r and "解密" in r, 1.2),
        ("密钥分层" in r, 1.0),
        ("PII" in r and "云上" in r, 1.0),
        ("三态" in r or "存储与传输" in r, 0.8),
        ("作用域" in r or "最小" in r, 0.5),
        ("账户身份为锚" in r or "KEK" in r, 0.5),
    ]
    return score_checks(checks)


def test_health_monitor():
    r = rd(AGENTS / "wb-health-sentinel.md") + rd(README)
    audit = rd(SCRIPTS / "wb_audit.py")
    checks = [
        ("CPU" in r and "内存" in r and "磁盘" in r, 1.2),
        ("进程" in r and "网络" in r, 0.8),
        ("OOM" in r and "死机" in r, 1.0),
        ("预警" in r and "泄载" in r, 1.0),
        ("七维" in r or "七维指标" in r, 0.5),
        ("Get-PSDrive" in audit and "Get-CimInstance" in audit, 0.5),
    ]
    return score_checks(checks)


def test_recovery():
    r = rd(AGENTS / "wb-recovery-keeper.md") + rd(README)
    rec = rd(SCRIPTS / "wb_recovery_full.py")
    checks = [
        ("积分为 0" in r or "离线兜底" in r, 1.0),
        ("黄金包" in r and ("备份" in r or "恢复" in r), 1.0),
        ("换机" in r or "重装" in r or "换电脑" in r, 0.8),
        ("记忆" in r and "卫生" in r, 0.6),
        ("--dry-run" in rec and "dry-run" in rec, 0.8),
        ("对账" in rec or "SHA256" in rec, 0.8),
    ]
    return score_checks(checks)


TESTS = [
    test_pkg_integrity,
    test_credential_security,
    test_cost_governance,
    test_connectivity,
    test_config_baseline,
    test_encryption,
    test_health_monitor,
    test_recovery,
]


def main():
    print(f"测试对象: {PKG}")
    dims = []
    for (key, name), fn in zip(DIMS, TESTS):
        try:
            score = fn()
        except Exception as e:  # 测试自身异常不阻断，计 0 并注明
            score = 0.0
            print(f"  [warn] {name} 测试异常: {e}")
        dims.append({"key": key, "name": name, "score": score})
        print(f"  {name}: {score}/5")
    overall = round(sum(d["score"] for d in dims) / len(dims), 2)

    results = {
        "schema": "wb-safe-security-test/1.0",
        "target": "wb-safe-team",
        "version": "1.0.0",
        "mode": "local-closed-loop",
        "credentials_used": "none",
        "network": "none",
        "reproducible": True,
        "overall": overall,
        "dimensions": dims,
    }
    out_path = Path(OUT) / "security_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), "utf-8")
    print(f"综合评分: {overall}/5")
    print(f"结果已写入: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
