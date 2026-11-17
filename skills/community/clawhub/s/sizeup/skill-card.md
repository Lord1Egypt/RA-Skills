## Description:

Disk usage analyzer with tree view, large file finder, and extension breakdown. Like `du` but actually readable. Pure Python, zero dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and system operators use this skill to inspect local disk usage, find large files, review file extension breakdowns, and generate JSON output for scripting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool reads directory names, file sizes, and extensions under paths the user asks it to scan.

Mitigation: Run it only on directories whose local metadata may be inspected, and avoid scanning sensitive paths unless that disclosure is acceptable.

Risk: Crafted filenames in untrusted directories may affect terminal display.

Mitigation: Review output cautiously for untrusted paths and prefer JSON output when the result will be processed by another tool.

Risk: Depth limiting is not a hard privacy or performance boundary.

Mitigation: Use explicit target paths and minimum-size filters, and do not rely on --depth alone to prevent broader local filesystem reads.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying tool can emit terminal tree views, largest-file lists, extension summaries, or JSON depending on CLI flags.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
