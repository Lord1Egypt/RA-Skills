## Description: <br>
Create a recoverable active-work brief for context-heavy coding, design, debugging, review, research, or handoff sessions, with resume, handoff, debug, review, design, and research policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkenny0](https://clawhub.ai/user/kkenny0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to capture recoverable active-work state for context-heavy coding, design, debugging, review, research, and handoff sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefs may include private decisions, command output, git diff summaries, or summarized code changes from the local workspace. <br>
Mitigation: Use only in workspaces where local project-state inspection is appropriate, and review .taku/context files before committing, syncing, or sharing them. <br>


## Reference(s): <br>
- [Taku Compact Brief](references/compact-brief.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown brief with structured YAML fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist briefs under .taku/context/ or return chat-only output when files cannot or should not be written.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
