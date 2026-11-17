## Description:

Security code linter that scans for vulnerabilities, leaked keys, and code smells.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lig-8max](https://clawhub.ai/user/lig-8max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code for common security issues and maintainability problems. It reports affected line numbers, risk levels, and remediation suggestions for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may consult external security references while reviewing code, which could expose private code, secrets, or proprietary details if snippets are sent outside the user's environment.

Mitigation: Avoid sending sensitive snippets, credentials, or proprietary details to external pages or searches; use approved internal references for confidential code.

Risk: The skill provides static review guidance and may miss issues in complex business logic.

Mitigation: Treat findings as advisory and require human security review before relying on the results for release decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lig-8max/skills/secure-linter)
- [Publisher profile](https://clawhub.ai/user/lig-8max)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown findings with line numbers, risk levels, and remediation suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static review only; does not execute code.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
