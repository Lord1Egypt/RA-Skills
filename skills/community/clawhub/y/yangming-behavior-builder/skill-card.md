## Description: <br>
Yangming Behavior Builder researches a named person's observable behavior, execution patterns, and outcomes, then generates a reusable behavior-perspective skill with friction diagnosis guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingsunzhang2026-oss](https://clawhub.ai/user/kingsunzhang2026-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to create behavior-focused skills for public figures or user-provided personas, using structured research, outcome validation, and gap diagnosis. It is intended for behavior analysis, execution coaching, and reusable skill generation rather than factual identity verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill stores sensitive behavioral self-reports in plaintext logs. <br>
Mitigation: Make logging opt-in or disabled by default, avoid entering sensitive personal or financial details, and define retention and deletion rules for generated logs. <br>
Risk: The security summary flags broad persona activation with limited user control. <br>
Mitigation: Use explicit invocation phrases, clearly label persona output as simulated, and keep users in control of when behavior-perspective generation or diagnosis is active. <br>
Risk: Generated behavior guidance can be misleading if source evidence is thin, contradictory, or overgeneralized. <br>
Mitigation: Require source quality review, preserve uncertainty and contradictions, and review generated skills before use or deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kingsunzhang2026-oss/yangming-behavior-builder) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Friction Diagnosis Script](artifact/scripts/friction_diagnosis.py) <br>
- [Execution Log Template](artifact/logs/execution_log.md) <br>
- [Andrew Ng Example Skill](artifact/references/andrew-ng-behavior/SKILL.md) <br>
- [Andrej Karpathy Example Skill](artifact/references/karpathy-behavior/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown skill files, Python scripts, shell commands, structured research notes, and diagnostic reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create skill directories containing research archives, generated SKILL.md files, Python diagnosis scripts, and plaintext usage logs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
