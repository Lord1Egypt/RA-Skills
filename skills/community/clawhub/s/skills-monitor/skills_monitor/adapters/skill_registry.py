"""
Skill 注册与发现 — 读取已安装 skills 的元数据
构建统一的 skill 注册表
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class SkillInfo:
    """单个 skill 的元信息"""

    def __init__(
        self,
        slug: str,
        name: str = "",
        version: str = "",
        description: str = "",
        category: str = "未分类",
        entry_file: str = "",
        entry_type: str = "unknown",  # cli / function / none
        dir_path: str = "",
        meta: Optional[Dict] = None,
    ):
        self.slug = slug
        self.name = name or slug
        self.version = version
        self.description = description
        self.category = category
        self.entry_file = entry_file
        self.entry_type = entry_type
        self.dir_path = dir_path
        self.meta = meta or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slug": self.slug,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "category": self.category,
            "entry_file": self.entry_file,
            "entry_type": self.entry_type,
            "dir_path": self.dir_path,
        }


# 分类映射（基于 slug 关键词）
CATEGORY_RULES = [
    (r"(data|real-time|clouddream)", "数据采集"),
    (r"(macro|gdp|cpi)", "宏观分析"),
    (r"(news|finance-news)", "新闻情报"),
    (r"(screen|analysis|research|stock-analysis)", "技术筛选"),
    (r"(signal|trading|decision)", "交易信号"),
    (r"(monitor)", "量化监控"),
    (r"(backtest|strategy)", "策略回测"),
    (r"(chart|image|render)", "可视化"),
    (r"(celebrity|hot-money|money-flow)", "资金追踪"),
    (r"(doc|webhook|search|robot)", "工具/通知"),
]


def _classify_skill(slug: str, description: str = "") -> str:
    """根据 slug 和描述推断分类"""
    text = f"{slug} {description}".lower()
    for pattern, category in CATEGORY_RULES:
        if re.search(pattern, text):
            return category
    return "未分类"


def _parse_skill_md(skill_md_path: str) -> Dict[str, str]:
    """从 SKILL.md 的 frontmatter 中提取 name 和 description"""
    result = {"name": "", "description": ""}
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 解析 YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.split("\n"):
                    line = line.strip()
                    if line.startswith("name:"):
                        result["name"] = line[5:].strip().strip('"').strip("'")
                    elif line.startswith("description:"):
                        result["description"] = line[12:].strip().strip('"').strip("'")
    except Exception:
        pass
    return result


def _find_entry_file(skill_dir: str) -> tuple:
    """查找 skill 的入口文件，返回 (entry_file, entry_type)"""
    # 优先级：main.py > scripts/main.py > scripts/*.py > index.py
    candidates = [
        ("main.py", "cli"),
        ("scripts/main.py", "cli"),
        ("index.py", "function"),
    ]
    
    for rel_path, entry_type in candidates:
        full_path = os.path.join(skill_dir, rel_path)
        if os.path.isfile(full_path):
            return rel_path, entry_type
    
    # 扫描 scripts/ 下的 .py 文件
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts_dir):
        py_files = [f for f in os.listdir(scripts_dir) if f.endswith(".py")]
        if py_files:
            return f"scripts/{py_files[0]}", "cli"
    
    return "", "none"


class SkillRegistry:
    """Skill 注册表"""

    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir
        self._skills: Dict[str, SkillInfo] = {}
        self._scan()

    def _scan(self):
        """扫描 skills 目录，构建注册表"""
        if not os.path.isdir(self.skills_dir):
            return

        for entry in os.listdir(self.skills_dir):
            subdir = os.path.join(self.skills_dir, entry)
            if not os.path.isdir(subdir) or entry.startswith((".","_","__")):
                continue

            meta_path = os.path.join(subdir, "_meta.json")
            skill_md_path = os.path.join(subdir, "SKILL.md")

            # 读取 _meta.json
            meta = {}
            slug = entry
            version = ""
            if os.path.isfile(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    slug = meta.get("slug", entry)
                    version = meta.get("version", "")
                except Exception:
                    pass

            # 读取 SKILL.md
            md_info = _parse_skill_md(skill_md_path) if os.path.isfile(skill_md_path) else {}

            # 查找入口
            entry_file, entry_type = _find_entry_file(subdir)

            # 分类
            category = _classify_skill(slug, md_info.get("description", ""))

            info = SkillInfo(
                slug=slug,
                name=md_info.get("name", "") or slug,
                version=version,
                description=md_info.get("description", ""),
                category=category,
                entry_file=entry_file,
                entry_type=entry_type,
                dir_path=subdir,
                meta=meta,
            )
            self._skills[slug] = info

    def list_skills(self) -> List[SkillInfo]:
        """列出所有已注册的 skills"""
        return list(self._skills.values())

    def get_skill(self, slug: str) -> Optional[SkillInfo]:
        """获取指定 skill"""
        return self._skills.get(slug)

    def get_runnable_skills(self) -> List[SkillInfo]:
        """获取有可执行入口的 skills"""
        return [s for s in self._skills.values() if s.entry_type != "none"]

    def get_skills_by_category(self) -> Dict[str, List[SkillInfo]]:
        """按分类获取 skills"""
        result: Dict[str, List[SkillInfo]] = {}
        for s in self._skills.values():
            result.setdefault(s.category, []).append(s)
        return result

    def summary(self) -> str:
        """返回汇总信息"""
        total = len(self._skills)
        runnable = len(self.get_runnable_skills())
        categories = self.get_skills_by_category()
        
        lines = [
            f"📦 已注册 Skills: {total} 个 (可执行: {runnable} 个)",
            "",
        ]
        for cat, skills in sorted(categories.items()):
            slugs = ", ".join(s.slug for s in skills)
            lines.append(f"  [{cat}] {slugs}")
        
        return "\n".join(lines)
