## Description:

Standard SAPCONET SSH command templates for bird reads, Puppeteer runs, and inbox messaging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to standardize SSH-based SAPCONET command patterns for connectivity checks, bird reads, Puppeteer environment checks, and inbox messaging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text passed to the inbox messaging script can become unintended remote shell commands.

Mitigation: Review and fix scripts/msg-sapconet.sh before using it with untrusted or variable message text.

Risk: SSH commands may run against the wrong remote host or account if SAPCONET_TARGET is incorrect.

Mitigation: Confirm SAPCONET_TARGET points to the intended SAPCONET host and account before running the scripts.

Risk: The included SSH scripts are templates with placeholders rather than ready-to-run production workflows.

Mitigation: Treat the scripts as templates and review remote command placeholders before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highlander89/skills/sapconet-ssh-bridge)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash script templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SAPCONET_TARGET configuration and review of remote command placeholders before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
