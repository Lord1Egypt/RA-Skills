# Technology Selection Configuration

Supplements the generic five-step framework for tech stack / architecture / tool selection decisions.

## Step 1 Additions: Value Node Decomposition for Tech Decisions

Map the dependency chain:

```
Developer → Framework / Runtime → Platform / Cloud → End User
```

For each option, identify:
- **Actual problem solved**: Is this solving a real pain point or is it "resume-driven development"?
- **Lock-in risk**: How hard is it to switch away later?
- **Ecosystem health**: Community size, corporate backing, release cadence

## Step 2 Additions: Tech-Specific Falsification Checklist

| Falsification Angle | Red Flags |
|---------------------|-----------|
| Benchmark cherry-picking | Only showing favorable comparisons |
| Survivor bias | Comparing against abandoned/dead alternatives |
| Complexity theater | Solves a simple problem with a complex solution |
| Vendor lock-in disguised as "integration" | Makes exit expensive |
| Hype-driven adoption | Adopted because it's trendy, not because it fits |
| Premature optimization | "We might need this at scale" when current scale doesn't justify it |

## Step 3 Additions: Tech Beneficiary Hierarchy

1. **Foundational layer** (standards, protocols, core runtimes) — Highest longevity
2. **Platform layer** (frameworks, cloud services, middleware) — Best balance of stability and innovation
3. **Tool layer** (libraries, dev tools, extensions) — Fast-moving, easy to swap

## Step 4 Additions: Tech Stress Tests

- **Team capability fit**: Can your team actually use this effectively?
- **Operational burden**: Who runs it in production? What breaks at 3am?
- **Migration cost**: What's the real cost of switching from current stack?
- **Diminishing returns**: Is the improvement over status quo worth the switching cost?

## Step 5 Additions: Tech Decision Output

Add to the standard output table:
- **Adoption recommendation**: Adopt / Trial / Hold / Avoid
- **Migration complexity**: Low / Medium / High
- **One concrete next step**
