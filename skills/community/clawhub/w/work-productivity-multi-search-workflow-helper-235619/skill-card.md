## Description:

Helps AI-agent users and skill authors create, debug, harden, and validate multi-search-engine-style workflows and adjacent productivity skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn multi-search-engine workflow needs into practical plans, checklists, code changes, and validation notes that remain feasible on local hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad keywords and implicit invocation can activate the skill on ordinary search-related prompts.

Mitigation: Prefer explicit invocation when this workflow helper is needed, and confirm that search-related prompts actually require this skill before applying its workflow.

Risk: The skill may propose workflow, code, shell command, or configuration changes that are unsuitable for a user's specific environment.

Mitigation: Review proposed artifacts before use and validate changes against the stated success criteria, local constraints, and any project tests or checks.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-multi-search-workflow-helper-235619)
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine)
- [Agent Browser Demand Signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional checklists, code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and follow-up risks.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
