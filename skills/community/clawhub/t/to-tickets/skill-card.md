## Description:

Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thefirstelement](https://clawhub.ai/user/thefirstelement)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to convert a plan, specification, issue, or conversation into dependency-aware tickets that can be reviewed and then published to local files or an issue tracker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ticket breakdowns may publish incorrect scope, parent issue references, blocking links, or triage labels to a public or automation-connected tracker.

Mitigation: Review the proposed ticket list, tracker configuration, parent issue, blocking relationships, and ready-for-agent label before approving publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thefirstelement/skills/to-tickets)

## Skill Output:

**Output Type(s):** [Markdown, Files, API Calls, Guidance]

**Output Format:** [Markdown ticket proposals and issue bodies, with local Markdown files or tracker issues after user approval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tickets include blocking relationships and are ordered with blockers first.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
