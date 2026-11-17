## Description:

Authorized SansFiction library manager. Adds books to your library, updates reading status, logs progress, and can schedule a daily "how much did you read today?" check-in. Requires a SansFiction personal token (read/write).

This skill is ready for commercial/non-commercial use.

## Publisher:

[fgbytes](https://clawhub.ai/user/fgbytes)

### License/Terms of Use:


## Use Case:

External users use this agent skill to manage a personal SansFiction library through authorized API calls, including adding books, updating reading status, logging reading progress, viewing current books, and checking reading stats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a read/write SansFiction personal token that could affect the user's library if exposed or misused.

Mitigation: Configure the token through a protected secret or environment variable, use a scoped and revocable token when available, and rotate it if exposure is suspected.

Risk: The setup flow asks the user to paste and persist the token in unsafe ways.

Mitigation: Do not paste the token into chat logs; store it only in protected configuration or secret storage.

Risk: The daily reading check-in can schedule recurring actions with a specific timezone.

Mitigation: Confirm the reminder time and timezone before enabling the check-in.

## Reference(s):

- [SansFiction](https://sansfiction.com)
- [SansFiction Agent Documentation](https://sansfiction.com/docs/agents)
- [SansFiction MCP Endpoint](https://sansfiction.com/api/mcp)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw Cron Jobs Documentation](https://docs.openclaw.ai/automation/cron-jobs)
- [ClawHub Skill Page](https://clawhub.ai/fgbytes/skills/sansfiction-library)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline bash commands and JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a SansFiction personal token exposed as SANSFICTION_TOKEN.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
