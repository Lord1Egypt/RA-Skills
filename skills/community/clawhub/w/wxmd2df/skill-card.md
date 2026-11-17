## Description:

Converts Markdown report files to PDF before sending them to channels such as WeChat and Feishu so recipients can view the report directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingxxxxx](https://clawhub.ai/user/jingxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a generated Markdown report needs to be delivered as a PDF, especially for WeChat and Feishu channels that require directly viewable files. It also provides fallback guidance for sending the original Markdown when conversion fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable third-party npm package during conversion, which creates code-execution and supply-chain risk.

Mitigation: Pin the converter version, use a lockfile or preinstalled vetted binary, and run conversion with limited filesystem and environment access.

Risk: PDF conversion can fail or produce imperfect layout for complex Markdown content.

Mitigation: Confirm that the generated PDF exists and is non-empty before sending; if conversion fails, send the original Markdown and notify the recipient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jingxxxxx/skills/wxmd2df)
- [Publisher profile](https://clawhub.ai/user/jingxxxxx)

## Skill Output:

**Output Type(s):** [guidance, shell commands, files]

**Output Format:** [Markdown guidance with an inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a PDF next to the source Markdown file and falls back to the original Markdown if conversion fails.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
