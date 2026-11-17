## Description:

Write and publish Ghost articles with AI using YouMind knowledge-base research, Ghost-oriented writing, Markdown-to-HTML conversion, feature image upload, and Ghost publishing through a YouMind-connected Ghost account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft, adapt, preview, and publish Ghost articles through YouMind. It supports topic-driven article generation, publishing existing Markdown, validating Ghost connectivity, and managing Ghost drafts or published posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change Ghost content, including publishing, unpublishing, or deleting posts.

Mitigation: Require a human review before publishing, unpublishing, or deleting Ghost content, and prefer draft mode unless direct publication is explicitly requested.

Risk: Unsafe Markdown or image inputs can expose local files or API keys through publishing-related code paths.

Mitigation: Use only trusted Markdown and image inputs, protect ~/.youmind/config.yaml with owner-only permissions, and avoid including secrets in article content or image paths.

Risk: Changing youmind.base_url away from the documented endpoint can send requests or credentials to an unintended service.

Mitigation: Keep youmind.base_url set to https://youmind.com/openapi/v1 unless doing controlled local development.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindy-youmind/skills/youmind-ghost-article)
- [YouMind Ghost OpenAPI Reference](references/api-reference.md)
- [Ghost Article Pipeline](references/pipeline.md)
- [Ghost Platform DNA](references/platform-dna.md)
- [Generation Playbook: Idea to Ghost-Native Draft](references/content-generation-playbook.md)
- [Adaptation Playbook: Existing Article to Ghost-Native](references/content-adaptation-playbook.md)
- [Ghost Content Adaptation Guide](references/content-adaptation.md)
- [Dispatch Integration Protocol](shared/DISPATCH_CONTRACT.md)
- [YouMind API key settings](https://youmind.com/settings/api-keys)
- [YouMind connector settings](https://youmind.com/settings/connector)
- [YouMind pricing](https://youmind.com/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles, Ghost-ready HTML, CLI output, configuration snippets, and result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local article drafts or previews and may publish, update, unpublish, or list Ghost posts through YouMind when configured.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, toolkit/package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
