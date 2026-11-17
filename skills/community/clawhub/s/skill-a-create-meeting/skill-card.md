## Description:

Skill A Create Meeting coordinates new meeting creation requests by taking upstream Tencent Meeting details, creating Gitea meeting records and agendas, resolving repository participants, logging the run, and returning invitation content for email delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team automation users use this skill as the primary entry point for new meeting requests that need repository-backed agenda files, meeting metadata, participant email resolution, and downstream invitation sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Gitea tokens and repository data, and the provided example configuration uses an HTTP Gitea endpoint.

Mitigation: Use only an HTTPS Gitea endpoint, rotate any token used with the HTTP default, and scope the bot token to the minimum repositories and actions needed.

Risk: Generated invitation content includes meeting and repository values that should be treated as untrusted until escaping and URL validation are added.

Mitigation: Escape user-controlled HTML fields and validate meeting and agenda URLs before generated invitation content is sent.

Risk: The setup guidance may install dependencies into the system Python environment.

Mitigation: Run setup as a non-root user in an isolated environment such as a virtual environment or disposable container.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/skill-a-create-meeting)
- [Publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration]

**Output Format:** [JSON containing user-facing text, email invitation fields, repository participant data, meeting directory details, and links to generated agenda content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Gitea meeting metadata, agenda files, and log entries when configured with the required repository access.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
