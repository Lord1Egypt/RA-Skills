# Skill: Psychology Research Assistant

## Description
A comprehensive skill for conducting psychology research, including literature search, systematic review support, meta-analysis assistance, and research methodology guidance.

## Triggers
- "psychology research"
- "literature review"
- "systematic review"
- "meta-analysis"
- "research methodology"
- "PRISMA"
- "GRADE"

## Capabilities

### 1. Literature Search
- Search psychology databases for relevant studies
- Filter by year, journal, methodology
- Find related citations

### 2. Systematic Review Support
- Help design search strategy
- PRISMA 2020 checklist guidance
- Study selection framework
- Data extraction templates

### 3. Meta-Analysis Assistance
- Effect size conversion (OR, RR, SMD)
- Heterogeneity assessment (I², Q-statistic)
- Publication bias detection (Egger's test, Funnel plot)
- Random effects model guidance
- R metafor code generation

### 4. Research Methodology
- Study design recommendations
- Sample size calculation
- Bias assessment tools
- Evidence quality rating (GRADE)

### 5. Writing Support
- Abstract structure
- Methods section guidance
- Results presentation
- Discussion framework

## Data Sources
- PubMed/MEDLINE
- PsycINFO
- Web of Science
- Scopus
- Cochrane Library
- PsyArXiv (preprints)

## Output Format
Structured research summaries with:
- Study characteristics
- Key findings
- Methodological quality
- Effect sizes
- Confidence intervals

## Examples
```
User: Find recent meta-analyses on loneliness intervention
Skill: Searches databases, returns list with effect sizes

User: Help with PRISMA flow diagram
Skill: Provides template and guidance

User: Convert correlation to OR
Skill: Uses formula OR = exp(3r/2), explains approximation
```

---

## Implementation Notes
- Use web_search for literature discovery
- Apply statistical formulas carefully
- Always cite sources
- Update knowledge base regularly
