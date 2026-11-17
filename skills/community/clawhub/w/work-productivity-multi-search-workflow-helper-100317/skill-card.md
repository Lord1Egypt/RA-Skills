## Description:

Helps agent users, skill authors, maintainers, and teams create practical multi-search workflow artifacts, checklists, analysis, code changes, and decision support for productivity tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn multi-search productivity needs into concrete plans, templates, checklists, analysis, code changes, or workflow guidance. It is intended for repeatable work where assumptions, constraints, validation criteria, and remaining risks need to be made explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger language and implicit invocation may cause the skill to activate for ordinary search or workflow requests.

Mitigation: Review routing behavior before deployment; narrow trigger phrases or disable implicit invocation where precise skill selection is required.

Risk: Generated workflow or implementation guidance may be incorrect or incomplete for a user's local constraints.

Mitigation: Require users or maintainers to review assumptions, validate outputs against stated success criteria, and scan any produced code or commands before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-multi-search-workflow-helper-100317)
- [Requirement Plan](artifact/references/requirement-plan.md)
- [Multi Search Engine demand signal](https://clawhub.ai/skills/multi-search-engine)
- [Agent Browser demand signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Tavily Search demand signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Hacker News demand signal](https://news.ycombinator.com/item?id=49014048)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text with optional code blocks, shell commands, checklists, templates, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, validation notes, and remaining risks when relevant.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
