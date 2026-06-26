## Description: <br>
自动化管理今日头条账号，支持热点监控、AI内容生成、封面设计及自动发布，适合自媒体和营销团队。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjsmme-hash](https://clawhub.ai/user/cjsmme-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, self-media operators, and marketing teams use this skill to monitor trending topics, draft Toutiao posts and articles, generate cover concepts, and coordinate reviewed publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide browser-driven publishing to a real Toutiao account. <br>
Mitigation: Require explicit user approval before publishing or scheduling any post. <br>
Risk: Account credentials may be needed for Toutiao operations. <br>
Mitigation: Use a dedicated account when possible and do not paste passwords into prompts or files. <br>
Risk: Generated drafts or cover images may be inaccurate, noncompliant, or unsuitable for a brand account. <br>
Mitigation: Review drafts, titles, tags, and covers before release, using the artifact content and cover checklists. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjsmme-hash/toutiao-ops) <br>
- [Agent team workflow](artifact/AGENTS.md) <br>
- [Toutiao content guidelines](artifact/CONTENT.md) <br>
- [Cover design guidelines](artifact/COVERS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with drafts, reports, checklists, prompts, and example Python code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose browser-driven publishing steps; live posting should require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
