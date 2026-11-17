## Description:

Generates structured thematic research reports from natural-language queries for topics, events, policies, investment themes, cross-industry impacts, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request deep thematic research reports on events, policies, market themes, technology trends, and cross-industry questions. The skill calls EastMoney's thematic research service and returns report content, a share link, and generated attachments when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries are sent to EastMoney using EM_API_KEY.

Mitigation: Install only when this external API use is acceptable, and handle EM_API_KEY as a secret that is not written to code, prompts, logs, or output files.

Risk: Generated DOCX/PDF attachments from the remote service can be saved locally, including when users expect non-persistent behavior from --no-save.

Mitigation: Do not rely on --no-save for non-persistent operation until fixed, and avoid opening generated attachments unless the API source is trusted.

Risk: Financial or thematic research output can be incomplete, delayed, or unsuitable as investment advice.

Mitigation: Present report content as reference material, include risk notice language, and return explicit errors instead of inventing conclusions when the service fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/topic-research-report)
- [Financial AI Analyst publisher profile](https://clawhub.ai/user/financial-ai-analyst)
- [EastMoney Miaoxiang service](https://ai.eastmoney.com/mxClaw)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown report text with share-link text and optional local DOCX/PDF file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and may save generated DOCX/PDF attachments locally when the EastMoney API returns them.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
