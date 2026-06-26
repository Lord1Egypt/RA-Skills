## Description: <br>
Daily trivia questions with scoring, streaks, and category selection. Learn something new every day. Competitive mode for group chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add daily trivia prompts, answer checking, score tracking, and streak summaries to an agent experience. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores score and streak state in a local JSON file, and a user-provided score file path could point at an important existing file. <br>
Mitigation: Use a dedicated, non-sensitive score file path for TriviaBot state and keep independent backups of important local data. <br>
Risk: The release claims group mode, difficulty selection, and weekly leaderboard behavior that the security evidence says is not implemented in this version. <br>
Mitigation: Treat those features as unavailable unless verified in a newer release, and do not rely on them for user-facing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/trivia-bot) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Text responses and JavaScript result objects containing quiz prompts, answer feedback, score, streak, and fact fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local score and streak state in a JSON file when used through the bundled JavaScript module.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
