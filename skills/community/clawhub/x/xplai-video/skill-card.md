## Description: <br>
Xplai Video generates explainer videos from text prompts, ideas, math problems, or optional image URLs using the Xplai service, with support for Chinese and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyxu](https://clawhub.ai/user/yuanyxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to create or explain content as a video, including tutorials, math explanations, news summaries, code explanations, and language-learning visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts and optional image URLs are sent to Xplai's external service for processing. <br>
Mitigation: Confirm before use and avoid secrets, confidential code, private documents, personal data, or signed/private media links. <br>
Risk: Generated videos may be inaccurate or unsuitable for the user's intended explanation. <br>
Mitigation: Review the returned video before relying on or sharing it, especially for math, news, code, or language-learning content. <br>


## Reference(s): <br>
- [Xplai official website](https://www.xplai.ai/) <br>
- [ClawHub skill listing](https://clawhub.ai/yuanyxu/xplai-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with shell commands, status values, video IDs, and video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May poll for up to 60 minutes; generated video media is hosted by Xplai and returned as a URL when successful.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
