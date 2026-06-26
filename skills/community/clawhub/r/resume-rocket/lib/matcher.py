"""匹配度评分：规则 + LLM 混合"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class MatchScore:
    tech_score: int = 0
    tech_max: int = 40
    experience_score: int = 0
    experience_max: int = 20
    education_score: int = 0
    education_max: int = 10
    highlights_score: int = 0
    highlights_max: int = 30
    matched_keywords: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.tech_score + self.experience_score + self.education_score + self.highlights_score

    def report(self) -> str:
        bar = lambda s, m: "#" * (s * 10 // max(m, 1)) + "-" * (10 - s * 10 // max(m, 1))
        lines = [
            f"# 匹配度报告",
            f"",
            f"## 总分: **{self.total}/100**",
            f"",
            f"| 维度 | 得分 | 可视化 |",
            f"|---|---|---|",
            f"| 技术栈 | {self.tech_score}/{self.tech_max} | `{bar(self.tech_score, self.tech_max)}` |",
            f"| 工作年限 | {self.experience_score}/{self.experience_max} | `{bar(self.experience_score, self.experience_max)}` |",
            f"| 学历 | {self.education_score}/{self.education_max} | `{bar(self.education_score, self.education_max)}` |",
            f"| 亮点项目 | {self.highlights_score}/{self.highlights_max} | `{bar(self.highlights_score, self.highlights_max)}` |",
            f"",
            f"## ✅ 已命中关键词 ({len(self.matched_keywords)})",
            "- " + "\n- ".join(self.matched_keywords) if self.matched_keywords else "_无_",
            f"",
            f"## ❌ 缺失关键词 ({len(self.missing_keywords)})",
            "- " + "\n- ".join(self.missing_keywords) if self.missing_keywords else "_无_",
            f"",
            f"## 💡 改写建议",
            "- " + "\n- ".join(self.suggestions) if self.suggestions else "_无_",
        ]
        return "\n".join(lines)


def score_match(resume, jd) -> MatchScore:
    s = MatchScore()
    resume_text = (resume.raw_text + " " + " ".join(resume.skills)).lower()

    matched, missing = [], []
    for kw in jd.keywords:
        if kw.lower() in resume_text:
            matched.append(kw)
        else:
            missing.append(kw)
    s.matched_keywords = matched
    s.missing_keywords = missing

    if jd.keywords:
        s.tech_score = round(len(matched) / len(jd.keywords) * s.tech_max)
    else:
        s.tech_score = s.tech_max // 2

    s.experience_score = s.experience_max if resume.experiences else s.experience_max // 2
    s.education_score = s.education_max
    s.highlights_score = min(s.highlights_max, len(resume.experiences) * 8 + 5)

    if missing:
        s.suggestions.append(f"简历中缺少 JD 要求的关键能力：{', '.join(missing[:5])}。考虑从现有项目中挖掘相关经验或学习并补充。")
    if not resume.experiences:
        s.suggestions.append("工作经历部分识别失败，请检查简历格式是否标准。")
    if len(matched) < 3 and jd.keywords:
        s.suggestions.append("关键词命中率过低，建议在工作经历里用 JD 原词重新表达。")
    if resume.experiences and all(len(e.bullets) < 2 for e in resume.experiences):
        s.suggestions.append("工作经历 bullet points 偏少，每段建议 3-5 条 STAR 结构描述。")

    return s
