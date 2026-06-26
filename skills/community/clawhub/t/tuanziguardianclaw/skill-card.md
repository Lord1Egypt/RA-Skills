## Description: <br>
TuanziGuardianClaw provides advisory security-policy guidance for reviewing skill actions, protecting secrets, identifying data exfiltration risks, and prompting for user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sawyerzm](https://clawhub.ai/user/sawyerzm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill as an advisory policy layer for reviewing requested actions by other skills and applying conservative responses to secret access, network use, and data export attempts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents itself as an always-on security kernel, but the server security summary identifies it as prompt-only and not a real sandbox or enforcement layer. <br>
Mitigation: Use it as advisory guidance only; rely on platform permissions, sandboxing, and human review for actual enforcement. <br>
Risk: Its blocking, override, and audit-log behavior may interfere with requested work or record sensitive file paths and attempted actions. <br>
Mitigation: Review the skill before allowing it to override other skills, block work, or create audit logs; avoid storing secrets or unnecessary sensitive details in logs. <br>


## Reference(s): <br>
- [Project homepage](https://claw.mytuanzi.com) <br>
- [ClawHub skill page](https://clawhub.ai/sawyerzm/tuanziguardianclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown policy guidance and decision prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce block, warning, confirmation, or audit-log style guidance; it does not provide platform-enforced sandboxing by itself.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
