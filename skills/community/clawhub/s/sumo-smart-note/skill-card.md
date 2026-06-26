## Description: <br>
Smart note-taking skill for 蘇茉家族. When master says "記下來" (record this), automatically save development notes to both workspace AND SumoNoteBook raw/shared. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumo0221](https://clawhub.ai/user/sumo0221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to capture development notes on request and sync them as Markdown notes to workspace memory and SumoNoteBook shared storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested notes may contain credentials, private customer data, proprietary details, or other sensitive material and are saved to local and shared folders. <br>
Mitigation: Avoid recording sensitive material unless the SumoNoteBook shared folder is appropriate for that data. <br>
Risk: The skill writes Markdown files to the OpenClaw workspace memory folder and a hard-coded SumoNoteBook raw/shared path. <br>
Mitigation: Verify OPENCLAW_WORKSPACE and the SumoNoteBook path before first use, and install only when this local note-writing behavior is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sumo0221/sumo-smart-note) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown note files with console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local Markdown files to workspace memory and SumoNoteBook raw/shared paths; workspace appends are deduplicated by content hash.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
