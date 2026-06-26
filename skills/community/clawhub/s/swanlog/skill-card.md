## Description: <br>
Pulls a SwanLab cloud experiment's metrics, config, metadata, requirements, and run information into a local directory, then summarizes what was fetched. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonwei1002](https://clawhub.ai/user/jasonwei1002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and machine learning engineers use this skill to inspect, sync, archive, diff, or analyze SwanLab experiment runs from a local machine without signing into the training host. It fetches scalar metrics and run profile files, then guides the agent to report a concise Markdown brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's existing SwanLab login to fetch experiment data that may include sensitive metrics, configuration, metadata, or requirements. <br>
Mitigation: Install and run it only when that access is intended, and review the exported files before sharing or syncing the output directory. <br>
Risk: Experiment dumps are written to a local directory that may be accidentally placed in a shared or synced location. <br>
Mitigation: Choose an output path appropriate for the data sensitivity and avoid shared folders unless the run contents are safe to disclose. <br>


## Reference(s): <br>
- [SwanLab](https://swanlab.cn) <br>
- [ClawHub swanlog release](https://clawhub.ai/jasonwei1002/swanlog) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown summary with local files including CSV, YAML, JSON, and text artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads from SwanLab using the user's existing local login and writes experiment data to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
