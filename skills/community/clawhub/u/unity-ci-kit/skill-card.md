## Description: <br>
Unity CI pipeline toolkit that provides a Python CLI and Unity Editor runner for automated Unity batchmode builds, compile checks, and structured error parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jssj07](https://clawhub.ai/user/jssj07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up reusable CI for Unity projects, run batchmode compilation and builds, and inspect generated build status for agent-assisted repair loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editable CI configuration values can affect Unity command execution, especially on Windows where the scanner reports shell execution risk. <br>
Mitigation: Install only for trusted Unity projects; review ci_config.json values before build or compile, especially unity_path, execute_method, log_file, and result_file. <br>
Risk: Running the skill in privileged CI can expose secrets or sensitive project files if command invocation is not hardened. <br>
Mitigation: Run with least-privilege CI permissions and avoid privileged environments with secrets unless command execution is hardened to argument lists with shell disabled. <br>


## Reference(s): <br>
- [Unity CI Kit setup guide](references/setup_guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/jssj07/skills/unity-ci-kit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python and C# code references, JSON configuration, and CI result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update ci_config.json, ci_output.log, and ci_result.json in the Unity project workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
