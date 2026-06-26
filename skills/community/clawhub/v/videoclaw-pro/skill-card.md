## Description: <br>
VideoClaw Pro generates structured video-editing suggestion scripts from Feishu prompt-library and source-material documents, with support for Feishu docx and wiki links plus permission guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiangxueweb](https://clawhub.ai/user/xiangxueweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Video editors and content-production teams use this skill to turn Feishu-hosted editing rules and live-session transcripts into a structured editing plan with timeline suggestions, scene-change points, highlights, subtitles, and a generated Feishu document link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the Feishu workflow embeds reusable app credentials. <br>
Mitigation: Install only if the publisher is trusted and the Feishu app credentials have been rotated or intentionally scoped for this exact workflow. <br>
Risk: The skill reads user-provided Feishu documents and can create persistent remote Feishu documents. <br>
Mitigation: Review the Feishu app permissions, confirm which documents are shared with the bot, and check where generated documents will be written before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiangxueweb/videoclaw-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown video-editing script with Feishu document link and permission guidance when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided Feishu docx/wiki links and can create a persistent Feishu document through the local Python CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
