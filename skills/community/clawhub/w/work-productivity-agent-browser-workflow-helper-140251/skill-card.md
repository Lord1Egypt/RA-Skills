## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical workflows, checklists, analyses, code changes, and decision support for Agent Browser-style browser automation work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn Agent Browser-style workflow needs into concrete plans, checklists, automation outlines, code changes, or implementation guidance. It focuses on browser and headless automation work where reliability, setup hardening, safety, and local hardware feasibility matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be selected for broad browser or automation requests because implicit invocation is enabled and trigger terms are generic.

Mitigation: Review generated automation plans, commands, and workflow changes before acting on them, especially when they affect browser setup, reliability, credentials, or safety posture.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-agent-browser-workflow-helper-140251)
- [Agent Browser ClawHub Demand Signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Evaluate removing Playwright as a first-class browser mode](https://github.com/manishiitg/mcp-agent-builder-go/issues/128)
- [Heredoc-style Agent Workflow Discussion](https://www.v2ex.com/t/1227024)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, checklists, and concise verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be actionable without requiring the reader to inspect the original demand sources.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
