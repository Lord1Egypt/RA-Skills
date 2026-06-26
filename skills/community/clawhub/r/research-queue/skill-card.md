## Description: <br>
Structured background research queue for unresolved technical, product, algorithmic, mathematical, and workflow questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozi1924](https://clawhub.ai/user/mozi1924) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to maintain a structured QUESTIONS.md queue, investigate one unresolved question at a time, and preserve evidence, conclusions, and durable memory notes for follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated research runs may inspect queue links or local files that contain sensitive configuration, credentials, or private context. <br>
Mitigation: Review QUESTIONS.md entries before enabling OpenClaw cron, keep allowedTools minimal, and avoid pointing the queue at secrets or credentials unless that access is intentional. <br>
Risk: Research entries can become misleading if a question is marked complete without enough evidence or without separating verified findings from hypotheses. <br>
Mitigation: Require a concrete evidence summary and conclusion for done items, keep blocked work in Active Questions, and distinguish verified findings, hypotheses, and blocked reasons. <br>


## Reference(s): <br>
- [Queue Format](references/queue-format.md) <br>
- [Automation](references/automation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown queue updates with concise evidence summaries, conclusions, and optional inline commands or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates at most one question by default and records timestamps, status, evidence, conclusion, and optional memory note paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
