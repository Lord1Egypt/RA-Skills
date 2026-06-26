## Description: <br>
Automated code review assistant that analyzes code changes, pull requests, commits, diffs, and files for quality issues, best-practice gaps, security concerns, and style violations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review source files, staged changes, commits, and diffs before merging or shipping code. It produces issue summaries and actionable suggestions that can support local checks, pre-commit workflows, and CI reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence notes that some actions can affect real repositories or ClawHub accounts. <br>
Mitigation: Install only if the publisher is trusted, review commands before running them, and use documented opt-outs or confirmation steps when tighter control is needed. <br>
Risk: Automated review findings may be incomplete, noisy, or incorrect. <br>
Mitigation: Treat reports as advisory and have a developer review findings before changing code, blocking a build, or publishing feedback. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/michealxie001/xie-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports or JSON reports, with optional shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include summary counts, per-file issues, severity labels, rule categories, line references, snippets, and suggested fixes when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
