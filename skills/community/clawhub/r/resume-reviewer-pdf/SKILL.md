---
name: resume-reviewer
description: Comprehensive review and analysis of software engineering resumes in PDF format (frontend, backend, or ML domains). Use this skill when users ask to review, analyze, provide feedback on, or evaluate a resume PDF. The skill analyzes technical content quality, career progression, ATS compatibility, grammar, structure, and provides actionable improvement suggestions based on current industry trends.
---

# Resume Reviewer for Software Engineers

This skill provides comprehensive analysis and feedback for software engineering resumes (frontend, backend, or ML domains) in PDF format, typically created with LaTeX.

## Analysis Framework

Perform analysis in the following order:

### 1. Extract Resume Content

**CRITICAL:** Always use the provided script to extract PDF text:

```bash
python3 scripts/extract_pdf_text.py <path_to_resume.pdf>
```

This ensures consistent text extraction and proper handling of LaTeX-formatted PDFs.

### 2. Initial Assessment

Identify:
- Candidate's domain (frontend, backend, ML)
- Experience level (junior: 0-2 years, mid: 3-5 years, senior: 6+ years)
- Target role type (based on recent experience)
- Resume format (1-page or 2-page)

### 3. Technical Content Analysis

Read `references/tech_trends.md` to understand current technology landscape and evaluation criteria for the identified domain.

Evaluate:

**Theme Identification:**
- Primary technical focus areas
- Technology stack evolution over time
- Specializations or niche expertise
- Career trajectory and progression

**Company and Impact Analysis:**
- Quality and reputation of companies
- Scale of systems worked on (users, data volume, traffic)
- Cross-company skill progression
- Industry diversity or specialization

**Technical Depth:**
- Modern vs. outdated technology usage
- Alignment with current industry trends
- Breadth vs. depth of expertise
- Evidence of continuous learning

**Major Contributions:**
- Quantified business impact
- System design and architecture work
- Technical leadership indicators
- Open source or community contributions
- Cross-functional collaboration

**Improvement Opportunities:**
- Missing relevant technologies for target role
- Weak quantification of impact
- Lack of leadership/mentoring evidence
- Outdated technology focus
- Missing key skills for domain

### 4. Content Structure and Writing Quality

Read `references/writing_quality.md` for detailed grammar and style guidelines.

Evaluate:

**Section Organization:**
- Logical flow and hierarchy
- Section completeness (Experience, Skills, Education, etc.)
- Appropriate emphasis on relevant sections
- Optimal use of available space

**Writing Quality:**
- Action verb usage and strength
- Tense consistency
- Conciseness and clarity
- Grammar and punctuation
- Parallel structure in lists

**Bullet Point Effectiveness:**
- Impact-focused vs. responsibility-focused
- Specificity and quantification
- Business value communication
- Technical detail appropriateness

**Formatting Consistency:**
- Date formats
- Capitalization
- Punctuation style
- Technology name casing
- Number representation

### 5. ATS Compatibility Analysis

Evaluate:

**Structure:**
- Standard section headers
- Chronological organization
- Contact information placement
- Overall layout simplicity

**LaTeX-Specific Issues:**
- Multi-column layout problems
- Special characters or symbols
- Text extractability (verify with script output)
- Graphics or custom formatting

**Keyword Optimization:**
- Presence of relevant technical keywords
- Natural keyword integration
- Acronym definitions
- Industry-standard terminology

**Formatting Risks:**
- Tables or text boxes for critical content
- Headers/footers with important information
- Non-standard fonts
- Complex nested structures

### 6. Generate Comprehensive Feedback

Structure feedback as follows:

#### Overall Assessment
- 2-3 sentence summary of resume strength
- Primary domain and experience level confirmation
- Key differentiators or standout qualities

#### Strengths (What's Good)
- Specific examples of effective content
- Well-executed sections or bullet points
- Strong technical expertise demonstrated
- Effective quantification or storytelling
- Good formatting choices

#### Technical Content Recommendations
- Missing relevant modern technologies
- Opportunities to strengthen impact statements
- Suggestions for better technical positioning
- Areas to highlight or expand
- Technologies to add based on target roles

#### Content Structure and Writing Improvements
- Grammar or style issues with specific examples
- Bullet point enhancements with before/after examples
- Section reorganization suggestions
- Consistency fixes needed
- Conciseness improvements

#### ATS Optimization Recommendations
- Specific parsing risks identified
- Keyword additions or improvements
- Formatting changes for better compatibility
- Section header standardization

#### Priority Action Items
- Rank top 5-7 improvements by impact
- Quick wins vs. larger rewrites
- Critical issues vs. nice-to-haves

## Output Format

Present feedback in clear, actionable format using markdown headers and bullet points. Use specific examples from the resume when citing issues or strengths. Provide before/after suggestions for concrete improvements.

Be encouraging and constructive while being honest about weaknesses. Frame criticism as opportunities for improvement.

## Important Notes

- Always extract PDF text using the provided script first
- Consult reference files for domain-specific and writing guidelines
- Tailor feedback to candidate's experience level and target domain
- Focus on high-impact improvements first
- Provide specific, actionable recommendations with examples
- Consider both ATS parsing and human readability
