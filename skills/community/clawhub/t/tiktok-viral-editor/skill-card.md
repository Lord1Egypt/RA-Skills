## Description: <br>
Scenario-focused Sparki skill for TikTok-native pacing and viral-style edits while using the official Sparki setup, API-key, and upload workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn source footage into faster, hook-driven short-form edits for TikTok-style pacing, captions, clips, reels, montages, and highlight videos. It guides setup, upload, and Sparki CLI commands for prompt-driven video editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uploads user video files to Sparki's cloud editing service. <br>
Mitigation: Upload only videos that are appropriate to send to Sparki and review the configured endpoint before use. <br>
Risk: The workflow uses a Sparki API key that may be stored locally or read from the environment. <br>
Mitigation: Prefer environment-based secrets on shared machines, protect persisted API keys, and rotate credentials if exposure is suspected. <br>
Risk: Users may try to send videos directly through Telegram chat even though the skill does not support that path. <br>
Mitigation: Use a local file path in the OpenClaw environment or the Telegram Mini App upload link from `sparki upload-tg`. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fischerlam/tiktok-viral-editor) <br>
- [Publisher Profile](https://clawhub.ai/user/fischerlam) <br>
- [Sparki Homepage](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may reference local file paths, Sparki API key configuration, upload commands, task status, and downloaded video output locations.] <br>

## Skill Version(s): <br>
1.0.12 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
