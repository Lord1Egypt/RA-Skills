#!/usr/bin/env python3
"""
伏笔自动扫描脚本 v2.2.0
扫描章节正文，发现潜在的伏笔线索，检查伏笔回收情况

用法：
  python3 foreshadow_scan.py --novel-dir <正文目录> [选项]

功能：
  1. 模式匹配：识别常见伏笔句式
  2. 异常细节描写检测
  3. 伏笔-回收匹配（需要 foreshadowing.json）
  4. 未回收伏笔警告
  5. 回收建议

输出：
  - 每章发现的潜在伏笔
  - 未回收伏笔列表
  - 建议回收时机
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

__version__ = "v2.2.0"

# ============================================================
# 工具函数
# ============================================================

def read_file(path: str) -> str:
    """读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[警告] 无法读取 {path}: {e}")
        return ""


def load_json(path: str) -> Optional[Dict[str, Any]]:
    """加载 JSON 文件"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


DRAFT_KEYWORDS = ('草稿', 'draft', 'wip', 'Draft', 'WIP', 'DRAFT')


def is_draft_filename(fname: str) -> bool:
    """判断文件名是否为草稿"""
    lower = fname.lower()
    return any(kw.lower() in lower for kw in DRAFT_KEYWORDS)


def list_chapters(dir_path: str, skip_drafts: bool = True) -> List[Tuple[int, str, str]]:
    """列出章节文件，返回 (章节号, 文件名, 完整路径) 列表"""
    if not os.path.isdir(dir_path):
        print(f"[错误] 正文目录不存在: {dir_path}")
        return []
    chapters = []
    for f in sorted(os.listdir(dir_path)):
        if not (f.endswith('.md') or f.endswith('.txt')):
            continue
        if skip_drafts and is_draft_filename(f):
            continue
        match = re.search(r'第(\d+)章', f)
        if match:
            num = int(match.group(1))
            chapters.append((num, f, os.path.join(dir_path, f)))
    chapters.sort(key=lambda x: x[0])
    return chapters


# ============================================================
# 伏笔模式定义
# ============================================================

# 忽略线索型：暗示某事被忽略，后续可能重要
IGNORE_PATTERNS = [
    r'不过那时候[他她它](?:并)?没(?:有)?在意',
    r'[他她它]没(?:有)?多想',
    r'当时谁也没(?:有)?注意到',
    r'[他她它]并没有?把[这事]放在心上',
    r'[他她它]随手[放丢扔塞].{0,10}没有再管',
    r'[他她它]没(?:有)?放在心上',
    r'这件事?就[这么]?过去了',
]

# 后知后觉型：暗示事后才明白的事
HINDSIGHT_PATTERNS = [
    r'后来[他她它]才(?:知道|明白|发现|意识到|懂)',
    r'多年以后[他她它]才(?:知道|明白|发现|意识到)',
    r'那时候[他她它]还不知道',
    r'直到很久以后[他她它]才(?:知道|明白|发现|意识到)',
    r'直到[他她它]后来才(?:知道|明白|发现|意识到)',
    r'后来的事[，,][他她它]当时完全没有?想到',
    r'此时此刻[，,][他她它]还不知道',
]

# 异常感觉型：暗示不对劲但没追究
UNEASE_PATTERNS = [
    r'奇怪的是',
    r'说不上来哪里不对',
    r'总觉得哪里不对(?:劲)?',
    r'[他她它]隐约觉得(?:有点)?不对(?:劲)?',
    r'有一瞬间[，,][他她它]觉得(?:有些)?不对',
    r'但[他她它]说不清楚(?:到底)?为什么',
    r'心里(?:隐隐)?觉得(?:有些)?不对(?:劲)?',
]

# 过度细节描写型：物品/人物描写超过一定长度，暗示后续重要性
# 通过单独函数检测


def compile_patterns(patterns: List[str]) -> List[re.Pattern]:
    """编译正则模式列表"""
    return [re.compile(p) for p in patterns]


class ForeshadowScanner:
    """伏笔扫描器"""

    def __init__(self, novel_dir: str,
                 foreshadowing_path: Optional[str] = None,
                 suggest: bool = False,
                 max_unresolved_gap: int = 30,
                 detail_length_threshold: int = 80):
        self.novel_dir = novel_dir
        self.foreshadowing_path = foreshadowing_path
        self.suggest = suggest
        self.max_unresolved_gap = max_unresolved_gap  # 超过N章未回收则警告
        self.detail_length_threshold = detail_length_threshold  # 细节描写长度阈值

        # 编译模式
        self.ignore_patterns = compile_patterns(IGNORE_PATTERNS)
        self.hindsight_patterns = compile_patterns(HINDSIGHT_PATTERNS)
        self.unease_patterns = compile_patterns(UNEASE_PATTERNS)

        # 加载伏笔追踪数据
        self.foreshadow_data: Optional[Dict[str, Any]] = None
        if foreshadowing_path:
            self.foreshadow_data = load_json(foreshadowing_path)

    def scan_text(self, text: str) -> List[Dict[str, Any]]:
        """扫描单段文本，返回发现的潜在伏笔列表"""
        findings: List[Dict[str, Any]] = []
        lines = text.split('\n')

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # 检查忽略型模式
            for pat in self.ignore_patterns:
                m = pat.search(stripped)
                if m:
                    findings.append({
                        "type": "忽略线索",
                        "pattern": m.group(),
                        "line": line_num,
                        "context": stripped[:100],
                    })

            # 检查后知后觉型
            for pat in self.hindsight_patterns:
                m = pat.search(stripped)
                if m:
                    findings.append({
                        "type": "后知后觉",
                        "pattern": m.group(),
                        "line": line_num,
                        "context": stripped[:100],
                    })

            # 检查异常感觉型
            for pat in self.unease_patterns:
                m = pat.search(stripped)
                if m:
                    findings.append({
                        "type": "异常感觉",
                        "pattern": m.group(),
                        "line": line_num,
                        "context": stripped[:100],
                    })

            # 检查过度细节描写（独立段落的物品/人物描写过长）
            self._check_detail_description(stripped, line_num, findings)

        return findings

    def _check_detail_description(self, line: str, line_num: int,
                                   findings: List[Dict[str, Any]]) -> None:
        """检测过度详细的物品/人物描写（暗示后续重要性）"""
        if len(line) < self.detail_length_threshold:
            return
        # 物品描写信号词
        item_signals = ['看起来', '摸起来', '散发着', '表面刻着', '做工精细',
                        '通体', '材质', '雕刻着', '纹路', '光泽']
        # 人物外貌信号词（过度描写外貌特征）
        person_signals = ['眉眼', '嘴角', '手指修长', '瞳孔', '目光深邃',
                          '轮廓', '锁骨', '手腕', '发丝']

        matched_signals = []
        for s in item_signals + person_signals:
            if s in line:
                matched_signals.append(s)

        # 至少命中2个信号词才标记（避免误报）
        if len(matched_signals) >= 2:
            findings.append({
                "type": "异常细节描写",
                "pattern": " + ".join(matched_signals[:3]),
                "line": line_num,
                "context": line[:100],
            })

    def scan_chapters(self) -> Dict[int, List[Dict[str, Any]]]:
        """扫描所有章节，返回 {章节号: [伏笔列表]} """
        chapters = list_chapters(self.novel_dir)
        results: Dict[int, List[Dict[str, Any]]] = {}

        for num, fname, fpath in chapters:
            text = read_file(fpath)
            if not text:
                continue
            findings = self.scan_text(text)
            if findings:
                results[num] = findings

        return results

    def check_unresolved(self, scan_results: Dict[int, List[Dict[str, Any]]],
                         total_chapters: int) -> List[Dict[str, Any]]:
        """检查未回收的伏笔（需要 foreshadowing.json）"""
        unresolved: List[Dict[str, Any]] = []

        if not self.foreshadow_data:
            return unresolved

        items = self.foreshadow_data.get("foreshadowing", [])
        if not items:
            return unresolved

        latest_chapter = total_chapters

        for item in items:
            status = item.get("status", "planted")
            if status == "resolved":
                continue
            planted_ch = item.get("planted_chapter", 0)
            gap = latest_chapter - planted_ch
            item_copy = dict(item)
            item_copy["gap"] = gap
            if gap > self.max_unresolved_gap:
                item_copy["warning"] = "可能遗忘"
            unresolved.append(item_copy)

        return unresolved

    def generate_suggestions(self, scan_results: Dict[int, List[Dict[str, Any]]],
                             unresolved: List[Dict[str, Any]]) -> List[str]:
        """生成回收建议"""
        suggestions: List[str] = []

        if not scan_results and not unresolved:
            return suggestions

        # 基于扫描结果的建议
        total_findings = sum(len(v) for v in scan_results.values())
        if total_findings > 0:
            # 按类型统计
            type_counts: Dict[str, int] = defaultdict(int)
            for findings in scan_results.values():
                for f in findings:
                    type_counts[f["type"]] += 1

            suggestions.append(f"共发现 {total_findings} 处潜在伏笔：")
            for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
                suggestions.append(f"  - {t}：{c} 处")

            # 最近章节发现的伏笔应尽快回收
            if scan_results:
                recent_ch = max(scan_results.keys())
                recent_count = len(scan_results[recent_ch])
                if recent_count > 0:
                    suggestions.append(
                        f"  ⚠ 第{recent_ch}章新发现 {recent_count} 处伏笔线索，"
                        f"建议在后续5-10章内安排回收"
                    )

        # 基于未回收伏笔的建议
        forgotten = [u for u in unresolved if u.get("warning") == "可能遗忘"]
        if forgotten:
            suggestions.append(f"\n⚠ {len(forgotten)} 处伏笔超过 "
                               f"{self.max_unresolved_gap} 章未回收，可能遗忘：")
            for u in forgotten:
                desc = u.get("description", "未知伏笔")
                ch = u.get("planted_chapter", "?")
                gap = u.get("gap", "?")
                suggestions.append(f"  - 第{ch}章「{desc}」已 {gap} 章未回收")
                suggestions.append(f"    → 建议在近期章节（3-5章内）安排回收")

        return suggestions

    def run(self) -> Dict[str, Any]:
        """执行完整扫描，返回报告"""
        chapters = list_chapters(self.novel_dir)
        total_chapters = len(chapters)

        # 1. 扫描章节
        scan_results = self.scan_chapters()

        # 2. 检查未回收
        unresolved = self.check_unresolved(scan_results, total_chapters)

        # 3. 生成建议
        suggestions = []
        if self.suggest:
            suggestions = self.generate_suggestions(scan_results, unresolved)

        return {
            "total_chapters": total_chapters,
            "scan_results": scan_results,
            "unresolved": unresolved,
            "suggestions": suggestions,
        }


def format_report(report: Dict[str, Any]) -> str:
    """格式化输出报告"""
    lines: List[str] = []
    lines.append("=" * 60)
    lines.append("伏笔扫描报告")
    lines.append("=" * 60)
    lines.append(f"扫描章节数：{report['total_chapters']}")
    lines.append("")

    # 每章发现
    scan_results = report.get("scan_results", {})
    if scan_results:
        lines.append("── 每章潜在伏笔 ──")
        for ch_num in sorted(scan_results.keys()):
            findings = scan_results[ch_num]
            lines.append(f"\n第{ch_num}章（{len(findings)}处）：")
            for f in findings:
                lines.append(f"  [{f['type']}] 第{f['line']}行：{f['context']}")
                lines.append(f"    匹配：「{f['pattern']}」")
    else:
        lines.append("── 未发现明显伏笔句式 ──")

    # 未回收伏笔
    unresolved = report.get("unresolved", [])
    if unresolved:
        lines.append("\n── 未回收伏笔 ──")
        for u in unresolved:
            desc = u.get("description", "未知")
            ch = u.get("planted_chapter", "?")
            gap = u.get("gap", "?")
            warn = u.get("warning", "")
            marker = " ⚠ 可能遗忘" if warn else ""
            lines.append(f"  第{ch}章「{desc}」— 已{gap}章未回收{marker}")

    # 建议
    suggestions = report.get("suggestions", [])
    if suggestions:
        lines.append("\n── 回收建议 ──")
        for s in suggestions:
            lines.append(s)

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="伏笔自动扫描脚本 — 发现潜在伏笔线索，检查回收情况"
    )
    parser.add_argument("--novel-dir", required=True,
                        help="章节正文目录路径")
    parser.add_argument("--foreshadowing", default=None,
                        help="foreshadowing.json 路径（可选）")
    parser.add_argument("--suggest", action="store_true",
                        help="输出回收建议")
    parser.add_argument("--max-gap", type=int, default=30,
                        help="超过N章未回收标记为可能遗忘（默认30）")
    parser.add_argument("--json", action="store_true",
                        help="JSON 格式输出")
    parser.add_argument("--output", default=None,
                        help="报告输出文件路径")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    scanner = ForeshadowScanner(
        novel_dir=args.novel_dir,
        foreshadowing_path=args.foreshadowing,
        suggest=args.suggest,
        max_unresolved_gap=args.max_gap,
    )

    report = scanner.run()

    # 输出
    if args.json:
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        output = format_report(report)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"报告已写入 {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
