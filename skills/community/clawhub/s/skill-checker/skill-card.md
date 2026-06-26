## Description: <br>
Audits a target SKILL.md against the Agent Skills specification and generates a Chinese HTML report for compliance review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oahc09](https://clawhub.ai/user/oahc09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to check whether a SKILL.md file or skill directory follows the Agent Skills specification, then review severe and warning findings in a generated HTML report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the local checker on the wrong path may inspect unintended SKILL.md content. <br>
Mitigation: Use explicit target paths and confirm the resolved SKILL.md before relying on the report. <br>
Risk: Generated HTML reports may expose skill contents or audit findings if written to shared locations. <br>
Mitigation: Write reports to an intended local path and avoid shared directories when findings or skill contents are sensitive. <br>


## Reference(s): <br>
- [Skill Checker Specification Checklist](references/specification-checklist.md) <br>
- [ClawHub Skill Checker Release Page](https://clawhub.ai/oahc09/skill-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [HTML report plus concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use --fail-on-audit when a CI-style failure exit code is required.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
