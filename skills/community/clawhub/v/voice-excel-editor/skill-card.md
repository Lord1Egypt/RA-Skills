## Description: <br>
Converts Chinese voice instructions and an Excel workbook into structured worksheet edits, applies supported changes, and returns the modified workbook with execution logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XinHao-96](https://clawhub.ai/user/XinHao-96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to turn Chinese spoken Excel editing requests into structured plans, then apply supported formatting, data entry, calculation, and worksheet-structure changes to a workbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio instructions are sent to SenseAudio and transcripts or logs may be retained locally. <br>
Mitigation: Use the skill only with audio the user is permitted to process, and review or remove generated transcript and log files when they contain sensitive information. <br>
Risk: Workbook-changing actions are executed from transcribed voice instructions and may be wrong if the transcript or operation plan is inaccurate. <br>
Mitigation: Review operation_plan.json before execution and keep the original workbook until the modified output has been verified. <br>
Risk: The script can automatically install unpinned Python packages when dependencies are missing. <br>
Mitigation: Run the skill in an isolated virtual environment and preinstall or pin requests and openpyxl before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/XinHao-96/voice-excel-editor) <br>
- [Operation schema](references/operation_schema.md) <br>
- [Planning prompt](references/planning_prompt.md) <br>
- [SenseAudio API endpoint](https://api.senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files, JSON] <br>
**Output Format:** [Markdown status text with file references, JSON execution artifacts, transcripts, logs, and a modified Excel workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SENSEAUDIO_API_KEY; produces separate output files rather than overwriting the source workbook by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
