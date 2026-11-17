## Description:

Word Converter helps agents convert .docx and .doc files to Markdown, HTML, LaTeX, DOCX, or JSON using the mineru-open-api CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and document pipeline maintainers use this skill to choose and run MinerU CLI commands for Word-to-Markdown or multi-format Word conversion, including batch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global third-party npm CLI.

Mitigation: Prefer a pinned local package version, avoid elevated privileges, and review the package before installation.

Risk: Word document contents may be handled by MinerU-related tooling.

Mitigation: Do not use the skill on sensitive documents unless MinerU privacy and data-handling terms have been verified.

## Reference(s):

- [ClawHub Word Converter Skill Page](https://clawhub.ai/veeicwgy/skills/word-converter)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create converted document files in a user-specified or generated output directory when commands are executed.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
