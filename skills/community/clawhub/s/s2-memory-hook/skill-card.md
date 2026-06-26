## Description: <br>
Automatically scans local chat logs, chunks new entries, and appends them into Space2-OS hippocampus memory for agent personality evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate ingestion of local chat logs into a Space2-OS memory buffer. It is intended for environments where persistent agent memory is desired and the watched log directory is intentionally curated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to read local chat logs and copy them into persistent agent memory. <br>
Mitigation: Use a dedicated watched log folder and inspect hippocampus_logs.json before and after runs. <br>
Risk: Sensitive chats, secrets, or proprietary material in the watched folder may be persisted into agent memory. <br>
Mitigation: Keep sensitive material out of openclaw_logs and review the target directory before enabling scheduled or heartbeat execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-memory-hook) <br>
- [Space2.world homepage](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, files] <br>
**Output Format:** [Local JSON files and console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends chunked memory entries to s2_consciousness_data/hippocampus_logs.json and maintains s2_hook_cursor.json for delta tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
