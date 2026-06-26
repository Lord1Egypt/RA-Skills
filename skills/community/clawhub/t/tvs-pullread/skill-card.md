## Description: <br>
Analyzes Git remote changes and local differences, summarizes the business or functional impact, explains implementation details on request, and asks whether to merge or handle conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inksnowhailong](https://clawhub.ai/user/inksnowhailong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand incoming Git changes at the business and functionality level before deciding whether to pull, merge, or inspect conflict risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact repository remotes while analyzing Git changes. <br>
Mitigation: Use it in repositories with trusted remotes. <br>
Risk: Pull, merge, or conflict-resolution recommendations can affect repository state if approved. <br>
Mitigation: Review any proposed pull, merge, or conflict resolution before approving changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inksnowhailong/tvs-pullread) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise summaries with risk levels, testing focus, conflict warnings, and optional Git command suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
