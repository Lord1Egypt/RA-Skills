## Description:

Helps developers, maintainers, and skill authors plan and implement GitHub-style workflows for bug fixing, setup hardening, reliability improvements, and adjacent ClawHub skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and skill authors use this skill to turn GitHub-style workflow requests into concrete plans, checklists, code-change guidance, and validation steps. It is aimed at practical support for fixing bugs, improving reliability, hardening setup and safety, or creating related ClawHub workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad GitHub and CLI triggers may cause the skill to activate on generic requests where another workflow is a better match.

Mitigation: Review invocation behavior before installation and narrow trigger keywords or routing policy when predictable activation is required.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-140352)
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github)
- [GitHub project maintainer has a lot of issues](https://news.ycombinator.com/item?id=48829445)
- [Broken Enclosure URL in PinePod generated Feeds](https://github.com/madeofpendletonwool/PinePods/issues/903)
- [thumbnail: Gemini / Nano Banana route prompt alignment issue](https://github.com/daiki-beppu/youtube-automation/issues/1742)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, validation steps, and remaining risks when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
