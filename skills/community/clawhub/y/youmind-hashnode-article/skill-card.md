## Description: <br>
Write and publish Hashnode articles through YouMind OpenAPI, with draft-first publishing, published post listing, draft listing, tag lookup, and connector or pricing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to draft, adapt, preview, and publish technical Hashnode articles through a YouMind-connected Hashnode account. It supports draft review workflows, immediate publication when explicitly requested, post and draft lookup, and Hashnode tag guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a YouMind API key that can publish through the connected Hashnode account and may access YouMind knowledge data. <br>
Mitigation: Install only when that access is acceptable, protect `~/.youmind/config.yaml` as a secret, and rotate or revoke the API key if it is exposed. <br>
Risk: Publishing and deletion actions can change or remove Hashnode content. <br>
Mitigation: Use draft mode first, require explicit user approval before publishing or deleting, and run delete commands only when permanent removal is intended. <br>
Risk: The artifact includes broader YouMind data and agent utilities beyond Hashnode publishing. <br>
Mitigation: Review the installed commands before use and avoid invoking unrelated YouMind utilities unless they are needed for the article workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mindy-youmind/youmind-hashnode-article) <br>
- [Hashnode API Reference](references/api-reference.md) <br>
- [Publishing Pipeline](references/pipeline.md) <br>
- [Hashnode Platform DNA](references/platform-dna.md) <br>
- [Content Generation Playbook](references/content-generation-playbook.md) <br>
- [Content Adaptation Playbook](references/content-adaptation-playbook.md) <br>
- [Shared Publishing Rules](shared/PUBLISHING.md) <br>
- [YouMind Home Configuration](shared/YOUMIND_HOME.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, terminal output summaries, and command or configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview mode writes adapted Markdown under output/. Publish commands may create drafts, publish posts, list posts or drafts, fetch content, search tags, or delete Hashnode content through YouMind OpenAPI.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, toolkit/package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
