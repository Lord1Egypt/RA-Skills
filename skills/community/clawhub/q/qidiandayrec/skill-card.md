## Description:

起点中文网好书推荐 skill，可从三江榜新书和万订/十万均订经典网文中生成 SBTI 个性化推荐，并附书籍链接、推荐理由、IP 衍生品和海外影响力信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[drow931](https://clawhub.ai/user/drow931)

### License/Terms of Use:

MIT-0

## Use Case:

External readers and agents use this skill to generate Chinese web novel recommendations from Qidian-related data sources, including daily Sanjiang picks, classic high-subscription titles, and SBTI-personalized selections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can automatically install Python packages.

Mitigation: Review the skill before installation and run it only in an isolated environment where automatic pip installs are acceptable.

Risk: Helper scripts can write local cache and recommendation history files.

Mitigation: Use the skill only where local cache and history writes are acceptable, and inspect or clear generated files according to local retention expectations.

Risk: The skill can create recurring daily recommendation automation.

Mitigation: Enable daily automation only when recurring runs are explicitly desired.

Risk: Generated Qidian links include a skill attribution trace parameter.

Mitigation: Inform users that recommendation links include attribution and review whether tracked links are appropriate for the deployment context.

## Reference(s):

- [Qidian Data Guide](references/qidian_data_guide.md)
- [ClawHub skill page](https://clawhub.ai/drow931/skills/qidiandayrec)
- [Qidiantu Sanjiang list pattern](https://www.qidiantu.com/bang/1/6/{date})
- [Qidiantu book detail pattern](https://www.qidiantu.com/info/{book_id})
- [Qidiantu 100k subscription badge](https://www.qidiantu.com/badge/shiwanjunding)
- [Qidiantu 10k subscription badge](https://www.qidiantu.com/badge/wanrenzhuipeng)
- [Qidian book link pattern](https://www.qidian.com/book/{book_id}/?_trace=qidiandayrec_skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown recommendation report or structured JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations include Qidian book links with a skill attribution trace parameter; local cache and history files may be written by the scripts.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
