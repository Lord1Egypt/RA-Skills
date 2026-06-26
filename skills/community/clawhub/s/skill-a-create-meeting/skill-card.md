## Description: <br>
Coordinates new meeting creation by requiring OpenClaw to gather meeting details, then preparing Gitea meeting records, attendee email data, logs, and invitation email content after Tencent Meeting details are available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent builders and meeting coordinators use this skill as the entry point for new meeting requests that need repository-backed agendas, metadata, attendee email lookup, logging, and prepared invitation email content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger rules may cause the workflow to prepare meetings, repository writes, member email lookups, logs, and invitation email content without a clear final confirmation step. <br>
Mitigation: Require the agent to show a concise meeting summary and obtain explicit user approval before creating meetings, writing repository files, collecting recipient emails, or sending invitations. <br>
Risk: The skill uses a Gitea bot token and writes meeting metadata, agendas, and logs to configured repositories. <br>
Mitigation: Use a least-privilege bot token limited to the intended repositories and verify the configured Gitea server and meta repository before installation. <br>
Risk: The setup flow creates or reads a local .env file containing Gitea connection details and credentials. <br>
Mitigation: Inspect the .env file before running setup.sh and keep credential files private with restrictive permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skill-a-create-meeting) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/myd2002) <br>
- [Configured Gitea server](http://43.156.243.152:3000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, JSON] <br>
**Output Format:** [JSON response with user-facing text, invitation email fields, repository member data, agenda link, and meeting directory metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates Gitea meta.yaml and agenda.md files, writes JSONL logs, and prepares HTML email content for a separate email-sending skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
