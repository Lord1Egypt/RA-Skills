## Description: <br>
Summarize recent posts from followed Knowledge Planet circles into a daily digest prioritizing key updates using local tokens or browser relay for access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sealiu1997](https://clawhub.ai/user/sealiu1997) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to collect recent Knowledge Planet updates from followed circles, deduplicate them, and produce a scan-friendly digest that helps decide what to read first. It is intended for private membership content where authentication material stays local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live account cookies and session tokens for private Knowledge Planet content. <br>
Mitigation: Keep `state/` private and out of git, backups, screenshots, and support bundles; delete captured cookie files after setup. <br>
Risk: Under-scoped probe or custom API-base paths could send credentials outside the intended ZSXQ service. <br>
Mitigation: Do not use probe or custom API-base modes against non-ZSXQ URLs unless the code is changed to enforce a ZSXQ allowlist. <br>
Risk: Browser bootstrap can expose account state through the active browser profile. <br>
Mitigation: Use a dedicated browser profile where possible and treat the skill as an account-access tool before installation. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Runtime modes](references/runtime-modes.md) <br>
- [Auth bootstrap design](references/auth-bootstrap.md) <br>
- [Session token guide](references/session-token-guide.md) <br>
- [Output schema](references/output-schema.md) <br>
- [Browser workflow](references/browser-workflow.md) <br>
- [Browser recovery](references/browser-recovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown digest output with JSON intermediate files, local configuration, and explicit status guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Groups updates by circle, preserves original links when available, and uses bounded local cursor state for deduplication.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
