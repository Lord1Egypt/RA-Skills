## Description:

Helps ecommerce, advertising, marketing, and product teams turn tabletop product demo video requests into top-down layouts, hand-action scripts, subtitles, prompts, AI-HIVE generation tasks, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce teams, and marketing operators use this skill to plan and produce top-down product demonstration videos for social, advertising, and commerce channels. It provides reviewable briefs, scripts, prompts, runnable AI-HIVE commands, task records, and quality checks before any potentially billable generation step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE API key can be sent to a user-configured API endpoint.

Mitigation: Use the default AI-HIVE endpoint, avoid untrusted --base-url, AI_HIVE_BASE_URL, or config.json values, and rotate the API key if it may have been used with an untrusted endpoint.

Risk: Selected media may be uploaded and generation may incur charges.

Mitigation: Confirm the prompt, model mode, routing choice, uploaded media, and price snapshot before submitting generation tasks; start batch work with a small sample.

Risk: Generated product content can misstate product facts, authorization, platform fit, or performance expectations.

Mitigation: Keep factual claims tied to user-provided evidence, mark uncertain claims for review, verify rights to reference materials, and avoid promises about traffic, sales, ranking, review outcomes, or investment return.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/tabletop-product-demo-video-ai-hive)
- [AI-HIVE product entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown with JSON artifacts and inline bash or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE generation tasks after user confirmation and may download generated media files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
