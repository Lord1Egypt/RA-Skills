## Description: <br>
Guides users through generating transmission CAD drawings by collecting design inputs, calling jixietools.com APIs, reviewing calculated parameters, and creating guest production sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and engineers use this skill to generate transmission CAD production workflows by selecting a transmission product, entering design parameters one at a time, reviewing calculated ratios and strength values, and creating a guest production sheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transmission design inputs and calculation references are sent to jixietools.com and may be sensitive. <br>
Mitigation: Use only with data appropriate for that external service; avoid confidential or proprietary designs unless the service's handling and retention practices are trusted. <br>
Risk: Guest-accessible production sheet links can expose generated results to anyone with the link. <br>
Mitigation: Treat returned guest links as sensitive and share them only with intended recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liv09370/transmission) <br>
- [JixieTools API base](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese conversational guidance with Markdown tables and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Polls guest production sheet status every 5 seconds when monitoring progress.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
