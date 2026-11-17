## Description:

Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[164149043](https://clawhub.ai/user/164149043)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to invoke the summarize CLI for concise summaries of web URLs and local document or media files. It is useful when an agent needs command examples for selecting summary length, output format, or an output file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input files, URLs, or media may contain confidential or sensitive information processed by the external summarize CLI.

Mitigation: Use the skill only with content appropriate for the installed CLI and verify the CLI's data-handling behavior before summarizing sensitive material.

Risk: The --output option saves generated summaries to local disk.

Mitigation: Choose output paths deliberately and avoid writing summaries containing sensitive information to shared or persistent locations.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/164149043/skills/summarize-cli)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers summary length, text/markdown/json output formats, and optional file output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
