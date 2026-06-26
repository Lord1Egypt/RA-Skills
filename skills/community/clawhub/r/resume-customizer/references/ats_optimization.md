# ATS Optimization Guide

## What is ATS?

**ATS (Applicant Tracking System)** is software used by employers to collect, scan, filter, and rank job applications.

### Common ATS Systems
- Workday
- Taleo (Oracle)
- Greenhouse
- Lever
- JazzHR
- BambooHR
- iCIMS

## How ATS Parses Resumes

### Parsing Process
1. **Text Extraction**: ATS extracts text from resume (PDF/Word)
2. **Section Identification**: Identifies standard section headings
3. **Keyword Matching**: Matches resume keywords with JD keywords
4. **Ranking**: Scores resume based on match quality
5. **Filtering**: Filters out low-scoring resumes

### Why Resumes Get Rejected
- ❌ Cannot parse PDF (scanned/image PDF)
- ❌ Non-standard section headings
- ❌ Graphics, tables, text boxes
- ❌ Headers/footers (often ignored)
- ❌ Special characters, symbols, icons
- ❌ Columns (confuses parsing order)

## Formatting Dos and Don'ts

### ✅ DOS (ATS-Friendly)

#### File Format
- **Preferred**: .docx (Word format)
- **Acceptable**: .pdf (text-based, not scanned)
- **Avoid**: .pdf (scanned/image), .pages, .txt

#### Layout
- **Single column** layout (left to right, top to bottom)
- **Standard fonts**: Arial, Calibri, Times New Roman, Helvetica
- **Font size**: 10-12pt for body, 14-16pt for headings
- **Margins**: 0.5-1 inch on all sides
- **Line spacing**: 1.0-1.15

#### Section Headings
Use **standard headings**:
- `Contact Information` (or just contact info, no heading needed)
- `Summary` or `Professional Summary`
- `Work Experience` or `Professional Experience`
- `Education`
- `Skills` or `Technical Skills`
- `Projects`
- `Certifications`
- `Awards` or `Honors`

#### Content
- Use **standard bullet points** (•, -, *)
- **Left-align** all text
- Use **standard date formats** (Month Year, e.g., "January 2023")
- **Spell out acronyms** at least once (e.g., "Artificial Intelligence (AI)")

### ❌ DON'TS (Avoid)

#### Layout/Design
- ❌ Tables (ATS often parses table cells incorrectly)
- ❌ Text boxes (content often ignored)
- ❌ Headers/footers (often skipped by ATS)
- ❌ Columns (confuses reading order)
- ❌ Graphics, icons, symbols (❖ ✦ ★ etc.)
- ❌ Images, photos (unless specifically requested)
- ❌ Logos, watermarks
- ❌ Borders, shading, fill colors

#### Fonts/Formatting
- ❌ Fancy fonts (script, decorative)
- ❌ Text in graphics (not parseable)
- ❌ Vertical text
- ❌ Text boxes with text wrapping
- ❌ Headers/footers for contact info

#### Content
- ❌ Keyword stuffing (unnatural repetition)
- ❌ Images of text (not parseable)
- ❌ Special characters (★, ❖, →, etc. - use standard bullets)
- ❌ Tables for layout (use tabs or spacing instead)

## Keyword Placement Strategies

### Where to Place Keywords

#### High-Impact Locations (70% weight)
1. **Professional Summary** (first 2-3 sentences)
2. **Skills Section** (dedicated section)
3. **Work Experience** (in bullet points)
4. **Job Title** (match JD title if possible)

#### Medium-Impact Locations (30% weight)
5. **Education Section** (relevant coursework, projects)
6. **Projects Section** (project descriptions)
7. **Certifications** (certification names)

### Keyword Density Guidelines

#### Target Density
- **Primary keywords**: 2-5 occurrences
- **Secondary keywords**: 1-3 occurrences
- **Avoid overstuffing**: >5% density looks spammy

#### Natural Integration
- ✅ "Developed Python applications to automate data processing workflows"
- ❌ "Python Python Python. Expert in Python. Python developer with Python skills."

### Keyword Variations
Include variations to catch different search terms:
- **Acronym + Full Form**: "Artificial Intelligence (AI)" or "AI (Artificial Intelligence)"
- **Synonyms**: "Managed" / "Led" / "Supervised"
- **Related Terms**: "Machine Learning" / "ML" / "Predictive Modeling"

## File Format Recommendations

### Best Format: .docx (Word)
**Pros**:
- ✅ Best ATS compatibility
- ✅ Preserves formatting
- ✅ Easy to edit

