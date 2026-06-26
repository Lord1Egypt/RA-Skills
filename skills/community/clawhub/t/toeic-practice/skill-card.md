## Description: <br>
Daily TOEIC practice coach for a user scoring 600+. Delivers one focused session daily for Parts 5, 6, and 7, explains answers with grammar and vocabulary notes, and targets improvement toward 700+. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cngvc](https://clawhub.ai/user/cngvc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External TOEIC learners use this skill for daily reading-focused homework across Parts 5, 6, and 7. It generates original practice questions, waits for answers, and then explains correct choices, grammar, vocabulary, and distractors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a small local state file to track the last delivered TOEIC part. <br>
Mitigation: Installers should allow the skill to write only its intended memory/toeic-state.md state file and review changes if the path differs. <br>
Risk: Automatically routed agents could invoke the skill for non-TOEIC study requests. <br>
Mitigation: Route this skill only for TOEIC reading practice, TOEIC Parts 5 to 7 homework, or answer-explanation requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cngvc/toeic-practice) <br>
- [Publisher profile](https://clawhub.ai/user/cngvc) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance, Configuration] <br>
**Output Format:** [Markdown and plain text practice sessions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a small local memory file to rotate TOEIC Parts 5, 6, and 7 across sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
