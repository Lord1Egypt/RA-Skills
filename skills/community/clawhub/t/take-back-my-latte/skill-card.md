## Description:

Analyze OpenAI Usage and Costs JSON, show actual spend in lattes, and estimate how many lattes the user could recover next month.

This skill is ready for commercial/non-commercial use.

## Publisher:

[margaretzybgl](https://clawhub.ai/user/margaretzybgl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze local OpenAI Costs and Usage JSON exports, understand spend in simple latte terms, and identify directional cost-recovery opportunities for the next month.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenAI billing or usage exports may contain sensitive organization cost and usage information.

Mitigation: Analyze exports locally, do not request API keys, avoid uploading raw exports, and review any report before sharing it.

Risk: The skill appends an external website link that is outside the local-only privacy boundary.

Mitigation: Treat the website as optional and do not paste billing data into it unless the user separately trusts that site.

Risk: Recoverable cost estimates could be mistaken for guaranteed savings.

Mitigation: Describe recoverable cost as directional and validate any optimization with a small production test.

## Reference(s):

- [Supported input formats](artifact/references/input-formats.md)
- [ClawHub skill page](https://clawhub.ai/margaretzybgl/skills/take-back-my-latte)
- [Take Back My Latte website](https://take-back-my-latte.margaret-zybgl.chatgpt.site)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report based on local JSON analyzer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report should stay under 250 words unless the user asks for detail; recoverable cost is directional, not guaranteed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
