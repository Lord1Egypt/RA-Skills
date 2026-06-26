## Description: <br>
微信读书伴侣 helps agents run enhanced WeRead workflows for daily book briefings, recommendations, read-before-you-commit analysis, public review lookup, highlight analysis, personal note export, reading reports, bookshelf planning, and side-by-side book decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze WeRead books and reading history, choose what to read next, export personal notes, and prepare privacy-aware reading reports using the official weread-skills dependency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a WeRead API key and private reading history. <br>
Mitigation: Install only if comfortable granting that access, keep WEREAD_API_KEY out of generated output, and follow the skill's privacy guidance. <br>
Risk: Personal note exports and shelf reports can contain private highlights, private books, and public-review identifiers. <br>
Mitigation: Choose output paths carefully and review generated files before sharing them. <br>
Risk: Reading recommendations and score factors can be mistaken for objective judgments. <br>
Mitigation: Present scores as ranking aids, include caveats, and explain the WeRead data behind each recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/weread-plus) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>
- [Official weread-skills download](https://cdn.weread.qq.com/skills/weread-skills.zip) <br>
- [WeRead Agent API gateway](https://i.weread.qq.com/api/agent/gateway) <br>
- [Privacy and Content Boundaries](references/privacy.md) <br>
- [Recommendation Design](references/recommendation.md) <br>
- [Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON summaries with shell commands and optional local Markdown or JSON exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include WeRead deep links, public review summaries, recommendation caveats, and locally written note or report files when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
