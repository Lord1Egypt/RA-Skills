#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _encoding_compat

"""
📚 Phase 15: Personal Knowledge Library (个人知识图书馆)
核心理念：把本地知识库变成一座私人图书馆 — 编目、分类、上架、检索、借阅追踪
功能：
  1. 自动编目 — 扫描本地 Markdown 笔记，提取元数据生成目录卡片
  2. 分类体系 — 自定义层级分类（如 01-低碳医学 > 生酮饮食 > 酮体代谢）
  3. 智能上架 — 根据关键词自动归档到对应分类书架
  4. 全文检索 — 按标题、标签、分类、正文关键词搜索
  5. 阅读追踪 — 未读/在读/已读 状态标记，阅读笔记
  6. 借阅卡片 — 可视化浏览书架，生成知识地图
用法：
  扫描入库：python personal_library.py --scan ./genesis_engine ./langchain_engine
  浏览书架：python personal_library.py --browse
  搜索知识：python personal_library.py --search "酮体"
  分类管理：python personal_library.py --categories
  阅读标记：python personal_library.py --read "title" --status done
"""

import os
import json
import re
import shutil
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict


LIBRARY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_library")
CATALOG_PATH = os.path.join(LIBRARY_DIR, "catalog.json")
CATEGORY_PATH = os.path.join(LIBRARY_DIR, "categories.json")


DEFAULT_CATEGORIES = {
    "01-低碳医学": {
        "label": "低碳医学",
        "emoji": "🫀",
        "children": {
            "生酮饮食": {"label": "生酮饮食", "keywords": ["酮体", "生酮", "keto", "脂肪代谢", "BHB", "乙酰乙酸"]},
            "间歇断食": {"label": "间歇断食", "keywords": ["断食", "禁食", "fasting", "自噬", "autophagy", "16:8", "5:2"]},
            "肠道菌群": {"label": "肠道菌群", "keywords": ["菌群", "肠道", "microbiome", "益生菌", "SCFA", "丁酸"]},
            "线粒体健康": {"label": "线粒体健康", "keywords": ["线粒体", "mitochondria", "ATP", "氧化磷酸化", "呼吸链"]},
            "代谢综合征": {"label": "代谢综合征", "keywords": ["胰岛素", "血糖", "糖尿病", "insulin", "代谢", "糖化"]},
        },
    },
    "02-AI技术": {
        "label": "AI 技术",
        "emoji": "🤖",
        "children": {
            "大语言模型": {"label": "大语言模型", "keywords": ["LLM", "GPT", "transformer", "prompt", "token", "fine-tune"]},
            "知识图谱": {"label": "知识图谱", "keywords": ["knowledge graph", "RAG", "向量", "embedding", "neo4j"]},
            "智能体": {"label": "智能体", "keywords": ["agent", "tool", "function call", "自主", "langchain"]},
            "数字分身": {"label": "数字分身", "keywords": ["数字分身", "digital twin", "persona", "人格", "胶囊"]},
        },
    },
    "03-编程开发": {
        "label": "编程开发",
        "emoji": "💻",
        "children": {
            "Python": {"label": "Python", "keywords": ["python", "pip", "conda", "pandas", "numpy", "flask"]},
            "系统设计": {"label": "系统设计", "keywords": ["架构", "设计模式", "微服务", "API", "数据库", "并发"]},
            "工具链": {"label": "工具链", "keywords": ["git", "docker", "CI/CD", "部署", "测试", "debug"]},
        },
    },
    "04-产品变现": {
        "label": "产品变现",
        "emoji": "💰",
        "children": {
            "微信生态": {"label": "微信生态", "keywords": ["微信", "小程序", "公众号", "支付", "裂变", "分销"]},
            "知识付费": {"label": "知识付费", "keywords": ["付费", "订阅", "会员", "课程", "社群", "转化"]},
            "独立开发": {"label": "独立开发", "keywords": ["独立开发", "indie", "出海", "SaaS", "PLG", "增长"]},
        },
    },
    "05-通用阅读": {
        "label": "通用阅读",
        "emoji": "📖",
        "children": {
            "哲学思辨": {"label": "哲学思辨", "keywords": ["哲学", "道家", "第一性原理", "认知", "思维模型"]},
            "未分类": {"label": "未分类", "keywords": []},
        },
    },
}


