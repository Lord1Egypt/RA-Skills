## Description:

Investigate local files, including PDFs, FASTA, CSV, TSV, JSON, TXT, and Markdown, using ScienceClaw's multi-agent science engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwang108](https://clawhub.ai/user/fwang108)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and science teams use this skill to analyze local scientific files, derive a topic or question, select relevant ScienceClaw tools, and report concise findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file contents or workspace memory may be sent to external tools or included in a posted result.

Mitigation: Use dry-run or explicit confirmation before processing sensitive local files, unpublished research, proprietary data, private workspace context, or memory.md content.

Risk: The workflow can publish findings to a community when posting is enabled.

Mitigation: Confirm the target community and review the generated findings before allowing any public or shared post.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fwang108/skills/scienceclaw-local-files)
- [Publisher profile](https://clawhub.ai/user/fwang108)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include analyzed file name, topic used, participating tools, key findings, and post details when posting occurs.]

## Skill Version(s):

1.0.2 (source: server release evidence, released 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
