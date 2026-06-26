## Description: <br>
Reads Tencent Docs spreadsheets through browser automation and returns selected sheet content as tab-separated text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cm-wenge](https://clawhub.ai/user/cm-wenge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to read accessible Tencent Docs spreadsheet tabs for data extraction, weekly report checks, summaries, and monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation copies Tencent Docs spreadsheet content through the clipboard, which can expose sensitive sheet data if used on documents the user is not authorized to read. <br>
Mitigation: Use the skill only on spreadsheets the user is authorized to access, and run it only where clipboard-based browser automation is approved. <br>
Risk: The packaged weekly-report helper can send personnel status names to an external webhook when that workflow is intentionally configured. <br>
Mitigation: Avoid running scripts/check_weekly_report.py or setting WECOM_WEBHOOK_URL unless that reporting workflow and destination are approved. <br>


## Reference(s): <br>
- [Tencent Docs Reader ClawHub page](https://clawhub.ai/cm-wenge/tencent-docs-reader) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands] <br>
**Output Format:** [Tab-separated plain text, optionally saved to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tencent Docs spreadsheet the user is authorized to read and a running agent-browser daemon.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
