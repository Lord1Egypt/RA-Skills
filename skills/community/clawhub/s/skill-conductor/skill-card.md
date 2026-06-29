## Description: <br>
Skill Conductor orchestrates the full skill-building pipeline from guidance through engineering and zipper stages, with gated loops for quality control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use Skill Conductor to take a new or existing skill through planning, implementation, lossless restructuring, and final audit. It is intended for end-to-end pipeline runs where failing gates should loop back to the responsible stage or stop honestly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a target skill, rerun audits, and overwrite stage artifacts during pipeline loops. <br>
Mitigation: Run it in a version-controlled or disposable working copy and review diffs before publishing. <br>
Risk: The workflow depends on trusted sibling skills, including skill-guidance, skill-engineer, skill-zipper, and vince-attacker. <br>
Mitigation: Install and pin trusted versions of the sibling skills before running the pipeline. <br>
Risk: The workflow may run local tests or harnesses as part of gate verification. <br>
Mitigation: Run it only in repositories where local test execution is acceptable and inspect unexpected commands before continuing. <br>


## Reference(s): <br>
- [Skill Conductor on ClawHub](https://clawhub.ai/vincentjiang06/skills/skill-conductor) <br>
- [SKILL.md](SKILL.md) <br>
- [Pipeline Gate Rules](rules/pipeline-loop.md) <br>
- [Final Acceptance Rules](rules/final-acceptance.md) <br>
- [Conductor Log Schema](assets/conductor-log.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json] <br>
**Output Format:** [Markdown guidance with shell commands and a JSON run log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes <target>/.skill-conductor/conductor-log.json and may update target skill files through sibling pipeline stages.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
