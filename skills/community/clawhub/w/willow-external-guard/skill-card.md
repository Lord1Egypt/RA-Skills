## Description: <br>
Use when Willow is about to ingest, summarize, or act on external content; it wraps untrusted content in boundary markers and scans for prompt injection, role hijack, leak attacks, and approval-bypass attempts before KB writes or LLM passes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rudi193-cmd](https://clawhub.ai/user/rudi193-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to screen untrusted external content before Willow ingests, summarizes, or acts on it. It helps route clean, suspicious, and blocked content through wrap, confirm, or refuse decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner is a guardrail, not a complete security boundary for prompt-injection handling. <br>
Mitigation: Check scan results and exit codes before passing wrapped content to an LLM or knowledge-base ingest path, and separately block BLOCKED results. <br>
Risk: Guard events write local metadata logs for suspicious or blocked content. <br>
Mitigation: Confirm local guard-event metadata logging is acceptable in the workspace and avoid logging raw flagged content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rudi193-cmd/willow-external-guard) <br>
- [Publisher profile](https://clawhub.ai/user/rudi193-cmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and plain-text or JSON scanner results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 on Linux or Darwin; the scanner exits 0 for CLEAN, 1 for SUSPICIOUS, and 2 for BLOCKED.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
