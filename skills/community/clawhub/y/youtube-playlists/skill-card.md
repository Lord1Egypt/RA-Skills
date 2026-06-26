## Description: <br>
Create and manage YouTube playlists, including creating playlists, adding videos, and listing existing playlists through a Python command-line helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matejmicek](https://clawhub.ai/user/matejmicek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to authenticate with a YouTube account, create playlists, add videos by ID or URL, and inspect playlist information from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad YouTube account authority and can modify playlists. <br>
Mitigation: Install and run it only for accounts where playlist modification is acceptable, and review each command before execution. <br>
Risk: The skill stores a reusable local OAuth token in token.pickle. <br>
Mitigation: Delete token.pickle or revoke the Google OAuth grant when the skill is no longer needed. <br>
Risk: Implemented commands can print liked videos and subscriptions in addition to documented playlist operations. <br>
Mitigation: Treat command output as account data and avoid sharing logs that may contain private viewing or subscription information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matejmicek/youtube-playlists) <br>
- [YouTube OAuth scope used by the skill](https://www.googleapis.com/auth/youtube) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can create or modify YouTube playlists and can print playlist, liked-video, and subscription data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
