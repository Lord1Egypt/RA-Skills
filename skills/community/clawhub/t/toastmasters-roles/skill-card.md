## Description:

头马官员 is a Chinese-language prompt skill that maps complex tasks into Toastmasters-style officer roles and returns a role-based task breakdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathanontheearth-spec](https://clawhub.ai/user/nathanontheearth-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to break complex planning or operations work into Toastmasters-style officer responsibilities, dependencies, deliverables, and timelines. It is most useful when a task benefits from explicit ownership across roles such as President, VPE, VPM, VPPR, Treasurer, SAA, Secretary, Risk Officer, or IPP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce role-planning guidance that is incomplete, poorly matched to the user's real organization, or misleading if treated as final operational advice.

Mitigation: Review the generated role assignments, dependencies, and timelines before using them for real work.

Risk: The README includes an unpinned global ClawHub CLI install command for publishing workflows.

Mitigation: Pin the ClawHub CLI version before following the publishing steps.

Risk: The skill is Chinese-language in scope, which may be unclear to users expecting English output.

Mitigation: Confirm the desired output language and translate or adapt officer labels when needed.

## Reference(s):

- [头马官员详细职责手册](references/roles.md)
- [ClawHub skill page](https://clawhub.ai/nathanontheearth-spec/skills/toastmasters-roles)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown task breakdown with role-assignment tables and action lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only output; no command execution, persistence, external calls, or private data access are indicated by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
