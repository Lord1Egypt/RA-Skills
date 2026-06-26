## Description: <br>
Track and view your watched movies and TV shows via trakt.tv. Use when user asks about their watch history, what they've been watching, or wants to search for movies/shows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search Trakt.tv and inspect their own movie and TV watch history through the documented trakt-cli commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the wrong or unexpected npm trakt-cli package could expose the user to untrusted command-line behavior. <br>
Mitigation: Verify the npm package identity before installation and review it before using the skill in an agent environment. <br>
Risk: Saved Trakt credentials in ~/.trakt.yaml may allow access to watch-history data. <br>
Mitigation: Protect the credentials file like an account secret, limit access to the intended user, and revoke or rotate credentials if the file is exposed. <br>
Risk: The history command requires Trakt authentication and may reveal personal viewing history. <br>
Mitigation: Authenticate only the intended Trakt account and confirm the requested output is appropriate before sharing results. <br>


## Reference(s): <br>
- [Trakt.tv](https://trakt.tv) <br>
- [Trakt OAuth Applications](https://trakt.tv/oauth/applications/new) <br>
- [ClawHub Trakt Skill](https://clawhub.ai/mjrussell/trakt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only watch-history access requires Trakt authentication; search works without authentication.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
