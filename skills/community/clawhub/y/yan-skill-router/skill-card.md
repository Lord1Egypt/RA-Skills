## Description:

Routes user requests to the most relevant agent skills with BM25 and embedding candidate selection, Chinese-to-English query bridging, top-5 ranking, and rejection rules for requests better handled by fallback tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awoo129](https://clawhub.ai/user/awoo129)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reduce token-heavy manual skill selection in large skill libraries, especially when user queries may be in Chinese and available skill metadata is primarily in English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback catalog can propose shell commands, package installs, external API calls, or email sending.

Mitigation: Require explicit confirmation before execution, constrain allowed tools, and validate or escape user-controlled input.

Risk: Routing and fallback behavior can expose agents to prompt injection or incorrect tool selection.

Mitigation: Treat routing output as a recommendation, review selected skills before execution, and keep rejection thresholds scoped to the deployment.

Risk: External fallback tools may send queries or credentials to third-party services.

Mitigation: Use scoped environment credentials, redact sensitive user data, and disable external fallback categories that are not required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/awoo129/skills/yan-skill-router)
- [Publisher Homepage](https://github.com/awoo129/wangyan)
- [Rejection Word Lists](artifact/references/noise-words.md)
- [Translation Bridge Map](artifact/references/zh2en-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python routing results and formatted Markdown/plain text for agent handoff]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ranked top-5 skill candidates, rejection or fallback notes, and optional chain guidance.]

## Skill Version(s):

2.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
