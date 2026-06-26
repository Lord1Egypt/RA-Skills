# Startup Validator — Analysis Framework & Guide

## Tool summary

- **Name**: Startup Validator  
- **Commands**: `validate` (validation pass), `compete` (competitive analysis), `mvp` (MVP scaffold)  
- **Optional dependency**: `pip install requests` (if you add HTTP calls)

## Analysis dimensions

- Multi-dimensional review — market / competitors / technology / business model  
- Persona and need validation  
- MVP scope and roadmap sketch  

## Framework

### Phase 1: Data collection
- Define sources and scope  
- Normalize inputs  
- Establish baseline comparison metrics  

### Phase 2: Insight & patterns
- Cross-cutting analysis  
- Trend and anomaly detection  
- Root-cause hypotheses where data supports them  

### Phase 3: Actions & decisions
- Concrete, prioritized recommendations  
- Risk register and mitigations  

## Scoring rubric

| Score | Level | Meaning | Suggested action |
|-------|-------|---------|------------------|
| 5 | ⭐⭐⭐⭐⭐ | Far above bar | Pursue aggressively |
| 4 | ⭐⭐⭐⭐ | Above bar | Prioritize |
| 3 | ⭐⭐⭐ | Meets bar | Optional improvements |
| 2 | ⭐⭐ | Below bar | Fix gaps before scaling |
| 1 | ⭐ | Fails bar | Reconsider or pivot |

## Output template

```markdown
# Startup validation analysis
## Key findings
1. …
2. …

## Evidence
| Metric | Value | Trend | Rating |
|--------|-------|-------|--------|

## Recommendations
| Priority | Action | Rationale | Expected impact |
|----------|--------|-----------|-------------------|
```

## Reference links

### Core
- [YC: The real product/market fit](https://www.ycombinator.com/library/5z-the-real-product-market-fit)
- [Pre-build idea validator (OpenClaw)](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/pre-build-idea-validator.md)
- [Market research product factory](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/market-research-product-factory.md)

### Community
- [Hacker News](https://news.ycombinator.com/item?id=41986396)
- [Reddit r/startups](https://www.reddit.com/r/startups/comments/1055d61yyz/idea_validator_ai/)

## Tips

1. Adapt the framework to stage (problem discovery vs GTM).  
2. Weight criteria by risk tolerance (e.g. regulated markets).  
3. Combine quantitative signals with qualitative interviews.  
4. Use the links as **starting points** for research, not as proof alone.  
