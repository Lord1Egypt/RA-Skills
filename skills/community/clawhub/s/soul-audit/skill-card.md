## Description: <br>
Evaluate an AI agent's soul file, system prompt, or AGENTS.md against the Guardian v0.7 framework and produce a scored ethics audit report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kapslap](https://clawhub.ai/user/kapslap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and reviewers use this skill to evaluate agent identity documents and system prompts for ethical grounding, symmetry issues, dependency risk, and actionable improvement opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auditing a system prompt or soul file may expose sensitive agent configuration content. <br>
Mitigation: Use local files or pasted text for sensitive prompts, confirm the exact document being audited, and avoid fetching remote URLs unless the source is trusted. <br>
Risk: A scored audit report can be mistaken for definitive ethical certification. <br>
Mitigation: Treat the report as diagnostic guidance and have a human reviewer decide which recommendations are appropriate for the agent's actual use case. <br>


## Reference(s): <br>
- [Soul Audit Rubric](references/rubric.md) <br>
- [Guardian v0.7 Constitution](https://delicatefire.com/soul_v7/CONSTITUTION.html) <br>
- [ClawHub skill page](https://clawhub.ai/kapslap/soul-audit) <br>
- [Publisher profile](https://clawhub.ai/user/kapslap) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with score table, strengths, gaps, symmetry violations, recommendations, and next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report quotes the audited document when identifying strengths and gaps.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
