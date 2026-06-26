## Description: <br>
Audit and fix all skills in the workspace for compliance with skill-creator requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1va7](https://clawhub.ai/user/1va7) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent-skill maintainers use this skill to find OpenClaw skill directories, audit them for skill-creator compliance, report issues, and repair non-compliant skill packaging or metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans broadly across the workspace and can make lasting file changes to skill directories. <br>
Mitigation: Run it first in audit or report-only mode, review exact paths and proposed changes, and explicitly approve deletions, renames, directory moves, or writes into skill workspaces. <br>
Risk: Compliance fixes can remove auxiliary files or change skill metadata in ways that affect packaging or discoverability. <br>
Mitigation: Review diffs before applying repairs and re-run the audit after changes to confirm the resulting skill remains intentional and compliant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1va7/skill-refiner) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenClaw skill-creator](https://github.com/openclaw/openclaw/tree/main/skills/skill-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown summaries, JSON audit results, shell commands, and file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect workspace paths and propose or apply changes to skill files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
