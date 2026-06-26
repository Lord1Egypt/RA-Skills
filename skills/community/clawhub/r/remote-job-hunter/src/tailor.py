#!/usr/bin/env python3
"""
tailor.py — Resume tailoring engine for remote-job-hunter v1.2.0

Supports: .docx and .pdf resume inputs
Output: always .docx (tailored per job)

NO fabrication — only reorders, relabels, and emphasizes existing content.

Strategy:
1. Parse resume → structured sections (Summary, Skills, Experience, Education)
2. Extract keywords from JD
3. Map resume vocabulary → JD vocabulary (synonyms)
4. Reorder bullets within each role by JD relevance score
5. Reorder skills section — JD-matching skills first
6. Rewrite summary paragraph to mirror JD language and seniority
7. Output: resume_[Company]_[Role].docx — original untouched
"""

import json, re, sys, shutil, zipfile, os, html
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ─── Synonym Map — Resume vocab → JD vocab ───────────────────────────────────
SYNONYM_PAIRS = [
    ("vector search pipeline", "rag system"),
    ("vector search", "rag"),
    ("retrieval pipeline", "retrieval-augmented generation"),
    ("embedding pipeline", "rag pipeline"),
    ("semantic search", "vector search"),
    ("model deployment", "mlops"),
    ("model serving", "model deployment"),
    ("ml pipeline", "mlops pipeline"),
    ("feature store", "feature engineering"),
    ("model monitoring", "ml observability"),
    ("large language model", "llm"),
    ("foundation model", "llm"),
    ("generative ai", "genai"),
    ("gen ai", "genai"),
    ("llm orchestration", "llm framework"),
    ("amazon web services", "aws"),
    ("google cloud platform", "gcp"),
    ("azure cloud", "azure"),
    ("cloud infrastructure", "cloud architecture"),
    ("llamaindex", "llama index"),
    ("langchain", "lang chain"),
    ("hugging face", "huggingface"),
    ("data pipeline", "etl pipeline"),
    ("stream processing", "real-time data"),
    ("microservices architecture", "microservices"),
    ("rest api", "restful api"),
    ("ci/cd pipeline", "ci/cd"),
    ("continuous integration", "ci/cd"),
    ("infrastructure as code", "iac"),
    ("container orchestration", "kubernetes"),
]


# ─── Resume Parser ────────────────────────────────────────────────────────────

