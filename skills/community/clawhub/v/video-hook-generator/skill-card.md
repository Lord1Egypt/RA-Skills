## Description:

Generates short-video opening hooks from a topic or script, producing multiple high-click hook styles such as conflict, numeric, suspense, emotional, and reveal hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nh5gntnf78-oss](https://clawhub.ai/user/nh5gntnf78-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate Chinese short-video hooks and optional first-three-second script suggestions for platforms such as Douyin, Xiaohongshu, and Bilibili.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional save feature can write outside the chosen output folder when the topic contains path characters.

Mitigation: Use trusted plain-text topics only and avoid path-like topic strings with --output until filename handling is fixed.

Risk: The skill uses broad activation phrases and operates primarily in Chinese, which can make unintended invocation or mismatched language expectations more likely.

Mitigation: Review the invocation context before use and confirm that Chinese short-video hook generation is the intended task.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line text output, with optional JSON files when saving generated hooks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3.8+ and no required API access; edge-tts is optional for voice testing.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
