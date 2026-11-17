## Description:

Plans 2-day weekend getaways by using the flyai CLI to search flights, hotels, attractions, and booking-linked travel options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill through an agent to compare short weekend trip options, including transport, lodging, attractions, and booking links. It is designed for quick 2-day getaway planning with real-time results from the configured travel CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a global npm CLI and execute external travel-search commands.

Mitigation: Review the package source and installation behavior first, prefer an isolated environment, and use pinned dependencies before deployment.

Risk: Travel searches may be sent to an external service and produce commercial booking links.

Mitigation: Disclose data sharing and commercial-link behavior to users, and require consent before sending travel queries.

Risk: The artifact describes local hidden logging of raw trip queries.

Mitigation: Disable or constrain local logging, avoid storing sensitive trip details, and document retention and deletion controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/weekend-trip)
- [Parameter and output templates](artifact/references/templates.md)
- [Weekend trip playbooks](artifact/references/playbooks.md)
- [Fallback handling](artifact/references/fallbacks.md)
- [Execution log schema](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when recovery steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires booking links in displayed results and uses the user's language for responses.]

## Skill Version(s):

3.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
