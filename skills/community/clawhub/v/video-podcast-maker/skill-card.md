## Description:

Use when the user gives a topic and wants an automated topic-driven narrated explainer, podcast, or knowledge-summary video, or asks to learn visual design patterns from a reference video or image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, developers, and agent users use this skill to turn a topic into a narrated knowledge video with research, script drafting, TTS audio, Remotion composition, thumbnails, background music, and publish-ready outputs. It is aimed at Bilibili, YouTube, Xiaohongshu, Douyin, and WeChat Channels style explainer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a shell-driven media pipeline that writes project files and calls external TTS and media tools.

Mitigation: Run it in a controlled workspace, review generated commands before execution, and use pinned dependencies or a locked environment for optional npx-based flows.

Risk: Security evidence reports helper scripts that can write or recursively delete outside intended project folders when crafted IDs are supplied.

Mitigation: Avoid untrusted asset IDs and design reference IDs, preview paths before destructive design operations, and do not use delete confirmation flags unless the target is clearly inside the intended reference folder.

Risk: Generated videos may depend on external assets, voices, or music with licensing and attribution requirements.

Mitigation: Use license-vetted assets, keep manifest license and credit records, and resolve asset-license warnings before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agents365-ai/skills/video-podcast-maker)
- [Project homepage](https://github.com/Agents365-ai/video-podcast-maker)
- [Design guide](references/design-guide.md)
- [Workflow: script](references/workflow-script.md)
- [Workflow: assets](references/workflow-assets.md)
- [Workflow: production](references/workflow-production.md)
- [Workflow: publish](references/workflow-publish.md)
- [Troubleshooting](references/troubleshooting.md)
- [Natural narration](references/natural-narration.md)
- [Azure TTS pitfalls](references/azure-tts-pitfalls.md)
- [Design learning](references/design-learning.md)
- [Hyperframes overlays](references/hyperframes-overlays.md)
- [Chinese polyphones](references/zh-polyphones.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance, generated project files, Remotion/TypeScript code, shell commands, media manifests, and rendered video artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces topic notes, narration scripts, TTS timing files, thumbnails, MP4 video outputs, background-music mixes, subtitles, and optional shorts when the required local tools and TTS backend are available.]

## Skill Version(s):

3.0.2 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
