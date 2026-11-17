#!/usr/bin/env python3
"""
iec62304-sdlc-check — IEC 62304 软件生命周期检查。
检查软件生命周期文件有没有覆盖 IEC 62304:2006/AMD1:2015 的关键阶段。
"""
import re
import sys
from pathlib import Path


# IEC 62304 关键阶段 + 建议
REQUIRED_PHASES = {
    "软件需求分析（Software Requirements）": {
        "keywords": ["software requirements", "软件需求", "需求规格"],
        "suggestion": "应该写：软件要实现什么功能、性能要求、接口要求"
    },
    "软件架构设计（Software Architecture）": {
        "keywords": ["software architecture", "软件架构", "体系结构"],
        "suggestion": "应该写：软件分几个模块、模块之间怎么交互、分层结构"
    },
    "软件详细设计（Detailed Design）": {
        "keywords": ["detailed design", "详细设计", "模块设计"],
        "suggestion": "应该写：每个模块的内部设计、数据结构、算法"
    },
    "软件单元实现（Unit Implementation）": {
        "keywords": ["unit implementation", "单元实现", "编码"],
        "suggestion": "应该写：代码怎么写的、用什么编程语言、编码规范"
    },
    "软件单元验证（Unit Verification）": {
        "keywords": ["unit verification", "单元验证", "单元测试"],
        "suggestion": "应该写：每个单元怎么测试的、测试用例、通过率"
    },
    "软件集成（Integration）": {
        "keywords": ["software integration", "软件集成", "集成测试"],
        "suggestion": "应该写：模块怎么集成的、集成测试怎么做的"
    },
    "软件系统测试（System Testing）": {
        "keywords": ["system testing", "系统测试", "确认测试"],
        "suggestion": "应该写：整个系统怎么测试的、测试环境、测试结果"
    },
    "软件发布（Release）": {
        "keywords": ["software release", "软件发布", "版本发布"],
        "suggestion": "应该写：版本号、发布日期、发布说明、回滚方案"
    },
    "风险管理（Risk Management）": {
        "keywords": ["risk management", "风险管理", "风险分析"],
        "suggestion": "应该写：软件相关的风险有哪些、怎么控制的"
    },
    "可追溯性（Traceability）": {
        "keywords": ["traceability", "可追溯", "追溯矩阵"],
        "suggestion": "应该写：需求→设计→代码→测试的追溯矩阵"
    },
}


def check_sdlc_file(filepath: str) -> list:
    """检查软件生命周期文件。"""
    content = Path(filepath).read_text(encoding="utf-8").lower()

    findings = []

    for phase, info in REQUIRED_PHASES.items():
        found = any(kw.lower() in content for kw in info["keywords"])
        if not found:
            findings.append({
                "phase": phase,
                "severity": "MEDIUM",
                "message": f"缺少 {phase}",
                "suggestion": info["suggestion"]
            })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python iec62304_sdlc_check.py <软件生命周期文件>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_sdlc_file(filepath)

    if not findings:
        print("✅ 软件生命周期文件覆盖完整！")
        sys.exit(0)

    print(f"发现 {len(findings)} 个缺失：")
    for f in findings:
        print(f"  [{f['severity']}] {f['message']}")
        print(f"    💡 建议: {f['suggestion']}")

    print(f"\n  覆盖率: {len(REQUIRED_PHASES) - len(findings)}/{len(REQUIRED_PHASES)}")

    sys.exit(1 if len(findings) > 4 else 0)


if __name__ == "__main__":
    main()
