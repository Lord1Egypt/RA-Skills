## Description:

Audit a named ClawHub skill or skill URL before installation by combining OpenClaw verification with bounded static analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanjing](https://clawhub.ai/user/jonathanjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review a ClawHub skill before installation, combining registry verification with bounded local checks and a concise risk report. It is intended to support install decisions, not to guarantee that another skill is safe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script installs Python packages in the active environment.

Mitigation: Run setup only inside a dedicated virtual environment and review the declared dependencies before first use.

Risk: The audit result is heuristic and a clean score is not proof that the target skill is safe.

Mitigation: Treat the report as a triage signal and manually inspect flagged, unusually large, omitted, or failed files for the exact release.

Risk: Optional LLM analysis may send excerpts from the audited skill to Anthropic.

Mitigation: Use --llm only when that data sharing is acceptable; otherwise run the static analysis mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonathanjing/skills/skill-trust-auditor)
- [ClawHub metadata homepage](https://clawhub.ai/jonathanjing/skill-trust-auditor)
- [ClawHavoc pattern reference](references/clawhavoc-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary and optional JSON report with risk findings, score, verdict, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run with --json-only for machine-readable output; optional --llm mode adds advisory analysis for ambiguous network findings.]

## Skill Version(s):

1.1.5 (source: frontmatter, changelog, skill.json, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
