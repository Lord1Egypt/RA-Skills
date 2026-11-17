## Description:

Core browser operations skill for SurfAgent and similar browser agents, covering tab discipline, perception-first execution, human-like driving, proof rules, and token-efficient fallback patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surfagentapp](https://clawhub.ai/user/surfagentapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and browser-agent operators use this skill to guide real-browser sessions with tab hygiene, perception-first action loops, visible verification, fallback handling, and concise progress reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may operate inside already logged-in browser sessions, including email, social posting, settings, or account identity surfaces.

Mitigation: Review sensitive actions before allowing them and require visible account, page, and post-action state verification before completion.

Risk: State-map notes or progress reports could capture sensitive session details.

Mitigation: Keep notes short and avoid storing credentials, private messages, account identifiers, or other sensitive browser-session data.

Risk: Browser actions may be reported as successful before the UI confirms completion.

Mitigation: Require visible post-action evidence such as confirmation states, rendered messages or posts, persisted settings, or refreshed UI state before claiming success.

## Reference(s):

- [SurfAgent homepage](https://surfagent.app)
- [ClawHub skill page](https://clawhub.ai/surfagentapp/skills/surfagent-browser-operations)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown guidance and concise evidence-based status language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code; directs browser hygiene, verification, fallback behavior, and progress reporting.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
