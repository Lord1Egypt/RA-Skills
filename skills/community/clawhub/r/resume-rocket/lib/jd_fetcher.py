"""JD 抓取：Boss 直聘 URL / 拉勾 / 纯文本"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import re
import urllib.parse


@dataclass
class JD:
    title: str = ""
    company: str = ""
    location: str = ""
    salary: str = ""
    years_required: str = ""
    education_required: str = ""
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    must_have: List[str] = field(default_factory=list)
    nice_to_have: List[str] = field(default_factory=list)


def _is_url(s: str) -> bool:
    return s.startswith(("http://", "https://"))


def _fetch_boss(url: str) -> JD:
    """用已有的 boss-zhipin skill 抓，或退到通用 HTML 抓取。"""
    try:
        import requests
    except ImportError:
        raise RuntimeError("请先 pip install requests")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    resp = requests.get(url, headers=headers, timeout=15)
    html = resp.text

    jd = JD()
    t = re.search(r'<h1[^>]*class="[^"]*name[^"]*"[^>]*>\s*([^<]+)', html)
    if t:
        jd.title = t.group(1).strip()
    c = re.search(r'<h3[^>]*class="[^"]*company-name[^"]*"[^>]*>[\s\S]*?>([^<]+)', html)
    if c:
        jd.company = c.group(1).strip()
    desc = re.search(r'<div[^>]*class="[^"]*job-sec-text[^"]*"[^>]*>([\s\S]*?)</div>', html)
    if desc:
        jd.description = re.sub(r"<[^>]+>", "\n", desc.group(1)).strip()

    if not jd.description:
        jd.description = re.sub(r"<[^>]+>", "\n", html)[:3000]

    return _enrich_keywords(jd)


def _parse_text(text: str) -> JD:
    jd = JD(description=text)
    first_line = (text.splitlines() or [""])[0][:40]
    jd.title = first_line
    return _enrich_keywords(jd)


_TECH_POOL = {
    "python", "java", "go", "golang", "rust", "c++", "c#", "javascript", "typescript",
    "react", "vue", "angular", "node", "next.js", "nuxt",
    "spring", "django", "flask", "fastapi",
    "mysql", "postgresql", "redis", "mongodb", "elasticsearch", "clickhouse",
    "kafka", "rabbitmq", "rocketmq", "spark", "flink", "hadoop", "hive",
    "docker", "kubernetes", "k8s", "jenkins", "gitlab", "ci/cd",
    "aws", "aliyun", "阿里云", "腾讯云", "gcp",
    "llm", "大模型", "rag", "agent", "langchain", "tensorflow", "pytorch",
    "机器学习", "深度学习", "nlp", "cv", "推荐系统", "数据分析", "数据挖掘",
    "sql", "etl", "数据仓库", "bi",
    "linux", "shell", "git",
}


def _enrich_keywords(jd: JD) -> JD:
    text = (jd.title + "\n" + jd.description).lower()
    hits = []
    for tech in _TECH_POOL:
        if tech.lower() in text:
            hits.append(tech)
    jd.keywords = hits

    yr = re.search(r"(\d+)\s*[-到至~]\s*(\d+)\s*年", text)
    if yr:
        jd.years_required = f"{yr.group(1)}-{yr.group(2)} 年"
    edu = re.search(r"(本科|硕士|博士|大专|不限)", text)
    if edu:
        jd.education_required = edu.group(1)

    must_kw = re.findall(r"(?:必须|要求|需要|必备)[：:]\s*([^\n。；]+)", text)
    jd.must_have = [k.strip() for k in must_kw[:5]]
    nice_kw = re.findall(r"(?:加分|优先|熟悉更好)[：:]?\s*([^\n。；]+)", text)
    jd.nice_to_have = [k.strip() for k in nice_kw[:5]]
    return jd


def fetch_jd(source: str) -> JD:
    if _is_url(source):
        host = urllib.parse.urlparse(source).netloc
        if "zhipin" in host:
            return _fetch_boss(source)
        import requests
        html = requests.get(source, timeout=15).text
        text = re.sub(r"<[^>]+>", "\n", html)
        return _parse_text(text[:5000])
    return _parse_text(source)
