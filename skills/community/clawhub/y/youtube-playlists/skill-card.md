## Description:

Create and manage YouTube playlists through a Python command-line helper that authenticates with YouTube via OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matejmicek](https://clawhub.ai/user/matejmicek)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to authenticate to a YouTube account, create playlists, add videos, list playlists, and manage playlist contents from shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a user's YouTube account through OAuth, including creating playlists, adding videos, and removing playlist items.

Mitigation: Run it only in a private, trusted workspace with an account intended for these changes, and review each command before execution.

Risk: The security summary reports undocumented commands that expose liked videos and subscriptions.

Mitigation: Avoid undocumented account-data commands, or use a reviewed version that removes them before installation.

Risk: The security summary reports that OAuth tokens are cached in an unsafe local pickle file.

Mitigation: Protect the skill directory, do not share token.pickle, and prefer a version that stores tokens safely without pickle and narrows OAuth permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matejmicek/skills/youtube-playlists)
- [Publisher profile](https://clawhub.ai/user/matejmicek)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, browser-based OAuth, a local credentials.json file, and a local token cache.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
