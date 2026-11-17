## Description:

RealChinese is a local Chinese writing helper that scores AI-like writing patterns and rewrites text into styles for Chinese content platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebuddha5566](https://clawhub.ai/user/thebuddha5566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to run local Chinese text analysis and generate platform-specific rewrites for social and publishing workflows. It is suited for local drafting assistance where users review heuristic scores and edited text before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic AI-trace scoring may be inaccurate or overstate detection certainty.

Mitigation: Use scores as drafting signals only and have a human reviewer evaluate the source text and rewritten output.

Risk: The advertised 29-detection claim and pip-install claim are not fully supported by the security evidence.

Mitigation: Confirm packaging and detection coverage before relying on those claims in production workflows.

Risk: Style rewriting may introduce misleading phrasing, platform-inappropriate language, or changes in meaning.

Mitigation: Review rewritten content against the original intent and platform policy before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thebuddha5566/skills/realchinese)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local heuristic detection reports and rewritten Chinese text; output should be reviewed before external use.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
