## Description:

Detects and flags wash trades in NFT transaction data using 7 confidence-weighted patterns, protecting all downstream scoring and signals from artificial inflation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperbuddha](https://clawhub.ai/user/paperbuddha)

### License/Terms of Use:


## Use Case:

Developers and marketplace analysts use this skill to assess NFT sales transaction records for wash-trade patterns and produce structured risk results for downstream review or scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic wash-trade flags may be mistaken for definitive fraud determinations.

Mitigation: Treat the structured result as an assessment and keep human or policy review around consequential marketplace or scoring actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, text, configuration]

**Output Format:** [Structured assessment object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns wash-trade flag, confidence, matched pattern, status, applied weight, exclusion indicator, and analysis timestamp.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
