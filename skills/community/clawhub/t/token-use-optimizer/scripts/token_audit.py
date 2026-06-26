#!/usr/bin/env python3
"""
Token Audit Tool — AI Agent 项目 Token 消耗自动审计
=================================================
扫描 Rules、Memory、Knowledge 文件，估算每轮对话的固定 token 开销，
输出分层诊断报告和优化建议。

使用方法:
  python3 scripts/token_audit.py [项目根目录]
  python3 scripts/token_audit.py [项目根目录] --json
  python3 scripts/token_audit.py [项目根目录] --knowledge-dir /path/to/knowledge

选项:
  --json              输出 JSON 格式报告
  --knowledge-dir DIR 自定义知识库目录路径（默认自动探测常见位置）
  -h, --help          显示帮助信息
"""

import os
import sys
import json
import glob
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


# ── Token 估算常量 ──────────────────────────────────────

CHARS_PER_TOKEN_ZH = 1.3   # 中文约 1.3 字符/token
CHARS_PER_TOKEN_EN = 4.0   # 英文约 4 字符/token
MIXED_RATIO = 0.6           # 假设中英混合比（60% 中文）
SYSTEM_PROMPT_OVERHEAD = 2000  # 平台 system prompt 固定开销估算


# ── 数据结构 ──────────────────────────────────────────

@dataclass
class FileAudit:
    """单个文件的审计结果"""
    path: str
    name: str
    lines: int
    chars: int
    estimated_tokens: int
    category: str  # always-rule, requestable-rule, memory, knowledge, skill
    issues: list = field(default_factory=list)


@dataclass 
class AuditReport:
    """完整审计报告"""
    project_root: str
    always_rules: list = field(default_factory=list)
    requestable_rules: list = field(default_factory=list)
    memories: list = field(default_factory=list)
    knowledge_files: list = field(default_factory=list)
    
    # 汇总
    total_always_tokens: int = 0
    total_memory_tokens: int = 0
    total_per_round: int = 0
    total_per_10_rounds: int = 0
    
    issues: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)


# ── 工具函数 ──────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """估算文本的 token 数"""
    if not text:
        return 0
    # 简单启发：统计中文字符占比
    zh_chars = len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', text))
    total_chars = len(text)
    if total_chars == 0:
        return 0
    zh_ratio = zh_chars / total_chars
    
    # 混合计算
    zh_tokens = zh_chars / CHARS_PER_TOKEN_ZH
    en_chars = total_chars - zh_chars
    en_tokens = en_chars / CHARS_PER_TOKEN_EN
    
    return int(zh_tokens + en_tokens)


def parse_mdc_frontmatter(content: str) -> dict:
    """解析 .mdc 文件的 frontmatter"""
    result = {'alwaysApply': False, 'description': ''}
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            for line in frontmatter.strip().split('\n'):
                if ':' in line:
                    key, _, value = line.partition(':')
                    key = key.strip()
                    value = value.strip()
                    if key == 'alwaysApply':
                        result['alwaysApply'] = value.lower() == 'true'
                    elif key == 'description':
                        result['description'] = value
                    elif key == 'enabled':
                        result['enabled'] = value.lower() == 'true'
    
    return result


