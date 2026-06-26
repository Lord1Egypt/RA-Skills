## Description: <br>
Load per-job runtime instructions from Google Sheets, cache them locally, and reconcile cron job enablement flags safely for OpenClaw operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage OpenClaw job instructions from a Google Sheet, maintain local runtime instruction cache files, and preview or apply cron job enablement changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Sheet editors can change runtime instructions and cron enablement, causing persistent local changes. <br>
Mitigation: Limit sheet editing to trusted operators and periodically audit or clear cached runtime instruction files. <br>
Risk: Broad credentials or personal gcloud credentials can expose more access than the skill needs. <br>
Mitigation: Use a dedicated read-only Google service account scoped to the intended spreadsheet. <br>
Risk: Applying reconciliation can disable jobs that are missing from the sheet. <br>
Mitigation: Run the reconciler without --apply first and inspect all proposed disables before applying changes. <br>


## Reference(s): <br>
- [Google Sheet Runtime Instructions Schema](references/google-sheet-instructions-schema.md) <br>
- [ClawHub release page](https://clawhub.ai/danielsinewe/runtime-instructions-control-plane) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated local JSON/Markdown runtime instruction files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus Google Sheets spreadsheet access through a read-only service account or gcloud token fallback.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
