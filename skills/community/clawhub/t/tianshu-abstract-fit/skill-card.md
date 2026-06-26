## Description: <br>
Checks abstract length and organizes draft sentences into rough background, methods, results, and conclusion Markdown slots for human revision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and academic writers use this skill to check a draft abstract against a rough character limit and arrange it into common academic abstract sections before manual editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The section split is heuristic and may produce incomplete or misleading academic structure. <br>
Mitigation: Review and rewrite each generated section before using it in coursework, thesis, or report submissions. <br>
Risk: The file input mode reads the local file path selected by the user. <br>
Mitigation: Run it only on abstract text or draft files intentionally chosen for this task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshengli0421/tianshu-abstract-fit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with a character count and four quoted section blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Heuristic sentence-order segmentation; the draft should be reviewed and rewritten before academic submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