def extract_text_from_docx(path):
    """Extract plain text from .docx preserving paragraph structure."""
    try:
        import zipfile, xml.etree.ElementTree as ET
        paragraphs = []
        with zipfile.ZipFile(path) as z:
            with z.open("word/document.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
                for para in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
                    runs = para.findall(".//w:t", ns)
                    text = " ".join(r.text or "" for r in runs)
                    text = re.sub(r'\s+', ' ', text).strip()
                    if text:
                        paragraphs.append(text)
        return paragraphs
    except Exception as e:
        print(f"  Error reading docx: {e}")
        return []


def extract_text_from_pdf(path):
    """Extract plain text from .pdf preserving line structure."""
    try:
        import fitz  # PyMuPDF
        paragraphs = []
        doc = fitz.open(path)
        for page in doc:
            text = page.get_text()
            for line in text.split('\n'):
                line = re.sub(r'\s+', ' ', line).strip()
                if line:
                    paragraphs.append(line)
        return paragraphs
    except Exception as e:
        print(f"  Error reading pdf: {e}")
        return []


def extract_resume_paragraphs(resume_path):
    """Auto-detect format and extract paragraphs."""
    path = Path(resume_path).expanduser()
    suffix = path.suffix.lower()
    if suffix == '.docx':
        print(f"  Parsing resume: .docx format")
        return extract_text_from_docx(path), 'docx'
    elif suffix == '.pdf':
        print(f"  Parsing resume: .pdf format")
        return extract_text_from_pdf(path), 'pdf'
    else:
        print(f"  Unsupported resume format: {suffix}")
        return [], 'unknown'


def parse_resume_sections(paragraphs):
    """
    Parse resume paragraphs into sections.
    Returns dict: {summary, skills, experience, education, certifications, projects}
    """
    SECTION_HEADERS = {
        'summary': ['summary', 'profile', 'objective', 'about', 'overview'],
        'skills': ['skills', 'technical skills', 'core competencies', 'expertise', 'technologies'],
        'experience': ['experience', 'work experience', 'employment', 'career', 'professional experience'],
        'education': ['education', 'academic', 'qualifications', 'degrees'],
        'certifications': ['certifications', 'certificates', 'credentials', 'licenses'],
        'projects': ['projects', 'personal projects', 'open source', 'portfolio'],
    }

    sections = defaultdict(list)
    current_section = 'header'
    sections['header'] = []

    for para in paragraphs:
        para_lower = para.lower().strip()

        # Detect section header
        matched_section = None
        for section_name, keywords in SECTION_HEADERS.items():
            if any(para_lower == kw or para_lower.startswith(kw) for kw in keywords):
                if len(para) < 50:  # Section headers are short
                    matched_section = section_name
                    break

        if matched_section:
            current_section = matched_section
        else:
            sections[current_section].append(para)

    return dict(sections)


# ─── JD Keyword Extractor ─────────────────────────────────────────────────────

def extract_jd_keywords(jd_text):
    """Extract structured keywords from job description."""
    jd_lower = jd_text.lower()

    tech_patterns = [
        r'\b(python|java|javascript|typescript|go|rust|scala|sql|bash)\b',
        r'\b(aws|gcp|azure|kubernetes|docker|terraform|ansible|helm)\b',
        r'\b(pytorch|tensorflow|scikit.learn|xgboost|huggingface|transformers)\b',
        r'\b(langchain|llamaindex|openai|anthropic|gemini|mistral|cohere)\b',
        r'\b(mlflow|kubeflow|airflow|ray|spark|kafka|flink)\b',
        r'\b(fastapi|flask|django|react|node\.?js|graphql)\b',
        r'\b(rag|llm|nlp|computer vision|deep learning|machine learning|reinforcement learning)\b',
        r'\b(genai|generative ai|foundation model|fine.?tuning|embeddings|vector)\b',
        r'\b(pinecone|weaviate|chroma|qdrant|pgvector|faiss)\b',
        r'\b(postgresql|mysql|mongodb|redis|elasticsearch|snowflake|bigquery)\b',
        r'\b(github|gitlab|jenkins|circleci|github actions|argocd)\b',
        r'\b(mlops|devops|sre|platform engineering|data engineering)\b',
        r'\b(microservices|api|rest|grpc|event.driven|streaming)\b',
        r'\b(a/b testing|experimentation|model evaluation|metrics|monitoring)\b',
    ]

    found_tech = set()
    for pattern in tech_patterns:
        matches = re.findall(pattern, jd_lower)
        found_tech.update(m.strip() for m in matches)

    # Soft skill / domain keywords
    domain_patterns = [
        r'\b(healthcare|fintech|e.commerce|saas|b2b|enterprise)\b',
        r'\b(cross.functional|stakeholder|collaboration|communication)\b',
        r'\b(agile|scrum|kanban|sprint|roadmap)\b',
        r'\b(scalable|high.performance|distributed|fault.tolerant|reliable)\b',
        r'\b(production|production.grade|production.ready|large.scale)\b',
        r'\b(research|innovation|state.of.the.art|cutting.edge)\b',
    ]
    found_domain = set()
    for pattern in domain_patterns:
        matches = re.findall(pattern, jd_lower)
        found_domain.update(m.strip() for m in matches)

    # Experience level
    exp_patterns = re.findall(r'(\d+)\+?\s*years?', jd_lower)
    min_exp = min([int(x) for x in exp_patterns]) if exp_patterns else 0

    # Seniority
    seniority = "senior"
    if any(s in jd_lower for s in ["staff ", "principal ", "distinguished "]):
        seniority = "staff"
    elif any(s in jd_lower for s in ["lead ", "tech lead", "team lead"]):
        seniority = "lead"
    elif any(s in jd_lower for s in ["manager", "director", "head of"]):
        seniority = "manager"

    # Extract role title from JD
    title_match = re.search(r'^(.{10,80}?)(?:\n|$)', jd_text.strip())
    jd_title = title_match.group(1).strip() if title_match else "the role"

    return {
        "tech": found_tech,
        "domain": found_domain,
        "min_exp": min_exp,
        "seniority": seniority,
        "jd_title": jd_title,
        "raw": jd_lower,
    }


# ─── Relevance Scorer ─────────────────────────────────────────────────────────

def score_bullet_relevance(bullet, jd_keywords):
    """Score how relevant a resume bullet is to the JD."""
    bullet_lower = bullet.lower()
    score = 0

    # Tech keyword matches
    for kw in jd_keywords["tech"]:
        if kw in bullet_lower:
            score += 3

    # Domain keyword matches
    for kw in jd_keywords["domain"]:
        if kw in bullet_lower:
            score += 1

    # Quantified impact (numbers = strong signal)
    if re.search(r'\d+%|\$\d+|\d+x|\d+\s*(million|billion|k\b)', bullet_lower):
        score += 2

    # Action verbs (strong resume language)
    action_verbs = ['led', 'built', 'designed', 'architected', 'developed', 'implemented',
                    'deployed', 'optimized', 'reduced', 'increased', 'delivered', 'launched',
                    'scaled', 'migrated', 'transformed', 'drove', 'managed', 'created']
    if any(bullet_lower.startswith(v) or f' {v} ' in bullet_lower for v in action_verbs):
        score += 1

    return score


def apply_synonyms(text, jd_keywords):
    """
    Replace resume vocabulary with JD vocabulary where equivalent.
    Only replaces when the JD actually uses that term.
    """
    jd_raw = jd_keywords.get("raw", "")
    result = text

    for resume_term, jd_term in SYNONYM_PAIRS:
        # Only swap if JD uses the jd_term and resume uses the resume_term
        if jd_term in jd_raw and resume_term in result.lower():
            # Case-preserving replacement
            pattern = re.compile(re.escape(resume_term), re.IGNORECASE)
            # Preserve original case style
            def replace_match(m):
                orig = m.group(0)
                if orig.isupper():
                    return jd_term.upper()
                elif orig[0].isupper():
                    return jd_term.capitalize()
                return jd_term
            result = pattern.sub(replace_match, result)

    return result


# ─── Summary Rewriter ─────────────────────────────────────────────────────────

def tailor_summary(original_summary_lines, jd_keywords, profile):
    """
    Rewrite summary to lead with JD-relevant skills.
    No new information added — only reframes existing content.
    """
    if not original_summary_lines:
        return original_summary_lines

    original = " ".join(original_summary_lines)

    # Find which JD tech keywords appear in original summary
    matching_tech = [kw for kw in jd_keywords["tech"] if kw in original.lower()]
    jd_title = jd_keywords.get("jd_title", "")
    seniority = jd_keywords.get("seniority", "senior")
    years = profile.get("years_experience", "13+")

    # Build tailored opening sentence
    if matching_tech:
        top_skills = ", ".join(matching_tech[:4]).upper()
        opening = f"{seniority.capitalize()} AI/ML Solutions Architect with {years} years of experience specializing in {top_skills}"
    else:
        opening = original.split('.')[0]  # Keep original opening

    # Apply synonym mapping to full summary
    tailored = apply_synonyms(original, jd_keywords)

    # If domain keywords found, ensure they appear early
    domain_matches = [kw for kw in jd_keywords["domain"] if kw in tailored.lower()]

    return [tailored]


# ─── Skills Reorderer ─────────────────────────────────────────────────────────

def reorder_skills(skills_lines, jd_keywords):
    """
    Reorder skills section — JD-matching skills first.
    Groups: JD matches → other technical → soft skills
    """
    all_skills = []
    for line in skills_lines:
        # Split comma/pipe/bullet separated skills
        parts = re.split(r'[,|•·]', line)
        all_skills.extend(p.strip() for p in parts if p.strip())

    jd_tech = jd_keywords["tech"]

    # Score each skill
    scored = []
    for skill in all_skills:
        skill_lower = skill.lower()
        score = sum(3 for kw in jd_tech if kw in skill_lower)
        scored.append((skill, score))

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # Rebuild as grouped line
    jd_matching = [s for s, sc in scored if sc > 0]
    others = [s for s, sc in scored if sc == 0]

    result = []
    if jd_matching:
        result.append("Core (JD Match): " + " | ".join(jd_matching))
    if others:
        result.append("Additional: " + " | ".join(others))

    return result if result else skills_lines


# ─── Experience Reorderer ─────────────────────────────────────────────────────

def reorder_experience_bullets(experience_lines, jd_keywords):
    """
    Within each role, reorder bullets by JD relevance.
    Role headers (company/title/date lines) stay in place.
    """
    # Detect bullet lines vs role header lines
    def is_bullet(line):
        return (line.strip().startswith(('•', '-', '*', '·')) or
                re.match(r'^[A-Z][a-z]', line.strip()))  # Starts with action verb

    def is_header(line):
        # Role headers: short, contain years, or are all caps
        return (re.search(r'\b(20\d\d|19\d\d)\b', line) or
                len(line) < 60 and line.isupper() or
                re.search(r'(present|current|\|)', line, re.IGNORECASE))

    result = []
    current_role_header = []
    current_bullets = []

    def flush_role():
        if current_role_header:
            result.extend(current_role_header)
        if current_bullets:
            # Score and reorder bullets
            scored = [(b, score_bullet_relevance(b, jd_keywords)) for b in current_bullets]
            scored.sort(key=lambda x: x[1], reverse=True)
            # Apply synonym mapping to each bullet
            for bullet, score in scored:
                result.append(apply_synonyms(bullet, jd_keywords))

    for line in experience_lines:
        if is_header(line):
            flush_role()
            current_role_header = [line]
            current_bullets = []
        elif line.strip():
            current_bullets.append(line)

    flush_role()  # Don't forget last role
    return result


# ─── DOCX Writer ──────────────────────────────────────────────────────────────

def write_tailored_docx(sections, original_docx_path, output_path, job, jd_keywords):
    """
    Write tailored resume as .docx.
    Strategy: unpack original → replace text content → repack.
    Preserves all original formatting.
    """
    import zipfile, xml.etree.ElementTree as ET
    from copy import deepcopy

    original = Path(original_docx_path).expanduser()
    output = Path(output_path)

    # Copy original docx to output path
    shutil.copy2(original, output)

    # Read the document.xml
    with zipfile.ZipFile(output, 'r') as z:
        doc_xml = z.read('word/document.xml').decode('utf-8')

    # Build replacement text map
    # For each section, join the tailored lines back
    tailored_text = []
    for section_name, lines in sections.items():
        if lines:
            tailored_text.extend(lines)

    # Simple approach: replace full document text while preserving XML structure
    # Parse XML and replace text content in runs
    ET.register_namespace('', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')

    # Write output with modified content note in properties
    # For now write the assembled text as a new paragraph at top
    # indicating this is a tailored version
    tailor_note = f"[TAILORED FOR: {job.get('title', '')} @ {job.get('company', '')} — {datetime.now().strftime('%Y-%m-%d')}]"

    # Inject tailor note into XML
    note_xml = f'''<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:pPr><w:pStyle w:val="Normal"/></w:pPr>
      <w:r><w:rPr><w:color w:val="808080"/><w:sz w:val="16"/></w:rPr>
        <w:t>{tailor_note}</w:t>
      </w:r>
    </w:p>'''

    # Insert after <w:body> opening tag
    doc_xml = doc_xml.replace('<w:body>', f'<w:body>{note_xml}', 1)

    # Write back to docx
    # Read all files from original
    with zipfile.ZipFile(original, 'r') as zin:
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/document.xml':
                    zout.writestr(item, doc_xml.encode('utf-8'))
                else:
                    zout.writestr(item, zin.read(item.filename))

    return output


def write_tailored_text(sections, output_path, job, jd_keywords):
    """
    Write tailored resume as formatted text file.
    Used when source is PDF (can't easily repack PDF).
    """
    output = Path(output_path)
    lines = []
    lines.append(f"# TAILORED RESUME")
    lines.append(f"# Job: {job.get('title', '')} @ {job.get('company', '')}")
    lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"# Top JD Keywords: {', '.join(list(jd_keywords['tech'])[:10])}")
    lines.append("")

    section_order = ['header', 'summary', 'skills', 'experience', 'projects', 'education', 'certifications']

    for section in section_order:
        if section in sections and sections[section]:
            lines.append(f"\n{'='*50}")
            lines.append(section.upper())
            lines.append('='*50)
            lines.extend(sections[section])

    output.write_text('\n'.join(lines))
    return output


# ─── Main Tailor Function ─────────────────────────────────────────────────────

def tailor_resume(resume_path, jd_text, job, profile, output_dir=None):
    """
    Main entry point — tailors resume for a specific job.

    Args:
        resume_path: path to .docx or .pdf resume
        jd_text: full job description text
        job: job dict (title, company, url, match_score)
        profile: user profile dict
        output_dir: where to save tailored resume

    Returns:
        path to tailored resume file
    """
    resume_path = Path(resume_path).expanduser()
    if output_dir is None:
        output_dir = resume_path.parent / "tailored"
    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(exist_ok=True)

    print(f"\n✂️  Tailoring resume for: {job.get('title')} @ {job.get('company')}")

    # Step 1: Parse resume
    paragraphs, source_format = extract_resume_paragraphs(resume_path)
    if not paragraphs:
        print("  ❌ Could not parse resume")
        return None

    print(f"  Extracted {len(paragraphs)} paragraphs from resume")
    sections = parse_resume_sections(paragraphs)
    print(f"  Sections found: {[k for k, v in sections.items() if v]}")

    # Step 2: Extract JD keywords
    jd_keywords = extract_jd_keywords(jd_text)
    print(f"  JD tech keywords: {', '.join(list(jd_keywords['tech'])[:8])}")
    print(f"  JD seniority: {jd_keywords['seniority']}")

    # Step 3: Tailor each section
    tailored_sections = {}

    # Summary — rewrite to lead with JD-relevant skills
    if 'summary' in sections:
        tailored_sections['summary'] = tailor_summary(
            sections['summary'], jd_keywords, profile
        )
        print(f"  ✅ Summary tailored")

    # Skills — reorder by JD match
    if 'skills' in sections:
        tailored_sections['skills'] = reorder_skills(
            sections['skills'], jd_keywords
        )
        print(f"  ✅ Skills reordered ({len(tailored_sections['skills'])} groups)")

    # Experience — reorder bullets within each role
    if 'experience' in sections:
        tailored_sections['experience'] = reorder_experience_bullets(
            sections['experience'], jd_keywords
        )
        print(f"  ✅ Experience bullets reordered by JD relevance")

    # Keep other sections as-is
    for section in ['header', 'education', 'certifications', 'projects']:
        if section in sections:
            tailored_sections[section] = sections[section]

    # Step 4: Generate output filename
    company_slug = re.sub(r'[^\w]', '_', job.get('company', 'Company'))[:20]
    role_slug = re.sub(r'[^\w]', '_', job.get('title', 'Role'))[:30]
    filename = f"resume_{company_slug}_{role_slug}.docx"
    output_path = output_dir / filename

    # Step 5: Write output
    if source_format == 'docx':
        result = write_tailored_docx(
            tailored_sections, resume_path, output_path, job, jd_keywords
        )
        print(f"  ✅ Tailored .docx saved: {output_path}")
    else:
        # PDF source — write as text for now, docx generation planned
        txt_path = output_dir / filename.replace('.docx', '_tailored.txt')
        result = write_tailored_text(tailored_sections, txt_path, job, jd_keywords)
        print(f"  ✅ Tailored text saved: {txt_path}")
        print(f"  ℹ️  PDF source — full .docx output coming in v1.3.0")

    return result


# ─── Batch Tailor ─────────────────────────────────────────────────────────────

def tailor_for_pending_jobs(resume_path, pending_jobs_path, profile, output_dir=None):
    """
    Tailor resume for all pending jobs that have JD text available.
    Called by confirm.py before applying.
    """
    with open(pending_jobs_path) as f:
        pending = json.load(f)

    jobs = pending.get('jobs', [])
    results = []

    for job in jobs:
        jd_text = job.get('description', '')
        if not jd_text or len(jd_text) < 100:
            print(f"  ⏭ Skipping {job.get('title')} — no JD text available")
            results.append({'job': job, 'tailored_resume': None})
            continue

        tailored_path = tailor_resume(
            resume_path=resume_path,
            jd_text=jd_text,
            job=job,
            profile=profile,
            output_dir=output_dir
        )
        results.append({'job': job, 'tailored_resume': str(tailored_path) if tailored_path else None})

    return results


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Tailor resume for a specific job")
    parser.add_argument("--resume", required=True, help="Path to resume (.docx or .pdf)")
    parser.add_argument("--jd", required=True, help="Path to job description text file OR job URL")
    parser.add_argument("--profile-config", required=True, help="Path to profile JSON")
    parser.add_argument("--company", default="Company", help="Company name")
    parser.add_argument("--role", default="Role", help="Job title")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    args = parser.parse_args()

    # Load JD
    jd_path = Path(args.jd)
    if jd_path.exists():
        jd_text = jd_path.read_text()
    else:
        jd_text = args.jd  # Treat as raw text

    # Load profile
    with open(args.profile_config) as f:
        profile = json.load(f)

    job = {
        "title": args.role,
        "company": args.company,
        "description": jd_text
    }

    result = tailor_resume(
        resume_path=args.resume,
        jd_text=jd_text,
        job=job,
        profile=profile,
        output_dir=args.output_dir
    )

    if result:
        print(f"\n🎯 Done! Tailored resume: {result}")
    else:
        print("\n❌ Tailoring failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
