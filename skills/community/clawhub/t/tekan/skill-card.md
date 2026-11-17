## Description:

特看视频 lets an agent create and edit AI-generated videos, images, digital avatar videos, speech audio, voice clones, product model images, and background-removed assets from natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxjhhhh](https://clawhub.ai/user/wxjhhhh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to ask an agent for AI media creation workflows such as text-to-video, image-to-video, AI image generation and editing, digital presenter videos, text-to-speech, voice cloning, background removal, product model images, and board-based result management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses a Tekan account, saves credentials locally, and uses paid media-generation credits.

Mitigation: Require explicit user confirmation before login or paid generation, check account credit status where appropriate, and use logout to remove ~/.tekan/credentials.json when access is no longer needed.

Risk: Media prompts, images, audio, and identity material may be uploaded to Tekan or TopView services for generation and cloning workflows.

Mitigation: Confirm user intent before uploading personal, sensitive, or third-party media, especially for avatar and voice-cloning tasks.

Risk: Voice cloning, saved avatars, board deletion, and custom voice deletion can affect user identity assets or stored work.

Mitigation: Ask for explicit confirmation before voice cloning, saved-avatar actions, board deletion, or custom voice deletion.

Risk: The security review notes broad auto-activation and branded login-message behavior that may surprise users.

Mitigation: Keep activation tied to clear user requests for Tekan media workflows and present login steps only when account authorization is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wxjhhhh/skills/tekan)
- [Publisher Profile](https://clawhub.ai/user/wxjhhhh)
- [特看视频](https://video.tekan.cn)
- [Agent Skills Specification](https://agentskills.io/specification)
- [README](artifact/README.md)
- [Authentication Reference](artifact/references/auth.md)
- [Video Generation Reference](artifact/references/video_gen.md)
- [AI Image Reference](artifact/references/ai_image.md)
- [Avatar Reference](artifact/references/avatar4.md)
- [Voice Reference](artifact/references/voice.md)
- [Board Reference](artifact/references/board.md)
- [Error Handling Reference](artifact/references/error_handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python command examples, generated media links, local files, and JSON responses when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media and board links depend on an authenticated Tekan account, available credits, uploaded user media, selected models, and remote service task completion.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
