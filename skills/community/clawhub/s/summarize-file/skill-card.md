## Description: <br>
Reads text files from workspace/paths and generates concise summaries. Handles logs, reports, CSVs, multi-line content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MuhammadMuazzain](https://clawhub.ai/user/MuhammadMuazzain) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and other workspace users use this skill to read local text files such as logs, reports, notes, and CSVs and return concise summaries of the important points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read outside the intended workspace because path resolution is not constrained to the workspace root. <br>
Mitigation: Constrain file resolution to the workspace root and review the skill before installing it in sensitive workspaces. <br>
Risk: Broad triggers may cause unintended file-summary behavior. <br>
Mitigation: Narrow triggers to explicit file-summary requests before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MuhammadMuazzain/summarize-file) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns concise prose and does not create a file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
