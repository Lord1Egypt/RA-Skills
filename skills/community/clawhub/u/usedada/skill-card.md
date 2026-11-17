## Description:

Hosted backend infrastructure for OpenClaw agents, including managed databases, webhooks, and file hosting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rotemtam](https://clawhub.ai/user/rotemtam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Dada to add persistent structured storage, typed tables, inbound webhooks, file hosting, and CLI-driven project operations to OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a mutable external CLI that can manage hosted data, webhooks, and local identity keys.

Mitigation: Use a pinned CLI version or verified release binary, and test in a separate project before using production data.

Risk: Broad update or delete filters can modify or remove persistent records.

Mitigation: Query and review the affected records first, use the narrowest practical filters, and keep backups or exports for important data.

Risk: Webhook URLs can grant access to inbound event flows if exposed.

Mitigation: Treat webhook URLs as secrets, store them only in trusted configuration, and rotate or delete them after exposure.

Risk: Local identity key material is stored on the user's machine.

Mitigation: Run the CLI only on trusted machines and protect the local key files with normal secret-handling controls.

## Reference(s):

- [Dada homepage](https://usedada.dev)
- [Dada GitHub Releases](https://github.com/honeybadge-labs/dada/releases)
- [ClawHub skill page](https://clawhub.ai/rotemtam/skills/usedada)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON output flags for reliable machine parsing.]

## Skill Version(s):

0.3.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
