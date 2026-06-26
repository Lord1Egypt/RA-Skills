---
name: literature-review
description: Use when "literature review", "research synthesis", "systematic review", "academic search", or asking about "find papers", "cite sources", "research gaps", "meta-analysis", "bibliography"
version: 1.0.0
---

<!-- Adapted from: claude-scientific-skills/scientific-skills/literature-review -->

# Literature Review Guide

Conduct comprehensive, systematic literature reviews using academic databases.

## When to Use

- Conducting systematic literature reviews
- Synthesizing research on a topic
- Writing literature review sections
- Identifying research gaps
- Building bibliographies

## Core Workflow

### Phase 1: Planning

1. **Define Research Question** (PICO framework for clinical)
   - Population, Intervention, Comparison, Outcome

2. **Establish Scope**
   - Review type: narrative, systematic, scoping
   - Time period, geographic scope
   - Study types to include

3. **Develop Search Strategy**
   - Key terms and synonyms
   - Boolean operators (AND, OR, NOT)
   - Database-specific syntax

### Phase 2: Searching

**Key Databases:**

| Database | Coverage |
|----------|----------|
| PubMed | Biomedical, life sciences |
| arXiv | Physics, CS, math preprints |
| Semantic Scholar | Broad academic |
| Google Scholar | Broad coverage |
| Web of Science | Multidisciplinary |

**Search Strategy Template:**

```
(term1 OR synonym1) AND (term2 OR synonym2) AND (term3)
```

### Phase 3: Screening

1. **Title/Abstract Screening**
   - Apply inclusion/exclusion criteria
   - Track reasons for exclusion

2. **Full-Text Review**
   - Assess eligibility
   - Extract key data

### Phase 4: Synthesis

**Organize Thematically:**

```markdown
## Theme 1: [Topic]
- Finding A (Author, Year)
- Finding B (Author, Year)
- Synthesis and gaps

## Theme 2: [Topic]
...
```

**Comparison Table:**

| Study | Methods | Sample | Key Findings |
|-------|---------|--------|--------------|
| Author 2023 | RCT | n=100 | Finding X |
| Author 2022 | Cohort | n=500 | Finding Y |

### Phase 5: Writing

**Structure:**

1. Introduction (scope, objectives)
2. Methods (search strategy, criteria)
3. Results (thematic synthesis)
4. Discussion (gaps, future directions)
5. Conclusion

## Citation Management

### Citation Styles

```markdown
**APA 7:**
Author, A. A., & Author, B. B. (Year). Title. Journal, Volume(Issue), pages. https://doi.org/xxx

**Nature:**
Author, A. A. & Author, B. B. Title. Journal Volume, pages (Year).

**Vancouver:**
Author AA, Author BB. Title. Journal. Year;Volume(Issue):pages.
```

### Tools

- Zotero (free, open source)
- Mendeley (free)
- EndNote (institutional)

## Quality Assessment

**For RCTs:** Cochrane Risk of Bias tool
**For Observational:** Newcastle-Ottawa Scale
**For Qualitative:** CASP checklist

## PRISMA Flow Diagram

```
Records identified (n=X)
    ↓
Duplicates removed (n=X)
    ↓
Records screened (n=X)
    ↓
Records excluded (n=X)
    ↓
Full-text assessed (n=X)
    ↓
Studies included (n=X)
```

## Best Practices

1. **Document everything** - reproducibility
2. **Use multiple databases** - comprehensive coverage
3. **Two reviewers** - reduce bias (when possible)
4. **Pre-register protocol** - transparency
5. **Update searches** - before publication

## Common Pitfalls

- Publication bias (positive results overrepresented)
- Language bias (English-only searches)
- Citation bias (citing famous papers)
- Not updating searches before submission

## Resources

- PRISMA Guidelines: <http://prisma-statement.org/>
- Cochrane Handbook: <https://training.cochrane.org/handbook>
- PROSPERO (protocol registration): <https://www.crd.york.ac.uk/prospero/>
