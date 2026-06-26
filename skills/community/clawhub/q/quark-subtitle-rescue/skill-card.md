## Description: <br>
Bulk add subtitles to Quark movie folders with high success and low wrong-match risk, using staged retries, multi-provider fallback, rollback safety, and completion reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangqi00987](https://clawhub.ai/user/tangqi00987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to recover or complete bulk subtitle uploads across Quark movie folders, especially after interrupted runs, failed folders, or provider-specific misses. It guides staged batch execution, strict retries, fallback providers, spot checks, rollback decisions, and final progress reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a Quark session cookie, which can expose account access if copied, logged, or stored with broad permissions. <br>
Mitigation: Protect the cookie file with restrictive permissions and avoid pasting or logging the cookie during setup, execution, and troubleshooting. <br>
Risk: External batch scripts can modify many cloud folders, including upload, rollback, or delete actions. <br>
Mitigation: Inspect and trust the separate quark_subtitle_tool installation first, use a narrow target folder, test on a small batch, and require explicit confirmation before upload, rollback, or delete actions. <br>
Risk: Batch subtitle matching can create false success if many files receive the same or wrong subtitle content. <br>
Mitigation: Pause on mismatch signals, run hash-based and content spot checks, and roll back bad batches before continuing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangqi00987/quark-subtitle-rescue) <br>
- [Workflow Reference](artifact/references/workflow.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Text] <br>
**Output Format:** [Markdown with inline bash commands and checklist-style operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize JSON progress reports produced by the external Quark subtitle tooling.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
