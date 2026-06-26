#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 记忆冲突检测
当新记忆与已有记忆矛盾时主动提示（不阻止操作）

用法:
    python3 conflict_detector.py --new "决定用方案A" --topic "项目X架构"
    python3 conflict_detector.py --new-file /path/to/new_content.md --topic "架构设计"
    python3 conflict_detector.py --new "决定用A" --topic "项目X" --json
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
ARCHIVE_DECISIONS_DIR = MEMORY_DIR / "archive" / "decisions"
ARCHIVE_PROJECTS_DIR = MEMORY_DIR / "archive" / "projects"
ARCHIVE_INDEX_FILE = MEMORY_DIR / "archive" / "index.json"

# 冲突检测模式
# 当新内容包含这些词时，检查已有记忆
DECISION_TRIGGERS = ["决定", "采用", "选择", "不用", "弃用", "拒绝", "放弃", "取消"]
CONFLICT_SIGNALS = [
    ("A|方案A", "B|方案B"),
    ("Python", "JavaScript|TypeScript"),
    ("React", "Vue|Angular"),
    ("微服务", "单体"),
    ("SQL", "NoSQL|MongoDB"),
    ("自研", "开源|第三方"),
    ("自建", "外包|采购"),
]


# ============== 冲突检测器 ==============