def _default_catalog():
    return {
        "version": "2.0",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "total_entries": 0,
        "entries": {},
    }


class PersonalLibrary:
    def __init__(self, library_dir=None):
        self.lib_dir = library_dir or LIBRARY_DIR
        os.makedirs(self.lib_dir, exist_ok=True)
        self._init_catalog()
        self._init_categories()

    def _init_catalog(self):
        if os.path.exists(CATALOG_PATH):
            with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                self.catalog = json.load(f)
        else:
            self.catalog = _default_catalog()
            self._save_catalog()

    def _init_categories(self):
        if os.path.exists(CATEGORY_PATH):
            with open(CATEGORY_PATH, "r", encoding="utf-8") as f:
                self.categories = json.load(f)
        else:
            self.categories = DEFAULT_CATEGORIES
            self._save_categories()

    def _save_catalog(self):
        self.catalog["updated"] = datetime.now().isoformat()
        self.catalog["total_entries"] = len(self.catalog["entries"])
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.catalog, f, ensure_ascii=False, indent=2)

    def _save_categories(self):
        with open(CATEGORY_PATH, "w", encoding="utf-8") as f:
            json.dump(self.categories, f, ensure_ascii=False, indent=2)

    def _extract_metadata(self, filepath):
        title = os.path.splitext(os.path.basename(filepath))[0]
        title = re.sub(r"^(Auto_Filled_|Filled_|Gap_Review_)", "", title)

        stat = os.stat(filepath)
        content = ""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read(2000)
        except Exception:
            pass

        headings = re.findall(r"^#{1,3}\s+(.+)$", content, re.MULTILINE)
        word_count = len(re.findall(r"[\u4e00-\u9fff]|\w+", content))

        return {
            "title": title,
            "original_filename": os.path.basename(filepath),
            "source_path": os.path.abspath(filepath),
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "added": datetime.now().isoformat(),
            "headings": headings[:5],
            "word_count_estimate": word_count,
            "content_preview": content[:300],
        }

    def _classify_by_keywords(self, metadata):
        text = (metadata["title"] + " " + " ".join(metadata["headings"]) + " " +
                metadata["content_preview"]).lower()

        best_category = "05-通用阅读"
        best_subcategory = "未分类"
        best_score = 0

        for cat_key, cat_info in self.categories.items():
            for sub_key, sub_info in cat_info.get("children", {}).items():
                score = 0
                for kw in sub_info.get("keywords", []):
                    if kw.lower() in text:
                        score += 1
                if score > best_score:
                    best_score = score
                    best_category = cat_key
                    best_subcategory = sub_key

        return best_category, best_subcategory, best_score

    def scan_directory(self, target_dir, recursive=True):
        target = Path(target_dir)
        if not target.exists():
            print(f"❌ 目录不存在: {target_dir}")
            return 0

        patterns = ("*.md", "*.txt")
        files = []
        for pat in patterns:
            if recursive:
                files.extend(target.rglob(pat))
            else:
                files.extend(target.glob(pat))

        skip_names = {"SKILL.md", "README.md", "requirements.txt", "Digital_Twin_Business_Case.md"}
        skip_prefixes = ("test_", "_trace", "output_", "lock_test", "unlock_")
        skip_suffixes = ("_output.txt", "_output2.txt")

        count = 0
        for fp in files:
            name = fp.name
            if name in skip_names:
                continue
            if any(name.startswith(p) for p in skip_prefixes):
                continue
            if any(name.endswith(s) for s in skip_suffixes):
                continue

            entry_id = str(fp.resolve())
            if entry_id in self.catalog["entries"]:
                existing = self.catalog["entries"][entry_id]
                existing_mtime = os.path.getmtime(fp)
                stored_mtime = time.mktime(time.strptime(
                    existing.get("modified", "2000-01-01T00:00:00")[:19], "%Y-%m-%dT%H:%M:%S"))
                if existing_mtime <= stored_mtime:
                    continue

            metadata = self._extract_metadata(fp)
            category, subcategory, score = self._classify_by_keywords(metadata)

            self.catalog["entries"][entry_id] = {
                **metadata,
                "category": category,
                "subcategory": subcategory,
                "tags": [],
                "reading_status": "unread",
                "reading_notes": "",
                "importance": score,
            }
            count += 1
            print(f"  📥 [{category}/{subcategory}] {metadata['title']}")

        if count > 0:
            self._save_catalog()
            print(f"\n✅ 入库 {count} 条知识，总计 {self.catalog['total_entries']} 条")
        else:
            print("📭 没有新内容需要入库")
        return count

    def search(self, query, limit=20):
        q = query.lower()
        results = []
        for eid, entry in self.catalog["entries"].items():
            score = 0
            if q in entry["title"].lower():
                score += 10
            if q in " ".join(entry.get("headings", [])).lower():
                score += 5
            if q in entry.get("content_preview", "").lower():
                score += 3
            if q in " ".join(entry.get("tags", [])).lower():
                score += 8
            if q in entry.get("category", "").lower() or q in entry.get("subcategory", "").lower():
                score += 4
            if score > 0:
                results.append((score, entry))

        results.sort(key=lambda x: x[0], reverse=True)
        return results[:limit]

    def browse(self, category=None, status=None):
        entries = list(self.catalog["entries"].items())

        if category:
            entries = [(eid, e) for eid, e in entries
                       if e.get("category") == category or e.get("subcategory") == category]

        if status:
            entries = [(eid, e) for eid, e in entries if e.get("reading_status") == status]

        return sorted(entries, key=lambda x: x[1].get("modified", ""), reverse=True)

    def mark_read(self, title_query, status="done", note=""):
        title_q = title_query.lower()
        found = False
        for eid, entry in self.catalog["entries"].items():
            if title_q in entry["title"].lower():
                entry["reading_status"] = status
                if note:
                    entry["reading_notes"] = note
                print(f"  📖 [{status}] {entry['title']}")
                found = True
        if found:
            self._save_catalog()
        else:
            print(f"❌ 未找到匹配的知识: {title_query}")

    def add_tag(self, title_query, tag):
        title_q = title_query.lower()
        for entry in self.catalog["entries"].values():
            if title_q in entry["title"].lower():
                if tag not in entry.setdefault("tags", []):
                    entry["tags"].append(tag)
                    print(f"  🏷️ [{tag}] → {entry['title']}")
        self._save_catalog()

    def stats(self):
        total = self.catalog["total_entries"]
        by_status = defaultdict(int)
        by_category = defaultdict(int)
        for entry in self.catalog["entries"].values():
            by_status[entry.get("reading_status", "unread")] += 1
            by_category[entry.get("category", "未知")] += 1

        print(f"\n📊 图书馆统计")
        print(f"   总藏书: {total} 册")
        print(f"   未读: {by_status.get('unread', 0)} | 在读: {by_status.get('reading', 0)} | 已读: {by_status.get('done', 0)}")
        print(f"\n📂 分类分布:")
        for cat in sorted(self.categories.keys()):
            cat_info = self.categories[cat]
            count = by_category.get(cat, 0)
            bar = "█" * min(count, 30)
            print(f"   {cat_info['emoji']} {cat_info['label']}: {count} {bar}")
        return {"total": total, "by_status": dict(by_status), "by_category": dict(by_category)}

    def view_categories(self):
        print("\n📂 分类体系:")
        for cat_key, cat_info in self.categories.items():
            count = sum(1 for e in self.catalog["entries"].values() if e.get("category") == cat_key)
            print(f"\n  {cat_info['emoji']} {cat_info['label']} [{cat_key}] — {count} 册")
            for sub_key, sub_info in cat_info.get("children", {}).items():
                sub_count = sum(1 for e in self.catalog["entries"].values() if e.get("subcategory") == sub_key)
                bar = "▌" * sub_count
                print(f"      ├─ {sub_info['label']}: {sub_count} {bar}")
        print()

    def add_category(self, parent_key, sub_key, label, keywords=None):
        if parent_key not in self.categories:
            print(f"❌ 父分类不存在: {parent_key}")
            return
        self.categories[parent_key].setdefault("children", {})[sub_key] = {
            "label": label,
            "keywords": keywords or [],
        }
        self._save_categories()
        print(f"✅ 已添加子分类: {parent_key} > {label}")

    def export_catalog(self, output_path=None):
        output_path = output_path or os.path.join(self.lib_dir, "catalog_export.md")
        lines = ["# 📚 个人知识图书馆 — 目录索引", f"*导出时间: {datetime.now().isoformat()}*", ""]

        for cat_key in sorted(self.categories.keys()):
            cat_info = self.categories[cat_key]
            lines.append(f"## {cat_info['emoji']} {cat_info['label']}")
            lines.append("")
            for eid, entry in self.catalog["entries"].items():
                if entry.get("category") == cat_key:
                    status_icon = {"unread": "📖", "reading": "📌", "done": "✅"}.get(
                        entry.get("reading_status"), "📖")
                    tags = " ".join(f"`#{t}`" for t in entry.get("tags", []))
                    lines.append(f"- {status_icon} **{entry['title']}** "
                                 f"({entry.get('subcategory', '')}) {tags}")
                    if entry.get("headings"):
                        for h in entry["headings"][:3]:
                            lines.append(f"  - {h}")
            lines.append("")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"📋 目录已导出: {output_path}")
        return output_path


