## Description: <br>
Mood Tracker helps users record moods, analyze patterns, identify triggers, and get general improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to track mood entries, review mood patterns over time, and receive general suggestions for improving mood awareness. It is suitable for personal reflection workflows rather than clinical diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports maintainer tooling behavior that can run a nested Codex review with broad filesystem access and bypassed approval prompts. <br>
Mitigation: Install only if comfortable with that access model, and prefer running the autoreview helper with --no-yolo or AUTOREVIEW_YOLO=0 unless broad local access is intentional. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference user-provided mood labels, notes, triggers, and time windows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
