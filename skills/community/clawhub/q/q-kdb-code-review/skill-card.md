## Description:

AI-powered code review for Q/kdb+ that catches bugs in the most terse language in finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beee003](https://clawhub.ai/user/beee003)

### License/Terms of Use:


## Use Case:

Developers, quant engineers, kdb+ DBAs, and trading infrastructure teams use this skill to review Q/kdb+ code for correctness, performance, and security issues. It provides issue findings with severity, line context, and suggested Q code patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends reviewed source code to Astrai and potentially downstream AI providers.

Mitigation: Use it only with code that may be shared with those services, and apply organizational review before sending sensitive or regulated code.

Risk: Configured provider API keys can be forwarded to the router when BYOK provider keys are present.

Mitigation: Limit the runtime environment to the provider keys intentionally approved for routing, and avoid co-locating unrelated credentials.

Risk: Untrusted configuration of ASTRAI_BASE_URL could redirect review requests and credentials.

Mitigation: Keep ASTRAI_BASE_URL unset or pinned to the expected Astrai endpoint in trusted deployment configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beee003/skills/q-kdb-code-review)
- [Astrai service](https://as-trai.com)
- [Astrai chat completions endpoint](https://as-trai.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [JSON review results rendered as human-readable review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, file, line, message, suggestion, summary, selected model, and cost metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
