## Description: <br>
Helps an agent create, maintain, query, audit, and archive a persistent LLM wiki in YoudaoNote using the youdaonote CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lephix](https://clawhub.ai/user/lephix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn source material, conversations, and research notes into a maintained YoudaoNote wiki with raw material, entity pages, concept pages, comparisons, query archives, indexes, and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requires YoudaoNote API-key access and can create or update persistent cloud notes in the user's account. <br>
Mitigation: Install only if that account access is acceptable, review what will be saved, and avoid ingesting secrets or regulated data. <br>
Risk: Broad wiki and archive triggers may save conversation content or perform multiple note updates. <br>
Mitigation: Use explicit commands where possible, review generated note content before saving, and confirm bulk writes before proceeding. <br>
Risk: Registry rebuilds and other maintenance actions can write account-level wiki metadata. <br>
Mitigation: Confirm registry rebuilds and maintenance writes before execution, and review the resulting registry note. <br>


## Reference(s): <br>
- [YoudaoNote LLM Wiki on ClawHub](https://clawhub.ai/lephix/youdaonote-llm-wiki) <br>
- [YoudaoNote](https://note.youdao.com) <br>
- [YoudaoNote CLI installation guide](https://note.youdao.com/help-center/cli-install-guide.html) <br>
- [YoudaoNote Open Platform](https://mopen.163.com) <br>
- [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and note content plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update persistent cloud notes through the youdaonote CLI when the user authorizes writes.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
