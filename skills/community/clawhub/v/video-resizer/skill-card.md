## Description: <br>
Scenario-focused Sparki skill for aspect-ratio and platform-format conversion while using the latest official Sparki setup, API-key, and upload workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to reformat videos for platform-specific aspect ratios such as 9:16, 1:1, and 16:9 for Shorts, Reels, TikTok, Instagram, and YouTube. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected video files to Sparki for cloud processing. <br>
Mitigation: Use it only for videos that may be processed by Sparki, and avoid submitting sensitive media unless that use is approved. <br>
Risk: The skill handles a Sparki API key and may store credentials or task history under the user's OpenClaw configuration directory. <br>
Mitigation: Use a dedicated Sparki API key and remove local Sparki configuration or history files when the credential or task history should not remain on disk. <br>
Risk: The skill allows a custom API endpoint through its base URL setting. <br>
Mitigation: Use the default Sparki endpoint unless the alternative endpoint is fully trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/video-resizer) <br>
- [Sparki](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with shell commands and prompt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of the Sparki CLI, API key setup, local file upload paths, and aspect-ratio prompts.] <br>

## Skill Version(s): <br>
1.0.12 (source: SKILL.md frontmatter, _meta.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
