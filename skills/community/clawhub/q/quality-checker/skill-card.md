## Description: <br>
Checks chapter drafts for word count, paragraph length, dialogue ratio, punctuation overuse, repeated words, and produces a scored quality report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and publishing teams use this skill to evaluate Markdown or text chapter drafts before publication, quantify quality signals, and generate improvement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependencies are unpinned. <br>
Mitigation: Install the skill in a virtual environment and pin rich and PyYAML before operational use. <br>
Risk: The checker reads local chapter/config files and can write a report to a user-selected path. <br>
Mitigation: Run it only on files you intend to inspect and choose the optional output path deliberately. <br>
Risk: Quality scores are heuristic and may not match project-specific editorial standards. <br>
Mitigation: Use the report as review guidance and adjust the configuration thresholds for the project. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text plus optional Markdown report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local Markdown or text chapter files and can create parent directories for the optional report path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
