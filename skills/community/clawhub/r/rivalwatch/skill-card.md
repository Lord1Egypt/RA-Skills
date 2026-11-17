## Description:

Rivalwatch provides a local Bash CLI for recording, reviewing, searching, and exporting competitor-intelligence notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use Rivalwatch to keep local competitor-intelligence notes, review recent entries, search activity history, and export logged data for reports or stakeholder review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Competitor notes may include confidential strategy, pricing, customer, or market information stored locally under ~/.local/share/rivalwatch/ and exported to local files.

Mitigation: Use the skill only for information suitable for local storage, review entries before export, and avoid entering confidential data unless local retention and export are acceptable.

Risk: The skill's analysis and reporting language can imply more automated competitive analysis than the local logging script performs.

Mitigation: Treat output as logged notes and exported records, and have a human review any strategic interpretation before relying on it.

## Reference(s):

- [ClawHub Rivalwatch Skill Page](https://clawhub.ai/bytesagain3/skills/rivalwatch)
- [bytesagain3 Publisher Profile](https://clawhub.ai/user/bytesagain3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured terminal text with local JSON, CSV, or plain-text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores logs and generated exports under ~/.local/share/rivalwatch/.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
