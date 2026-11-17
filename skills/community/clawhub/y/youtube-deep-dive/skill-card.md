## Description:

Analyzes a YouTube video and produces a timestamped transcript of speech and key-frame visuals alongside a structured, in-depth summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

People who want to study or review YouTube videos use the skill to get timestamped speech and visual notes, then a structured summary with key points and cited resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance asks users to paste their full Cue API key into chat, creating a risk of credential exposure.

Mitigation: Configure the key locally in a restricted file or environment variable; rotate any key already shared in conversation.

Risk: Selected video links are sent to Cue for processing, consume service credits, and server retention and automatic cleanup are unverified.

Mitigation: Submit only links you are comfortable sharing; avoid confidential material and check the service's retention terms.

Risk: Speech transcription and key-frame descriptions may be inaccurate, especially with unclear or noisy audio; transcripts may also be subject to copyright restrictions.

Mitigation: Mark unclear passages rather than guessing, treat visual notes as model interpretations, and obtain authorization before publishing transcripts.

## Reference(s):

- [YouTube 视频深度解析 on ClawHub](https://clawhub.ai/panting09266-ai/skills/youtube-deep-dive)
- [Cue Omni Reader online experience](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown with timestamped transcript, key-frame notes, and a structured summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamps and speaker labels; visual notes are model interpretations, and transcription quality can vary with audio conditions.]

## Skill Version(s):

1.0.2 (source: server-resolved release; artifact frontmatter reports 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
