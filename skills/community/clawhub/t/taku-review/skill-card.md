## Description: <br>
Use after implementation is complete to analyze diffs for security issues, bugs, code quality, scope drift, and missing verification before shipping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkenny0](https://clawhub.ai/user/kkenny0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill as a delivery gate after implementation work to inspect the current diff, identify blocking defects or security issues, and summarize residual concerns before merge or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect repository diffs and may run local git or verification commands. <br>
Mitigation: Use it in version-controlled repositories, inspect command output and edits, and ask for report-only review when automatic fixes are not desired. <br>
Risk: Review findings can be incorrect or incomplete when intent, test output, or repository context is missing. <br>
Mitigation: Provide the approved requirements and visible verification evidence, then treat the report as review input rather than a replacement for human judgment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kkenny0/taku-review) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with HARD STOPS, CONCERNS, and SUMMARY sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make small local code fixes when the correct change is clear and locally verifiable; does not commit, push, or open pull requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
