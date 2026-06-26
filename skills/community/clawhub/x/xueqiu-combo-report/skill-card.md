## Description: <br>
Xueqiu Combo Report guides agents through collecting Xueqiu self-selected combo holdings from a logged-in browser session, merging and patching batches, ranking stocks by combo ownership, and exporting JSON, Markdown, HTML, and PDF reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ning-kun](https://clawhub.ai/user/ning-kun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to turn Xueqiu self-selected combo holdings batches into a ranked stock summary and final report files. It is intended for authorized Xueqiu sessions and locally held holdings data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The collection workflow depends on a logged-in Xueqiu browser session and may access account-specific holdings data. <br>
Mitigation: Use only accounts and data you are authorized to access, and keep collection batches short and explicit. <br>
Risk: Exported holdings files can contain sensitive financial information. <br>
Mitigation: Store generated JSON, Markdown, HTML, and PDF files locally with appropriate access controls. <br>
Risk: Rendering untrusted JSON to PDF through Chrome or Chromium can expose the local environment to unsafe input. <br>
Mitigation: Render only trusted or reviewed JSON, or run the Chrome step in a trusted isolated environment. <br>


## Reference(s): <br>
- [Data formats](references/data-format.md) <br>
- [End-to-end workflow](references/end-to-end.md) <br>
- [ClawHub skill page](https://clawhub.ai/ning-kun/xueqiu-combo-report) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, text, markdown, configuration] <br>
**Output Format:** [Markdown guidance with inline shell and browser-side code snippets; generated workflow artifacts may include JSON, Markdown, HTML, and PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PDF export depends on local Chrome or Chromium availability.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
