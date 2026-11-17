## Description: <br>
视频翻译-免费版 helps agents submit single-video Chinese-English translation and dubbing tasks to the LuoJi online translation service, poll job status, and return a translated video preview link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, learners, and content operators use this skill to localize individual short videos between Chinese and English with translated subtitles or dubbing. Agents use it to guide API-key setup, submit a video file or URL, poll the translation job, and return the preview result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected video files or video URLs to the LuoJi online translation service. <br>
Mitigation: Use it only for videos that may be shared with that service, and review organizational data-handling requirements before submitting sensitive content. <br>
Risk: The skill uses a LuoJi API key in request headers for translation jobs. <br>
Mitigation: Store the API key in a secret or environment variable and avoid pasting it into shared prompts, logs, or files. <br>
Risk: The free edition is limited to Chinese-English video translation and single-video workflows. <br>
Mitigation: Route multilingual, batch, real-time, certified, legal, or medical translation needs to a more appropriate reviewed tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/video-translator-tool-free) <br>
- [LuoJi service homepage](https://luoji.cn) <br>
- [LuoJi global video translation API](https://audiox-api-global.luoji.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task status, execution logs, and preview URLs when the external translation service completes successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
