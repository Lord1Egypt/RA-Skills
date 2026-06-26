#!/usr/bin/env python3
"""
scorer.py — Resume parsing + NLP match scoring.
Supports: .docx (Word) and .pdf resume formats.
Fixes:
  - jobs with 0 extractable skills → score=None (N/A)
  - jobs with <3 skill matches → score=None (too little signal)
  - PDF support via pymupdf
"""
import json, zipfile, re
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config"
MIN_SKILLS_FOR_SCORING = 3  # Need at least 3 skill signals to produce a meaningful score

def load_skill_keywords(domain):
    with open(CONFIG_DIR / "skill_keywords.json") as f:
        data = json.load(f)
    return [s.lower() for s in data.get(domain, [])]

def extract_resume_text(resume_path):
    """Extract raw text from .docx or .pdf resume."""
    path = Path(resume_path)
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return _extract_docx(path)
    elif suffix == ".pdf":
        return _extract_pdf(path)
    else:
        print(f"  ⚠️  Unsupported resume format: {suffix}. Supported: .docx, .pdf")
        return ""

def _extract_docx(path):
    try:
        with zipfile.ZipFile(path) as z:
            with z.open('word/document.xml') as f:
                content = f.read().decode('utf-8')
        text = re.sub(r'<[^>]+>', ' ', content).lower()
        # Normalize multiple spaces/newlines to single space
        text = re.sub(r'\s+', ' ', text)
        return text
    except Exception as e:
        print(f"  Resume (.docx) parse error: {e}")
        return ""

def _extract_pdf(path):
    try:
        import fitz
        text = ""
        with fitz.open(str(path)) as doc:
            for page in doc:
                text += page.get_text()
        return text.lower()
    except ImportError:
        print("  ⚠️  pymupdf not installed. Run: pip install pymupdf --break-system-packages")
        return ""
    except Exception as e:
        print(f"  Resume (.pdf) parse error: {e}")
        return ""

def extract_known_skills(resume_text, skill_keywords):
    return {skill for skill in skill_keywords if skill in resume_text}

def extract_job_skills(description, skill_keywords):
    if not description:
        return set()
    text = description.lower()
    return {skill for skill in skill_keywords if skill in text}

def compute_match_score(job_skills, known_skills):
    """
    Returns integer 0-100, or None if insufficient skill signals.
    None = unscored (shown as N/A) — NOT inflated to 100%.
    Requires MIN_SKILLS_FOR_SCORING skills in job description to score.
    """
    if len(job_skills) < MIN_SKILLS_FOR_SCORING:
        return None
    matches = job_skills & known_skills
    return round(len(matches) / len(job_skills) * 100)

def is_title_relevant(title, domain_keywords):
    """Filter out obviously irrelevant jobs by title."""
    title_lower = title.lower()
    # Always exclude these regardless of domain
    exclude_titles = [
        # Sales / Marketing / Finance / Legal / HR
        "sales executive", "sales manager", "marketing manager",
        "account executive", "account manager", "business development",
        "finance", "accounting", "legal", "hr ", "recruiter",
        "paid media", "retail", "customer success", "customer service",
        "site contracts", "bilingual", "controller", "copywriter",
        "content writer", "social media", "seo specialist", "brand manager",
        # Product / Project / Business
        "product manager", "program manager", "project manager",
        "business analyst", "scrum master", "agile coach",
        "operations manager", "technical writer", "documentation",
        # Entry level / Intern
        "intern,", "internship", "entry level", "entry-level",
        "junior ", "graduate ", "trainee", "fresh graduate",
        "0-2 years", "1-2 years", "no experience",
        # Other non-engineering
        "designer", "ux researcher", "data entry", "virtual assistant"
    ]
    if any(ex in title_lower for ex in exclude_titles):
        return False
    return True

def score_jobs(jobs, domain, resume_path):
    skill_keywords = load_skill_keywords(domain)
    resume_text = extract_resume_text(resume_path)

    if not resume_text:
        print("  ⚠️  Resume text empty — scoring disabled")
        for job in jobs:
            job["job_skills"] = set()
            job["match_score"] = None
        return jobs, set()

    known_skills = extract_known_skills(resume_text, skill_keywords)
    print(f"  Known skills from resume: {len(known_skills)}")

    # Title relevance filter
    domain_keywords = skill_keywords
    before = len(jobs)
    jobs = [j for j in jobs if is_title_relevant(j.get("title", ""), domain_keywords)]
    filtered = before - len(jobs)
    if filtered:
        print(f"  Title filter: removed {filtered} irrelevant jobs")

    for job in jobs:
        job_skills = extract_job_skills(job.get("description", ""), skill_keywords)
        job["job_skills"] = job_skills
        job["match_score"] = compute_match_score(job_skills, known_skills)

    # Sort: scored high→low, then unscored at bottom
    scored = sorted(
        [j for j in jobs if j["match_score"] is not None],
        key=lambda x: x["match_score"], reverse=True
    )
    unscored = [j for j in jobs if j["match_score"] is None]

    return scored + unscored, known_skills
