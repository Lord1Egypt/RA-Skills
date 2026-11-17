## Description:

Screens A-share and Hong Kong stocks for technical patterns such as moving-average alignment, volume pullbacks, volume breakouts, and candlestick setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otouman](https://clawhub.ai/user/otouman)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to screen Chinese A-share and Hong Kong equities with configurable technical-analysis strategies and price filters. Results are intended as informational screening output, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hong Kong stock screening results may be unreliable because the security evidence flags Hong Kong support as requiring validation.

Mitigation: Validate Hong Kong results independently before relying on them, and prefer markets whose data retrieval path has been tested for the release.

Risk: Dependency behavior may change over time because the artifact documents unpinned AKShare, pandas, and numpy dependencies.

Mitigation: Run the skill in a virtual environment with reviewed or pinned dependencies.

Risk: Technical-analysis signals could be mistaken for investment advice.

Mitigation: Present outputs as informational screening results and require human review before any trading decision.

## Reference(s):

- [A-share technical screening strategies](references/strategies.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON result arrays and Markdown summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include stock code, name, price, matched strategy, score, reason, and change percentage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
