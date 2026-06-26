## Description: <br>
Uploads a video to YouTube using the official YouTube Data API v3 and OAuth 2.0, with support for titles, descriptions, privacy settings, and large file chunking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrOrlandi](https://clawhub.ai/user/BrOrlandi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to upload local video files to YouTube through the official API after configuring Google Cloud OAuth credentials. It is suited for agent-assisted publishing workflows that need title, description, privacy, and resumable upload support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires YouTube upload permission through Google OAuth. <br>
Mitigation: Install and run it only when that permission is acceptable, and revoke the Google OAuth grant when it is no longer needed. <br>
Risk: OAuth client secrets and generated tokens can allow access if exposed. <br>
Mitigation: Keep client_secret.json and token.pickle private, avoid committing or sharing them, and delete token.pickle when resetting access. <br>
Risk: An unintended file or privacy setting could publish content incorrectly. <br>
Mitigation: Confirm the target video path, title, description, and privacy setting before each upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BrOrlandi/youtube-upload) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, pip, Google API Python libraries, a Google Cloud OAuth client secret file, and local user authentication on first run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
