## Description:

End-to-end WeChat Official Account article writing and publishing pipeline for topic research, Chinese-first drafting, blind review, fact-checking, formatting, preview, illustration, and draft-box publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:

MIT

## Use Case:

Content creators, operators, and developers use this skill to create WeChat Official Account articles from topic ideation through reviewed, fact-checked, formatted drafts. It supports draft publishing workflows that use either WeChat API credentials or browser automation, with human approval before final publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent behavior and workspace rule changes may affect future sessions.

Mitigation: Install only in workspaces where persistent AGENTS.md and HEARTBEAT.md changes are acceptable, and remove those rules if automatic resumption is not wanted.

Risk: WeChat app credentials and image-generation API keys can be exposed or used against the wrong account.

Mitigation: Store secrets in protected locations, avoid printing them, and confirm the target WeChat account before creating drafts.

Risk: Rendering untrusted Markdown with remote images or PlantUML blocks can introduce network and content risks.

Mitigation: Restrict network destinations for rendering, review untrusted Markdown before rendering, and pin or review external dependencies during setup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/skills/wechat-article-forge)
- [README](README.md)
- [Writer Prompt](references/writer-prompt.md)
- [Reviewer Rubric](references/reviewer-rubric.md)
- [Fact Checker Prompt](references/fact-checker-prompt.md)
- [Browser Automation](references/browser-automation.md)
- [Quality Checks](references/quality-checks.md)
- [Pipeline State](references/pipeline-state.md)
- [WeChat HTML Rules](references/wechat-html-rules.md)
- [Data Layout](references/data-layout.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown drafts, JSON state files, formatted HTML, shell commands, configuration guidance, and WeChat draft creation actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces drafts under the configured workspace, uses human preview before publication, and may call external services for fact checking, image generation, rendering dependencies, and WeChat draft creation.]

## Skill Version(s):

2.4.1 (source: server release metadata and CHANGELOG, released 2026-03-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
