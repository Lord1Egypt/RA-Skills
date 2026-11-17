## Description:

Web Search Enhanced is a ClawHub skill that claims to perform paged web searches with progress updates, intermediate result handling, resume support, and merged final reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaokkkl](https://clawhub.ai/user/zhaokkkl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers may use this skill to request search-style summaries across multiple result pages and receive a merged final report. Security evidence says the current implementation produces simulated results rather than verified web search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a real web search tool even though security evidence says it does not perform real web searches.

Mitigation: Do not rely on results as verified web evidence unless the skill is changed to call a verifiable search provider.

Risk: The skill may create, overwrite, or delete a predictable temporary file in the working directory.

Mitigation: Review file-system behavior before deployment and isolate execution from important working files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaokkkl/skills/web-search-enhanced)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown-style text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces merged search-style result summaries; security evidence indicates results are simulated unless changed to use a verifiable search provider.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
