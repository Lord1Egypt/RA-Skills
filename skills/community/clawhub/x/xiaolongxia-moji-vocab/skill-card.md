## Description: <br>
Manages a Moji Dictionary vocabulary list and generates daily Japanese vocabulary quizzes with oldest-first review, mixed meaning and reading questions, and deletion of mastered words. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and language learners use this skill to review saved Japanese vocabulary from Moji Dictionary, generate short quizzes, inspect vocabulary statistics, and remove words they have mastered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts require a Moji session token and device ID, which may grant access to the user's Moji account data. <br>
Mitigation: Store credentials locally, pass them through environment variables or command-line arguments only in trusted environments, and do not paste them into shared chats or logs. <br>
Risk: Deletion workflows can remove saved vocabulary from the user's Moji favorites. <br>
Mitigation: Run deletion commands with --dry-run first, review the selected word IDs or JLPT levels, and delete only after confirming the target set. <br>
Risk: The skill makes live requests to Moji Dictionary services using the user's account credentials. <br>
Mitigation: Install and run the skill only when the user trusts the third-party publisher and accepts the account-level API access described in the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dadaniya99/xiaolongxia-moji-vocab) <br>
- [Moji Dictionary](https://www.mojidict.com) <br>
- [Moji Dictionary API endpoint](https://api.mojidict.com/parse/functions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and quiz output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Moji session token and device ID for live account operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
