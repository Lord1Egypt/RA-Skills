"""简历解析：PDF / DOCX / MD / TXT → 结构化 Resume"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
import re


@dataclass
class Experience:
    company: str = ""
    title: str = ""
    period: str = ""
    bullets: List[str] = field(default_factory=list)


@dataclass
class Resume:
    raw_text: str = ""
    name: str = ""
    contact: str = ""
    summary: str = ""
    experiences: List[Experience] = field(default_factory=list)
    projects: List[Experience] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    education: List[str] = field(default_factory=list)


def _read_pdf(path: Path) -> str:
    try:
        import pdfplumber
    except ImportError:
        raise RuntimeError("请先 pip install pdfplumber")
    parts = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n".join(parts)


def _read_docx(path: Path) -> str:
    try:
        import docx
    except ImportError:
        raise RuntimeError("请先 pip install python-docx")
    d = docx.Document(str(path))
    return "\n".join(p.text for p in d.paragraphs if p.text.strip())


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _extract_sections(text: str) -> Resume:
    """简单规则分段；后续可用 LLM 强化。"""
    r = Resume(raw_text=text)

    # 姓名：第一非空行
    for line in text.splitlines():
        line = line.strip()
        if line and len(line) < 20:
            r.name = line
            break

    # 联系方式：找手机号 + 邮箱
    phone = re.search(r"1[3-9]\d{9}", text)
    email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    r.contact = " / ".join(x.group() for x in (phone, email) if x)

    # 技能：找"技能"段到下一个标题
    sk = re.search(r"(?:技能|技术栈|skills?)\s*[:：\n]+([\s\S]{0,400}?)(?:\n\n|项目|工作|教育|自我)", text, re.IGNORECASE)
    if sk:
        raw = sk.group(1)
        tokens = re.split(r"[,、,/;；\n\s]+", raw)
        r.skills = [t.strip() for t in tokens if 1 < len(t.strip()) < 30]

    # 工作经历：粗暴按"公司 + 日期"启发式分段
    exp_block = re.search(r"(?:工作经历|工作经验|experience)([\s\S]+?)(?:项目经历|项目经验|教育|自我评价|$)", text, re.IGNORECASE)
    if exp_block:
        blocks = re.split(r"\n(?=\S.*(?:20\d{2}|19\d{2}))", exp_block.group(1))
        for b in blocks:
            b = b.strip()
            if not b:
                continue
            lines = [l.strip("-• \t") for l in b.splitlines() if l.strip()]
            if not lines:
                continue
            e = Experience()
            e.company = lines[0][:60]
            if len(lines) > 1:
                e.title = lines[1][:40]
            e.bullets = [l for l in lines[2:] if len(l) > 5][:10]
            r.experiences.append(e)

    return r


def parse_resume(path: Path) -> Resume:
    if not path.exists():
        raise FileNotFoundError(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text = _read_pdf(path)
    elif suffix in (".docx", ".doc"):
        text = _read_docx(path)
    else:
        text = _read_text(path)
    return _extract_sections(text)
