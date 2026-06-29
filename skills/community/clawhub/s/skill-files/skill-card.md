## Description: <br>
Review UI code for Web Interface Guidelines compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[divyamprusty](https://clawhub.ai/user/divyamprusty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and reviewers use this skill to check UI files for Web Interface Guidelines compliance and receive terse file:line findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review depends on live guideline content from an external raw GitHub URL, so results can change if that source changes. <br>
Mitigation: Check the fetched guideline source when results are surprising and rerun reviews after confirming the source is expected. <br>
Risk: The skill reads user-specified UI files during review. <br>
Mitigation: Run it only on code files you are comfortable letting the agent inspect, and scope file patterns to the intended review area. <br>


## Reference(s): <br>
- [Web Interface Guidelines source](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis, Guidance] <br>
**Output Format:** [Plain text findings in file:line format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings depend on the current external Web Interface Guidelines source.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
