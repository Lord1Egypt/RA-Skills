## Description:

Collaborative task and project management for Human + AI Agent teamwork, with scoped REST API access for listing boards, creating and updating cards, adding comments, uploading and attaching files, filtering work items, and viewing activity history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simplysemantics](https://clawhub.ai/user/simplysemantics)

### License/Terms of Use:

MIT

## Use Case:

External teams, project managers, small businesses, and agent-enabled workflows use Semantic Hub to coordinate work on shared boards where agents can create, update, comment on, and summarize tasks within granted board access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy disclosures conflict with file upload behavior and email-bearing member or assignee data.

Mitigation: Use the skill only with boards, files, member emails, and assignee data that are approved for transmission to Semantic Hub, and correct the privacy disclosure before broad deployment.

Risk: Agents can upload local files or attach external URLs to cards and comments.

Mitigation: Require explicit user approval before uploading local files or attaching external URLs, and confirm the target board or comment before sending the request.

Risk: The skill depends on a scoped API key for access to Semantic Hub boards.

Mitigation: Provision least-privilege SEMANTIC_HUB_API_KEY credentials per agent and rotate or revoke keys when access is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/simplysemantics/skills/semantic-hub)
- [Semantic Hub Homepage](https://www.simplysemantics.com/semantic-hub.html)
- [Semantic Hub Dashboard](https://dashboard.simplysemantics.com/hub)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown and structured text summaries of board, card, comment, attachment, and history operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEMANTIC_HUB_API_KEY and scoped board access; file uploads and agent counts are subject to plan limits.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact clawhub.json; changelog released 2026-03-06; SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
