## Description:

The rstack skill suite helps resolved.sh operators audit and improve page quality, A2A agent cards, data products, paid service endpoints, monetized content, and external distribution listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hichana](https://clawhub.ai/user/hichana)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and resolved.sh operators use this skill suite to assess and improve agent-native businesses by generating scorecards, page and agent-card content, marketplace/service/content commands, and registry listing artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shell commands may change live resolved.sh account resources.

Mitigation: Review each generated curl command before execution and use a least-privilege resolved.sh API key.

Risk: Untrusted user values may be inserted into shell snippets or JSON payloads.

Mitigation: Serialize values safely as JSON and quote shell variables before running generated commands.

Risk: API keys and webhook secrets may be exposed through shared temp files, terminal output, or logs.

Mitigation: Keep secrets out of shared logs, redact outputs before sharing, and avoid storing webhook secrets in shared temporary paths.

Risk: Global auto-confirmed installation can obscure the exact code being installed.

Mitigation: Install only after reviewing the exact source version, preferably pinned to an immutable commit or trusted release artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hichana/skills/resolved-sh-rstack)
- [resolved.sh](https://resolved.sh)
- [rstack documentation](https://github.com/resolved-sh/rstack)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ready-to-run curl commands, generated configuration payloads, webhook verification snippets, and distribution submission text.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
