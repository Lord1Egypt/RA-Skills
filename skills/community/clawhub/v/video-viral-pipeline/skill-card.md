## Description: <br>
Automates turning a foreign-language long video into Chinese or bilingual captioned output, viral-style vertical clips with covers, and optional publishing to WeChat Channels, Douyin, Xiaohongshu, and WeChat Official Account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators and automation-focused operators use this skill to transform long-form foreign-language videos into captioned short-form clips, cover assets, publishing configurations, and guided posting workflows across Chinese social platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged-in social-platform sessions can publish multiple posts immediately without a dry-run or final confirmation safeguard. <br>
Mitigation: Review publish.json before use, run only one item with --idx first, use draft mode where available, and stop if platform errors or rate-limit signals appear. <br>
Risk: AI cover generation sends cover prompts to Ofox and requires API credentials. <br>
Mitigation: Use only non-sensitive prompt content, provide API keys through environment variables, and install only if this external API use is acceptable. <br>
Risk: Untrusted configuration files can cause unintended media processing or posting behavior. <br>
Mitigation: Review clips, covers, and publish JSON files before execution, keep backups of generated media, and avoid running configs from untrusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dizhu/video-viral-pipeline) <br>
- [social-auto-upload dependency](https://github.com/dreammis/social-auto-upload.git) <br>
- [Ofox image generation API endpoint](https://api.ofox.ai/v1/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create video, image, subtitle, and publishing configuration files when run with user-provided media and credentials.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
