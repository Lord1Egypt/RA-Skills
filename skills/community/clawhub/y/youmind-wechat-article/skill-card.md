## Description: <br>
Writes, formats, previews, and sends WeChat Official Account article drafts through a YouMind-backed article workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and marketing teams use this skill to turn a topic or finished Markdown draft into a WeChat-ready article, including formatting, previewing, cover/image handling, and draft-box publishing. It is also used to review article performance and adapt future content based on YouMind knowledge-base material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write to a connected WeChat draft box and perform broad YouMind account actions. <br>
Mitigation: Review the target account, generated article, cover/image choices, and result links before relying on or further publishing any draft. <br>
Risk: The skill requires a YouMind API key and may upload article content, prompts, images, metadata, or knowledge-base material to YouMind/WeChat services. <br>
Mitigation: Use an approved account and avoid confidential drafts or regulated content unless that remote processing is explicitly permitted. <br>
Risk: Optional scheduled automation or companion tooling can increase the chance of unintended publishing workflow changes. <br>
Mitigation: Enable automation only after validating configuration, account binding, and expected draft behavior in a manual run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/youmind-wechat-article) <br>
- [YouMind API keys](https://youmind.com/settings/api-keys?utm_source=youmind-wechat-article) <br>
- [YouMind connector settings](https://youmind.com/settings/connector?utm_source=youmind-wechat-article) <br>
- [Setup guide](references/setup.md) <br>
- [Runtime rules](references/runtime-rules.md) <br>
- [YouMind integration guide](references/youmind-integration.md) <br>
- [CLI reference](references/cli-reference.md) <br>
- [WeChat constraints](references/wechat-constraints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, command snippets, configuration guidance, and result links for preview or WeChat draft review.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, Python 3, a YouMind API key, and a YouMind-connected WeChat Official Account for publishing actions.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
