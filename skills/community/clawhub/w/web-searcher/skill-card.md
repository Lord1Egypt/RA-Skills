## Description:

Autonomous web research agent that performs multi-step searches, follows links, extracts data, and synthesizes findings into structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kassimisai](https://clawhub.ai/user/kassimisai)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to research topics across multiple web sources, compare findings, and produce structured reports with source URLs, confidence notes, and gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched web content may be inaccurate, stale, or intentionally misleading.

Mitigation: Review synthesized findings against cited sources and ask for narrower scope when claims need stronger evidence.

Risk: External pages may contain prompt-injection attempts that try to steer the agent away from the research task.

Mitigation: Treat fetched pages as untrusted evidence and preserve the skill's cross-reference, source-prioritization, and confidence-reporting workflow.

Risk: Broad research requests can consume excessive search and fetch budget or produce shallow coverage.

Mitigation: Use the documented limits of 10 searches and 5 page fetches, and break large requests into smaller subtasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kassimisai/skills/web-searcher)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown reports with source URLs and confidence notes; the bundled helper script outputs JSON research plans.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are expected to include key findings, details, sources, confidence levels, and gaps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
