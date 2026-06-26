## Description: <br>
Research RedNote/Xiaohongshu discussion signals for sentiment, reputation, updates, local recommendations, and post or media analysis using public-web mode by default with optional login-enhanced review when explicitly chosen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pippin1214](https://clawhub.ai/user/Pippin1214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and researchers use this skill to perform RedNote/Xiaohongshu-first community intelligence checks, including reputation scans, trend updates, local recommendation synthesis, account summaries, comment analysis, and multimodal post review. It helps separate inspectable evidence from rumor, snippet-only signals, and platform chatter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public-web RedNote coverage can be incomplete because indexed pages, snippets, account feeds, comments, and app-only media may be missing or stale. <br>
Mitigation: State the access mode used, label snippet-only or partial evidence, and ask for seed links, screenshots, copied titles, or login-enhanced review when fuller coverage is needed. <br>
Risk: Login-enhanced review exposes the agent to a user's active RedNote session and may reveal account-level or comment-level content beyond public-web results. <br>
Mitigation: Use login-enhanced mode only after explicit user choice, have the user complete login through the normal site flow, avoid passwords in chat, and keep navigation limited to the research request. <br>
Risk: Community chatter, repeated anecdotes, screenshots, OCR, subtitles, ASR, and clipped media can be mistaken for verified facts. <br>
Mitigation: Separate direct evidence from interpretation, assign credibility and risk scores, cross-check material claims with official or reputable sources, and keep unsupported allegations at rumor level. <br>


## Reference(s): <br>
- [RedNote Access Modes](references/access-modes.md) <br>
- [Login-Enhanced Workflow](references/login-enhanced-workflow.md) <br>
- [Minimal User Input Paths](references/minimal-user-input-paths.md) <br>
- [Account Summary Templates](references/account-summary-template.md) <br>
- [RedNote Structured Claim Log](references/claim-log-schema.md) <br>
- [RedNote Multimodal Capture Patterns](references/multimodal-capture.md) <br>
- [RedNote Community Intelligence Output Patterns](references/output-patterns.md) <br>
- [RedNote Public-Web Recovery Patterns](references/public-web-recovery.md) <br>
- [RedNote Community Intelligence Scoring Rubric](references/scoring-rubric.md) <br>
- [RedNote Community Intelligence Verification Patterns](references/verification-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Pippin1214/rednote-research) <br>
- [Publisher Profile](https://clawhub.ai/user/Pippin1214) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with evidence bullets, optional JSON claim logs, and optional shell command examples for bundled helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state whether public-web or login-enhanced mode was used and should distinguish direct evidence from snippet-only or user-provided material.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
