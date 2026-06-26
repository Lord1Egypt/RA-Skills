## Description: <br>
Translate and dub existing videos into multiple languages using HeyGen, including lip-sync, audio-only translation, and multi-language video variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelwang11394](https://clawhub.ai/user/michaelwang11394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to create translated or dubbed versions of existing videos through HeyGen, starting from either a video URL or a HeyGen video ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted video content, video URLs, or HeyGen video IDs are processed by HeyGen for cloud translation. <br>
Mitigation: Avoid confidential, regulated, or third-party media unless you have permission and have reviewed your organization's and HeyGen's data-handling requirements. <br>
Risk: HeyGen API access depends on HEYGEN_API_KEY, which could expose account access if hard-coded or shared. <br>
Mitigation: Store the key in the environment, avoid placing it in prompts or source files, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/michaelwang11394/video-translate) <br>
- [HeyGen Video Translate API](https://api.heygen.com/v2/video_translate) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with curl, TypeScript, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HEYGEN_API_KEY for HeyGen API calls.] <br>

## Skill Version(s): <br>
2.23.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
