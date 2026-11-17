## Description:

Quickly captures a short note to a local Markdown inbox file with an ISO timestamp and optional tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to append quick notes, tasks, ideas, and reference snippets to a local notes inbox from a command-line or automation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Callers or automations can write unintended note text or tags into ~/notes/inbox.md.

Mitigation: Review any caller or automation that invokes the script and pass only intended note text and tags.

Risk: The skill depends on local filesystem access to create or append to ~/notes/inbox.md.

Mitigation: Install only in environments where writing to the local notes directory is expected and acceptable.

## Reference(s):

- [Skill page](https://clawhub.ai/terrycarter1985/skills/quick-note-capture)
- [Tags reference](references/tags.md)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [markdown, shell commands, text]

**Output Format:** [Markdown note line appended to ~/notes/inbox.md, with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and a writable ~/notes/ directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
