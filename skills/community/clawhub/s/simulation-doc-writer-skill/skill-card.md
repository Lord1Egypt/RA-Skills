## Description:

Writes, revises, and reviews Chinese documentation for communication simulation programs, including model descriptions, reproduction guides, MATLAB file/function inventories, and paper-to-code comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbisz](https://clawhub.ai/user/orbisz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and communication-system engineers use this skill to produce Chinese engineering documentation for wireless, optical, satellite, radar, modulation/coding, channel-modeling, link-level, system-level, MATLAB, Python, or C++ simulation code. It helps map papers to implementation files, document MATLAB scripts and functions, identify simulation-environment files, and produce reproducibility guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a self-evolution mechanism that can ask the agent to write diary files and propose edits to its own instructions.

Mitigation: Review or remove the self-evolution section before installation unless persistent self-review notes and proposed instruction changes are intended.

Risk: Artifact files disagree about whether the generated documentation should be plain text .txt or Markdown .md.

Mitigation: Clarify the expected output format before use; prefer the SKILL.md plain-text .txt requirement unless the user explicitly requests Markdown.

Risk: README installation examples mention npx-based installation without a pinned package or version.

Mitigation: Review and pin any npx-based installation workflow before using it in automated or managed environments.

## Reference(s):

- [Chinese communication simulation documentation template](references/communication-simulation-doc-template.md)
- [ClawHub skill page](https://clawhub.ai/orbisz/skills/simulation-doc-writer-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Chinese technical documentation with tables, runnable commands, verification steps, and reproduction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects generated program documentation to be saved as a plain-text .txt file unless the user explicitly requests another export.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
