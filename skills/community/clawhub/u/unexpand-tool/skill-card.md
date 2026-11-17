## Description:

Convert spaces to tabs in text files. Use for consistent indentation and reducing file size by replacing spaces with tabs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert space-indented text files to tab-indented text for formatting consistency or smaller files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can accidentally treat piped stdin text as a local file path and print that file's contents.

Mitigation: Use only explicit, trusted local file paths until stdin handling is fixed; do not expose the script to services, automation, or untrusted input.

Risk: Security evidence marks the release verdict as suspicious.

Mitigation: Review the script before installation or execution and apply the server guidance before using it in shared or automated environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/unexpand-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May transform local file content by replacing spaces with tab characters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
