## Description: <br>
Find recurring OpenClaw jobs that may be wasting tokens before the waste compounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choosenobody](https://clawhub.ai/user/choosenobody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect recurring OpenClaw jobs for likely token waste, review evidence, and prepare safe manual verification before making changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit evidence may include private job names, logs, paths, delivery details, or operational context. <br>
Mitigation: Inspect metadata locally and redact secrets, private payloads, credentials, and identifying details before sharing examples externally. <br>
Risk: A recurring job flagged as waste may still be useful in its operating context. <br>
Mitigation: Use the generated manual verification prompt and review the evidence before editing, disabling, deleting, or rescheduling any job. <br>


## Reference(s): <br>
- [OpenClaw Waste Audit reference patterns](references/openclaw-waste-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with evidence summaries, ranked findings, inline shell commands, and a manual verification prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only guidance; recommendations require manual verification before changing jobs.] <br>

## Skill Version(s): <br>
1.8.12 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
