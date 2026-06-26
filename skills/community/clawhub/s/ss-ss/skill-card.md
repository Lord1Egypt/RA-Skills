## Description: <br>
Analyzes a given URL and automatically generates comprehensive functional, UI, and boundary test cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kushanlk](https://clawhub.ai/user/kushanlk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to turn a target URL into a Markdown test plan covering functional, UI, and boundary scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may not work as described because the required DOM analysis script is empty in this version. <br>
Mitigation: Only install this version with that limitation understood, and review any future analyzer implementation before running it against URLs. <br>
Risk: Future DOM analysis may open user-provided URLs through local browser automation. <br>
Mitigation: Run the skill only against URLs you are comfortable opening locally and review analyzer behavior before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kushanlk/ss-ss) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kushanlk) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown test plan with steps to reproduce, expected results, and edge cases.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a URL input. The release security summary says the required DOM analysis script is empty in this version.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
