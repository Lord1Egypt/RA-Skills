## Description:

AI-powered code analysis via LogicArt to find bugs, security issues, and logic flow visualizations during code review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to send selected code snippets or files to LogicArt for bug detection, security review, complexity assessment, suggestions, and logic-flow analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code sent to LogicArt or Validate Repo can expose proprietary logic, trade secrets, or embedded credentials.

Mitigation: Use the skill only for code approved for external analysis, manually check and redact secrets first, and confirm each transmission before sending.

Risk: The helper script can upload arbitrary code files without enforcing the consent and secret checks promised in the docs.

Mitigation: Avoid CI, cron, repository-wide, or unattended usage until per-file consent and secret scanning are enforced outside the agent instructions.

## Reference(s):

- [Quack Code Review Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/skills/quack-code-review-hardened)
- [Faberlens Publisher Profile](https://clawhub.ai/user/snazar-faberlens)
- [LogicArt](https://logic.art)
- [LogicArt Analyze API](https://logic.art/api/agent/analyze)
- [Validate Repo](https://validate-repo.replit.app)
- [SAFETY.md](SAFETY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with optional JSON returned by the LogicArt analysis helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized critical issues, complexity score, suggestions, and logic flow when provided by LogicArt.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
