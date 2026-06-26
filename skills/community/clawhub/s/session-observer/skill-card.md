## Description: <br>
Observe OpenClaw session usage, token consumption, context pressure, and model/runtime state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qsczseasd](https://clawhub.ai/user/qsczseasd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to request concise session diagnostics, understand token and context pressure, and choose a practical next step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session diagnostics can expose private operational details such as model choice, token usage, context pressure, cache behavior, runtime mode, and usage or budget status. <br>
Mitigation: Return concise summaries only to the intended user, avoid dumping raw status cards unless requested, and omit or mark unavailable any fields not provided by the session status tool. <br>
Risk: Cost or usage conclusions can be misleading if the underlying status data does not include explicit cost numbers. <br>
Mitigation: Do not invent cost numbers; report only values shown by the tool and frame recommendations as operational next steps. <br>


## Reference(s): <br>
- [Session Observer Checklist](references/checklist.md) <br>
- [ClawHub Release Page](https://clawhub.ai/qsczseasd/session-observer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown status summary with Current state, What it means, and Recommended next step sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model, token, context, cache, usage, and runtime signals when available; unavailable fields are reported as unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
