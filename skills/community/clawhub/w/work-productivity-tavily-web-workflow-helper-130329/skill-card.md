## Description:

Helps agent users and skill authors create, debug, harden, and validate Tavily-style web search productivity workflows for ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn demand for Tavily-style web search workflows into practical plans, templates, checklists, code changes, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers and implicit invocation may activate the skill for generic web search or bug-fix requests.

Mitigation: Invoke the skill explicitly by name, or narrow the triggers before deployment when precise routing matters.

Risk: Workflow, code, or shell guidance produced by the skill may be incorrect or incomplete for a user's environment.

Mitigation: Review generated artifacts before use and validate them against the stated success criteria.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-130329)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Web Research Capability Issue](https://github.com/hugimuni-labs/brnrd/issues/411)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional checklists, code blocks, shell snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and remaining risks.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
