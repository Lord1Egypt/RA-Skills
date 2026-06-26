## Description: <br>
Write and publish Ghost articles with AI through YouMind knowledge base research, Ghost-oriented writing, Markdown-to-HTML conversion, feature image upload, and Ghost publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and publishing teams use this skill to draft, adapt, preview, and publish Ghost articles through a YouMind-connected Ghost account. It supports topic generation, Markdown publishing, draft review, post listing, and publish or unpublish operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a connected Ghost site and post externally. <br>
Mitigation: Use the documented draft-first flow, review Ghost Admin result links, and verify the target site and post status before publishing, unpublishing, or deleting content. <br>
Risk: The skill requires a YouMind API key and a connected publishing workflow. <br>
Mitigation: Install only from a trusted publisher, keep credentials in the documented ~/.youmind configuration, and do not place Ghost Admin credentials in the skill repository. <br>
Risk: Feature image and Markdown inputs may reference local files. <br>
Mitigation: Avoid providing sensitive local file paths and review file inputs before passing them to publish or preview commands. <br>
Risk: Drafts and author profile data under ~/.youmind are shared persistent content. <br>
Mitigation: Treat ~/.youmind content as durable shared workspace data and avoid storing secrets or private material that is not needed for publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/youmind-ghost-article) <br>
- [YouMind Ghost OpenAPI Reference](references/api-reference.md) <br>
- [Ghost Article Pipeline](references/pipeline.md) <br>
- [Ghost Platform DNA](references/platform-dna.md) <br>
- [Content Generation Playbook](references/content-generation-playbook.md) <br>
- [Content Adaptation Playbook](references/content-adaptation-playbook.md) <br>
- [Dispatch Capability Manifest](dispatch-capabilities.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, HTML previews, command output, configuration guidance, and Ghost post result links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create drafts or published posts through YouMind Ghost OpenAPI; draft is the documented default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence, toolkit/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
