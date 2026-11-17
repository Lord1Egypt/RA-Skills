## Description:

RSS Summarizer helps an agent manage RSS/Atom subscriptions, fetch recent feed items, filter updates by keyword, and return summaries or feed updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanan9812](https://clawhub.ai/user/wanan9812)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to subscribe to RSS/Atom feeds, list and remove subscriptions, fetch recent entries, apply keyword filters, and produce feed updates for chat or document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches arbitrary user-supplied feed URLs without network-safety limits.

Mitigation: Use only trusted feed URLs and add URL validation, egress controls, and blocks for localhost, private network, and cloud metadata addresses before broad deployment.

Risk: Untrusted feed text is passed back to the agent.

Mitigation: Treat feed titles, links, and snippets as untrusted data, isolate them from agent instructions, and review summaries before acting on feed content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanan9812/skills/rss-summarizer)
- [Publisher Profile](https://clawhub.ai/user/wanan9812)
- [rss-parser package](https://registry.npmjs.org/rss-parser/-/rss-parser-3.13.0.tgz)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON results containing markdown, plain text, or structured feed-item data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include feed titles, item titles, links, publication dates, snippets, errors, and saved subscription/configuration data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
