## Description: <br>
Edit videos with AI background removal, color grading, upscaling, stabilization, and enhancement tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and editors use this skill to choose AI-assisted video editing workflows for background removal, color grading, upscaling, stabilization, audio cleanup, effects, and export preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud and API workflows can upload source footage to third-party services. <br>
Mitigation: Confirm the footage is allowed to leave the user's environment, review provider terms, and prefer local tools for confidential or regulated media. <br>
Risk: API examples may encourage exposing credentials in chats, source files, or shared project folders. <br>
Mitigation: Keep API keys out of prompts and files, use environment variables or a secrets manager, and rotate any credential that may have been exposed. <br>
Risk: Face-swap workflows can enable impersonation, harassment, or non-consensual synthetic media. <br>
Mitigation: Use face-swap features only with clear consent and reject requests involving impersonation, harassment, or non-consensual synthetic media. <br>
Risk: AI video enhancement can introduce visual artifacts, flicker, or misleading edits. <br>
Mitigation: Work on copies, preserve originals, test short segments first, and review key frames before publishing or delivering output. <br>


## Reference(s): <br>
- [Video Audio Enhancement](artifact/audio.md) <br>
- [Video Background Removal](artifact/background-removal.md) <br>
- [Video Color Grading](artifact/color-grading.md) <br>
- [Video Effects](artifact/effects.md) <br>
- [Video Stabilization](artifact/stabilization.md) <br>
- [Video Editing Tools](artifact/tools.md) <br>
- [Video Upscaling](artifact/upscaling.md) <br>
- [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve) <br>
- [Adobe Podcast Enhance](https://podcast.adobe.com/enhance) <br>
- [Unscreen](https://www.unscreen.com/) <br>
- [GyroFlow](https://gyroflow.xyz/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with workflow steps, tables, shell commands, and API code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local desktop tools and third-party cloud or API services depending on the selected editing workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
