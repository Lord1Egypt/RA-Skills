## Description: <br>
Automates TikTok search, commenting, likes, favorites, and video publishing on a 720x1280 Android device through ADB, with optional AI-generated comments from screen screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[molin-g](https://clawhub.ai/user/molin-g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and automation operators use this skill to configure and run Android ADB workflows for TikTok engagement, including topic search, commenting, likes, favorites, and publishing. Operators can choose static comments or AI-generated comments that analyze TikTok screen screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post comments, likes, favorites, and videos publicly through a logged-in TikTok app. <br>
Mitigation: Use a dedicated test phone and account, review every mode before execution, and add explicit confirmations before enabling publish mode. <br>
Risk: AI comment mode can send TikTok screen screenshots to Anthropic, OpenAI, or OpenRouter. <br>
Mitigation: Enable AI mode only when screen contents are acceptable to share with the configured provider, and keep provider API keys scoped and protected. <br>
Risk: Publish mode can delete videos from the phone camera folder and accept video URLs for upload. <br>
Mitigation: Avoid publish mode unless the camera folder contains no personal videos, patch the media deletion behavior, and do not pass untrusted video URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/molin-g/tiktok-android-720p) <br>
- [Publisher profile](https://clawhub.ai/user/molin-g) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python CLI usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run ADB commands against a connected Android device and may send screenshots to configured AI providers when AI comment mode is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
