## Description:

Audits OpenCode and OpenClaw skills with local pattern scanning and optional VirusTotal hash checks before approving, warning on, or quarantining them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanew197894fun-cmd](https://clawhub.ai/user/lanew197894fun-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenCode or OpenClaw skill installations can use this skill to audit skills, gate installs, configure VirusTotal checks, and quarantine skills flagged by its review flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports unsafe install behavior for untrusted slugs.

Mitigation: Review the implementation before use and avoid the install command with untrusted slugs.

Risk: The release evidence reports quarantine and audit-all behavior that can move or delete local skill directories.

Mitigation: Run only on disposable or test skill directories until path validation and confirmation controls are added.

Risk: The release evidence says the sandbox protections are overstated.

Mitigation: Treat sandboxing as a file-copy review workflow, not real isolation; use operating-system isolation when evaluating untrusted skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanew197894fun-cmd/skills/skill-gatekeeper)
- [VirusTotal file report API](https://www.virustotal.com/api/v3/files/{hash})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown usage guidance with bash examples and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bun; optional VirusTotal API key enables cloud hash checks.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
