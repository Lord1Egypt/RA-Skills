## Description: <br>
Tvs Review guides agents through scoped code reviews, requiring explicit review boundaries and reporting correctness, security, regression, testing, maintainability, and architecture issues without providing fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inksnowhailong](https://clawhub.ai/user/inksnowhailong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when they want an agent to review a specified file, directory, diff, PR, commit range, or code snippet. It focuses on identifying evidenced issues and test gaps while avoiding repair instructions or code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a deliberately sharp review tone that may be inappropriate for teams expecting neutral feedback. <br>
Mitigation: Use it only where that review posture is desired, or select a more neutral review skill. <br>
Risk: A code review without a clear scope can produce broad or low-value findings. <br>
Mitigation: Provide an explicit file, directory, diff, PR, commit range, or code snippet before invoking the review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inksnowhailong/tvs-review) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown review report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the user to provide an explicit review scope before analysis; reports findings by severity and confidence.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
