## Description:

Profound LLM citation tracker (extension). Time-series brand citation rates across ChatGPT, Perplexity, and other LLMs. Pairs with seo-seranking for triangulated AI visibility coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

SEO and content teams use this skill to track brand citation rates across LLM search surfaces, inspect prompts that surface or omit a brand, compare cited competitors, and monitor spike or drop alerts over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking the full Claude settings file before every tool call can expose unrelated credentials or private configuration.

Mitigation: Check only whether PROFOUND_API_KEY exists in the current environment immediately before Profound API use, and do not read or display the full settings file.

Risk: The skill references installer scripts that are not included in the submitted artifact evidence.

Mitigation: Inspect and trust those installer scripts separately before running them, or configure PROFOUND_API_KEY manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-profound)
- [Publisher profile](https://clawhub.ai/user/asale-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with command-oriented guidance and metric summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PROFOUND_API_KEY; Profound metrics should be cited with live confidence when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
