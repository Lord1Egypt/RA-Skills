## Description:

Use Siemens TIA Portal Openness API to diff two .zap18 projects and return structured code & hardware changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjmore66](https://clawhub.ai/user/cjmore66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to compare Siemens TIA Portal .zap18 projects and summarize code, data block, hardware, and network changes for CI/CD review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unbundled external TIA Openness diff script with unclear provenance and path control.

Mitigation: Use only a known, trusted script invoked by an explicit path, preferably with a pinned checksum or trusted code-signing check.

Risk: The skill reads and processes industrial project archives supplied by path.

Mitigation: Run the workflow in a dedicated working directory with access limited to the project files being compared.

## Reference(s):

- [TIA Openness Diff Scripts](artifact/Scripts/README.md)
- [ClawHub skill page](https://clawhub.ai/cjmore66/skills/tia-cicd-diff)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a structured diff summary and human-facing explanation after an external Siemens TIA Openness diff script processes the compared .zap18 files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
