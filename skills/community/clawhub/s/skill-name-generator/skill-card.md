## Description: <br>
基于功能描述生成符合规范且易于搜索的Skill名称；当用户需要为Skill命名、或询问"我的skill应该叫什么"时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to generate Chinese and English skill names from a feature description, with naming rationale, SEO analysis, and keyword extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad naming requests or return both Chinese and English when only one language is wanted. <br>
Mitigation: Specify the desired language, naming constraints, and output scope before using the suggestions. <br>
Risk: The release metadata includes crypto and purchase-related capability tags that are unrelated to the instruction-only behavior reported by the security scan. <br>
Mitigation: Review metadata tags before using them for automated routing, trust decisions, or policy enforcement. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/yuanyi-github/skill-name-generator) <br>
- [Skill 命名示例与参考](references/naming-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with ranked English and Chinese name options, rationale, SEO analysis, and extracted keywords.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 2-3 English and Chinese naming options and may include SEO scores or ranking notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
