## Description: <br>
WiseDiag-Checkup uploads PDF checkup reports or local report files to WiseDiag for AI-powered health interpretation, including abnormal item detection, clinical explanations, lifestyle assessment, and personalized recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wisediag](https://clawhub.ai/user/wisediag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit checkup reports by local file upload or public PDF URL, poll WiseDiag's cloud analysis workflow, and save the finished health interpretation as a Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkup reports, questionnaire details, and member-profile identifiers may contain sensitive health information and are sent to WiseDiag's cloud service. <br>
Mitigation: Use the skill only when WiseDiag's privacy and retention practices are acceptable, and avoid highly sensitive documents when an offline workflow is required. <br>
Risk: Saved Markdown reports may contain private medical information on the local filesystem. <br>
Mitigation: Save reports to a private output directory with appropriate access controls. <br>
Risk: The required WiseDiag API key is sensitive credential material. <br>
Mitigation: Store the API key in the WISEDIAG_API_KEY environment variable and avoid pasting it into prompts, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wisediag/wiseanalyze) <br>
- [WiseDiag API key console](https://console.wisediag.com/apiKeyManage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports plus command-line status fields such as TASK_ID, STATUS, PROGRESS, and REPORT_PATH.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WISEDIAG_API_KEY and sends report files or URLs to WiseDiag's cloud service; saved reports are written as local .md files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
