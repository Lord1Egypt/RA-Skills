## Description:

Helps agent users, skill authors, maintainers, and teams create practical workflows, checklists, artifacts, analysis, or code support for Agent Browser-style automation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to plan and improve Agent Browser-style workflows for bug fixing, setup hardening, reliability, and adjacent skill creation. It helps produce actionable local-hardware-friendly workflows, checklists, artifacts, analysis, code changes, or decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger words and implicit invocation may route ordinary browser, automation, CLI, or bug-fix requests to this skill when it is not the best match.

Mitigation: Narrow trigger terms where possible and have the agent confirm the Agent Browser workflow context before applying recommendations.

Risk: Generated workflow guidance may influence automation setup, safety hardening, or reliability changes without enough local validation.

Mitigation: Review generated plans, commands, configuration, and checklists before use, then test changes in a non-production environment before wider deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-agent-browser-workflow-helper-110309)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: Agent Browser](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Ask HN: How do you test AI-generated code?](https://news.ycombinator.com/item?id=48655020)
- [LiteLLM issue summary - 2026-06-25](https://github.com/arielb1-sun-security/copilot-studio-test/issues/2209)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and follow-up risks.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
