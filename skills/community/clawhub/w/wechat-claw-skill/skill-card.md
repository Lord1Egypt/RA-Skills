## Description:

Generates WeChat public-account articles from structured JSON, with helpers for source collection, image planning, HTML rendering, validation, draft creation, and optional publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[th3ee9ine](https://clawhub.ai/user/th3ee9ine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and agent operators use this skill to turn structured article inputs into WeChat-ready HTML, validate platform constraints, plan images, and optionally prepare or publish drafts through companion tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional publish path can create and publish drafts on a real WeChat account.

Mitigation: Run the pipeline in dry-run mode first, review the rendered HTML and resolved article JSON, and approve draft or publish actions manually.

Risk: Source collection can fetch user-supplied URLs and render user-supplied article content.

Mitigation: Use trusted source specs, avoid internal or sensitive URLs, and review collected source bundles before article generation.

Risk: External image-generation and WeChat helper scripts are invoked when the full pipeline is enabled.

Mitigation: Point the pipeline only at reviewed helper scripts and verify generated media, uploaded image URLs, and returned media IDs before publishing.

Risk: Generated output may include default attribution such as 39Claw.

Mitigation: Check article metadata, rendered HTML, and author fields for expected attribution before connecting a real account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/th3ee9ine/skills/wechat-claw-skill)
- [English README](docs/README.en.md)
- [OpenClaw integration guide](docs/openclaw.en.md)
- [Writing guide](references/writing-guide.md)
- [Title formulas](references/title-formulas.md)
- [Image prompt reference](references/image-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON article plans, HTML files, image prompt plans, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write rendered article HTML, resolved article JSON, image-plan JSON, and publish pipeline summaries when its scripts are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
