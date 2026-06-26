## Description: <br>
Full pipeline to turn a video podcast episode into Instagram content, including carousel posts, quote cards, and Reels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veezvg](https://clawhub.ai/user/veezvg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and agent operators use this skill to convert long-form podcast or video episodes into Instagram-ready transcripts, content plans, carousel slides, Reel clips, captions, previews, and posting drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Episode audio may be sent to OpenAI for transcription. <br>
Mitigation: Use only media you are allowed to process, avoid confidential episodes, and provide OPENAI_API_KEY through a shell, secret manager, or trusted runtime. <br>
Risk: The skill can operate an already logged-in Instagram browser session and may publish content if posting is allowed. <br>
Mitigation: Run preview or dry-run first, verify the target account, media, caption, and crop, and require explicit user approval before enabling any posting step. <br>
Risk: Preview screenshots and staged uploads may remain in temporary locations. <br>
Mitigation: Delete retained /tmp screenshots and staged upload files after the workflow completes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veezvg/veezvg-episode-to-instagram) <br>
- [Publisher profile](https://clawhub.ai/user/veezvg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, JSON content plans, shell commands, local media files, and browser automation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local working files such as transcripts, frame manifests, rendered carousel images, Reel clips, preview screenshots, and Instagram drafts that require explicit user approval before posting.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
