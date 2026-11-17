## Description:

Signal-Search is a retrieval-quality skill that helps agents search, research, compare sources, fact-check claims, and return concise answers with source scoring, fact-level anchoring, adaptive depth, and token-budget controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabre232](https://clawhub.ai/user/sabre232)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Signal-Search as an embeddable retrieval primitive for web and document research, source comparison, fact checking, and evidence-grounded answer generation. It is intended to return findings, sources, scores, confidence, budget usage, and trace information rather than a raw link list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default retrieval path can fetch unvalidated URLs.

Mitigation: Review before installing in environments with internal network access, cloud metadata services, or sensitive private APIs; prefer outbound network restrictions and source allowlists.

Risk: Private-source token handling can expose credentials.

Mitigation: Do not put tokens in URL templates; keep credentials in environment variables or a dedicated secret manager and review custom source configuration before use.

Risk: A tool-capable LLM used as a conflict-check callback can be exposed to prompt injection through fetched content.

Mitigation: Do not pass a tool-capable LLM directly into the callback without prompt-injection defenses, tool restrictions, and review of retrieved content boundaries.

Risk: Fetched content may be cached.

Mitigation: Disable or scope caching for sensitive sources, and avoid using shared cache locations for private or regulated content.

## Reference(s):

- [Signal-Search README](README.md)
- [Anti-scraping and compliance guidance](references/anti-scraping.md)
- [Engine list and integration specification](references/engines.md)
- [Evaluation golden set](references/eval-golden-set.md)
- [Intent decomposition and routing](references/intent-decomposition.md)
- [Tier policy L0-L3](references/tier-policy.md)
- [Token optimization guidance](references/token-optimization.md)
- [Eastmoney connector notes](references/eastmoney-example.md)
- [ClawHub skill page](https://clawhub.ai/sabre232/skills/signal-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON-like retrieval results, Python snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include findings, sources, scores, confidence, token usage, exhausted status, tier selection, and trace metadata.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