def read_file_safe(path: str) -> str:
    """安全读取文件"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return ''


# ── 扫描函数 ──────────────────────────────────────────

def scan_rules(project_root: str) -> tuple:
    """扫描 .codebuddy/rules/ 下的所有规则文件"""
    always_rules = []
    requestable_rules = []
    
    rules_dir = os.path.join(project_root, '.codebuddy', 'rules')
    if not os.path.exists(rules_dir):
        return always_rules, requestable_rules
    
    for mdc_file in glob.glob(os.path.join(rules_dir, '**', '*.mdc'), recursive=True):
        content = read_file_safe(mdc_file)
        if not content:
            continue
        
        meta = parse_mdc_frontmatter(content)
        lines = content.count('\n') + 1
        tokens = estimate_tokens(content)
        rel_path = os.path.relpath(mdc_file, project_root)
        name = os.path.basename(mdc_file).replace('.mdc', '')
        
        issues = []
        
        # 检查：过长规则
        if lines > 150:
            issues.append(f"⚠️ 规则过长（{lines} 行 > 150 行阈值），建议拆分")
        
        # 检查：always-on 但可能可以降级
        if meta.get('alwaysApply'):
            if not meta.get('description'):
                issues.append("💡 缺少 description 字段（降级为 requestable 时必需）")
        
        audit = FileAudit(
            path=rel_path,
            name=name,
            lines=lines,
            chars=len(content),
            estimated_tokens=tokens,
            category='always-rule' if meta.get('alwaysApply') else 'requestable-rule',
            issues=issues
        )
        
        if meta.get('alwaysApply'):
            always_rules.append(audit)
        else:
            requestable_rules.append(audit)
    
    return always_rules, requestable_rules


def scan_knowledge(project_root: str, custom_knowledge_dir: Optional[str] = None) -> list:
    """扫描知识库入口文件。支持自定义知识库路径或自动探测常见位置。"""
    knowledge_files = []
    
    # 知识库路径：优先使用用户指定，否则自动探测常见位置
    if custom_knowledge_dir:
        knowledge_dirs = [os.path.abspath(custom_knowledge_dir)]
    else:
        knowledge_dirs = [
            os.path.join(project_root, 'knowledge'),
            os.path.join(project_root, 'docs', 'knowledge'),
            os.path.join(project_root, 'openclaw-workspace', 'knowledge'),
        ]
    
    # 只扫描入口文件（路由表/索引）
    entry_patterns = ['KNOWLEDGE-MAP*', 'CROSS-DOMAIN*', 'BOOK-INDEX*', 'INDEX*', 'README*']
    
    for kdir in knowledge_dirs:
        if not os.path.exists(kdir):
            continue
        
        # 先扫描入口文件
        for pattern in entry_patterns:
            for f in glob.glob(os.path.join(kdir, pattern)):
                content = read_file_safe(f)
                lines = content.count('\n') + 1
                tokens = estimate_tokens(content)
                rel_path = os.path.relpath(f, project_root)
                
                issues = []
                if lines > 300:
                    issues.append(f"⚠️ 入口文件过大（{lines} 行），建议拆分为路由表+详细文件")
                
                knowledge_files.append(FileAudit(
                    path=rel_path,
                    name=os.path.basename(f),
                    lines=lines,
                    chars=len(content),
                    estimated_tokens=tokens,
                    category='knowledge',
                    issues=issues
                ))
        
        # 统计总体规模
        all_md = glob.glob(os.path.join(kdir, '**', '*.md'), recursive=True)
        if all_md and not knowledge_files:
            total_lines = 0
            for f in all_md:
                content = read_file_safe(f)
                total_lines += content.count('\n') + 1
            knowledge_files.append(FileAudit(
                path=os.path.relpath(kdir, project_root),
                name=f"知识库总计（{len(all_md)} 个文件）",
                lines=total_lines,
                chars=0,
                estimated_tokens=0,
                category='knowledge-summary',
                issues=[f"ℹ️ 共 {len(all_md)} 个知识文件，{total_lines} 行"]
            ))
    
    return knowledge_files


def count_memories_estimate(project_root: str) -> int:
    """估算 Memory 条目的 token 消耗（无法直接读取 update_memory 内容）"""
    # Memory 条目存在 CodeBuddy 内部，无法直接扫描
    # 但可以从 MEMORY.md 和 daily logs 估算
    memory_tokens = 0
    
    memory_md = os.path.join(project_root, '.codebuddy', 'MEMORY.md')
    if os.path.exists(memory_md):
        content = read_file_safe(memory_md)
        memory_tokens += estimate_tokens(content)
    
    return memory_tokens


# ── 报告生成 ──────────────────────────────────────────

def generate_report(project_root: str, knowledge_dir: Optional[str] = None) -> AuditReport:
    """生成完整审计报告"""
    report = AuditReport(project_root=project_root)
    
    # L1: Rules
    report.always_rules, report.requestable_rules = scan_rules(project_root)
    
    # L3: Knowledge
    report.knowledge_files = scan_knowledge(project_root, knowledge_dir)
    
    # 汇总 always-on 开销
    report.total_always_tokens = sum(r.estimated_tokens for r in report.always_rules)
    
    # 估算 memory 开销（提示用户手动确认）
    memory_file_tokens = count_memories_estimate(project_root)
    report.total_memory_tokens = memory_file_tokens
    
    # 每轮固定开销
    report.total_per_round = (
        SYSTEM_PROMPT_OVERHEAD 
        + report.total_always_tokens
        + report.total_memory_tokens
    )
    report.total_per_10_rounds = report.total_per_round * 10
    
    # 生成建议
    if report.total_always_tokens > 5000:
        report.suggestions.append(
            "🔴 Always-on Rules 开销过高（>{:,} tokens），建议审查是否有规则可降级为 requestable".format(
                report.total_always_tokens
            )
        )
    
    always_count = len(report.always_rules)
    if always_count > 5:
        report.suggestions.append(
            f"🟡 Always-on Rules 数量较多（{always_count} 条），建议只保留身份铁律类规则"
        )
    
    long_rules = [r for r in report.always_rules if r.lines > 120]
    if long_rules:
        for r in long_rules:
            report.suggestions.append(
                f"🟡 规则 `{r.name}` 有 {r.lines} 行，建议拆分（核心留 rule，详细内容移到 references/）"
            )
    
    # 汇总所有 issues
    for r in report.always_rules + report.requestable_rules + report.knowledge_files:
        report.issues.extend(r.issues)
    
    return report


def print_report(report: AuditReport):
    """打印彩色报告"""
    print("\n" + "=" * 60)
    print("  🔍 Token 消耗审计报告")
    print("=" * 60)
    print(f"\n📁 项目: {report.project_root}\n")
    
    # ── L1: Rules ──
    print("─" * 40)
    print("📋 L1: Rules 层")
    print("─" * 40)
    
    print(f"\n  Always-on Rules ({len(report.always_rules)} 条):")
    for r in sorted(report.always_rules, key=lambda x: -x.estimated_tokens):
        marker = " ⚠️" if r.issues else ""
        print(f"    {r.name:<35} {r.lines:>5} 行  ~{r.estimated_tokens:>5} tokens{marker}")
    
    print(f"\n  Requestable Rules ({len(report.requestable_rules)} 条):")
    for r in report.requestable_rules:
        print(f"    {r.name:<35} {r.lines:>5} 行  (按需加载)")
    
    print(f"\n  📊 Always-on Rules 小计: ~{report.total_always_tokens:,} tokens/轮")
    
    # ── L2: Memory ──
    print(f"\n{'─' * 40}")
    print("🧠 L2: Memory 层")
    print("─" * 40)
    print(f"\n  MEMORY.md 估算: ~{report.total_memory_tokens:,} tokens")
    print("  ⚠️ update_memory 条目无法直接扫描，请手动确认条目数量")
    print("  💡 建议: Memory 条目控制在 ~15 条以内，每条不超过 3 行")
    
    # ── L3: Knowledge ──
    if report.knowledge_files:
        print(f"\n{'─' * 40}")
        print("📚 L3: Knowledge 层")
        print("─" * 40)
        for k in report.knowledge_files:
            marker = " ⚠️" if k.issues else ""
            print(f"\n    {k.name:<40} {k.lines:>5} 行  ~{k.estimated_tokens:>5} tokens{marker}")
            for issue in k.issues:
                print(f"      {issue}")
    
    # ── 汇总 ──
    print(f"\n{'=' * 60}")
    print("  📊 汇总")
    print("=" * 60)
    print(f"\n  System Prompt 固定开销:  ~{SYSTEM_PROMPT_OVERHEAD:,} tokens")
    print(f"  Always-on Rules:         ~{report.total_always_tokens:,} tokens")
    print(f"  Memory (MEMORY.md):      ~{report.total_memory_tokens:,} tokens")
    print(f"  {'─' * 35}")
    print(f"  每轮固定开销估算:        ~{report.total_per_round:,} tokens/轮")
    print(f"  10 轮对话累计:           ~{report.total_per_10_rounds:,} tokens")
    
    # ── 建议 ──
    if report.suggestions:
        print(f"\n{'─' * 40}")
        print("💡 优化建议")
        print("─" * 40)
        for s in report.suggestions:
            print(f"  {s}")
    
    if report.issues:
        print(f"\n{'─' * 40}")
        print("⚠️ 发现的问题")
        print("─" * 40)
        for issue in report.issues:
            print(f"  {issue}")
    
    print()


# ── 主入口 ──────────────────────────────────────────

def main():
    # 解析参数
    project_root = os.getcwd()
    output_json = False
    knowledge_dir = None
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--json':
            output_json = True
        elif arg == '--knowledge-dir' and i + 1 < len(args):
            i += 1
            knowledge_dir = args[i]
        elif arg == '--help' or arg == '-h':
            print(__doc__)
            sys.exit(0)
        else:
            project_root = os.path.abspath(arg)
        i += 1
    
    if not os.path.exists(project_root):
        print(f"❌ 目录不存在: {project_root}")
        sys.exit(1)
    
    # 运行审计
    report = generate_report(project_root, knowledge_dir)
    
    if output_json:
        # JSON 输出
        output = {
            'project_root': report.project_root,
            'always_rules': [asdict(r) for r in report.always_rules],
            'requestable_rules': [asdict(r) for r in report.requestable_rules],
            'knowledge_files': [asdict(r) for r in report.knowledge_files],
            'totals': {
                'always_tokens_per_round': report.total_always_tokens,
                'memory_tokens_estimate': report.total_memory_tokens,
                'total_per_round': report.total_per_round,
                'total_per_10_rounds': report.total_per_10_rounds,
            },
            'suggestions': report.suggestions,
            'issues': report.issues,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_report(report)


if __name__ == '__main__':
    main()
