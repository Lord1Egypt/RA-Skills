## Description:

Automates Remnawave account creation, subscription retrieval, template-based onboarding email delivery, carbon-copy recipients, and internal squad assignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uepuer](https://clawhub.ai/user/uepuer)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and administrative teams use this skill to provision Remnawave users, assign internal squads, send onboarding emails, and record account-creation outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged Remnawave and SMTP credentials can be used insecurely.

Mitigation: Install only in a controlled admin workspace, rotate any matching credentials, keep secrets outside the artifact, and require validated TLS before production use.

Risk: The bundled scripts can create, modify, or delete user accounts without enough safeguards.

Mitigation: Require human approval for destructive or force-recreate paths, restrict API token permissions, and avoid running delete or test scripts against production.

Risk: Account identifiers, emails, subscription URLs, and operation outcomes may be written to local logs.

Mitigation: Restrict access to the log directory, review retention needs, and avoid invoking the skill with untrusted account parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uepuer/skills/remnawave-account-creator)
- [README](artifact/README.md)
- [Remnawave API Reference](artifact/API-REFERENCE.md)
- [Workflow](artifact/WORKFLOW.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets; scripts emit console text, account details, email status, and local JSON or Markdown logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Remnawave API and SMTP configuration; may create, update, search, or delete Remnawave users when invoked with privileged credentials.]

## Skill Version(s):

1.2.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
