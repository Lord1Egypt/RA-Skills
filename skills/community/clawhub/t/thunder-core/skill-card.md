## Description:

Windows Thunder download client via COM interface for adding, committing, canceling, and managing download tasks programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate Thunder/Xunlei downloads on Windows through Python and the Thunder COM interface, including queueing downloads, applying optional headers, committing tasks, checking tasks, and canceling active tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start or cancel real Thunder downloads.

Mitigation: Use it only for explicit Thunder/Xunlei download tasks and confirm URLs, destinations, and cancellation intent before committing actions.

Risk: Download tasks can include cookies and custom headers.

Mitigation: Avoid passing cookies unless necessary, and do not provide sensitive session values unless the destination and need are clear.

Risk: The module includes a direct-run test that downloads an unrelated executable without confirmation.

Mitigation: Do not run the module directly as a test; import its functions or classes and call them only with user-approved inputs.

Risk: COM registration troubleshooting may encourage elevated execution.

Mitigation: Avoid administrator shells unless needed for the Thunder COM registration issue and the operational impact is understood.

## Reference(s):

- [Thunder official website](https://www.xunlei.com/)
- [ClawHub skill page](https://clawhub.ai/534422530/skills/thunder-core)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; relies on Python, pywin32, an installed Thunder client, and COM component availability.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
