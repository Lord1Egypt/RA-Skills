## Description:

Evaluates agent skills through static analysis, assigns a 100-point quality score, and provides review reports and improvement recommendations using type-aware policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to assess agent skill quality and robustness, receive a scored review with prioritized improvements, and validate suggested fixes when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled script can run an unrestricted executable through an option passed to it.

Mitigation: Review the script execution option and its behavior before running it; only use a trusted, intended executable.

Risk: The delegated CI rerun workflow and unpinned npx references may invoke tools or actions whose behavior is not fixed.

Mitigation: Inspect the rerun workflow, verify the package source, and pin tool versions before relying on those actions.

Risk: The security scan could not resolve some local references, so its verdict does not establish that the skill is safe.

Mitigation: Review unresolved local references and inspect the skill and its scripts before installation.

## Reference(s):

- [Project homepage](https://github.com/z-Zihan/awesome-skills)
- [ClawHub skill release](https://clawhub.ai/z-zihan/skills/skill-review-pro)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report with scores, findings, and prioritized improvement recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are based on the supplied skill and its selected review policies; fixes are applied only when requested.]

## Skill Version(s):

2.3.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
