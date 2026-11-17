## Description:

Helps agent users and skill maintainers create, fix, harden, and validate Tavily-style web search workflows for ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn demand for Tavily-style web search workflows into practical plans, checklists, templates, scripts, configuration guidance, bug fixes, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms may cause the skill to trigger on generic web, search, or API requests.

Mitigation: Use explicit invocation for Tavily-style workflow work, or narrow platform triggers before deployment.

Risk: Workflow guidance may produce unsuitable changes if the user's search provider, safety policy, or reliability requirements are not checked.

Mitigation: Validate generated plans, scripts, and configuration against the user's stated constraints and review criteria before applying them.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-080414)
- [Tavily search demand signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Web research capability demand signal](https://github.com/hugimuni-labs/brnrd/issues/411)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, checklists, templates, implementation notes, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow helper; no executable code or persistence is included in the artifact.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
