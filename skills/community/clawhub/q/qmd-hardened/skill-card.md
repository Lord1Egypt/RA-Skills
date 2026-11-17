## Description:

Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to index local files and run qmd search, vector search, hybrid query, document retrieval, status, update, collection, and MCP-mode commands while preserving local data boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The qmd installer pulls from a mutable GitHub source.

Mitigation: Review the dependency source before installation and prefer a pinned or audited qmd version where release controls require reproducibility.

Risk: qmd indexes local files, so search results may expose sensitive local content.

Mitigation: Avoid indexing sensitive paths unless necessary and review or redact results before displaying or sharing them.

Risk: Using a non-localhost OLLAMA_URL can transmit indexed content to an endpoint outside the local machine.

Mitigation: Keep OLLAMA_URL on localhost unless the endpoint is deliberately trusted, and confirm before persisting endpoint changes to shell configuration.

Risk: Deleting, clearing, or rebuilding the qmd index destroys search state.

Mitigation: Require explicit confirmation before destructive index operations and explain what state will be lost.

Risk: Piping qmd output to network commands can exfiltrate indexed content.

Mitigation: Do not pipe or redirect qmd output to network-transmitting commands; inspect results locally and share only reviewed content.

## Reference(s):

- [qmd package source](https://github.com/tobi/qmd)
- [qmd homepage](https://tobi.lutke.com)
- [Qmd Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/skills/qmd-hardened)
- [Faberlens qmd safety evaluation](https://faberlens.ai/explore/qmd)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and retrieval outputs may include local indexed content and should be reviewed for secrets before display or sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
