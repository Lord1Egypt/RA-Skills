## Description:

Provides single-stock comprehensive diagnosis for Shanghai, Shenzhen, and Beijing A-share equities from natural-language questions, returning structured Markdown reports for broad questions about overall outlook, holding decisions, risks, and opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request a concise diagnosis of one mainland China A-share stock from a broad natural-language question. It is intended for single-stock review and decision support, not for multi-stock comparison, non-A-share markets, or precise calculation of a named indicator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock questions are sent to Eastmoney's service using EM_API_KEY.

Mitigation: Use a revocable, scoped key where available and avoid including sensitive personal context in stock questions.

Risk: Markdown diagnosis reports may be saved locally by default.

Mitigation: Run with --no-save when local report retention is not desired.

Risk: The report may be mistaken for investment advice.

Mitigation: Keep the skill's risk notice visible and treat outputs as reference information rather than financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/stock-diagnosis)
- [Eastmoney Miaoxiang service](https://ai.eastmoney.com/mxClaw)
- [Eastmoney stock analysis API base](https://ai-saas.eastmoney.com/proxy/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown report text, with optional saved .md files and command-line or Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY; accepts one natural-language stock question through --query or stdin; --no-save prevents local Markdown report retention.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
