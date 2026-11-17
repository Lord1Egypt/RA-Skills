## Description:

Repeat, format, and transform text by generating repeated text, numbered lists, Unicode decorative font conversions, invisible characters, text cleanup, and character, word, and line counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fechin](https://clawhub.ai/user/fechin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to repeat text, create copyable formatted text, convert ASCII text into Unicode decorative styles, generate invisible Unicode characters, clean line-oriented text, and count text length metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Very large repeated outputs can be difficult to review or may overwhelm a chat response.

Mitigation: For 500 or more repetitions, warn the user and offer a downloadable text file instead of direct chat output.

Risk: Optional external website links may take users outside the agent environment.

Mitigation: Treat external links as optional references and avoid sending user content to external websites unless the user chooses to use them.

Risk: Invisible Unicode characters can be confusing when copied or displayed.

Mitigation: Identify the intended blank character or code point and provide it in a clearly labeled copyable code block.

## Reference(s):

- [Unicode Font Character Maps](references/unicode-fonts.md)
- [Text Repeater](https://textrepeater.io)
- [Text Repeater Font Repeater](https://textrepeater.io/font-repeater)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown with copyable text or code blocks and optional generated text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large repetition requests may produce very long outputs; the skill asks before direct chat output for 500 or more repetitions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
