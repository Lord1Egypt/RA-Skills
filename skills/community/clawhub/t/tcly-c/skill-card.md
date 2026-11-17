## Description:

Travel Customizer helps collect travel requirements through conversation and submit structured trip request details to a Feishu Bitable table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijingxu007](https://clawhub.ai/user/lijingxu007)

### License/Terms of Use:

MIT-0

## Use Case:

Travel teams can use this skill to collect traveler requirements and submit destination, party size, departure date, budget, preferences, special requests, name, and phone details into a Feishu Bitable table. Treat it as a Feishu lead-capture workflow unless the public instructions and available tool behavior are aligned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public instructions describe itinerary creation, search, update, and deletion, while the security evidence says the available behavior is Feishu lead capture.

Mitigation: Present the skill as lead capture until documentation and implemented behavior are aligned.

Risk: The skill can submit personal travel and contact details to a third-party Feishu table without enforced confirmation.

Mitigation: Use only a Feishu app and table controlled by the deploying team, restrict collaborators, collect only necessary details, and require explicit user confirmation before submission.

## Reference(s):

- [Travel Customizer on ClawHub](https://clawhub.ai/lijingxu007/skills/tcly-c)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [Text, API calls, Configuration guidance]

**Output Format:** [Plain text or Markdown responses with structured Feishu Bitable record submissions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials, base token, and table ID.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
