## Description:

Generates a word-cloud PNG image from supplied text, Markdown files, or Markdown files in a directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijiahao885](https://clawhub.ai/user/lijiahao885)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to turn supplied text or Markdown content into a saved word-cloud PNG for quick visual analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency-install instructions include names that are built into Python or may not map to the intended package.

Mitigation: Install reviewed third-party dependencies manually in a virtual environment, such as jieba, numpy, wordcloud, and Pillow; do not blindly install os, argparse, datetime, or PIL from a package registry.

Risk: Broad file or directory inputs can cause the skill to read more local Markdown content than intended, and the output path controls where the PNG is written.

Mitigation: Use narrow target_file or target_dir paths and choose the output directory intentionally before running the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijiahao885/skills/wordcloud-skill)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; generated artifact is a PNG image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a text source and max_words; optional width, height, mask, font path, stop words, and output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
