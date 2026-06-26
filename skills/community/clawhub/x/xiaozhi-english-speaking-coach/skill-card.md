## Description: <br>
An English speaking coach for warmups, roleplay, impromptu speaking, pronunciation review, and learner-profile-based follow-up when the user permits continuous tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External English learners use this skill to practice spoken English through short daily warmups, scenario roleplays, impromptu speeches, pronunciation drills, and concise review. It can continue from a learner profile only when profile access and continuous tracking are allowed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep a continuing learner profile for pronunciation weaknesses, fluency trends, vocabulary, milestones, and topic preferences. <br>
Mitigation: Enable continuous tracking only when the user wants it, and confirm how the OpenClaw environment lets the user view, disable, or delete the stored speaking profile. <br>
Risk: Broad English voice-practice cues may activate the coach when the user did not intend to start a tracked practice session. <br>
Mitigation: Confirm the user wants English speaking practice before using learner-profile context, and use scheduled reminders only after explicit subscription. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qizhitang/xiaozhi-english-speaking-coach) <br>
- [分年级口语话题库](references/topic-bank.md) <br>
- [5套真实场景完整对话脚本](references/roleplay-scripts.md) <br>
- [中国学生高频发音弱点与纠正方法](references/pronunciation-issues.md) <br>
- [晨间热身5步 · 状态机定义](references/morning-warmup-statemachine.md) <br>
- [口语陪练参考资源库](references/speaking-resources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational coaching responses and markdown progress summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May adapt responses using an authorized learner profile; no shell commands, code, or configuration files are produced.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
