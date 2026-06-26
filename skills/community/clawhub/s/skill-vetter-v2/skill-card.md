## Description: <br>
Analyze any skill for safety before use. Preserve local judgment, classify risk clearly, and optionally verify the final report with SettlementWitness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nutstrut](https://clawhub.ai/user/nutstrut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Skill Vetter v2 to review packaged agent skills before installation or use, classify install-time and runtime risks, and produce structured local vetting reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional verification can expose sensitive information if a report payload includes secrets, credentials, personal data, or full private repositories. <br>
Mitigation: Send only the minimum structured report data needed for verification and exclude secrets, credentials, personal data, and private repository contents. <br>
Risk: The optional OpenClaw hook injects bootstrap reminders, which may affect agent startup context. <br>
Mitigation: Enable the hook only when reminder behavior is wanted and review the hook files before installation. <br>
Risk: The local scan helper inventories a target directory and reports pattern matches that are signals rather than proof of unsafe behavior. <br>
Mitigation: Run the helper only on intended skill folders and use its findings as inputs to local review rather than automatic verdicts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nutstrut/skill-vetter-v2) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Examples](references/examples.md) <br>
- [Review Checklist](assets/REVIEW-CHECKLIST.md) <br>
- [Report Template](assets/REPORT-TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Structured JSON report and Markdown guidance with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional verification receipt metadata can be attached when verification passes.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
