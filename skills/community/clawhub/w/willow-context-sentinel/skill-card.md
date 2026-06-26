## Description: <br>
Checks Willow/OpenClaw session context state on Linux and reports whether the agent should continue, compact, hand off, or pause for Postgres recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rudi193-cmd](https://clawhub.ai/user/rudi193-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents operating Willow/OpenClaw sessions use this skill as a heartbeat check before large tasks, after transitions, or when context pressure is suspected. It produces a simple routing status so the session can continue, compact, hand off, or stop for infrastructure recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Willow session metadata files and runs a bundled shell script. <br>
Mitigation: Install only if that local read access is acceptable, and review the script before use in managed environments. <br>
Risk: The published metadata declares bash but the script also invokes python3. <br>
Mitigation: Confirm python3 is available on target Linux hosts before relying on the sentinel in heartbeat automation. <br>
Risk: Missing or unparsable state files cause the script to default to STATUS_OK. <br>
Mitigation: Treat warnings on stderr as operational signals and verify Willow state file health when expected context or Postgres data is absent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rudi193-cmd/willow-context-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain-text status output with Markdown operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Status values are STATUS_OK, COMPACT_NOW, HANDOFF_NOW, and POSTGRES_DOWN.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