class ConflictDetector:
    def __init__(self):
        self.decisions_dir = ARCHIVE_DECISIONS_DIR
        self.projects_dir = ARCHIVE_PROJECTS_DIR
        self.index_file = ARCHIVE_INDEX_FILE

    def load_archive_index(self) -> Dict:
        """加载归档索引"""
        if self.index_file.exists():
            try:
                return json.loads(self.index_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"topics": {}, "files": {}}

    def extract_topics(self, text: str) -> List[str]:
        """从文本中提取话题关键词"""
        topics = []

        # 技术栈
        tech_patterns = [
            r'(React|Flask|LangGraph|RAG|OpenClaw|Claude|MiniMax|Stm32|Python|JavaScript|TypeScript)',
            r'([A-Z][a-zA-Z]+)',
        ]
        for pattern in tech_patterns:
            matches = re.findall(pattern, text)
            topics.extend(matches)

        # 中文词汇
        chinese_pattern = r'([\u4e00-\u9fa5]{2,10}(?:项目|架构|系统|框架|方案|设计|技术))'
        matches = re.findall(chinese_pattern, text)
        topics.extend(matches)

        return [t for t in topics if len(t) >= 2][:10]

    def extract_decision(self, text: str) -> Optional[Dict]:
        """从文本中提取决策信息"""
        patterns = [
            r'(?:决定|决策|最终选择|采用|选择)[:：]\s*(.+?)(?:\n|$)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                decision = match.group(1).strip()
                # 提取涉及的技术/方案
                technologies = []
                for tech_pattern in [r'(方案[ABCDEF]|技术栈|React|Flask|LangGraph|Python|JavaScript)']:
                    tech_matches = re.findall(tech_pattern, decision)
                    technologies.extend(tech_matches)

                return {
                    "decision": decision,
                    "technologies": list(set(technologies)) if technologies else []
                }
        return None

    def find_related_decisions(self, topics: List[str]) -> List[Path]:
        """根据话题找到相关的已有决策文件"""
        related = []

        if not self.decisions_dir.exists():
            return related

        # 使用索引快速查找
        index = self.load_archive_index()

        for topic in topics:
            # 直接匹配索引
            for file_path in index.get("topics", {}).get(topic, []):
                full_path = MEMORY_DIR / file_path
                if full_path.exists() and full_path not in related:
                    related.append(full_path)

        # 如果索引没有，降级到全文搜索
        if not related:
            for md_file in self.decisions_dir.glob("*.md"):
                content = md_file.read_text(encoding="utf-8").lower()
                if any(topic.lower() in content for topic in topics):
                    related.append(md_file)

        return related

    def detect_conflicts(self, new_decision: Dict, related_files: List[Path]) -> List[Dict]:
        """检测冲突，返回冲突列表"""
        conflicts = []

        new_tech = set(new_decision.get("technologies", []))
        new_text_lower = new_decision["decision"].lower()

        for file_path in related_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                file_decision = self.extract_decision(content)

                if not file_decision:
                    continue

                old_tech = set(file_decision.get("technologies", []))

                # 检测技术冲突
                if new_tech and old_tech:
                    # 如果新决策包含某个技术，但旧决策推荐了另一个，标记为潜在冲突
                    for signal_pair in CONFLICT_SIGNALS:
                        new_has = any(re.search(signal_pair[0], new_text_lower) for _ in [1])
                        old_has = any(re.search(signal_pair[1], content.lower()) for _ in [1])
                        if new_has and old_has:
                            conflicts.append({
                                "type": "technical_conflict",
                                "file": str(file_path.relative_to(MEMORY_DIR)),
                                "old_decision": file_decision["decision"],
                                "new_decision": new_decision["decision"],
                                "signal": f"{signal_pair[0]} vs {signal_pair[1]}",
                                "severity": "high"
                            })

                # 检测"之前决定X，现在决定Y"类型的冲突
                old_text_lower = content.lower()
                for trigger in DECISION_TRIGGERS:
                    if trigger in new_text_lower and trigger in old_text_lower:
                        # 两个决策都包含决策类词汇
                        if new_decision["decision"] != file_decision["decision"]:
                            # 决策内容不同，可能是冲突
                            conflicts.append({
                                "type": "decision_conflict",
                                "file": str(file_path.relative_to(MEMORY_DIR)),
                                "old_decision": file_decision["decision"],
                                "new_decision": new_decision["decision"],
                                "trigger": trigger,
                                "severity": "medium"
                            })

            except Exception:
                continue

        # 去重
        seen = set()
        unique_conflicts = []
        for c in conflicts:
            key = (c.get("file"), c.get("old_decision", ""))
            if key not in seen:
                seen.add(key)
                unique_conflicts.append(c)

        return unique_conflicts

    def format_conflict_report(self, conflicts: List[Dict], topic: str) -> str:
        """格式化冲突报告（供 AI 直接展示给用户）"""
        if not conflicts:
            return ""

        output = [f"\n⚠️ **记忆冲突检测** (话题: {topic})\n"]
        output.append(f"发现 {len(conflicts)} 条潜在冲突：\n")

        for i, c in enumerate(conflicts, 1):
            severity_icon = "🔴" if c.get("severity") == "high" else "🟡"
            output.append(f"{severity_icon} **冲突 {i}** ({c.get('type', 'unknown')})")

            if c.get("file"):
                output.append(f"   相关归档: `{c['file']}`")

            if c.get("old_decision"):
                output.append(f"   旧决策: {c['old_decision'][:60]}...")

            if c.get("new_decision"):
                output.append(f"   新决策: {c['new_decision'][:60]}...")

            if c.get("signal"):
                output.append(f"   冲突信号: {c['signal']}")

            output.append("")

        output.append("> 如需确认，请告诉我是否要更新记忆或保留原有决策。")
        return '\n'.join(output)

    def check(self, new_content: str, topic: str) -> Dict:
        """执行冲突检测，返回结果"""
        topics = self.extract_topics(topic + " " + new_content)

        if not topics:
            # 如果没提取到话题，把整个 topic 当作关键词
            topics = [topic]

        related_files = self.find_related_decisions(topics)

        new_decision = self.extract_decision(new_content)
        if not new_decision:
            new_decision = {"decision": new_content, "technologies": []}

        conflicts = self.detect_conflicts(new_decision, related_files)

        return {
            "topic": topic,
            "topics_extracted": topics,
            "related_files": [str(f.relative_to(MEMORY_DIR)) for f in related_files],
            "new_decision": new_decision,
            "conflicts": conflicts,
            "conflict_count": len(conflicts)
        }


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 秘书式记忆系统 - 冲突检测")
    parser.add_argument("--new", "-n", default="", help="新决策内容")
    parser.add_argument("--topic", "-t", default="", help="相关话题")
    parser.add_argument("--new-file", "-f", type=Path, help="从文件读取新内容")
    parser.add_argument("--json", "-j", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    if not args.topic:
        parser.print_help()
        print("\n[Error] 请提供 --topic 参数")
        return

    # 获取新内容
    new_content = args.new
    if args.new_file:
        if args.new_file.exists():
            new_content = args.new_file.read_text(encoding="utf-8")
        else:
            print(f"[Error] 文件不存在: {args.new_file}")
            return

    if not new_content:
        print("[Info] 未提供新内容，仅检查相关归档")
        new_content = ""

    detector = ConflictDetector()
    result = detector.check(new_content, args.topic)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 输出格式化报告
    if result["conflicts"]:
        report = detector.format_conflict_report(result["conflicts"], result["topic"])
        print(report)
    else:
        print(f"[OK] 未检测到与「{args.topic}」相关的冲突")


if __name__ == "__main__":
    main()
