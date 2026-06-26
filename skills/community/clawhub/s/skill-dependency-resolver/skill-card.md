## Description: <br>
Skill Dependency Resolver scans OpenClaw skill requirements files, detects Python package version conflicts, and generates a merged requirements file with a conflict report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, skill authors, and system administrators use this skill to inspect multiple installed skills for requirements.txt conflicts and produce a single requirements file for installation planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured output file can be overwritten. <br>
Mitigation: Choose the output path deliberately and review or back up any existing requirements file before running the skill. <br>
Risk: A merged requirements file can select package versions that are unsuitable for a specific environment. <br>
Mitigation: Review the generated requirements file and test installation in an isolated environment before using it with pip in a shared or production setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/skill-dependency-resolver) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands] <br>
**Output Format:** [CLI output plus generated requirements.txt content and a structured conflict report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a merged requirements file to the configured output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
