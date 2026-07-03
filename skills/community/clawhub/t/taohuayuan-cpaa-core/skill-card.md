## Description: <br>
Scans embodied AI agent configuration JSON to verify S2-DID identity format, CD-U6A domain mapping, and locked control settings against CPAA safety checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators working with embodied AI agents use this skill to check a JSON configuration before deployment or startup. It reports whether identity, domain address, temperature, and hardware lock settings pass the stated CPAA criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using this skill as an automatic hardware control could trigger unsafe actuator power changes. <br>
Mitigation: Treat the skill as a configuration checker unless a hardware-specific safe-stop procedure, operator controls, and validated interlocks are added. <br>
Risk: A pass result may be mistaken for full physical safety certification. <br>
Mitigation: Use the returned report as one input to a broader safety review, and validate all robot, motor, or actuator behavior outside the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/taohuayuan-cpaa-core) <br>
- [artifact/skill.md](artifact/skill.md) <br>
- [artifact/changelog.md](artifact/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON compliance report with pass/fail fields, a numeric score, and a final status string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes one JSON agent configuration payload and returns local validation results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version, artifact/skill.json, changelog released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
