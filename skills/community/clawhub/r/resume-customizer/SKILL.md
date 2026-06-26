---
name: resume-customizer
description: >
  Tailors resumes to match specific job descriptions (JD) with multi-format support
  (PDF, Word, Markdown, HTML, text), ATS optimization, keyword analysis, skill matching,
  and industry-specific customization. Supports both Chinese and English resumes.
version: 1.0.3
metadata:
  openclaw:
    install:
      - kind: uv
        package: PyPDF2
        bins: []
      - kind: uv
        package: python-docx
        bins: []
      - kind: uv
        package: beautifulsoup4
        bins: []
      - kind: uv
        package: requests
        bins: []
      - kind: uv
        package: jieba
        bins: []
    always: false
    emoji: "\U0001F4C4"
agent_created: true
---

# Resume Customizer Skill

This skill provides comprehensive resume customization capabilities to match job descriptions (JD). It supports multiple input/output formats and provides ATS optimization.

## When to Use This Skill

This skill should be used when the user wants to:
- Customize an existing resume to match a specific job description
- Generate a new resume based on a JD and user background
- Optimize a resume for ATS (Applicant Tracking System) systems
- Extract and match skills between a resume and JD
- Convert a resume between different formats (PDF, Word, Markdown, HTML, text)

## Supported Formats

### Input Formats
- **Resume Input**: PDF (.pdf), Word (.docx), Plain Text (.txt), Markdown (.md), HTML (.html)
- **JD Input**: Plain text, URL (webpage), PDF (.pdf), Word (.docx), Markdown (.md)

### Output Formats
- PDF (.pdf)
- Word (.docx)
- Markdown (.md)
- HTML (.html)
- Plain Text (.txt)

## Core Workflow

### Step 1: Parse Inputs

1. **Parse Resume** (if provided):
   - Use `scripts/parse_resume.py` to extract structured data from the resume
   - Supported formats: PDF, Word, text, Markdown
   - Extract: contact info, summary, work experience, education, skills, projects, certifications

2. **Parse JD**:
   - Use `scripts/parse_jd.py` to extract structured data from the job description
   - Supported inputs: text, URL, PDF, Word, Markdown
   - Extract: job title, company, required skills, preferred skills, responsibilities, qualifications, keywords

### Step 2: Analysis and Matching

1. **Skill Matching**:
   - Compare skills in resume vs JD
   - Identify matching skills, missing skills, and additional skills
   - Use `references/industry_keywords.json` for comprehensive keyword coverage

2. **Keyword Extraction**:
   - Extract important keywords from JD (required qualifications, preferred qualifications, responsibilities)
   - Identify ATS-relevant keywords
   - Use `references/ats_optimization.md` for ATS best practices

3. **Gap Analysis**:
   - Identify gaps between resume and JD
   - Suggest improvements to address gaps
   - Prioritize improvements based on JD requirements

### Step 3: Customization

1. **Tailor Resume Content**:
   - Reorder sections based on JD priorities
   - Highlight matching skills and experiences
   - Adjust summary/objective to align with JD
   - Quantify achievements relevant to the position
   - Use action verbs from `references/best_practices.md`

2. **Keyword Optimization**:
   - Naturally incorporate JD keywords into resume
   - Ensure keyword density is appropriate for ATS systems
   - Use synonyms and related terms to avoid keyword stuffing
   - Follow guidelines in `references/ats_optimization.md`

3. **Format Optimization**:
   - Ensure ATS-friendly formatting (simple layout, standard section headings)
   - Remove graphics, tables, and special characters that may confuse ATS
   - Use standard fonts and formatting

### Step 4: Generate Output

1. **Select Output Format**:
   - Ask user for preferred output format (default: same as input format)
   - Use `scripts/export_resume.py` to generate the output

2. **Apply Template** (optional):
   - Use templates from `assets/templates/` for professional formatting
   - Available templates: standard (English), standard-zh (Chinese), modern, professional

3. **Generate Output**:
   - Create the resume in the specified format
   - Ensure all customizations are applied
   - Validate the output for completeness

## Advanced Features

### ATS Optimization

Follow the guidelines in `references/ats_optimization.md`:
- Use standard section headings (Work Experience, Education, Skills, etc.)
- Avoid headers/footers, tables, text boxes, graphics
- Use standard fonts (Arial, Calibri, Times New Roman)
- Include keywords from JD naturally
- Save as .docx or .pdf (text-based PDF, not scanned)

### Industry-Specific Customization

Use `references/industry_keywords.json` for industry-specific keywords:
- Technology/Software Development
- Data Science/Analytics
- Product Management
- Marketing/Sales
- Finance/Accounting
- Healthcare
- Education
- General/All Industries

### Skill Extraction and Matching

Use `scripts/optimize_keywords.py` to:
1. Extract skills from both resume and JD
2. Categorize skills (technical, soft, domain-specific)
3. Calculate match percentage
4. Suggest skills to add based on JD

## Scripts Usage

### parse_resume.py

Parses resume files and extracts structured data.

```bash
python scripts/parse_resume.py --input <resume_file> --output <output_json>
```

Supported input formats: .pdf, .docx, .txt, .md, .html

### parse_jd.py

Parses job description from various sources.

