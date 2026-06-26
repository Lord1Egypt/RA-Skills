---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_11bc05b95d0711f19299525400d9a7a1
    ReservedCode1: H0wXDq7zKMF9Tm3I2DK1d8AbaVioWU5W3whMTjslL9vy4bp+FF40cEUgkbYBbUQGqGJVuA2KKth67V6hPxfk7ChNUBBkhFE3PMTW1s8Xc7D4yCJtmwV0/irCGrHp7QBVPgQo/R0hG1ftcj9zB4rS8lwJjMwKwQJDBOGj5wXB2xWirnTxU58v/h3giKQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_11bc05b95d0711f19299525400d9a7a1
    ReservedCode2: H0wXDq7zKMF9Tm3I2DK1d8AbaVioWU5W3whMTjslL9vy4bp+FF40cEUgkbYBbUQGqGJVuA2KKth67V6hPxfk7ChNUBBkhFE3PMTW1s8Xc7D4yCJtmwV0/irCGrHp7QBVPgQo/R0hG1ftcj9zB4rS8lwJjMwKwQJDBOGj5wXB2xWirnTxU58v/h3giKQ=
---

# Worldwide Research Synthesizer (全球学术研究聚合器)

## Description
A rigorous academic research synthesis skill that aggregates, cross-references, and critically synthesizes scholarly literature from global databases. It conducts structured literature reviews, identifies research gaps, tracks citation networks, and generates PRISMA-compliant systematic review outputs. Designed for researchers, PhD candidates, R&D teams, and evidence-based decision-makers who need comprehensive, unbiased literature synthesis across languages and disciplines.

**Keywords**: research, literature review, academic, papers, systematic review, meta-analysis, citation, scholarly, evidence-based, science

## Triggers
- "conduct a literature review on [topic]"
- "what does the research say about [question]"
- "find papers on [topic] from the last [N] years"
- "synthesize findings on [research area]"
- "what are the research gaps in [field]"
- "track citations for [paper title / DOI]"
- "compare research approaches between [method A] and [method B]"
- "is [claim] supported by academic evidence"
- "recent breakthroughs in [scientific domain]"

## Capabilities

### 1. Multi-Engine Literature Search
- Search across 6 engines: Google Scholar, Semantic Scholar, PubMed, arXiv, SSRN, ResearchGate
- Support 10+ languages with region-specific academic databases (CNKI for Chinese, J-STAGE for Japanese, SciELO for Spanish/Portuguese, etc.)
- Filter by: publication date, citation count, journal impact, open-access status
- Deduplicate results across engines using title + DOI + author matching

### 2. Systematic Review Methodology (PRISMA-Compliant)
Follow the PRISMA 2020 flow:
```
Records identified through database searching (n=___)
Records after duplicates removed (n=___)
Records screened by title/abstract (n=___)
Full-text articles assessed for eligibility (n=___)
Studies included in qualitative synthesis (n=___)
Studies included in quantitative synthesis / meta-analysis (n=___)
```

### 3. Quality Assessment & Critical Appraisal
- **Journal credibility check**: Verify indexing in DOAJ/Scopus/Web of Science, check Impact Factor / CiteScore
- **Predatory journal detection**: Apply 6-point checklist from references
- **Paper-level assessment**: Citation count, Altmetric score, field-weighted citation impact
- **Methodology rigor**: Evaluate sample size, study design, confounding control, reproducibility indicators
- Flag retracted papers via CrossRef Retraction Watch integration

### 4. Synthesis & Gap Analysis
- **Thematic synthesis**: Identify and group recurring themes across selected papers
- **Contradiction mapping**: Explicitly document conflicting findings with paper references
- **Research gap identification**: Highlight under-explored areas, methodological limitations, and future research directions
- **Temporal trend analysis**: Track how findings and consensus have evolved over time

### 5. Citation Network Analysis
- Forward citation tracking (who cited this paper)
- Backward citation tracking (what this paper cites)
- Identify seminal papers (high citation count + high network centrality)
- Map author collaboration networks across institutions and countries

### 6. Output Formats
Structure every synthesis with:
1. **Research Question & Scope** (PICO framework where applicable)
2. **Search Strategy** (databases searched, query strings, date ranges, inclusion/exclusion criteria)
3. **PRISMA Flow Diagram** (record counts at each stage)
4. **Synthesis Table** (columns: Author/Year | Methodology | Key Findings | Quality Score | Relevance)
5. **Thematic Findings** (organized by theme, with supporting citations)
6. **Contradictions & Debates** (documenting scholarly disagreements)
7. **Research Gaps & Future Directions**
8. **Full Reference List** in requested citation format (default: APA 7th)

## Workflow

```
User Query
    ↓
[Step 1] Decompose question → PICO/PICo framework
[Step 2] Construct search strings for multi-engine search
[Step 3] Execute parallel web_search across academic engines
    ↓
[Step 4] Deduplicate and screen by title/abstract (apply inclusion criteria)
    ↓
[Step 5] web_fetch top papers for full-text assessment
    ↓
[Step 6] Quality assessment → flag low-quality / predatory sources
    ↓
[Step 7] Thematic coding of findings → identify consensus and conflicts
    ↓
[Step 8] Synthesize with PRISMA flow + evidence tables + gap analysis
    ↓
Final Output: Structured systematic review with full citations
```

## Usage Guidelines
1. **Evidence hierarchy**: Prioritize meta-analyses > RCTs > cohort studies > case studies > expert opinion
2. **Publication bias awareness**: Proactively search for null/negative results, not just positive findings
3. **Open access preference**: When paywalled, note the paywall but provide preprint/OA alternatives where available
4. **Recency vs. foundations**: Balance seminal older papers with cutting-edge recent publications
5. **Language**: Conduct searches in the user's language AND English (the lingua franca of science); note language bias explicitly

## Examples

**Query**: "What is the current evidence on intermittent fasting's effects on longevity?"

**Response Structure**:
1. PICO: Population (adults) | Intervention (intermittent fasting protocols) | Comparison (continuous calorie restriction / ad libitum) | Outcome (lifespan/longevity biomarkers)
2. Search strategy: PubMed + Google Scholar, 2019-2026, English + Chinese
3. PRISMA flow: 847 → 523 deduped → 89 screened → 34 full-text → 22 included
4. Synthesis table with 22 studies, each scored on quality (Jadad scale for RCTs)
5. Key findings: autophagy mechanisms, NAD+ pathways, human vs animal evidence gaps
6. Contradictions: 16:22 vs 8 pattern debate, optimal fasting window unresolved
7. Gaps: lack of decade-scale human trials, elderly population underrepresented
8. Full APA 7th reference list

## References
- `references/academic_sources.json`: Search engine catalog, open-access repositories, citation formats, PRISMA methodology, multi-language database mappings, quality assessment checklists
*（内容由AI生成，仅供参考）*
