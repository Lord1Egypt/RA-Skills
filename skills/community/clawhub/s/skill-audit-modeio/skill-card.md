## Description:

Runs a deterministic static safety audit for third-party AI skill or plugin repositories before install or execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modeioai](https://clawhub.ai/user/modeioai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to run static, evidence-backed pre-install audits of AI skill, plugin, or repository contents and produce findings for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted repositories may influence model-facing prompt output through scanned snippets.

Mitigation: Review generated prompts and treat model-assisted results as advisory input rather than a final safety gate.

Risk: Scanning repositories from broad or privileged directories may expose files through symlinked paths.

Mitigation: Run scans in a sandboxed or low-privilege workspace with only the target repository mounted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modeioai/skills/skill-audit-modeio)
- [Project Homepage](https://github.com/mode-io/mode-io-skills/tree/main/skill-audit)
- [Architecture](references/architecture.md)
- [Prompt Contract](references/prompt-contract.md)
- [Output Contract](references/output-contract.md)
- [Benchmarking](references/benchmarking.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON audit outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static scan reports include scoring, highlights, findings, validation results, and adjudication output when requested.]

## Skill Version(s):

0.1.0 (source: release, frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
