## Description:

Tencent Meeting MCP helps an agent create, update, cancel, query, and analyze Tencent Meeting sessions, including participants, recordings, transcripts, and AI summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris8265-cl](https://clawhub.ai/user/chris8265-cl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to manage Tencent Meeting workflows through an agent, including meeting scheduling, participant lookup, recording access, transcript search, and AI meeting summaries. It is intended for authorized Tencent Meeting data and requires a configured Tencent Meeting token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and expose sensitive meeting content such as transcripts, recordings, passwords, join links, and participant details.

Mitigation: Use the skill only with meetings the user is authorized to access and share, and avoid requesting or disclosing sensitive meeting data outside that authorization.

Risk: The setup step may install or configure mcporter broadly for the current environment.

Mitigation: Review setup.sh before running it, avoid administrator execution, and consider installing a reviewed or pinned mcporter version separately.

Risk: A Tencent Meeting token can grant access beyond a single task if it is overprivileged.

Mitigation: Use a least-privileged Tencent Meeting token and keep TENCENT_MEETING_TOKEN out of shared logs, prompts, and generated artifacts.

## Reference(s):

- [Tencent Meeting MCP Tool Reference](references/api_references.md)
- [Tencent Meeting MCP Endpoint](https://mcp.meeting.tencent.com/mcp/wemeet-open/v1)
- [Tencent Meeting AI Skill Token Page](https://meeting.tencent.com/ai-skill)
- [ClawHub Skill Page](https://clawhub.ai/chris8265-cl/skills/tencent-meeting-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include meeting identifiers, participant details, passwords, recording links, transcript text, and AI-generated meeting summaries when authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
