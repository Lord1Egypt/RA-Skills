## Description: <br>
Extracts a leader's or mentor's guidance, requirements, and action items for a specific person from Chinese or English meeting transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tengjie888](https://clawhub.ai/user/tengjie888) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, managers, team leads, mentors, and students use this skill to turn meeting transcripts into concise guidance summaries for a named member. It identifies direct instructions, indirect guidance, priorities, deadlines, quality expectations, collaboration notes, and selected original quotes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags a helper that can run a nested agent with broad filesystem access and approval bypassed. <br>
Mitigation: Install only when the publisher is trusted, prefer non-yolo review settings, and avoid sending sensitive content to fallback reviewer tools unless that data flow is approved. <br>
Risk: Meeting transcripts may contain confidential business, academic, or personal information. <br>
Mitigation: Use approved transcript-sharing channels, redact sensitive details when possible, and avoid processing meetings whose participants have not authorized this use. <br>
Risk: The skill infers indirect guidance, priorities, and implied expectations from conversational context. <br>
Mitigation: Review inferred action items against the original meeting transcript before treating them as assigned tasks or commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tengjie888/zeelin-meetinginstructions) <br>
- [Publisher profile](https://clawhub.ai/user/tengjie888) <br>
- [Skill artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with structured action items, priorities, deadlines, context, and selected original quotes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the meeting transcript language and marks uncertain conclusions with an explicit inference label.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
