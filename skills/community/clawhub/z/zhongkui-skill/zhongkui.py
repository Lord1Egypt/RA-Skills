#!/usr/bin/env python3
"""钟馗 Skill 安全审查引擎 - 主入口

用法:
    python zhongkui.py <skill目录路径> [--quick] [--update]

    --quick   仅执行 Layer 1 静态审计（秒级完成）
    --update  预览漏洞库增量，交互确认后注入（默认不自动升级）
    --apply   配合 --update 使用，跳过确认直接注入
    --dry-run 配合 --update 使用，仅预览不注入
"""

import sys
import os
from pathlib import Path

# 将当前目录加入路径以便导入 core 子模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.auditor import Auditor
from core.scorer import Scorer
from core.intel.updater import run_update


def main():
    args = sys.argv[1:]
    update_mode = "--update" in args
    quick_mode = "--quick" in args
    dry_run = "--dry-run" in args
    auto_apply = "--apply" in args

    # 传入参数（去掉标志位）
    paths = [a for a in args if not a.startswith("--")]
    
    # --update 单独运行（无审查目标）
    if update_mode and not paths:
        print("钟馗漏洞库更新")
        print("=" * 50)
        result = run_update(dry_run=True)  # 先干跑
        print("=" * 50)
        print(f"拉取 {result['fetched']} → 过滤 {result['filtered']} → 生成 {result['generated']} 条候选签名")
        
        if result['generated'] == 0:
            print("无新增签名，漏洞库已是最新。")
            return
        
        if dry_run:
            print("干跑模式，未实际注入。加 --apply 确认注入。")
            return
        
        if auto_apply:
            print("--apply 模式，直接注入 ...")
        else:
            print()
            try:
                choice = input("是否注入以上签名？[y/N] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("已取消。")
                return
            if choice not in ("y", "yes"):
                print("已取消。如需注入请加 --apply 参数。")
                return
        
        # 真正注入
        result = run_update(dry_run=False)
        print("=" * 50)
        print(f"已注入 {result['injected']} 条新签名")
        for cat, n in result.get('by_category', {}).items():
            print(f"  {cat}: +{n}")
        print("漏洞库已更新。")
        return

    if not paths:
        print("用法: python zhongkui.py <skill目录路径> [--quick] [--update] [--apply] [--dry-run]")
        print()
        print("示例:")
        print("  python zhongkui.py ./my-skill")
        print("  python zhongkui.py ./my-skill --quick")
        print("  python zhongkui.py ./my-skill --update          # 预览+确认后注入+审查")
        print("  python zhongkui.py ./my-skill --update --apply  # 直接注入+审查")
        print("  python zhongkui.py --update                     # 仅预览并确认更新漏洞库")
        print("  python zhongkui.py --update --dry-run           # 仅预览不注入")
        print("  python zhongkui.py --update --apply             # 直接更新漏洞库")
        sys.exit(1)
    
    target_path = Path(paths[0]).resolve()
    
    if not target_path.exists():
        print(f"错误: 路径不存在 - {target_path}")
        sys.exit(1)
    
    if not target_path.is_dir():
        print(f"错误: 不是目录 - {target_path}")
        sys.exit(1)
    
    # --update：审查前先预览并确认更新漏洞库
    if update_mode:
        print(">>> 检查漏洞库更新 ...")
        result = run_update(dry_run=True)
        if result['generated']:
            print(f">>> 发现 {result['generated']} 条候选签名（拉取 {result['fetched']} / 过滤 {result['filtered']}）")
            if dry_run:
                print(">>> 干跑模式，跳过注入，继续审查\n")
            elif auto_apply:
                result = run_update(dry_run=False)
                print(f">>> 已注入 {result['injected']} 条新签名\n")
            else:
                try:
                    choice = input(">>> 是否注入以上签名？[y/N] ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    print(">>> 已取消注入，继续审查\n")
                else:
                    if choice in ("y", "yes"):
                        result = run_update(dry_run=False)
                        print(f">>> 已注入 {result['injected']} 条新签名\n")
                    else:
                        print(">>> 跳过注入，继续审查（加 --apply 可跳过确认）\n")
        else:
            print(">>> 签名库已是最新\n")
    
    # 执行 Layer 1 静态审计
    auditor = Auditor(target_path)
    if quick_mode:
        auditor._load_files()
        auditor._check_metadata()
        auditor._check_skill_content()
        auditor.checks_skipped = 30  # S1-S12(12) + P1-P11(11) + D1-D7(7)
        auditor._gen_summary()
    else:
        auditor.run_full()
    
    # 评分
    scorer = Scorer()
    final_score, verdict, flags = scorer.compute(auditor, l3_penalty=0)
    
    # 输出报告
    print_report(auditor, final_score, verdict, flags, quick_mode, update_mode)


def print_report(audit, score, verdict, flags, quick_mode, update_mode=False):
    """输出 Markdown 格式审查报告 —— 与 SKILL.md 强制输出格式一致"""
    icon_map = {"clean": "✅", "suspicious_low": "⚠️", "suspicious_high": "⚠️", "malicious": "🚫"}
    icon = icon_map.get(verdict, "❓")
    
    print(f"## 钟馗裁定：[{icon}]")
    print(f"**总分**：{score} / 100")
    print(f"**一句话**：{audit.summary}")
    print()
    
    # 一票否决判定
    veto_hits = audit.get_veto_hits()
    if veto_hits:
        print("### 🚫 一票否决项（命中即判恶）")
        print("| 红线 | 命中内容 | 文件:行号 |")
        print("|:---|:---|:---|")
        for v in veto_hits:
            content = v['content'][:60]
            print(f"| {v['rule']} | {content} | {v['file']}:L{v['line']} |")
        print()
        print("> 命中一票否决项，直接裁定 🚫 恶意。修复后方可重新审查。")
        print()
        return
    
    # 即时拒绝红线
    redline_hits = audit.get_redline_hits()
    if redline_hits:
        print("### 🔴 即时拒绝红线")
        print("| 红线 | 命中内容 | 文件:行号 |")
        print("|:---|:---|:---|")
        for r in redline_hits:
            print(f"| {r['rule']} | {r['content']} | {r['file']}:L{r['line']} |")
        print()
        print("> 命中即时拒绝红线，直接裁定 🚫 恶意。修复后方可重新审查。")
        print()
        return
    
    # 扣分项
    deductions = audit.get_deductions()
    if deductions:
        print("### 扣分项")
        print("| 层级 | 检查项 | 风险类型 | 扣分 | 命中内容（行号） |")
        print("|:---|:---|:---|:---|:---|")
        for d in deductions:
            content = d.get('content', '')[:50]
            line_info = f"{d['file']}:L{d['line']}" if d.get('line') else d['file']
            print(f"| L1 | {d['check']} | {d['risk']} | -{d['points']} | {line_info} |")
        print()
    
    # 审计覆盖统计
    stats = audit.get_stats()
    print("### 审计覆盖")
    print(f"- 文件数：{stats['files_scanned']}")
    print(f"- 检查项：{stats['checks_total']}（命中 {stats['checks_hit']}，通过 {stats['checks_pass']}）")
    print()
    
    # 模式标识
    if quick_mode:
        print("> 模式：快速审计（仅 Layer 1）。完整审计请去掉 --quick 参数。")
    if update_mode:
        print("> 模式：已启用漏洞库更新。本次审查基于最新漏洞库。" if not quick_mode else "")
    
    # 结论
    print(f"> 审查完成。裁定：{icon} {verdict.upper()}")


if __name__ == "__main__":
    main()
