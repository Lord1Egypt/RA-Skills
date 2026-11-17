## Description:

Generates Architecture Decision Records from decisions made during the current session by gathering repository context, extracting decisions, confirming user selections, writing ADR files, reporting results, and verifying output quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after architecture discussions to turn confirmed decisions into MADR-style ADR documentation. It is intended for repository workflows where ADRs should be created, numbered, reviewed, and verified before commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ADRs may misrepresent architectural decisions or omit important context.

Mitigation: The workflow requires presenting extracted decisions for user confirmation before files are written and recommends reviewing generated ADRs before committing them.

Risk: ADR numbering or file creation can fail if the expected repo-local numbering script or related ADR skills are unavailable.

Mitigation: Verify the required ADR helper skills and numbering script exist in the target repository before relying on the generated files.

Risk: Generated ADR files may not meet the expected frontmatter, alternatives, or consequences requirements.

Mitigation: Use the skill's verification step to check YAML frontmatter, status, date, documented alternatives, and Good/Bad consequences for every created ADR.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/write-adr)
- [Publisher profile](https://clawhub.ai/user/anderskev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown ADR files, confirmation prompts, JSON decision extraction payloads, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or adjusts Markdown files under docs/adrs/ after user confirmation and reports verification status.]

## Skill Version(s):

1.1.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
