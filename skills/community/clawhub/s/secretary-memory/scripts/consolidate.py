#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 归档脚本
将 memory/daily/ 下超过7天的日志归档到 memory/archive/

用法:
    python3 consolidate.py [--dry-run] [--verbose]
    python3 consolidate.py --restore    # 从 archive 恢复到 daily/

归档流程:
    1. 扫描 memory/daily/ 下超过7天的日志
    2. 提取项目信息 → memory/archive/projects/
    3. 提取决策信息 → memory/archive/decisions/
    4. 移动日志 → memory/archive/daily/
    5. 更新 memory/memory.md 精选摘要
    6. 更新 memory/archive/index.json 话题索引
"""

import os
import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple
import argparse

# 导入容量管理器
from capacity_manager import CapacityManager, WARN_THRESHOLD, CRITICAL_THRESHOLD

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
DAILY_DIR = MEMORY_DIR / "daily"       # 每日日志（7天内）
ARCHIVE_DIR = MEMORY_DIR / "archive"  # 归档目录
AGENDA_DIR = MEMORY_DIR / "agenda"     # 待办
PROFILE_DIR = MEMORY_DIR / "profile"   # 偏好
PROJECTS_DIR = MEMORY_DIR / "projects"  # 进行中项目
KNOWLEDGE_DIR = MEMORY_DIR / "knowledge" # 知识
MEMORY_MD = MEMORY_DIR / "memory.md"   # 长期记忆精选
RESTORE_LOG_FILE = ARCHIVE_DIR / ".restore_log.json"  # 归档操作日志

DAYS_TO_KEEP_IN_DAILY = 7  # 7天后归档

# ============== 工具函数 ==============

def is_daily_file(path: Path) -> bool:
    """检查是否是日期格式的日志文件（YYYY-MM-DD.md）"""
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}\.md$', path.name))

def daily_files() -> List[Path]:
    """返回 DAILY_DIR 下所有日期格式的日志文件"""
    result = []
    if DAILY_DIR.exists():
        for f in DAILY_DIR.iterdir():
            if is_daily_file(f):
                result.append(f)
    return sorted(result)

def get_date_from_file(path: Path) -> datetime:
    """从文件名提取日期"""
    return datetime.strptime(path.stem, "%Y-%m-%d")

# ============== 归档引擎 ==============

class ConsolidationEngine:
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.stats = {
            "archived_daily": [],
            "archived_projects": [],
            "archived_decisions": [],
            "topics_linked": [],
            "errors": []
        }
        self.archive_index_file = ARCHIVE_DIR / "index.json"
        self.restore_log = []  # 归档操作日志
        self._load_restore_log()

    def log(self, msg: str):
        if self.verbose:
            print(f"[Consolidation] {msg}")

    def _load_restore_log(self):
        """加载恢复日志"""
        if RESTORE_LOG_FILE.exists():
            try:
                self.restore_log = json.loads(RESTORE_LOG_FILE.read_text(encoding="utf-8"))
            except Exception:
                self.restore_log = []

    def _save_restore_log(self):
        """保存恢复日志"""
        if self.dry_run:
            return
        RESTORE_LOG_FILE.write_text(
            json.dumps(self.restore_log, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def _log_archive(self, source: Path, dest: Path, file_type: str):
        """记录归档操作"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "archive",
            "source": str(source.relative_to(MEMORY_DIR)),
            "dest": str(dest.relative_to(MEMORY_DIR)),
            "type": file_type
        }
        self.restore_log.append(entry)
        self._save_restore_log()

    def run(self):
        """执行归档"""
        self.log(f"开始执行 (dry_run={self.dry_run})")

        # ========== 容量检查 ==========
        if not self.dry_run:
            cm = CapacityManager(verbose=self.verbose)
            report = cm.check_usage()

            # 打印容量警告
            cm.warn_if_full(report)

            # 检查是否需要自动归档
            if report["overall"]["status"] == "critical":
                triggered, msg = cm.auto_archive_if_needed()
                if triggered:
                    print(f"[容量管理器] 触发原因: {msg}")
        # ========== 容量检查结束 ==========

        # 确保目录存在
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        (ARCHIVE_DIR / "daily").mkdir(exist_ok=True)
        (ARCHIVE_DIR / "projects").mkdir(exist_ok=True)
        (ARCHIVE_DIR / "decisions").mkdir(exist_ok=True)

        # 1. 提取项目信息并归档
        self.extract_and_archive_projects()

        # 2. 提取决策信息并归档
        self.extract_and_archive_decisions()

        # 3. 清理过期的 daily 文件
        self.archive_old_daily_files()

        # 4. 更新 memory.md
        self.update_memory_md()

        # 5. 更新 archive 话题索引
        self.update_archive_index()

        self.print_stats()
        return self.stats

    def extract_and_archive_projects(self):
        """从 daily 文件中提取项目信息并归档"""
        for daily_file in daily_files():
            try:
                content = daily_file.read_text(encoding="utf-8")
                # 匹配项目相关行
                patterns = [
                    r"(?:项目|project)[:：]\s*(.+?)(?:\n|$)",
                    r"- (.+?项目.+?)(?:\n|$)",
                    r"### (.+?项目.+?)(?:\n|$)",
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for m in matches:
                        proj_name = m.strip()
                        if len(proj_name) > 3:
                            self.archive_project(proj_name, daily_file.stem)
            except Exception as e:
                self.stats["errors"].append(f"提取项目失败 {daily_file.name}: {e}")

    def extract_and_archive_decisions(self):
        """从 daily 文件中提取决策信息并归档"""
        for daily_file in daily_files():
            try:
                content = daily_file.read_text(encoding="utf-8")
                patterns = [
                    r"(?:决定|决策|最终选择|采用)[:：]\s*(.+?)(?:\n|$)",
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for m in matches:
                        dec_text = m.strip()
                        if len(dec_text) > 3:
                            self.archive_decision(dec_text, daily_file.stem, content)
            except Exception as e:
                self.stats["errors"].append(f"提取决策失败 {daily_file.name}: {e}")

    def archive_project(self, project_name: str, source_date: str):
        """归档项目到 archive/projects/"""
        safe_name = re.sub(r'[^\w\s-]', '', project_name)
        safe_name = re.sub(r'\s+', '-', safe_name).lower()[:50]
        archive_file = ARCHIVE_DIR / "projects" / f"{source_date}-{safe_name}.md"

        if self.dry_run:
            print(f"[DRY] 归档项目: {project_name}")
            return

        try:
            if not archive_file.exists():
                archive_file.write_text(f"""# {project_name}

## 归档日期
{source_date}

## 来源
每日日志自动归档

## 备注
（由 consolidation 自动创建）
""", encoding="utf-8")
                self.stats["archived_projects"].append(project_name)
        except Exception as e:
            self.stats["errors"].append(f"归档项目失败: {e}")

    def archive_decision(self, decision_text: str, source_date: str, context: str = ""):
        """归档决策到 archive/decisions/"""
        safe_name = re.sub(r'[^\w\s-]', '', decision_text[:30])
        safe_name = re.sub(r'\s+', '-', safe_name).lower()[:50]
        archive_file = ARCHIVE_DIR / "decisions" / f"{source_date}-{safe_name}.md"

        # 提取话题关键词
        topics = self.extract_topics(decision_text + " " + context[:200])
        related = self.find_related_archives(topics, archive_file)

        if self.dry_run:
            print(f"[DRY] 归档决策: {decision_text[:50]}... (关联话题: {topics[:3]})")
            return

        try:
            if not archive_file.exists():
                content = f"""# 决策记录

## 日期
{source_date}

## 决策内容
{decision_text}

## 话题标签
{', '.join(topics[:5]) if topics else '(无)'}

## 相关归档
{self.format_related_links(related) if related else '(无)'}

## 来源
每日日志自动归档
"""
                archive_file.write_text(content, encoding="utf-8")
                self.stats["archived_decisions"].append(decision_text[:50])
                if related:
                    self.stats["topics_linked"].extend(related)
        except Exception as e:
            self.stats["errors"].append(f"归档决策失败: {e}")

    def archive_old_daily_files(self):
        """归档超过7天的日志文件"""
        cutoff = datetime.now() - timedelta(days=DAYS_TO_KEEP_IN_DAILY)
        archive_daily_dir = ARCHIVE_DIR / "daily"

        for daily_file in daily_files():
            try:
                file_date = get_date_from_file(daily_file)
                if file_date < cutoff:
                    archive_file = archive_daily_dir / daily_file.name
                    if self.dry_run:
                        print(f"[DRY] 归档日志: {daily_file.name}")
                    else:
                        daily_file.rename(archive_file)
                        self._log_archive(daily_file, archive_file, "daily")
                        self.log(f"归档日志: {daily_file.name}")
                    self.stats["archived_daily"].append(daily_file.name)
            except Exception as e:
                self.stats["errors"].append(f"归档日志 {daily_file.name} 失败: {e}")

    def update_memory_md(self):
        """更新 memory.md 精选记忆"""
        if self.dry_run:
            print("[DRY] 更新 memory.md")
            return

        # 从 profile/ 读取用户信息
        profile_content = ""
        pref_file = PROFILE_DIR / "preferences" / "preferences.md"
        if pref_file.exists():
            profile_content = pref_file.read_text()

        new_content = f"""# MEMORY.md - 长期记忆

<!-- 自动生成 by consolidation.py -->
<!-- 上次更新: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->

## 用户画像

{profile_content if profile_content else '(未设置)'}

## 重要项目状态

（请手动维护或从 projects/ 目录汇总）

## 最近决策

（从 archive/decisions/ 自动汇总）

---
*此文件由 consolidation 脚本自动维护*
"""

        MEMORY_MD.write_text(new_content, encoding="utf-8")
        self.log("memory.md 已更新")

    def extract_topics(self, text: str) -> List[str]:
        """从文本中提取话题关键词 - 智能提取版本

        使用多策略提取：
        1. 正则匹配已知模式
        2. 基于词频的关键词提取
        3. N-gram 短语提取
        4. 停用词过滤
        """
        # 停用词列表
        stop_words = {
            # 中文停用词
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
            '自己', '这', '那', '里', '为', '什么', '可以', '这个', '那个', '还', '能', '但',
            '而', '于', '与', '或', '如果', '因为', '所以', '但是', '然后', '以及', '等',
            # 英文停用词
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
            'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'what', 'which', 'who', 'when', 'where', 'why', 'how',
        }

        topics = []

        # 策略1: 正则匹配已知模式（保持原有能力）
        patterns = [
            r'(?:项目|project)[:：]\s*([^"\n]+)',
            r'([\u4e00-\u9fa5]{2,8}(?:项目|系统|框架|架构|论文|设计))',
            r'(React|Flask|LangGraph|RAG|OpenClaw|Claude|MiniMax|Stm32|Python|JavaScript)',
            r'(GUI|Agent|记忆|记忆系统|秘书|技术|架构|设计|实现|优化|问题|修复)',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            topics.extend([m.strip() for m in matches if len(m.strip()) > 1])

        # 策略2: 基于词频的关键词提取
        # 提取所有2-6字的中文词组合
        chinese_word_pattern = r'[\u4e00-\u9fa5]{2,6}'
        chinese_words = re.findall(chinese_word_pattern, text)

        # 提取英文单词
        english_word_pattern = r'[A-Za-z]{3,}'
        english_words = re.findall(english_word_pattern, text)

        # 统计词频
        word_freq = {}
        for word in chinese_words + english_words:
            word_lower = word.lower()
            if word_lower not in stop_words and len(word) >= 2:
                word_freq[word_lower] = word_freq.get(word_lower, 0) + 1

        # 取高频词作为候选关键词
        if word_freq:
            sorted_words = sorted(word_freq.items(), key=lambda x: -x[1])
            # 取出现2次以上或单次但较长的词
            for word, freq in sorted_words[:15]:
                if freq >= 2 or len(word) >= 4:
                    # 保持原始大小写
                    original = word
                    for w in chinese_words + english_words:
                        if w.lower() == word:
                            original = w
                            break
                    if original not in topics:
                        topics.append(original)

        # 策略3: 提取2-gram和3-gram短语
        all_tokens = chinese_words + english_words
        for n in [2, 3]:
            for i in range(len(all_tokens) - n + 1):
                phrase = ''.join(all_tokens[i:i+n])
                phrase_lower = phrase.lower()
                # 短语长度>=4且不是全是停用词
                if len(phrase) >= 4:
                    # 检查短语中非停用词的比例
                    non_stop = sum(1 for t in all_tokens[i:i+n] if t.lower() not in stop_words)
                    if non_stop >= n / 2 and phrase not in topics:
                        topics.append(phrase)

        # 去重并限制数量
        seen = set()
        unique_topics = []
        for t in topics:
            t_lower = t.lower()
            if t_lower not in seen and t_lower not in stop_words:
                seen.add(t_lower)
                unique_topics.append(t)

        return unique_topics[:15]  # 增加到15个

    def find_related_archives(self, topics: List[str], current_file: Path) -> List[Dict]:
        """查找与话题相关的已有归档"""
        related = []
        if not topics:
            return related

        for archive_type in ["projects", "decisions"]:
            archive_path = ARCHIVE_DIR / archive_type
            if not archive_path.exists():
                continue

            for f in archive_path.glob("*.md"):
                if f == current_file:
                    continue
                try:
                    content = f.read_text(encoding="utf-8")
                    for topic in topics:
                        if topic.lower() in content.lower():
                            related.append({
                                "file": str(f.relative_to(ARCHIVE_DIR)),
                                "type": archive_type,
                                "matched_topic": topic
                            })
                            break
                except Exception:
                    pass

        return related[:5]

    def format_related_links(self, related: List[Dict]) -> str:
        """格式化关联链接"""
        if not related:
            return "(无)"
        return "\n".join([f"- [[{r['file']}]] (匹配话题: {r['matched_topic']})" for r in related])

    def update_archive_index(self):
        """更新 archive 话题索引"""
        if self.dry_run:
            print("[DRY] 更新 archive 索引")
            return

        index = {"topics": {}, "files": {}}

        for archive_type in ["projects", "decisions", "daily"]:
            archive_path = ARCHIVE_DIR / archive_type
            if not archive_path.exists():
                continue

            for f in archive_path.rglob("*.md"):
                rel_path = str(f.relative_to(ARCHIVE_DIR))
                try:
                    content = f.read_text(encoding="utf-8")
                    topics = self.extract_topics(content)
                    for topic in topics:
                        if topic not in index["topics"]:
                            index["topics"][topic] = []
                        index["topics"][topic].append(rel_path)
                    index["files"][rel_path] = {"topics": topics, "type": archive_type}
                except Exception:
                    pass

        self.archive_index_file.write_text(
            json.dumps(index, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        self.log(f"archive 索引已更新 ({len(index['files'])} 文件, {len(index['topics'])} 话题)")

    def print_stats(self):
        """打印统计信息"""
        print("\n[Consolidation] 完成!")
        print(f"  归档日志: {len(self.stats['archived_daily'])}")
        print(f"  归档项目: {len(self.stats['archived_projects'])}")
        print(f"  归档决策: {len(self.stats['archived_decisions'])}")
        print(f"  话题关联: {len(self.stats['topics_linked'])}")

        # 容量状态
        cm = CapacityManager()
        print(f"\n  容量状态: {cm.get_summary()}")

        if self.stats["errors"]:
            print(f"  错误: {len(self.stats['errors'])}")
            for err in self.stats["errors"][:5]:
                print(f"    - {err}")

    def restore(self):
        """从 archive/daily/ 恢复到 daily/"""
        archive_daily = ARCHIVE_DIR / "daily"
        if not archive_daily.exists():
            print("没有找到归档日志")
            return

        count = 0
        for f in archive_daily.glob("*.md"):
            dest = DAILY_DIR / f.name
            f.rename(dest)
            count += 1
            print(f"恢复: {f.name}")

        print(f"\n恢复了 {count} 个日志文件到 daily/")


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 秘书式记忆系统 - 归档脚本")
    parser.add_argument("--dry-run", action="store_true", help="仅显示将要执行的操作，不实际修改")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--restore", action="store_true", help="从 archive 恢复到 daily/")
    parser.add_argument("--restore-log", action="store_true", help="查看归档操作历史")
    parser.add_argument("--check-capacity", action="store_true", help="仅检查容量，不执行归档")
    args = parser.parse_args()

    # 容量检查模式
    if args.check_capacity:
        cm = CapacityManager(verbose=True)
        report = cm.check_usage()
        cm.warn_if_full(report)
        print(f"\n容量摘要: {cm.get_summary()}")
        return

    engine = ConsolidationEngine(dry_run=args.dry_run, verbose=args.verbose)

    if args.restore_log:
        # 查看归档历史
        if RESTORE_LOG_FILE.exists():
            try:
                log = json.loads(RESTORE_LOG_FILE.read_text(encoding="utf-8"))
                print(f"## 归档操作历史 (共 {len(log)} 条)\n")
                for entry in log[-20:]:  # 显示最近20条
                    timestamp = entry.get("timestamp", "")[:19]
                    print(f"- [{timestamp}] {entry.get('type', 'unknown')}: {entry.get('source', '')} -> {entry.get('dest', '')}")
            except Exception as e:
                print(f"[Error] 读取归档日志失败: {e}")
        else:
            print("[Info] 暂无归档操作记录")
        return

    if args.restore:
        engine.restore()
    else:
        engine.run()


if __name__ == "__main__":
    main()
