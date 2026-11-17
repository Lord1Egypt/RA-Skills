## Description:

Search the web on a topic and produce a structured markdown digest summarizing key findings with source references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to research a topic, fetch relevant web sources, and receive a source-backed markdown digest with findings, source summaries, and gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends the research topic to web search and fetch tools, and retrieved sources may contain incomplete or misleading claims.

Mitigation: Confirm the topic before search, include source counts and references, mark uncertain claims as reported or unverified, and review the digest before relying on it.

Risk: When file output is requested, the skill may create a markdown digest file in the workspace.

Mitigation: Confirm desired filename behavior when overwrites or workspace changes would matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/web-search-digest)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Markdown digest with source count, key findings, per-source summaries, and gaps/open questions; optional digest-{slug}.md workspace file when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses web search and fetch tools; source quality depends on retrieved pages.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
