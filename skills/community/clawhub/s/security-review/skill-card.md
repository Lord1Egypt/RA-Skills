## Description: <br>
Runs a pre-installation security assessment for external packages, CLIs, libraries, browser extensions, and third-party integrations, producing a GO, NO-GO, or CONDITIONAL verdict. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mpbshhx](https://clawhub.ai/user/mpbshhx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to assess the legitimacy, vulnerability history, source behavior, data flows, permissions, and dependency risks of a third-party package or tool before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow includes a hardcoded review-log path and named approval wording. <br>
Mitigation: Change the log path and approval wording to match the target environment before use. <br>
Risk: Package review prompts can accidentally include secrets, private URLs, or sensitive workspace details. <br>
Mitigation: Redact secrets and sensitive identifiers before prompting, searching, or fetching external sources. <br>
Risk: The skill records review outcomes in logs and updates MEMORY.md, creating persistent side effects. <br>
Mitigation: Decide whether persistent logs and memory updates are acceptable, and limit stored content to non-sensitive verdict summaries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mpbshhx/security-review) <br>
- [Publisher profile](https://clawhub.ai/user/mpbshhx) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security review with a GO, NO-GO, or CONDITIONAL verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source review, current vulnerability checks, data-flow assessment, permission review, dependency review, confidence, top risks, and install conditions when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
