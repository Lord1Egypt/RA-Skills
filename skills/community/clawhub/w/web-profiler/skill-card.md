## Description: <br>
Web Profiler is a local command-line tool for recording, reviewing, searching, and exporting web profiling notes and history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to keep local notes about web request profiling runs, compare results, review recent activity, and export profiling history for reports or dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profiling notes, private URLs, credentials, request bodies, or incident details may be stored locally and later exported. <br>
Mitigation: Avoid entering secrets or sensitive production details unless local storage under ~/.local/share/web-profiler and later export are acceptable. <br>
Risk: The profiler wording may imply deeper framework instrumentation than the artifact provides. <br>
Mitigation: Treat the skill as a local profiling notes and history tool, and verify any performance conclusions against authoritative application telemetry. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Plain text CLI output with optional JSON, CSV, or TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores command logs and exported data under ~/.local/share/web-profiler.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
