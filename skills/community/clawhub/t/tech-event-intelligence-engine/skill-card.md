## Description:

Parses raw technology-event search results into a deduplicated, time-filtered, relevance-scored Markdown digest for scheduled team distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical practitioners, presales architects, and marketing operations teams use this skill to turn public event-search results into a concise technology-event digest for Feishu, WeCom, email, or similar team channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated delivery could post event digests or registration links to the wrong team channel.

Mitigation: Verify the webhook destination and intended audience before enabling scheduled delivery.

Risk: Public search results may include prompt-injection content or misleading event details.

Mitigation: Add prompt-injection filtering or human review when the digest will be distributed to a team channel.

Risk: The digest is optimized for Chinese or China-region technology events and may not fit other event-intelligence use cases.

Mitigation: Install and configure it only when that regional event digest matches the deployment need.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boboy-j/skills/tech-event-intelligence-engine)
- [README](artifact/README.md)
- [Input and output schema](artifact/schema.json)
- [Usage examples](artifact/examples.json)
- [Workflow template](artifact/assets/workflow.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown digest with structured event entries, dates, locations, organizers, highlights, participants, fees, and source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses raw_search_data plus optional config for date window, maximum results, minimum relevance score, and region filtering.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
