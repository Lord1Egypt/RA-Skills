## Description:

Uses a seven-step method to analyze China A-share stocks and generate HTML reports covering ROE decomposition, profit model identification, industry comparison, and investment insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luokeer52](https://clawhub.ai/user/luokeer52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit China A-share stock analysis requests and receive financial analysis reports for Shanghai and Shenzhen exchange stocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance prompts and identifiers are processed by a remote Prana service.

Mitigation: Install only when remote processing is acceptable, keep the default trusted HTTPS endpoint, and avoid sending unnecessary sensitive information.

Risk: Reusable API credentials may be stored in config/api_key.txt.

Mitigation: Prefer environment-provided credentials, do not commit credential files, set PRANA_SKILL_SKIP_WRITE_API_KEY=1 to avoid plaintext persistence, and rotate exposed keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luokeer52/skills/stock-analysis-7step)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, HTML reports]

**Output Format:** [HTML report with financial analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs through Python or Node thin clients that send prompts to a remote Prana service.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
