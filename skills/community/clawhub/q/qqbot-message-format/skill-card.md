## Description:

Formats final QQ and QQBot replies into concise Chinese messages with conclusion-first structure, QQ-friendly headings, flat bullet lists, restrained emphasis, and functional emoji.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hlgate](https://clawhub.ai/user/hlgate)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to restyle final agent replies for QQ chat presentation, especially task updates, troubleshooting notes, status reports, debugging conclusions, and short answers that need clearer mobile or desktop readability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally restyles final answers for QQ chat presentation, which may be unsuitable when exact original formatting, multilingual output, or unstyled replies are required.

Mitigation: Use it only for final QQ or QQBot replies, and modify or disable it when the response must preserve original formatting or language.

Risk: QQ rendering may not reliably preserve deeply nested Markdown lists, making complex replies harder to scan.

Mitigation: Keep primary bullets flat and convert child details into visible indented guide lines, as described in the skill templates.

## Reference(s):

- [QQBot message examples](references/examples.md)
- [QQBot message templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Concise Chinese Markdown-style chat messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conclusion-first QQ/QQBot formatting with flat lists, two effective heading levels, restrained bold emphasis, and functional emoji.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