**Cons**:
- ⚠️ Formatting may shift on different systems

### Second Best: .pdf (Text-Based)
**Pros**:
- ✅ Preserves layout
- ✅ Universal compatibility

**Cons**:
- ⚠️ Some ATS cannot parse PDF correctly
- ⚠️ Scanned PDFs are unparseable

### How to Check PDF Type
1. Open PDF in a PDF reader
2. Try to select text with cursor
3. **If text is selectable** → Text-based PDF ✅
4. **If text is not selectable** → Scanned PDF ❌

### Export to Text-Based PDF
- **From Word**: File → Save As → PDF → Options → Check "Optimize for: Online and print"
- **From Google Docs**: File → Download → PDF Document
- **Avoid**: "Print to PDF" from scanned document

## Section Heading Standards

### Standard Headings (ATS-Friendly)
| Section | Standard Headings |
|---------|----------------------|
| Contact | (No heading needed) or "Contact Information" |
| Summary | "Summary", "Professional Summary", "Profile" |
| Experience | "Work Experience", "Professional Experience", "Employment History" |
| Education | "Education", "Educational Background" |
| Skills | "Skills", "Technical Skills", "Core Competencies" |
| Projects | "Projects", "Relevant Projects" |
| Certifications | "Certifications", "Licenses & Certifications" |
| Awards | "Awards", "Honors", "Awards & Honors" |

### Non-Standard Headings (Avoid)
- ❌ "Where I've Worked" (use "Work Experience")
- ❌ "My Awesome Skills" (use "Skills")
- ❌ "Schooling" (use "Education")
- ❌ "Things I'm Good At" (use "Skills")

## Parsing Error Avoidance

### Common Parsing Errors

#### Error 1: Incorrect Contact Info Extraction
**Cause**: Contact info in header/footer, text boxes, or graphics
**Fix**: Place contact info in main body, left-aligned, no text boxes

#### Error 2: Section Misidentification
**Cause**: Non-standard section headings, creative headings
**Fix**: Use standard headings (see table above)

#### Error 3: Date Misinterpretation
**Cause**: Non-standard date formats ("01/2023", "2023/01")
**Fix**: Use "Month Year" format ("January 2023")

#### Error 4: Skills Not Extracted
**Cause**: Skills in graphics, tables, or non-standard section
**Fix**: Create dedicated "Skills" section with bullet points

#### Error 5: Work Experience Out of Order
**Cause**: Columns, tables, or non-chronological layout
**Fix**: Use single-column, reverse-chronological order

### Pre-Applicant Tracking System Testing

#### Test 1: Copy-Paste Test
1. Open resume in plain text editor (Notepad)
2. Copy all text (Ctrl+A, Ctrl+C)
3. Paste into new document (Ctrl+V)
4. **If formatting is mostly preserved** → ATS-friendly ✅
5. **If formatting is broken** → Not ATS-friendly ❌

#### Test 2: Online ATS Checker
Use free online tools:
- JobScan (free trial)
- ResumeWorded
- VMock

#### Test 3: PDF Text Selection
1. Open PDF in Adobe Reader / Browser
2. Try selecting text with cursor
3. **If all text is selectable** → Good ✅
4. **If some text is not selectable** → Graphics/images issue ❌

## Industry-Specific ATS Tips

### Technology/Software Development
- Include specific programming languages (Python, Java, C++)
- List frameworks (React, Django, Spring)
- Mention tools (Git, Docker, AWS)
- Use standard job titles ("Software Engineer" not "Code Ninja")

### Finance/Accounting
- Include certifications (CPA, CFA, MBA)
- List financial software (SAP, Oracle, Excel)
- Use standard titles ("Financial Analyst" not "Money Manager")

### Healthcare
- Include licenses (MD, RN, LPN)
- List medical software (Epic, Cerner)
- Use standard abbreviations (spell out first time)

### Marketing
- Include marketing tools (HubSpot, Google Analytics)
- List channels (Social Media, Email, SEO)
- Use standard metrics (ROI, Conversion Rate)

## Pre-Submission Checklist

Before submitting resume to ATS:
- [ ] Saved as .docx or text-based .pdf
- [ ] Used standard section headings
- [ ] No tables, text boxes, graphics, columns
- [ ] Standard fonts (Arial, Calibri, Times New Roman)
- [ ] Keywords from JD included naturally
- [ ] Contact information in main body (not header/footer)
- [ ] No special characters or symbols
- [ ] Passed copy-paste test (see Test 1 above)
- [ ]Spell-checked and grammar-checked
- [ ] No typos in company names or software tools
