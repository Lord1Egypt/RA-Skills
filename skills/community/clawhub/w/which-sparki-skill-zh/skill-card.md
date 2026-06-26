## Description: <br>
Helps agents choose and operate Sparki video-editing workflows for vlogs, short clips, captions, resizing, highlights, and cloud-rendered video outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to choose a Sparki editing workflow, configure a Sparki API key, upload local or Telegram Mini App video assets, start cloud edits, check status, and retrieve rendered results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is presented as a chooser/navigation skill but includes a full cloud video-editing CLI with upload, edit, polling, and download behavior. <br>
Mitigation: Install it only when a full Sparki cloud editing workflow is intended, and review commands before allowing video upload or task execution. <br>
Risk: Local videos may be uploaded to Sparki cloud services for processing. <br>
Mitigation: Use the skill only with videos that are appropriate to upload to Sparki, and confirm the target files before running upload or run commands. <br>
Risk: The setup flow can store a Sparki API key in a local plaintext configuration file. <br>
Mitigation: Prefer providing SPARKI_API_KEY from the environment when possible, and review or remove $HOME/.openclaw/config after setup if local key storage is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/which-sparki-skill-zh) <br>
- [Sparki homepage](https://sparki.io) <br>
- [Sparki Telegram bot](https://t.me/Sparki_AI_bot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload local video files to Sparki, poll cloud editing tasks, and download rendered video files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, pyproject.toml, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
