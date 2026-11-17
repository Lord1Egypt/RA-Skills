## Description:

Read Later Pro helps agents save web articles for later reading by extracting clean article content, organizing a local library, and converting saved content for offline use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awdasfdada](https://clawhub.ai/user/awdasfdada)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture web articles, extract readable text, organize a local read-later library, and convert saved content for offline reading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports weakly scoped URL, file, and credential-related workflows.

Mitigation: Use the skill only with trusted URLs and files, and avoid providing service passwords or tokens until credential handling is clarified.

Risk: The security evidence notes unsafe or unsupported behavior, including advertised features that may not be fully implemented.

Mitigation: Review generated commands and expected outputs before relying on them, especially for service integration, paywall-related behavior, and format conversion.

Risk: Saved library data is written under the user's home directory and deletions can remove saved article directories.

Mitigation: Confirm the library location before use, back up important saved articles, and review article IDs before deletion.

## Reference(s):

- [Read Later Pro on ClawHub](https://clawhub.ai/awdasfdada/skills/read-later-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, plus JSON or text output from bundled helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write saved article content and index data under the user's home directory when library-management helpers are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
