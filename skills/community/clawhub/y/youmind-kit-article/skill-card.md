## Description:

Write and publish Kit broadcasts with AI using YouMind knowledge-base research, creator-profile-aware drafting, Markdown-to-HTML conversion, and Kit publishing through the user's connected YouMind account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, newsletter operators, and publishing teams use this skill to draft, adapt, preview, and publish Kit broadcasts through YouMind. It is intended for workflows that need topic research, Kit-native subject and preview writing, Markdown-to-HTML conversion, template discovery, and result links for public or private broadcasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local content and a YouMind API key to a configurable API origin.

Mitigation: Keep the base URL on the official YouMind endpoint, protect the ~/.youmind config files, and only use trusted account credentials.

Risk: Publishing, updating, and deleting broadcasts can make real changes to the connected Kit account.

Mitigation: Validate the connection first, use private drafts or a test account for validation, and require user approval before publish or delete actions.

Risk: Local Markdown preview can expose unsafe content if generated from untrusted Markdown.

Mitigation: Preview only trusted Markdown or review/sanitize imported content before generating local HTML previews.

Risk: Deep-check workflows exercise remote publishing and cleanup paths.

Mitigation: Do not run deep-check against production accounts unless the operator accepts test broadcast creation and deletion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindy-youmind/skills/youmind-kit-article)
- [YouMind Kit OpenAPI Reference](references/api-reference.md)
- [Kit Pipeline](references/pipeline.md)
- [Kit Platform DNA](references/platform-dna.md)
- [Content Generation Playbook](references/content-generation-playbook.md)
- [Content Adaptation Playbook](references/content-adaptation-playbook.md)
- [YouMind Home Directory](shared/YOUMIND_HOME.md)
- [Dispatch Integration Protocol](shared/DISPATCH_CONTRACT.md)
- [YouMind API Keys](https://youmind.com/settings/api-keys?utm_source=youmind-kit-article)
- [YouMind Connector Settings](https://youmind.com/settings/connector)
- [Kit Campaigns](https://app.kit.com/campaigns)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, local draft files, HTML previews, and Kit publish result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm; uses a local YouMind API key and a Kit account connected in YouMind for publishing.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
