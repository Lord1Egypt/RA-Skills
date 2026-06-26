## Description: <br>
Toggles the Sumo task assignment method among sessions_spawn, clawteam, and SumoSubAgent through the /Sumo_Assign_Tasks command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumo0221](https://clawhub.ai/user/sumo0221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to inspect or change how Sumo delegates subagent work among supported assignment methods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes settings to a hardcoded Windows user path, which may target the wrong location on non-Windows systems or shared machines. <br>
Mitigation: Review or adjust the config path before running so the settings file is written to the intended OpenClaw workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sumo0221/sumo-assign-tasks) <br>
- [Publisher profile](https://clawhub.ai/user/sumo0221) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text status messages and a local JSON configuration file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes assign_method.json to a hardcoded Windows OpenClaw workspace memory path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
