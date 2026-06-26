## Description: <br>
欧路词典生词本管理与每日测试技能。支持自动从欧路词典收藏夹出题、管理单词、删除已掌握词汇。适合每日背单词使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to automate Eudic vocabulary-list review, generate daily multiple-choice quizzes, list saved words, and delete words they have mastered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Eudic API token for account access. <br>
Mitigation: Store the token privately, prefer environment variables or protected local configuration, and avoid putting the token in shell history or shared cron files. <br>
Risk: Delete commands can remove words from the user's Eudic vocabulary list. <br>
Mitigation: Double-check word IDs before running delete actions and review generated delete commands before execution. <br>
Risk: Generated quiz and answer files can expose vocabulary data and correct answers. <br>
Mitigation: Write quiz output to a private directory and avoid sharing generated answer files. <br>


## Reference(s): <br>
- [Eudic OpenAPI Authorization](https://my.eudic.net/OpenAPI/Authorization) <br>
- [Eudic Open API Base URL](https://api.frdic.com/api/open/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/dadaniya99/xiaolongxia-eudic-vocab) <br>
- [Publisher Profile](https://clawhub.ai/user/dadaniya99) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with JSON quiz and answer files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Eudic API token and can write quiz output files locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
