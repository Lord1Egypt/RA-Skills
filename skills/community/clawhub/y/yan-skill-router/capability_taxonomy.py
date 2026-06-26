#!/usr/bin/env python3
"""Capability Taxonomy — query→capability→skill 三层抽象

用户 query 先映射到 capability（要做什么），
capability 再解析到具体 skill（用什么做）。
不直接绑 skill 名，避免 skill 装卸/改名导致路由失效。
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Capability:
    """一个能力节点"""
    name: str                     # 英文ID, e.g. "systematic_review"
    zh_name: str                  # 中文名, e.g. "系统综述/Meta分析"
    description: str              # 英文说明（供 embedding 匹配）
    parent: Optional[str] = None  # 父能力, e.g. "literature_research"
    zh_keywords: set = field(default_factory=set)   # 中文触发词
    en_keywords: set = field(default_factory=set)   # 英文触发词
    prefer_skill_patterns: list = field(default_factory=list)  # 优先匹配的skill名模式
    fallback_skills: list = field(default_factory=list)  # 兜底skill（当embedding都不行时）


class CapabilityTaxonomy:
    """
    能力分类树
    
    用法:
        cap = CapabilityTaxonomy()
        matched = cap.detect("做一篇系统综述")
        # → [Capability(name="systematic_review"), ...]
        
        skills = cap.resolve(matched, all_skills)
        # → [skill_idx_42, skill_idx_15]
    """

    def __init__(self):
        self._caps: dict[str, Capability] = {}
        self._zh_index: dict[str, str] = {}    # 中文词 → capability name
        self._en_index: dict[str, str] = {}    # 英文词 → capability name
        self._build()

    # ─── 能力定义 ──────────────────────────────────────────────────────

    def _add(self, cap: Capability):
        """注册一个能力"""
        self._caps[cap.name] = cap
        for kw in cap.zh_keywords:
            self._zh_index[kw] = cap.name
        for kw in cap.en_keywords:
            self._en_index[kw] = cap.name

    def _build(self):
        """构建能力树 —— 从最具体的到最通用的"""
        # ======== 学术研究 ========

        self._add(Capability(
            name="systematic_review",
            zh_name="系统综述/Meta分析",
            description="Systematic review and meta-analysis methodology",
            parent="literature_research",
            zh_keywords={"系统综述","系统评价","meta分析","系统回顾",
                         "森林图","发表偏倚","异质性","meta回归"},
            en_keywords={"systematic review","meta-analysis","metaanalysis",
                         "forest plot","publication bias","heterogeneity"},
            prefer_skill_patterns=["meta-maker","literature-search",
                                    "meta-analysis","systematic"],
            fallback_skills=[],
        ))

        self._add(Capability(
            name="bibliometric",
            zh_name="文献计量分析",
            description="Bibliometric analysis and science mapping",
            parent="literature_research",
            zh_keywords={"文献计量","科学图谱","发文趋势","引文分析",
                         "vosviewer","biblioshiny","共现分析"},
            en_keywords={"bibliometric","science mapping","citation analysis",
                         "vosviewer","co-occurrence"},
            prefer_skill_patterns=["bibliometrician","bibliometrics"],
            fallback_skills=[],
        ))

        self._add(Capability(
            name="literature_search",
            zh_name="文献检索",
            description="Search academic literature across databases",
            parent="literature_research",
            zh_keywords={"文献检索","文献搜索","搜文献","查文献","pubmed",
                         "搜索文献","检索文献","找文献"},
            en_keywords={"literature search","pubmed","academic search",
                         "find papers","search articles"},
            prefer_skill_patterns=["pubmed-search","literature-search",
                                    "pubmed-database","lit-review"],
            fallback_skills=[],
        ))

        self._add(Capability(
            name="guideline",
            zh_name="指南查询",
            description="Clinical guideline and best practice recommendation",
            parent="literature_research",
            zh_keywords={"指南","guideline","临床指南","诊疗指南","专家共识"},
            en_keywords={"guideline","clinical practice guideline",
                         "best practice","recommendation"},
            prefer_skill_patterns=["guideline","clinical-guidelines",
                                    "clinical-decision"],
            fallback_skills=[],
        ))

        self._add(Capability(
            name="reference_citation",
            zh_name="引用管理",
            description="Reference formatting, citation management and bibliography",
            parent="literature_research",
            zh_keywords={"引用","参考文献","参考文献格式","vancouver",
                         "apa格式","引用格式","文献管理"},
            en_keywords={"citation","reference","bibliography",
                         "vancouver","apa format","reference management"},
            prefer_skill_patterns=["citation-manager","reference",
                                    "scientific-writing"],
            fallback_skills=[],
        ))

        # ======== 内容创作 ========

        self._add(Capability(
            name="paper_writing",
            zh_name="论文写作",
            description="Academic paper and manuscript writing",
            parent="content_creation",
            zh_keywords={"写论文","论文写作","写一篇","引言","讨论",
                         "手稿","manuscript","撰写"},
            en_keywords={"write paper","manuscript","academic writing",
                         "draft paper","paper writing"},
            prefer_skill_patterns=["academic-writing","scientific-writing",
                                    "paper-writing","academic-paper"],
            fallback_skills=[],
        ))

        self._add(Capability(
            name="visualization",
            zh_name="图表/可视化",
            description="Data visualization, charts, plots, and figures",
            parent="content_creation",
            zh_keywords={"画图","图表","可视化","森林图","柱状图",
                         "折线图","散点图","热图"},
            en_keywords={"visualization","plot","chart","figure",
                         "forest plot","graph"},
            prefer_skill_patterns=["visualization","bio-data-visualization",
                                    "plotly","seaborn","chart"],
            fallback_skills=[],
        ))

        self._add(Capability(
            name="data_analysis",
            zh_name="数据分析",
            description="Statistical analysis, differential expression, bioinformatics",
            parent="content_creation",
            zh_keywords={"分析","统计分析","差异表达","转录组","基因",
                         "bioinformatics","rna-seq","表达水平"},
            en_keywords={"data analysis","differential expression",
                         "transcriptome","bioinformatics","gene expression",
                         "statistical analysis"},
            prefer_skill_patterns=["geo-database","bio-de","deseq2",
                                    "bio-pathway","gwas"],
            fallback_skills=[],
        ))

        # ======== 操作工具 ========

        self._add(Capability(
            name="email",
            zh_name="发送邮件",
            description="Send email via SMTP",
            parent="operation",
            zh_keywords={"发邮件","发一封","邮件","邮箱","写信"},
            en_keywords={"send email","email","mail"},
            prefer_skill_patterns=["email-sender","agentmail"],
            fallback_skills=[],
        ))

        self._add(Capability(
            name="code_review",
            zh_name="代码审查",
            description="Review source code for quality and security",
            parent="operation",
            zh_keywords={"审查代码","代码审查","审代码","review代码"},
            en_keywords={"code review","review code","code quality"},
            prefer_skill_patterns=["code-review","receiving-code-review",
                                    "requesting-code-review"],
            fallback_skills=[],
        ))

        self._add(Capability(
            name="task_management",
            zh_name="任务管理",
            description="Manage tasks, todos, and priorities",
            parent="operation",
            zh_keywords={"任务","待办","todo","待办事项","优先级","deadline"},
            en_keywords={"task","todo","task management","priority"},
            prefer_skill_patterns=["task-planner","task-tracker","task"],
            fallback_skills=[],
        ))

        self._add(Capability(
            name="system_ops",
            zh_name="系统操作",
            description="System operations like mount, disk check, git",
            parent="operation",
            zh_keywords={"挂载","磁盘","剩余空间","mount","重启","git"},
            en_keywords={"mount","disk","storage","git","restart",
                         "system status"},
            prefer_skill_patterns=["cos-mount","healthcheck","git"],
            fallback_skills=[],
        ))

        # ======== 通用信息查询（应被拒选） ========

        self._add(Capability(
            name="general_info",
            zh_name="通用信息查询",
            description="General knowledge lookup, weather, encyclopedia",
            parent="_rejected",
            zh_keywords={"天气","时间","现在几点","什么是","百科",
                         "用法用量","多少钱"},
            en_keywords={"weather","time","what is","encyclopedia",
                         "definition","price"},
            prefer_skill_patterns=[],
            fallback_skills=[],
        ))

    # ─── 检测 ──────────────────────────────────────────────────────────

    def detect(self, query: str) -> list[str]:
        """
        检测 query 匹配哪些 capability

        返回: 按匹配度排序的 capability name 列表
        匹配度 = 命中关键词数 + 长词优先
        """
        q_lower = query.lower()
        scores: dict[str, float] = {}

        # 中文关键词匹配（优先长词，避免短词误匹配）
        sorted_zh = sorted(self._zh_index.items(), key=lambda x: -len(x[0]))
        for keyword, cap_name in sorted_zh:
            if keyword in query:
                scores[cap_name] = scores.get(cap_name, 0) + len(keyword)  # 长词加分

        # 英文关键词匹配
        for keyword, cap_name in self._en_index.items():
            if keyword in q_lower:
                scores[cap_name] = scores.get(cap_name, 0) + len(keyword)

        # 按分数排序（分数相同则父节点靠前）
        sorted_caps = sorted(scores.items(), key=lambda x: -x[1])

        # 去子留父：如果子能力匹配分够高，返回子能力；否则返回父能力
        results = []
        seen_parents = set()
        for cap_name, score in sorted_caps:
            if score < 2:  # 分数太低，忽略
                continue
            cap = self._caps[cap_name]
            # 如果父能力已经在结果中，且子能力分数更高，替换
            if cap.parent and cap.parent in seen_parents and score > scores.get(cap.parent, 0):
                results = [r for r in results if r != cap.parent]
                seen_parents.discard(cap.parent)
                results.append(cap_name)
                seen_parents.add(cap_name)
            elif cap_name not in seen_parents:
                results.append(cap_name)
                seen_parents.add(cap_name)

        return results

    def resolve(self, cap_names: list[str], all_skills: list[dict],
                top_k: int = 3) -> list[int]:
        """
        能力名 → skill 索引列表

        策略:
        1. 按 prefer_skill_patterns 匹配 skill 名（子串匹配）
        2. 匹配到的按匹配度排序
        3. 不够 top_k 的话... 交给 embedding 去补
        """
        matched_indices: set[int] = set()

        for cap_name in cap_names:
            cap = self._caps.get(cap_name)
            if not cap:
                continue

            for pattern in cap.prefer_skill_patterns:
                pat_lower = pattern.lower()
                for idx, skill in enumerate(all_skills):
                    if idx in matched_indices:
                        continue
                    name = skill.get("name", "").lower()
                    desc = skill.get("description", "").lower()
                    if pat_lower in name or pat_lower in desc:
                        matched_indices.add(idx)

        return list(matched_indices)[:top_k]

    def get_cap(self, name: str) -> Optional[Capability]:
        return self._caps.get(name)

    def list_caps(self, category: str = None) -> list[Capability]:
        if category:
            return [c for c in self._caps.values() if c.parent == category]
        return list(self._caps.values())


# ─── 快速测试 ──────────────────────────────────────────────────────
if __name__ == "__main__":
    cap = CapabilityTaxonomy()
    test_queries = [
        "做一篇新生儿低血糖的系统综述",
        "帮我在PubMed上搜一下脓毒症脑病",
        "帮我画一个森林图",
        "发一封邮件给黄兰",
        "挂载COS桶",
        "今天天气怎么样",
        "查一下头孢曲松的用法用量",
        "做GSE65682的差异表达分析",
        "帮我把参考文献改成Vancouver格式",
    ]
    print("Capability 检测测试:")
    for q in test_queries:
        caps = cap.detect(q)
        print(f"  {q[:40]:42s} → {caps}")
