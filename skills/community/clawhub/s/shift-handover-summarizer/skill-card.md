## Description: <br>
Generate structured shift handover summaries from EHR records, highlighting critical events, vital sign changes, and pending tasks for incoming clinical staff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical staff and authorized healthcare operations teams use this skill to generate structured end-of-shift handover summaries from supplied EHR records, with patients prioritized by critical events, abnormal vitals, medication changes, procedures, and pending tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes EHR records that may contain protected health information. <br>
Mitigation: Use it only with authorized records, run it in a restricted working directory, and avoid writing summaries containing PHI to shared or unintended locations. <br>
Risk: Generated handover summaries may omit context or classify events imperfectly because event priority is based on supplied records, thresholds, and keywords. <br>
Mitigation: Require qualified clinical staff to manually verify all outputs before handover, treatment decisions, triage, or physician sign-off. <br>
Risk: Shift filtering can be incorrect when shift times omit timezone offsets. <br>
Mitigation: Provide explicit ISO 8601 timezone offsets for shift start and end times, and review the stated shift period before using the summary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/shift-handover-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON summary, plain-text handover narrative, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a JSON summary file when an output path is provided; otherwise prints JSON to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
