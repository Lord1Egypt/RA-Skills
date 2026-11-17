## Description:

SearXNG-lite provides lightweight multi-engine web search aggregation through a local Python script without requiring Docker, a server, or a SearXNG instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrzhangkris](https://clawhub.ai/user/mrzhangkris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run aggregated web, code, academic, news, and community searches from a local Python command-line tool. It is useful when multiple search engines or specific search categories are needed beyond a single quick lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to multiple external search providers or through a configured proxy.

Mitigation: Avoid using the skill for secrets, confidential terms, regulated personal data, proprietary incident details, or other sensitive queries.

Risk: Dependency behavior can change if packages are installed without version controls.

Mitigation: Install the skill in a virtual environment and pin dependencies when reproducible behavior is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrzhangkris/skills/searxng-lite)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results by default, with optional compact human-readable text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes result titles, URLs, snippets, source engines, scores, elapsed time, and non-fatal engine errors.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
