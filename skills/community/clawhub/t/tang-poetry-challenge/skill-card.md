## Description:

Tang Poetry Challenge is a Chinese-language Tang poetry quiz that prompts users with an upper line and asks them to provide the matching lower line, then reports scoring and missed-question analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rikhou](https://clawhub.ai/user/rikhou)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and Chinese-language users can use this skill to practice recalling lines from Tang poems through a timed quiz with answer checking, scoring, hints, and missed-question review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is Chinese-only and may not fit users who cannot read Chinese poetry prompts and feedback.

Mitigation: Use it for Chinese-language learning or poetry practice contexts, and provide translation or localization support when serving non-Chinese readers.

Risk: Quiz behavior depends on bundled poetry data and local Python scripts.

Mitigation: Review the bundled poem dataset and run the local scripts in the intended agent environment before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rikhou/skills/tang-poetry-challenge)
- [Publisher profile](https://clawhub.ai/user/rikhou)
- [Bundled Tang poetry data](artifact/references/tang_poetry.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language quiz prompts, answer feedback, scoring summaries, hints, and missed-question analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
