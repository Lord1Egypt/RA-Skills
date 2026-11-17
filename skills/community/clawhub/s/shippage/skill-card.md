## Description:

Publish HTML or Markdown to a public URL instantly with zero config and auto-registration on first use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncle-jacky](https://clawhub.ai/user/uncle-jacky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content authors use Shippage to publish generated HTML, Markdown, reports, dashboards, documentation, prototypes, and landing pages as shareable public webpages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-provided content to shippage.ai and make it available at a public URL.

Mitigation: Require explicit user confirmation before publishing and avoid uploading secrets, private data, or regulated content.

Risk: The skill includes a silent auto-update flow that can replace its own instructions from a remote server.

Mitigation: Remove or disable the auto-update section before installation, or require explicit review before applying downloaded instructions.

Risk: Auto-registration may store ShipPage credentials in a local file.

Mitigation: Store credentials with restrictive file permissions or move them into an approved secret store.

## Reference(s):

- [Shippage ClawHub listing](https://clawhub.ai/uncle-jacky/skills/shippage)
- [ShipPage homepage](https://shippage.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code snippets; runtime responses are JSON containing published URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes user-provided HTML or Markdown to a public URL and may store local credentials after auto-registration.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
