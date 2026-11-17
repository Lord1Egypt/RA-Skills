## Description:

Automates WeChat Official Account article workflows, including Markdown or plain-text rendering with WeMD themes, image and cover upload, draft creation or update, preview, explicit human-confirmed publishing, status checks, asset lookup, and theme management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[traceless929](https://clawhub.ai/user/traceless929)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and publishing teams use this skill to prepare WeChat Official Account articles, render them with selectable themes, upload article assets, create or update drafts, review previews, and publish only after explicit human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a WeChat account, local article files, and image paths, and can create or publish account content.

Mitigation: Run it in a constrained workspace containing only intended article assets, use dedicated WeChat credentials, keep unrelated secrets out of the configured environment, and require explicit preview review before publishing.

Risk: First use may perform Node, Git, and npm setup for the bundled rendering workflow.

Mitigation: Review the bundled setup path and npm dependencies before first use, and install only in an environment where mutable dependency setup is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/traceless929/skills/wechat-publisher-wemd)
- [API Mapping](references/api-mapping.md)
- [Safety Rules](references/safety-rules.md)
- [WeMD Render Engine](https://github.com/tenngoxars/WeMD)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status summaries with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WeChat draft identifiers, preview URLs, publish status results, asset query summaries, and theme names.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
