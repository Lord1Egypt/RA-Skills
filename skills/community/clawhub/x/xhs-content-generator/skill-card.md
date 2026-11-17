## Description:

Generates Chinese-language Xiaohongshu content prompts with headline options, content frameworks, hashtags, and engagement copy from a selected topic and hot keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesiyoq965-sudo](https://clawhub.ai/user/mesiyoq965-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing teams use this skill to draft Xiaohongshu post ideas around topics such as AI side hustles, AI tools, and earning methods. It produces a reusable prompt for a downstream AI assistant rather than final validated marketing copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can create local text files, including at a user-supplied output path.

Mitigation: Run it in an intended workspace and review the output path before execution.

Risk: Final content depends on a downstream AI assistant and may contain inaccurate or overstated marketing claims if used without review.

Mitigation: Review generated content for accuracy, platform policy, and the prompt's restrictions against exaggerated earnings claims, prohibited content, and copying others.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mesiyoq965-sudo/skills/xhs-content-generator)
- [Publisher profile](https://clawhub.ai/user/mesiyoq965-sudo)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Chinese Markdown-style prompt text, printed to stdout or written as a .txt file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a topic, hot keyword, and optional output path; otherwise writes a timestamped local text file.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
