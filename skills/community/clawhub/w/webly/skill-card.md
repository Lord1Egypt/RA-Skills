## Description:

Webly lets agents publish websites and share files by live URL, then claim and manage sites through an account and MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tokifyi](https://clawhub.ai/user/tokifyi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use Webly to publish websites or share files, then manage claimed sites through Webly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Folder sharing could expose files outside the intended selection.

Mitigation: Review the explicit file list, exclude secrets and repository history, and reject symlinks that leave the selected folder.

Risk: Update instructions may run new code without approval.

Mitigation: Require approval for updates and choose the narrowest account access needed. Confirm the intended access for published links; expiry and random URLs do not make sensitive files private.

## Reference(s):

- [Webly homepage](https://webly.ai)
- [Webly documentation](https://api.webly.ai/docs)
- [Webly API contract](https://api.webly.ai/llms.txt)
- [Webly MCP server](https://api.webly.ai/v1/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, URLs]

**Output Format:** [Markdown with inline commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns publication or file-sharing links and status details; available actions depend on account and site state.]

## Skill Version(s):

0.14.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
