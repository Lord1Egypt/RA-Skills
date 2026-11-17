## Description:

从专利发展脉络梳理一项技术的演进阶段，整理关键专利、其解决的问题及推动者，并提供有来源的时间线。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

面向撰写综述、制作汇报或了解行业发展的研究人员与从业者，用专利检索结果梳理技术发展阶段、代表专利及其贡献。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential forwarding may expose an API key.

Mitigation: Have credential forwarding fixed before using a paid key; provide credentials outside chat, and test in an isolated environment with a limited trial key.

Risk: Malformed patent numbers may allow access to files outside the task cache.

Mitigation: Require a fix for patent-number validation before use; test only in an isolated environment.

Risk: Confidential invention details could be exposed during research.

Mitigation: Do not submit confidential invention details, and set an API spending cap.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ip930/skills/tech-evolution-timeline)
- [PatentMax API](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Markdown, CSV-compatible table]

**Output Format:** [Markdown technology timeline and a tabular file that can be opened in Excel]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sourced patent timeline organized into stages, with key patents and explanations of the problems they address and who drove the work.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
