## Description: <br>
Writes and publishes Dev.to articles with AI, using YouMind for topic research, developer-audience adaptation, Markdown front matter, draft preview, and publishing through a connected Dev.to account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and developer advocates use this skill to generate, validate, preview, and publish Dev.to posts from a topic or existing Markdown while keeping publishing draft-first unless the user confirms public release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a YouMind API key and accesses YouMind content and Dev.to publishing APIs. <br>
Mitigation: Store credentials only in the shared YouMind config, avoid committing config files, and review generated drafts for secrets or private content before publishing. <br>
Risk: Publishing actions can make content public or change existing Dev.to articles. <br>
Mitigation: Keep draft mode as the default and require explicit user confirmation before public publishing, publish-by-ID, or unpublish-by-ID operations. <br>
Risk: Generated technical articles may include inaccurate claims, outdated examples, or unsuitable tags. <br>
Mitigation: Run the skill's validation and conformance checks, verify code examples and sources, and edit drafts before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/youmind-devto-article) <br>
- [YouMind Dev.to OpenAPI Reference](references/api-reference.md) <br>
- [Pipeline](references/pipeline.md) <br>
- [Platform DNA](references/platform-dna.md) <br>
- [Content Generation Playbook](references/content-generation-playbook.md) <br>
- [Content Adaptation Playbook](references/content-adaptation-playbook.md) <br>
- [YouMind API keys](https://youmind.com/settings/api-keys?utm_source=youmind-devto-article) <br>
- [Dev.to dashboard](https://dev.to/dashboard) <br>
- [YouMind pricing](https://youmind.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown article drafts with Dev.to front matter, command-line guidance, validation reports, and result links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts are saved locally; publishing uses the user's YouMind API key and Dev.to account connected in YouMind.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
