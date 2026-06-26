## Description: <br>
Word Memory is a vocabulary practice skill that schedules review with an Ebbinghaus-style memory curve and supports daily study plans, quizzes, word lookup, and progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and language-study assistants use this skill to generate daily vocabulary practice, review due words, quiz recall, look up sample word details, and track learning progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local progress files can contain the selected word list, daily count, learned words, review history, and mastery statistics. <br>
Mitigation: Keep generated progress files local, avoid sharing them unintentionally, and remove them when the study history is no longer needed. <br>
Risk: Future dictionary API or scheduled reminder features could add external calls or notifications. <br>
Mitigation: Enable those features only when they are explicit, configured by the user, and easy to disable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/word-memory) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown-style text responses and local JSON progress data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local progress and statistics files for selected word list, daily count, learned words, review history, and mastery stats.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
