#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自我进化系统一键安装脚本
运行后自动完成：
1. 创建目录结构
2. 复制脚本到 ~/.qclaw/workspace/scripts/
3. 初始化 .learnings/ 档案
4. 注册 cron 定时任务（每3天运行 SEA 进化扫描）

使用方式:
    python install_self_evolver.py
"""

import os
import sys
import shutil
import platform

def _resolve_workspace():
    return os.path.expanduser(os.environ.get("QW_WORKSPACE", "~/.qclaw/workspace"))

WORKSPACE     = _resolve_workspace()
SCRIPTS_DIR   = os.path.join(WORKSPACE, "scripts")
LEARNINGS_DIR = os.path.join(WORKSPACE, ".learnings")

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def copy_scripts():
    """将 scripts/ 目录复制到工作区"""
    src_dir = os.path.join(os.path.dirname(__file__))
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    scripts_to_copy = [
        "sea_evolve.py",
        "auto_learn.py",
        "skill_evolution.py",
        "skill_metrics.py",
    ]

    copied = []
    for s in scripts_to_copy:
        src = os.path.join(src_dir, s)
        dst = os.path.join(SCRIPTS_DIR, s)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied.append(s)
            print(f"  ✅ {s}")
        else:
            print(f"  ⚠️  {s} 未找到，跳过")

    return copied

def init_learnings():
    """初始化 .learnings/ 目录"""
    os.makedirs(LEARNINGS_DIR, exist_ok=True)

    files = {
        "LEARNINGS.md": """| 时间 | 错误做法 | 正确做法 | 区域 | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

<!-- 新记录会自动追加到这里 -->
""",
        "ERRORS.md": """| 时间 | 命令 | 错误 | 影响 |
| --- | --- | --- | --- |
| | | | |

<!-- 格式：时间|失败的命令|错误信息|造成的影响 -->
""",
        "FEATURE_REQUESTS.md": """| 时间 | 请求 | 状态 | 优先级 |
| --- | --- | --- | --- |
| | | | |
""",
        "pending.md": "",  # 空文件，心跳时处理
    }

    for fname, content in files.items():
        path = os.path.join(LEARNINGS_DIR, fname)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ {fname}")
        else:
            print(f"  ℹ️  {fname} 已存在，跳过")

def init_skill_metrics():
    """初始化技能指标文件"""
    metrics_file = os.path.join(WORKSPACE, "skill_metrics.json")
    if not os.path.exists(metrics_file):
        with open(metrics_file, "w", encoding="utf-8") as f:
            f.write("{}\n")
        print(f"  ✅ skill_metrics.json")

def register_cron():
    """注册每3天运行 SEA 进化的定时任务"""
    try:
        from openclaw.cron import CronManager
        import os

        # 检测是否是 openclaw 环境
        try:
            import openclaw
        except ImportError:
            print("  ℹ️  openclaw 模块不可用，跳过 cron 注册")
            print("     请手动添加 cron 任务：")
            print("     openclaw cron add --name 'SEA-Evolution' --every 3days")
            return

        cm = CronManager()
        job = {
            "name": "SEA-Evolution-Scan",
            "schedule": {"kind": "every", "everyMs": 3 * 24 * 60 * 60 * 1000},
            "payload": {
                "kind": "agentTurn",
                "message": "运行自我进化：python ~/.qclaw/workspace/scripts/sea_evolve.py --quiet",
            },
            "sessionTarget": "isolated",
            "enabled": True,
        }
        # 检查是否已存在
        existing = [j for j in cm.list() if j.get("name") == "SEA-Evolution-Scan"]
        if existing:
            print("  ℹ️  cron 任务已存在，跳过")
        else:
            cm.add(job)
            print("  ✅ cron 任务已注册（每3天运行）")
    except Exception as e:
        print(f"  ℹ️  cron 注册失败（非致命）：{e}")
        print("     请手动添加：每3天运行 python ~/.qclaw/workspace/scripts/sea_evolve.py --quiet")

def main():
    print("=" * 50)
    print("🌱 Self Evolver 安装程序")
    print("=" * 50)
    print(f"\n工作区：{WORKSPACE}")
    print(f"系统：{platform.system()}")

    print("\n📁 复制核心脚本...")
    copied = copy_scripts()

    print("\n📚 初始化学习档案...")
    init_learnings()

    print("\n📊 初始化技能指标...")
    init_skill_metrics()

    print("\n⏰ 注册定时任务...")
    register_cron()

    print("\n" + "=" * 50)
    print("✅ 安装完成！")
    print("=" * 50)
    print()
    print("下一步：")
    print("1. 重启 OpenClaw 使 cron 生效")
    print("2. 说「安装自我进化」或「我有自我进化能力了吗」验证")
    print("3. 被纠正时自动记录到 pending.md")
    print()
    print("手动测试：")
    print("  python ~/.qclaw/workspace/scripts/sea_evolve.py")
    print("  python ~/.qclaw/workspace/scripts/auto_learn.py --status")

if __name__ == "__main__":
    main()
