## Description:

Research a specific group's needs from community discussions. Collect authorized sources, read complete conversations, distinguish wishes from behavior, and produce traceable findings, counterexamples, and product tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kunhai1994](https://clawhub.ai/user/kunhai1994)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-oriented agents use Voice2Need to plan and run bounded community research, then turn authorized discussion records into traceable need findings and next product tests. It is intended for decision support from observed conversations, not for estimating market prevalence from samples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Discord export gives a sensitive token and the full environment to a configurable external program.

Mitigation: Prefer the offline demo or existing Discord exports; for live Discord runs, verify the exporter path yourself, confirm the intended account and specific channel access, and run with a minimal environment.

Risk: Live collection can expose raw community data, credentials, or budget to external source providers if scope and storage are handled loosely.

Mitigation: Approve only specific sources and budgets, use only trusted API tokens supplied through environment variables, and keep raw run directories private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kunhai1994/skills/voice2need)
- [Server-resolved GitHub provenance](https://github.com/kunhai1994/Voice2Need/tree/dev/skills/voice2need)
- [Research method](references/research-method.md)
- [Operations](references/operations.md)
- [Source configuration](references/sources.md)
- [Findings JSON](references/findings-format.md)
- [Semantic evaluation](references/semantic-evaluation.md)
- [Apify actor runs API](https://docs.apify.com/api/v2/actors-runs-post)
- [Apify dataset items API](https://docs.apify.com/api/v2/dataset-items-get)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration and findings files, analysis packets, and a final Markdown report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs preserve source snippets, evidence IDs, coverage gaps, counterevidence, and explicit unknowns.]

## Skill Version(s):

0.1.0 (source: server release metadata and bundled package __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
