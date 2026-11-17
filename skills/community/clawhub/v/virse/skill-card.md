## Description:

Virse Design helps agents use the Virse AI Design Platform for image generation, canvas layout, workspace management, and asset organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vxcent](https://clawhub.ai/user/vxcent)

### License/Terms of Use:

MIT-0

## Use Case:

External designers, creative operators, and developers use this skill to connect an agent to Virse for workspace and canvas inspection, AI image generation, asset organization, and repeatable visual design workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Virse credentials and can read or change Virse workspaces, canvases, assets, and generated images using the user's token.

Mitigation: Install only if the Virse service and publisher are trusted, use an appropriate token, and require user confirmation before destructive operations.

Risk: A custom VIRSE_BASE_URL could send authentication or workspace operations to an untrusted host.

Mitigation: Keep VIRSE_BASE_URL unset or set only to a trusted Virse endpoint before using the skill.

Risk: The skill includes an update path that checks a GitHub source and can apply updates after user approval.

Mitigation: Review any proposed update and its source before approving installation or pull operations.

## Reference(s):

- [Virse Design Skill Page](https://clawhub.ai/vxcent/skills/virse)
- [Virse Tools Reference](artifact/tools-reference.md)
- [Virse Authentication Guide](artifact/auth-guide.md)
- [Product Listing Image Pipeline](artifact/examples/product-listing-pipeline.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool-call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Virse MCP operations that read or change workspaces, canvases, assets, and image generations when the user authorizes the workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
