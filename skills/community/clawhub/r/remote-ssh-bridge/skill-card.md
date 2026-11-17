## Description:

Standard SSH command templates for a remote operator machine (bird reads, Puppeteer runs, inbox-style messaging).

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to apply standard SSH command patterns for remote operator machines, including connectivity checks, bird read placeholders, Puppeteer prerequisite checks, and inbox-style message templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted message text can become commands on the configured SSH host.

Mitigation: Review and fix the message script before using it with generated or untrusted message text; prefer stdin to a fixed remote handler or robust remote-shell-safe quoting.

Risk: Remote SSH execution can affect the configured host with the privileges of the SSH account.

Mitigation: Set REMOTE_TARGET deliberately, review placeholders before running commands, and restrict the SSH account to the least privilege needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highlander89/skills/remote-ssh-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a configured REMOTE_TARGET value and reviewed remote command placeholders before use.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
