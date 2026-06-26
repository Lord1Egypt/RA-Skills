## Description: <br>
Verifier helps agents evaluate claims, sources, screenshots, profiles, offers, and suspicious messages by scoring evidence quality, consistency, risk, missing evidence, confidence, and recommended next verification steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProjectSnowWork](https://clawhub.ai/user/ProjectSnowWork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Verifier to turn claims, suspicious messages, offers, screenshots, profiles, and sources into structured local cases. The skill supports review workflows that produce verdicts, confidence levels, risk notes, missing-evidence guidance, and next verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verifier stores user-entered claims, messages, profile details, offers, and screenshot-derived text in a local cases file. <br>
Mitigation: Avoid entering secrets or highly sensitive material unless local retention is acceptable, and clear local storage according to workspace policy when review is complete. <br>
Risk: Scores depend on the claim and evidence supplied to the skill; the scripts do not browse the web, inspect images directly, or fetch remote content. <br>
Mitigation: Provide source context, extracted screenshot text, and supporting or contradicting evidence before relying on a verdict. <br>


## Reference(s): <br>
- [Verifier Philosophy](references/philosophy.md) <br>
- [ClawHub Verifier release page](https://clawhub.ai/ProjectSnowWork/verifier) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with CLI examples and structured JSON scoring output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local filesystem storage for case records; no external packages are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
