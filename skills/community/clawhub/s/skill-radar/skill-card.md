## Description: <br>
Skill Radar scans an OpenClaw skill ecosystem to report skill usage, readiness, recommendations, and version status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeter226](https://clawhub.ai/user/freeter226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Skill Radar to audit installed skills, identify idle or missing capabilities, and check ClawHub version updates before changing their skill set. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive local OpenClaw history, memory, configuration, and installed skill contents. <br>
Mitigation: Run it only in workspaces where that local data may be inspected, and review generated reports before sharing them. <br>
Risk: The skill can run local commands and may execute another skill's Mem0 script while gathering usage evidence. <br>
Mitigation: Review the installed skill set first and avoid running the usage report in untrusted environments. <br>
Risk: The skill writes local cache files and queries ClawHub for search, recommendation, and version information. <br>
Mitigation: Treat cache files and network-backed recommendations as operational data, and clear local caches when reports should not persist. <br>
Risk: Reports may be incomplete or misleading when optional data sources or CLI dependencies are unavailable. <br>
Mitigation: Use reports as decision support rather than an authoritative inventory, and confirm important cleanup or update actions manually. <br>


## Reference(s): <br>
- [Skill Radar on ClawHub](https://clawhub.ai/freeter226/skill-radar) <br>
- [freeter226 ClawHub profile](https://clawhub.ai/user/freeter226) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports printed to standard output, optionally redirected to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports summarize installed skill usage, missing or ready status, recommendations, version checks, and full-report mode.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
