## Description:

企業PUA話術と構造化デバッグ方法論で、失敗後の問題解決における調査、検証、方針転換を促す日本語プロンプトスキルです。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanweai](https://clawhub.ai/user/tanweai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to push a Japanese-language agent toward more persistent troubleshooting after repeated failures, including broader investigation, hypothesis changes, and verification before giving up. It is best suited to controlled debugging or problem-solving sessions where assertive prompting is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill pressures the agent to keep acting and use available tools broadly across task types, which can exceed the intended scope in sensitive environments.

Mitigation: Use it only with clear task boundaries, approval gates, and agents that are restricted from production mutation, sensitive local files, costly APIs, and deployment actions unless separately authorized.

Risk: The high-pressure Japanese troubleshooting style may produce overly forceful guidance during user-facing interactions.

Mitigation: Review tone expectations before installation and avoid enabling it where calm, neutral, or customer-facing communication is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanweai/skills/pua-debugging-ja)
- [Project homepage](https://openpua.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown or plain text guidance, with code blocks or shell commands when the underlying task calls for them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Japanese-language high-pressure troubleshooting guidance that can apply across coding, research, writing, operations, API integration, data analysis, and deployment tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
