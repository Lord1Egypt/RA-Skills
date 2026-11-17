## Description:

Generates and rewrites short-video marketing copy for Douyin and TikTok, with optional translation and text-to-speech support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web-seeker](https://clawhub.ai/user/web-seeker)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and content operators use this skill to draft, rewrite, translate, title, tag, and voice short-video promotional copy for Douyin, TikTok Japan, and TikTok US.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated copy, product details, and submitted text may be sent to third-party translation and text-to-speech services even though some documentation says data stays local.

Mitigation: Install only if those service calls are acceptable, avoid secrets, personal data, and proprietary drafts, and prefer running the static HTML locally or through a local static server.

Risk: Security evidence marks the release suspicious and says the advertised CSP, XSS, and privacy claims may be overstated.

Mitigation: Review and scan the static web app before deployment, and validate the privacy and browser security behavior against organizational requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/web-seeker/skills/viral-copy-generator)
- [Edge TTS service endpoint](https://tts.wangwangit.com/v1/audio/speech)
- [MyMemory Translate API endpoint](https://api.mymemory.translated.net/get)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text copy with optional launch commands and service configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated text can be translated through MyMemory and converted to audio through the configured TTS service; saved records are limited to browser localStorage.]

## Skill Version(s):

1.1.0 (source: server release metadata, skill.json, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
