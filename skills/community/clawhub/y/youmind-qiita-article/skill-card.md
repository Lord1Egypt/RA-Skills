## Description: <br>
Write and publish Qiita articles with AI using YouMind knowledge-base research, Japanese developer-audience adaptation, GFM Markdown with Qiita extensions, and one-click publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to research, draft, validate, and publish Qiita articles through YouMind. It also adapts existing Markdown for Qiita's Japanese developer audience and publishing workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a YouMind API key, YouMind knowledge-base content, and a connected Qiita account. <br>
Mitigation: Install only when that access is acceptable, store only the YouMind API key in the shared config, and do not paste Qiita personal tokens into the skill repository. <br>
Risk: The skill can mutate or delete Qiita content, and server evidence reports a conflict between documented private-by-default behavior and actual publish defaults. <br>
Mitigation: Verify article body, tags, images, and visibility before publishing; use private mode explicitly; and treat update, set-public, and delete commands as high-impact actions requiring user confirmation. <br>
Risk: Generated or adapted technical articles can include incorrect, outdated, or non-reproducible guidance. <br>
Mitigation: Run the preview or validation flow, check code examples and environment information, and review tags and references before publishing. <br>
Risk: External image URLs such as cdn.gooo.ai may fail or leak unsuitable hotlinks when published to Qiita. <br>
Mitigation: Re-host images through Qiita before publishing and confirm the final Markdown contains no blocked image-hosting URLs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mindy-youmind/youmind-qiita-article) <br>
- [YouMind Qiita OpenAPI Reference](references/api-reference.md) <br>
- [Qiita Platform DNA](references/platform-dna.md) <br>
- [Content Generation Playbook](references/content-generation-playbook.md) <br>
- [Content Adaptation Playbook](references/content-adaptation-playbook.md) <br>
- [Pipeline](references/pipeline.md) <br>
- [Dispatch Capability Manifest](dispatch-capabilities.yaml) <br>
- [YouMind Connector Settings](https://youmind.com/settings/connector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown articles, review notes, shell commands, configuration snippets, and Qiita publishing results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create, update, publish, make private or public, list, and delete Qiita items through YouMind OpenAPI; review publishing actions before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, SKILL.md frontmatter, toolkit/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
