## Description:

Send X/Twitter posts to Kindle for distraction-free reading. Use when user shares an X/Twitter link and wants to read it on Kindle, or asks to send a tweet/thread to their Kindle device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianlu365ai](https://clawhub.ai/user/brianlu365ai)

### License/Terms of Use:

ISC

## Use Case:

External users and developers use this skill to turn X/Twitter posts or threads into Kindle-readable attachments and send local PDF, HTML, or TXT files to a configured Kindle email address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can email any readable local file path supplied to its helper script.

Mitigation: Use only with tightly controlled generated files and require explicit confirmation of the exact source path and Kindle recipient before sending.

Risk: SMTP credentials may be exposed if stored in shared project files or plaintext setup notes.

Mitigation: Keep SMTP app passwords in environment variables or a proper secret store, and do not place app passwords in TOOLS.md or shared project files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianlu365ai/skills/x-to-kindle)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline code blocks, generated HTML attachments, and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided SMTP and Kindle email configuration; sends selected local files as email attachments.]

## Skill Version(s):

0.1.1 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
