# Shared Agent Output Instructions

## Finding Output (LOD Architecture)

For each finding you discover:

1. **Write the atomic finding file** to `{FINDINGS_DIR}/{FINDING-ID}.md` using the LOD-2 format from `{FINDING_TEMPLATE_PATH}`
2. **Build your LOD-0 summary table** — one row per finding: `| [ID] | [Severity] | [One-sentence summary] |`

When you are done with all analysis, return ONLY the following to the orchestrator:

```
## Agent: {AGENT_NAME}

**Endpoints/items analyzed:** [count]
**Findings:** [count] ([severity breakdown])

### LOD-0 Summary

| ID          | Severity | Summary        |
| ----------- | -------- | -------------- |
| HTTP-001 | High     | [one sentence] |
| HTTP-002 | Medium   | [one sentence] |

### IDOR-Suspect Endpoints (if applicable)

[list of endpoints flagged for logic stage deep dive]

### Incidental Findings

[IX-prefixed findings in abbreviated format]
```

Do NOT send full finding details in your return message. They are on disk.

## Reading Prior Findings

Your `{PRIOR_FINDINGS_SUMMARY}` contains LOD-0 summaries from earlier execution groups. If you need full detail on a specific finding:

1. Note the finding ID from the LOD-0 table
2. `Read` the file at `{FINDINGS_DIR}/{FINDING-ID}.md` for the full LOD-2 content
3. Only read findings relevant to your analysis — do not read all of them

## Incidental Findings

While performing your primary analysis, you may discover security issues OUTSIDE your focus area:

- Use finding ID prefix `IX-{AGENT_PREFIX}-XXX` (IX = incidental)
- Use abbreviated format (severity, file:line, one-paragraph description, ATT&CK technique if obvious)
- Do NOT write atomic files for incidentals — include them in your return message only
- Do NOT let incidental findings distract from your primary analysis

## Reading Recon Data

Your recon context comes in three levels:
- **LOD-0 + LOD-1**: In `{RECON_INDEX_PATH}` — summary table + paragraph per section
- **LOD-2**: Atomic step files in `{RECON_DIR}/step-{NN}-{name}.md` — full tables with file:line references

Your "Inputs" section specifies which step files are most relevant to your analysis. Read the index first, then selectively read the step files you need. Do not read all 14 step files unless your analysis requires broad context.
