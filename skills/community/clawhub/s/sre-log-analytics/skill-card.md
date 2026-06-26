## Description: <br>
Analyzes system and application logs over a specified time range, classifies reliability issues using SRE principles, scores system health, and produces improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roryyu](https://clawhub.ai/user/roryyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations engineers use this skill to inspect selected logs, summarize system behavior, identify repeated exceptions, and prepare a structured reliability report with short-, mid-, and long-term recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive operational logs, including secrets, personal data, or privileged system details supplied by the user. <br>
Mitigation: Provide only explicit log paths and time ranges, redact sensitive values where possible, and review any saved or shared report before it leaves the conversation. <br>
Risk: Reliability findings and suggested remediation may be incomplete or misleading if the provided logs are partial, stale, or missing surrounding operational context. <br>
Mitigation: Review findings against monitoring data, deployment history, and incident context before taking production action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roryyu/sre-log-analytics) <br>
- [Google SRE Core Principles](references/sre-principles.md) <br>
- [System Log Analysis Report Template](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with structured findings and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include health scores, exception summaries, sample log excerpts, and short-, mid-, and long-term recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
