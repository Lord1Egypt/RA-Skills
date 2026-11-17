## Description:

This skill should be used when the user asks about Workvivo — their company's employee intranet / social feed (Zoom Workvivo) — through the workvivo-mcp server's workvivo_* tools. Triggers on "check Workvivo", "what's on the intranet", "company news", "Workvivo feed", "town hall", "upcoming company events", "who is <colleague>", "search Workvivo for…", "shoutouts", or a Workvivo space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use the skill to read and search their organization's Workvivo feed, news, events, spaces, documents, and people through their signed-in account. It provides read-only answers and summaries of the retrieved company content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan could not resolve the referenced docs/WORKVIVO-API.md, so that material was not assessed.

Mitigation: Review the referenced document and assess it before installing if you need it to evaluate the skill.

Risk: Workvivo search records queries in the user's own search history.

Mitigation: Consider query visibility in that history when searching for sensitive subjects.

## Reference(s):

- [Workvivo MCP on ClawHub](https://clawhub.ai/chrischall/skills/workvivo-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text or Markdown summaries and answers based on Workvivo content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only access; content may include UTC timestamps and results can be compact or full.]

## Skill Version(s):

0.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