```bash
python scripts/parse_jd.py --input <jd_file_or_url> --output <output_json>
```

Supported inputs: text, URL, .pdf, .docx, .md

### customize_resume.py

Customizes resume based on JD analysis.

```bash
python scripts/customize_resume.py --resume <resume_json> --jd <jd_json> --output <customized_json>
```

Options:
- `--match-threshold 0.7` (similarity threshold for skill matching)
- `--ats-optimize` (apply ATS optimization)
- `--industry <industry>` (apply industry-specific customization)

### export_resume.py

Exports customized resume to specified format.

```bash
python scripts/export_resume.py --input <resume_json> --output <output_file> --format <format>
```

Supported formats: pdf, docx, md, html, txt

Options:
- `--template <template_name>` (use a template from assets/templates/)
- `--ats-friendly` (ensure ATS-friendly formatting)

### optimize_keywords.py

Optimizes keyword usage for ATS systems.

```bash
python scripts/optimize_keywords.py --resume <resume_json> --jd <jd_json> --output <optimized_json>
```

Options:
- `--density 2.0` (target keyword density percentage)
- `--synonyms` (use synonym expansion)

## References

### best_practices.md

Contains resume writing best practices:
- Action verbs by category
- Achievement quantification guidelines
- Summary/objective writing tips
- Section ordering recommendations
- Common mistakes to avoid

### ats_optimization.md

Contains ATS optimization guidelines:
- Formatting dos and don'ts
- Keyword placement strategies
- File format recommendations
- Section heading standards
- Parsing error avoidance

### industry_keywords.json

Contains industry-specific keyword lists:
- Common skills by industry
- Job titles by industry
- Tools/technologies by industry
- Certifications by industry
- Action verbs by function

### resume_structures.md

Contains resume structure guidelines:
- Standard resume sections
- Optional sections by career level
- Section ordering by experience level
- Length recommendations
- Content guidelines by section

## Assets

### templates/

Contains resume templates:
- `standard-en.json` - Standard English resume template
- `standard-zh.json` - Standard Chinese resume template
- `modern-en.json` - Modern English resume template
- `professional-en.json` - Professional English resume template

### examples/

Contains example resumes:
- `example-software-engineer-en.json` - Software engineer resume (English)
- `example-product-manager-zh.json` - Product manager resume (Chinese)
- `example-data-scientist-en.json` - Data scientist resume (English)

## Multi-Language Support

This skill supports both Chinese (中文) and English resumes:

### Chinese Resumes:
- Use `standard-zh.json` template
- Follow Chinese resume conventions (photo optional, age/gender not required)
- Use Chinese keywords from `industry_keywords.json`
- Output formats: .docx (with Chinese fonts), .pdf (embed fonts)

### English Resumes:
- Use `standard-en.json` template
- Follow Western resume conventions (no photo, no personal info beyond contact)
- Use English keywords from `industry_keywords.json`
- Output formats: all supported formats

## Error Handling

If any script fails:
1. Check input file format and accessibility
2. Verify all dependencies are installed (see below)
3. Check JSON output for parsing errors
4. Consult error messages for specific issues

## Dependencies

Ensure these Python packages are installed:

```bash
pip install PyPDF2 python-docx markdown bs4 requests spacy nltk
python -m spacy download en_core_web_sm
```

For Chinese processing:
```bash
pip install jieba
```

## Important Notes

1. **Privacy**: Always handle user resumes and personal data with strict confidentiality
2. **Accuracy**: Do not invent or fabricate experiences not present in the original resume
3. **Honesty**: Optimize and tailor content, but never misrepresent qualifications
4. **User Review**: Always have the user review customized resumes before submitting to employers
5. **Backup**: Keep original resume files and provide both original and customized versions to the user

## Example Usage

### Example 1: Customize existing resume for a specific JD

User: "Help me customize my resume for this software engineer position at Google."

Steps:
1. Parse user's existing resume (uploaded as resume.pdf)
2. Parse JD (provided as text or URL)
3. Analyze skill match and gaps
4. Customize resume content to highlight matching skills
5. Optimize for ATS systems
6. Export customized resume as PDF and Word

### Example 2: Generate new resume from scratch

User: "Create a resume for me based on this JD. Here's my background information."

Steps:
1. Collect user background information (work history, education, skills)
2. Parse JD to identify key requirements
3. Generate resume structure based on JD priorities
4. Draft resume content tailored to JD
5. Optimize for ATS systems
6. Export resume in user's preferred format

### Example 3: Optimize resume for ATS

User: "My resume isn't getting past ATS systems. Can you optimize it for this JD?"

Steps:
1. Parse existing resume
2. Parse JD
3. Analyze current resume for ATS compatibility issues
4. Reformat resume for ATS compatibility
5. Optimize keyword usage
6. Export ATS-friendly version

## Customization Checklist

Before delivering the customized resume, ensure:
- [ ] All JD-required skills present (or addressed in cover letter)
- [ ] Keywords from JD incorporated naturally
- [ ] Achievements quantified where possible
- [ ] Action verbs used throughout
- [ ] Formatting is ATS-friendly
- [ ] Contact information is current and professional
- [ ] Spelling and grammar checked
- [ ] Length appropriate for experience level
- [ ] User has reviewed and approved all changes
