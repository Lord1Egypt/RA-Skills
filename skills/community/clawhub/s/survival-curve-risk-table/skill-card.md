## Description: <br>
Analyze data with `survival-curve-risk-table` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and clinical research teams use this skill to generate number-at-risk tables aligned with Kaplan-Meier survival curves for review-ready clinical oncology figures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can load Python pickle files as input data, and malicious pickle files can execute code when read. <br>
Mitigation: Install and run the skill only in an isolated environment, avoid .pkl and .pickle inputs unless they come from a fully trusted source, and prefer CSV, Excel, or SAS input files. <br>
Risk: Dependencies are declared without pinned versions, which can make runtime behavior and security posture vary across installations. <br>
Mitigation: Pin and review dependency versions before broad use, then run a non-destructive smoke check such as `python -m py_compile scripts/main.py` before processing user data. <br>
Risk: The dependency list includes `pil`, which the security guidance says should be removed. <br>
Mitigation: Remove `pil`, keep the maintained Pillow dependency if image processing is needed, and re-scan the release before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/survival-curve-risk-table) <br>
- [Runtime checklist](references/runtime_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The packaged workflow can create PNG, JPEG, PDF, SVG, PowerPoint-compatible image outputs, and CSV risk-table data when executed with validated inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
