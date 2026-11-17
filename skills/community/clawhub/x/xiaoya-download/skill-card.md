## Description:

Xiaoya Download helps an agent search a configured Xiaoya/Alist media server for movies or TV series, present selectable results, and copy selected files from a local WebDAV mount into a configured download directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanshojin](https://clawhub.ai/user/hanshojin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and media-library operators use this skill to search a configured Xiaoya/Alist instance, review available media variants, and copy selected files into a local download directory through a mounted WebDAV path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts the configured Xiaoya/Alist host and copies selected files into the configured download directory.

Mitigation: Install and run it only with a trusted Xiaoya/Alist server, a deliberately chosen download directory, and a WebDAV mount path you expect the skill to read from.

Risk: Search result names from untrusted servers are printed to the terminal without control-character sanitization.

Mitigation: Treat results from untrusted servers cautiously and review selected paths before running the copy command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanshojin/skills/xiaoya-download)
- [Publisher profile](https://clawhub.ai/user/hanshojin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include JSON emitted by the bundled Python script.]

## Skill Version(s):

1.3.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