def main():
    lib = PersonalLibrary()

    if "--scan" in sys.argv:
        idx = sys.argv.index("--scan")
        dirs = sys.argv[idx + 1:]
        if not dirs:
            dirs = ["./genesis_engine"]
        for d in dirs:
            print(f"🔍 扫描: {d}")
            lib.scan_directory(d)
    elif "--search" in sys.argv:
        idx = sys.argv.index("--search")
        query = " ".join(sys.argv[idx + 1:])
        print(f"🔍 搜索: {query}")
        results = lib.search(query)
        for score, entry in results:
            status = {"unread": "📖", "reading": "📌", "done": "✅"}.get(entry.get("reading_status"), "📖")
            cat = f"{entry.get('category', '')}/{entry.get('subcategory', '')}"
            print(f"  {status} [{score}] {entry['title']}  |  {cat}")
        if not results:
            print("  (无结果)")
    elif "--browse" in sys.argv:
        cat = None
        if "--category" in sys.argv:
            idx = sys.argv.index("--category")
            cat = sys.argv[idx + 1]
        entries = lib.browse(category=cat)
        for eid, entry in entries:
            status = {"unread": "📖", "reading": "📌", "done": "✅"}.get(entry.get("reading_status"), "📖")
            cat_path = f"{entry.get('category', '')}/{entry.get('subcategory', '')}"
            print(f"  {status} {entry['title']}  |  {cat_path}  |  {entry.get('word_count_estimate', 0)} 字")
    elif "--read" in sys.argv:
        idx = sys.argv.index("--read")
        title = sys.argv[idx + 1]
        status = "done"
        if "--status" in sys.argv:
            sidx = sys.argv.index("--status")
            status = sys.argv[sidx + 1]
        note = ""
        if "--note" in sys.argv:
            nidx = sys.argv.index("--note")
            note = sys.argv[nidx + 1]
        lib.mark_read(title, status, note)
    elif "--tag" in sys.argv:
        idx = sys.argv.index("--tag")
        title = sys.argv[idx + 1]
        if "--add" in sys.argv:
            aidx = sys.argv.index("--add")
            tag = sys.argv[aidx + 1]
            lib.add_tag(title, tag)
    elif "--categories" in sys.argv:
        lib.view_categories()
    elif "--stats" in sys.argv:
        lib.stats()
    elif "--export" in sys.argv:
        output = None
        if "--output" in sys.argv:
            oidx = sys.argv.index("--output")
            output = sys.argv[oidx + 1]
        lib.export_catalog(output)
    elif "--add-category" in sys.argv:
        idx = sys.argv.index("--add-category")
        parent = sys.argv[idx + 1]
        sub = sys.argv[idx + 2]
        label = sys.argv[idx + 3]
        kw = sys.argv[idx + 4:] if len(sys.argv) > idx + 4 else []
        lib.add_category(parent, sub, label, kw)
    else:
        print("📚 个人知识图书馆")
        print("   --scan <dirs...>    扫描目录入库")
        print("   --search <关键词>    全文搜索")
        print("   --browse [--category <分类>]  浏览书架")
        print("   --read <标题> [--status done|reading|unread] [--note <笔记>]  标记阅读")
        print("   --tag <标题> --add <标签>  添加标签")
        print("   --categories        查看分类体系")
        print("   --stats             查看统计")
        print("   --export [--output <path>]  导出目录索引")
        print("   --add-category <父分类> <子分类key> <标签> [关键词...]  添加分类")
        lib.stats()


if __name__ == "__main__":
    main()