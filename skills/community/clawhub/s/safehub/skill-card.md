## Description:

Scan OpenClaw skills for malware and security issues before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumeetghimire](https://clawhub.ai/user/sumeetghimire)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use SafeHub to scan OpenClaw skills by name, local path, or GitHub URL before installation. It reports static analysis findings, optional sandbox behavior, a trust score, and an install recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning untrusted GitHub URLs could run attacker-controlled commands.

Mitigation: Prefer vetted local paths and avoid untrusted GitHub URL scans until command construction is fixed.

Risk: Sandbox results may be incomplete and could give a misleading sense of safety.

Mitigation: Treat sandbox output as one signal, review static findings manually, and do not use a clean scan as proof that a skill is safe.

Risk: Rule updates can overwrite local scanner rules from the configured source.

Mitigation: Run updates only from trusted, pinned rule sources.

## Reference(s):

- [SafeHub ClawHub page](https://clawhub.ai/sumeetghimire/skills/safehub)
- [SafeHub homepage](https://github.com/sumeetghimire/safehub)
- [SafeHub support](https://github.com/sumeetghimire/safehub/issues)
- [Semgrep documentation](https://semgrep.dev)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal text and Markdown-style security reports with findings, scores, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be cached locally for later review.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, package.json, clawhub.json, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
