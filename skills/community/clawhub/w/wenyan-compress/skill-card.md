## Description:

Wenyan Compress helps an agent rewrite Chinese or English text into concise classical Chinese, with options for compression style, fidelity checks, and compression statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnskycn](https://clawhub.ai/user/cnskycn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compress long Chinese or English text, meeting notes, product requirements, quotes, and summaries into concise classical Chinese while choosing detailed, minimal, poetic, or high-fidelity modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compressed or translated text can drop or alter exact facts, numbers, names, dates, legal meaning, or domain terms.

Mitigation: Use high-fidelity mode for exact information and compare the compressed result against the source before using it in sensitive, legal, financial, or exact-data contexts.

Risk: The bundled Python helper appears incomplete and returns a prompt placeholder rather than performing compression, privacy reduction, fidelity checking, or token measurement itself.

Mitigation: Treat the release as an LLM prompt and instruction aid; verify generated text and statistics externally when accuracy matters.

## Reference(s):

- [Wenyan Compress ClawHub release](https://clawhub.ai/cnskycn/skills/wenyan-compress)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with compressed classical Chinese output, statistics, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fidelity notes, compression ratios, and warnings to verify sensitive or exact-data material.]

## Skill Version(s):

1.0.2 (source: artifact/SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
