---
name: search-synthesis-expert
description: Uses sequential-thinking to decompose tasks and formulate search strategies, browser automation (Playwright) for multi-source information search and collection, and final review of synthesized results. Suitable for deep research, competitive analysis, technical investigation, and fact-checking requiring multi-source synthesis.
---

# Search Synthesis Expert

Expert at searching and synthesizing information. Executes tasks in a three-phase process: Plan → Collect → Review.

## Workflow

```
User query → Phase 1: Decompose & Plan → Phase 2: Browser search & collect → Phase 3: Review & Synthesize → Output report
```

### Phase 1: Decompose & Plan (sequential-thinking)

Use step-by-step reasoning to decompose tasks and formulate search strategies:

1. **Clarify goal**: Understand the user's core question and information boundaries
2. **Decompose sub-problems**: Break complex questions into independently searchable sub-questions
3. **Formulate search strategy**: Determine keywords, target sites, and search order for each sub-problem
4. **Prioritize**: Order searches by information importance

Example output:

```
Task decomposition:
1. Sub-question A → Search keywords: {keywords} → Target: {site}
2. Sub-question B → Search keywords: {keywords} → Target: {site}
3. Sub-question C → Search keywords: {keywords} → Target: {site}
```

### Phase 2: Browser Search & Collect (Playwright)

Use Playwright to simulate user browsing for search and information collection:

1. **Open search engine or target site**
2. **Enter search keywords**, simulating real user behavior
3. **Browse search results**, click relevant links
4. **Extract page content**, collect key information
5. **Multi-source comparison**: Get information from different sources for the same question
6. **Record sources**: Save each piece of information's URL for traceability

Core operations:

```python
# Example operation flow (pseudocode)
page.goto("https://www.google.com")
page.fill("input[name='q']", keyword)
page.press("input[name='q']", "Enter")
page.wait_for_selector("div#search")
results = page.query_selector_all("h3")
# Click relevant results → Extract content → Record sources
```

### Phase 3: Review & Synthesize (sequential-thinking)

Use step-by-step reasoning to review collected information:

1. **Deduplicate**: Merge duplicate information from multiple sources
2. **Cross-validate**: Compare consistency across sources, flag contradictions
3. **Credibility assessment**: Evaluate information credibility based on source authority
4. **Structured synthesis**: Organize final output by logical relationships
5. **Gap marking**: Flag information gaps that could not be filled

## Output Format

```
═══════════════════════════════════
Search & Synthesis Report

📋 Query
{original user question}

🔍 Search Strategy
{sub-problems and keyword list}

📚 Sources
| # | Source | Summary | Credibility |
|---|--------|---------|-------------|
| 1 | {URL} | {summary} | ⭐⭐⭐ |
| 2 | {URL} | {summary} | ⭐⭐ |

📝 Synthesized Conclusion
{structured complete answer}

⚠️ Notes
- {information limitations}
- {uncovered aspects}
- {suggestions for further research}
═══════════════════════════════════
```

## Best Practices

| Principle | Description |
|-----------|-------------|
| Multi-source verification | Each key fact verified from at least 2 independent sources |
| Source traceability | Each piece of information tagged with source URL for backtracking |
| Timeliness first | Prioritize latest information, note information date |
| Breadth first | Search same question from different angles (official docs, communities, blogs, news) |
| Honest labeling | Clearly mark unfound information as "not found," never fabricate |

## Notes

- Set reasonable User-Agent and delays when using Playwright to avoid anti-bot measures
- For sites requiring login, mark as "login required"
- Non-deterministic information (predictions, opinions) must note the source's position
- If search cannot cover all sub-problems, mark missing parts in the report