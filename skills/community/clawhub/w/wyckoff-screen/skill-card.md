## Description:

Screens A-share stocks with Wyckoff phase and volume profile scoring to identify accumulation or trend-start candidates and return a ranked candidate list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxarch1980](https://clawhub.ai/user/dxarch1980)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-tool developers use this skill to run post-close A-share market scans and review Wyckoff-based candidates by score, phase, VPOC position, and signal summary. It supports right-side trend confirmation and left-side accumulation screening modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence financial decisions while relying on external stock-data services and generated screening scores.

Mitigation: Review results before acting on them, validate market data independently, and treat ranked candidates as analysis support rather than investment advice.

Risk: Server security evidence reports a hardcoded market-data token and an undocumented plaintext HTTP endpoint.

Mitigation: Remove embedded secrets and replace the plaintext endpoint with a user-provided secret and trusted HTTPS data provider before use.

Risk: The skill writes local SQLite caches and dated result files.

Mitigation: Run it in a workspace where local market-data caches and screening outputs are expected, review file paths before execution, and avoid sharing generated caches if they contain sensitive usage context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxarch1980/skills/wyckoff-screen)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Ranked screening summaries with stock codes, phases, scores, VPOC values, current prices, signal notes, and dated text result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local SQLite stock-data caches and dated screening result files; outputs are based on end-of-day market data rather than real-time quotes.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
