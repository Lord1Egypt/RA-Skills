## Description:

Helps developers and skill authors remediate snyk-agent-scan alerts for agent skill files by restructuring content for W001, W011, and W012 patterns without suppressing useful information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill authors use this skill to triage and fix snyk-agent-scan findings in SKILL.md, references, assets, and related Markdown during authoring, local scans, CI failures, and PR review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or runs an external scanner that may be unpinned.

Mitigation: Review before installing, prefer a pinned and audited snyk-agent-scan version, and run it only on intended skill directories.

Risk: The scanner workflow requires a Snyk token.

Mitigation: Use a minimally scoped Snyk token and store it as a secret in CI environments.

Risk: Moving install commands into metadata can reduce scanner visibility without controlling supply-chain risk.

Mitigation: Do not treat metadata relocation alone as a security fix; require pinned versions or hashes where executable dependencies are introduced.

## Reference(s):

- [W001 prompt-injection pattern catalog](references/w001-patterns.md)
- [W011 third-party content exposure pattern catalog](references/w011-patterns.md)
- [W012 external URL and supply-chain pattern catalog](references/w012-patterns.md)
- [ClawHub skill page](https://clawhub.ai/samber/skills/snyk-agent-scan-compliance)
- [ClawHub metadata homepage](https://github.com/samber/cc-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose skill-file restructuring and scanner remediation steps; does not address dependency vulnerabilities, code security findings, or infrastructure misconfigurations.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
