## Description:

Helps agents collect and analyze public Truth Social profiles, posts, and account timelines through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to inspect public Truth Social accounts and posts, collect account timelines, and report findings with cost and coverage information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SocQ receives the API key and submitted public research queries.

Mitigation: Trust the provider before use; keep SOCQ_API_KEY in the environment and out of prompts, URLs, and saved commands.

Risk: Unpinned npx execution can fetch a newer CLI package at runtime.

Mitigation: Use an installed or pinned @socq/cli version for better supply-chain control.

Risk: Large or repeated collections can consume paid credits.

Mitigation: Estimate cost, set credit limits, and confirm larger paid runs before submitting.

Risk: Partial timelines or current engagement counters may misrepresent historical or platform-wide activity.

Mitigation: Report collection dates, pagination limits, and coverage gaps; avoid inferring platform trends or historical engagement from current counts.

## Reference(s):

- [SocQ Truth Social API documentation](https://docs.socq.ai/api-manual/truth-social)
- [SocQ MCP and CLI integration documentation](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools homepage](https://github.com/SocQAPI/socq-devtools)
- [Truth Social endpoint reference](artifact/references/platform.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSONL exports]

**Output Format:** [Markdown research summary with optional raw JSONL export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, query scope, task status, credit usage, result count, and coverage gaps when available.]

## Skill Version(s):

1.0.3 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
