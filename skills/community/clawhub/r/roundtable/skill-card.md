## Description:

Roundtable runs a structured multi-agent debate council with Scholar, Engineer, and Muse roles, then synthesizes their findings into a final answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT

## Use Case:

Developers, teams, and external users can use Roundtable for complex questions that benefit from multiple perspectives, cross-examination, and a synthesized final recommendation. It is not intended for simple questions, quick lookups, or casual chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Council questions and intermediate responses may be saved to local session logs, including sensitive or proprietary content.

Mitigation: Use only after reviewing the logging behavior; ensure logs are written only when log_sessions is true and avoid persisting sensitive sessions without explicit per-run consent.

Risk: Multi-agent synthesis can incorporate incorrect, outdated, or contaminated claims from web research or intermediate agent findings.

Mitigation: Keep untrusted input wrappers and cross-verification steps in place, require source review for important claims, and use the second debate round for higher-impact decisions.

## Reference(s):

- [Roundtable ClawHub Skill Page](https://clawhub.ai/robbyczgw-cla/skills/roundtable)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured council sections and optional JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence, agreement, dissent, source summaries, cost estimates, and local session logs when logging is enabled.]

## Skill Version(s):

0.5.0 (source: frontmatter and changelog, released 2026-08-31; server release version 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
