## Description:

Syscheck is presented as a system health checker and diagnostics tool, but the reviewed release mainly stores, searches, and exports user-supplied command text in local logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sysadmins, and DevOps users may invoke Syscheck from a Linux shell for quick status-style commands. Reviewers should note that the inspected release mainly records, searches, and exports user-entered text rather than performing live diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as a live system diagnostics tool, but the security evidence says the inspected script mainly stores, searches, and exports user-supplied text in local logs.

Mitigation: Review the skill carefully before installing and do not rely on this release as a trustworthy system health checker unless it is rewritten to match its stated purpose.

Risk: User-entered secrets, host details, incident notes, tokens, or other sensitive operational data may be retained in local history and export files.

Mitigation: Avoid entering sensitive operational data; require clear storage and retention disclosure, hardened file permissions, and safe export encoding before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/syscheck)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text command output with optional JSON, CSV, or text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist user-supplied command text in local logs and export files under ~/.local/share/syscheck.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
