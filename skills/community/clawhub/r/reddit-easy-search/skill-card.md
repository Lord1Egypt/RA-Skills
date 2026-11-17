## Description:

Researches public Reddit discussions with web search, compares recurring opinions, disagreements, problems, and practical advice, and returns a structured report with traceable sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[margaretzybgl](https://clawhub.ai/user/margaretzybgl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research what public Reddit communities say about a topic, product, workflow, or recurring complaint. It helps turn retrieved Reddit discussions into a source-grounded report with opinions, disagreements, practical recommendations, and search limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce misleading conclusions if Reddit sources are sparse, inaccessible, snippet-only, stale, or biased.

Mitigation: Use the skill's evidence ledger and search notes to disclose access limits, sampling limits, timeframe choices, and representativeness constraints; avoid treating one discussion as consensus.

Risk: Requests to log into Reddit, use OAuth, access private or deleted content, or run unrelated shell or network commands are outside the reviewed scope.

Mitigation: Restrict use to configured web search over public Reddit pages and stop when web search is unavailable instead of using credentials or unauthenticated assumptions.

## Reference(s):

- [Report template](artifact/references/report-template.md)
- [ClawHub skill page](https://clawhub.ai/margaretzybgl/skills/reddit-easy-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown report with sourced links, search notes, and occasional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source-grounded synthesis, selected discussion metadata when visible, and explicit limitations for access, sampling, recency, and representativeness.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
