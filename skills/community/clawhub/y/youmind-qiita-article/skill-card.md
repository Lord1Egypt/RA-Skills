## Description:

Write and publish Qiita articles with AI using YouMind knowledge-base research, Japanese developer-audience adaptation, GFM Markdown with Qiita extensions, and guided publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical authors use this skill to research, draft, adapt, validate, and publish Qiita articles through YouMind and a connected Qiita account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing visibility may differ from private-by-default documentation when using the CLI.

Mitigation: Before publishing, explicitly pass --private or set private: true in front matter, then verify the resulting Qiita URL and visibility.

Risk: Update, delete, and set-public commands can change content in the connected Qiita account.

Mitigation: Review the command and target item ID with the user before running account-impacting actions.

Risk: The skill requires a YouMind API key with publishing-related access.

Mitigation: Keep the key in the documented YouMind config file, use only a key appropriate for publishing workflows, and avoid committing credentials.

Risk: Changing youmind.base_url away from the official endpoint can route publishing actions to a local or non-production service.

Mitigation: Keep youmind.base_url on https://youmind.com/openapi/v1 unless deliberately testing locally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindy-youmind/skills/youmind-qiita-article)
- [YouMind publisher profile](https://clawhub.ai/user/mindy-youmind)
- [YouMind Qiita OpenAPI Reference](artifact/references/api-reference.md)
- [Qiita Platform DNA](artifact/references/platform-dna.md)
- [Content Generation Playbook](artifact/references/content-generation-playbook.md)
- [Content Adaptation Playbook](artifact/references/content-adaptation-playbook.md)
- [Pipeline](artifact/references/pipeline.md)
- [YouMind API keys](https://youmind.com/settings/api-keys?utm_source=youmind-qiita-article)
- [YouMind OpenAPI base URL](https://youmind.com/openapi/v1)
- [YouMind pricing](https://youmind.com/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles, validation notes, JSON API payloads, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Qiita-ready drafts and publishing result links; publishing actions depend on a configured YouMind API key and connected Qiita account.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
