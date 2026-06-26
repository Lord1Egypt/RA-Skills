## Description: <br>
Article Writer helps agents research, structure, draft, archive, and publish technical articles to a WeChat Official Account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viodmain](https://clawhub.ai/user/viodmain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and external users can use this skill to turn a requested technical topic into a researched Markdown article with metadata, examples, source attribution, and optional WeChat publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save drafts and publish to a WeChat Official Account without a clearly required final approval step. <br>
Mitigation: Require the agent to show the final draft, destination, and publication action, then obtain explicit user approval before saving or publishing. <br>
Risk: Publishing requires WECHAT_APP_ID and WECHAT_APP_SECRET credentials. <br>
Mitigation: Keep WeChat credentials in protected environment variables, avoid exposing them in prompts or article content, and review the referenced publishing workflow before use. <br>
Risk: The skill performs online research and may incorporate incorrect, outdated, or weakly sourced material. <br>
Mitigation: Prioritize authoritative sources, keep attribution links in the article, and verify technical claims before publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/viodmain/tech-article-writer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles with frontmatter metadata, citations, optional code examples, and inline shell commands for publication workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save drafts to an Obsidian vault and publish through a configured WeChat Official Account workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
