## Description:

Transcribes supported MP4 videos and turns their spoken content into summaries, rewrites, quote extracts, storyboards, or translations with custom prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, educators, and teams can turn a local MP4 or direct MP4 link into a cleaned transcript, then request a summary, rewrite, quote extraction, storyboard, or translation. A provider-issued GUAIKEI_API_TOKEN is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a token issued by a third-party service.

Mitigation: Review the provider's terms and use only a token you are comfortable supplying to that provider; keep it in GUAIKEI_API_TOKEN and out of prompts or shared logs.

Risk: A resumed download that fails or is stopped may cause loss of an existing file.

Mitigation: Use an isolated temporary download directory and keep a separate copy of any file that must be preserved.

Risk: The security scan was partial: only 7 of 18 components were fully inspected.

Mitigation: Review the remaining components and monitor behavior before relying on the skill with sensitive material.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/quicksub)
- [速转字幕官网](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or Markdown prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript or prompt-directed text such as summaries, rewrites, extracted quotes, storyboards, and translations.]

## Skill Version(s):

1.0.1 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
