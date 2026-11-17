## Description:

Writes and publishes Dev.to articles by researching with YouMind, adapting for developer audiences, formatting Markdown front matter, validating content, and publishing drafts or public posts through the user's connected Dev.to account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical authors use this skill to turn topics or existing Markdown into Dev.to-native articles, validate tags, front matter, and code blocks, and publish or manage drafts through YouMind.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles publishing credentials and article content that may be sent to YouMind and then Dev.to.

Mitigation: Keep youmind.base_url set to https://youmind.com/openapi/v1, protect ~/.youmind/config.yaml, and do not use config overrides from untrusted sources.

Risk: The skill can publish public Dev.to posts through a connected account.

Mitigation: Use draft mode first and require explicit approval before setting published output to public.

Risk: The installation flow uses npm install and the security evidence notes unpinned npm packages.

Mitigation: Review dependencies and add or verify a lockfile before treating this release as low-risk.

## Reference(s):

- [YouMind Dev.to OpenAPI Reference](references/api-reference.md)
- [Dev.to Platform DNA](references/platform-dna.md)
- [Generation Playbook: Idea to Dev.to-Native Draft](references/content-generation-playbook.md)
- [Adaptation Playbook: Existing Article to Dev.to-Native](references/content-adaptation-playbook.md)
- [Dev.to Content Adaptation Guide](references/content-adaptation.md)
- [Dev.to Article Pipeline](references/pipeline.md)
- [Publishing Guidelines](shared/PUBLISHING.md)
- [YouMind Home Directory](shared/YOUMIND_HOME.md)
- [Dispatch Integration Protocol](shared/DISPATCH_CONTRACT.md)
- [YouMind API Keys](https://youmind.com/settings/api-keys?utm_source=youmind-devto-article)
- [YouMind Pricing](https://youmind.com/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles with YAML front matter, inline shell commands, validation notes, and result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts are preferred by default; public publishing requires explicit user intent.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
