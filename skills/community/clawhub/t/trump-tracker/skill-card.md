## Description:

Samples RSS news feeds and produces bilingual sentiment-based commentary framed as Trump-related unreliability, execution-probability, and market-impact output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneychen](https://clawhub.ai/user/kenneychen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run a Python-based news monitor and bilingual sentiment commentary workflow about Trump-related topics. Its output should be treated as informal analysis, not reliable live news or financial or political forecasting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate live Trump tracking because it uses generic RSS sources and fallback data.

Mitigation: Treat output as informal commentary and clearly label fallback data as sample or cached data.

Risk: RSS feed integrity is weakened by disabled TLS verification.

Mitigation: Review the code before use and remove disabled TLS verification before relying on fetched feed content.

Risk: The output can be mistaken for reliable live news or financial or political forecasting.

Mitigation: Do not use the generated scores or commentary as financial, political, legal, or safety-critical advice.

Risk: Unpinned dependencies may change behavior or introduce dependency risk.

Mitigation: Install in a virtual environment and review or pin dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kenneychen/skills/trump-tracker)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Console text with bilingual English and Chinese sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses RSS feed samples when available and fallback sample data when fetching fails.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
