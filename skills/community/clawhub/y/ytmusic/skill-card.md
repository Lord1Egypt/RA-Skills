## Description:

Manage YouTube Music library, playlists, and discovery via ytmusicapi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gentrycopsy](https://clawhub.ai/user/gentrycopsy)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure ytmusicapi access and manage YouTube Music library items, playlists, metadata, lyrics, and discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow stores sensitive YouTube Music browser session data in plaintext files.

Mitigation: Keep headers.txt and browser.json out of source control and shared folders, restrict file permissions, delete headers.txt after generating browser.json, and revoke or rotate the browser session if either file is exposed.

Risk: Installing ytmusicapi directly can pull dependencies into the active Python environment.

Mitigation: Install dependencies in an isolated, pinned environment.

## Reference(s):

- [YouTube Music](https://music.youtube.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local authentication files such as oauth.json or browser.json.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
