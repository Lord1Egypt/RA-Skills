## Description: <br>
Automates a stock prediction workflow that extracts stock codes from images, checks and starts the local prediction environment, verifies and switches the model, runs batch prediction, and returns the result text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanhang89](https://clawhub.ai/user/guanhang89) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate local stock prediction runs from user-provided images containing stock codes and prediction parameters. The skill coordinates OCR-derived inputs, a local Kronos backend, model selection, batch prediction execution, and result return. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local PowerShell commands, start a backend service, switch a local model, and execute batch prediction scripts. <br>
Mitigation: Install and run it only in a trusted local Kronos environment, review commands before execution, and stop the backend when the prediction task is complete. <br>
Risk: The skill writes stock-code input files and reads prediction result files under hardcoded Windows paths. <br>
Mitigation: Review generated files for sensitive content, restrict filesystem access to the intended Kronos directories, and clean up stored input and result files after use. <br>
Risk: Prediction parameters are parsed from user prompts and could be malformed or outside the expected range. <br>
Mitigation: Use normal YYYY-MM-DD dates and integer sample counts, and validate parsed values before running the batch prediction command. <br>


## Reference(s): <br>
- [Stock Prediction on ClawHub](https://clawhub.ai/guanhang89/stock-prediction) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown or plain text with command execution status and prediction-result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes stock-code input files and reads result files under a hardcoded local Windows Kronos prediction path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
