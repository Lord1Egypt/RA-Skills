## Description: <br>
Updates a specific skill within a repository and triggers the automated publishing pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wells1137](https://clawhub.ai/user/wells1137) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to release a new version of a single skill by collecting the target skill, version, and changelog, then running the repository's release script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user-selected repository release script performs the actual publish action and may trigger an unintended skill release if inputs or script contents are wrong. <br>
Mitigation: Before running the skill, verify the repository path, skill name, version, changelog, and contents of scripts/release.sh. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wells1137/wells1137-skill-updater) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Text and shell command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for repository path, skill name, version, and changelog before running a release script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
