## Description:

Xia Card helps an agent create, manage, share, and sync a personal social card and contact roster, including recognizing agent-card:// messages to save other people's cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxd20010606-cmd](https://clawhub.ai/user/sxd20010606-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and their agents use Xia Card to build a shareable profile, maintain a local contact roster, import agent-card:// contacts, and publish or sync selected public card fields with the configured card server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A fetched card response may direct the agent to install another skill.

Mitigation: Require explicit user confirmation and manually verify the publisher and source before installing any skill from a remote card response.

Risk: The skill stores contacts and an API key locally and publishes selected profile fields to the configured server.

Mitigation: Review public fields before publishing, keep private notes out of published fields, and protect config.json because it can contain api_key and user_id values.

Risk: Contact sync may change locally stored roster details.

Mitigation: Review sync conflict prompts and preserve manually_edited_fields for details that should not be overwritten by server data.

## Reference(s):

- [Xia Card ClawHub release](https://clawhub.ai/sxd20010606-cmd/skills/xia-card)
- [Data format reference](references/data-format.md)
- [Operation manual](references/manual.md)
- [Card service endpoint](https://www.adonghub.cn)
- [schema.org Person](https://schema.org/Person)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance, api calls]

**Output Format:** [Markdown-style text responses and JSON file updates, including a fixed three-part share block.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local profile, contacts, and config JSON files and call the configured card server after user confirmation.]

## Skill Version(s):

2.5.1 (source: ClawHub release metadata; artifact frontmatter reports 2.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
