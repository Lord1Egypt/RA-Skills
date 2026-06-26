## Description: <br>
Guides Chinese-speaking users through generating steering-gear CAD drawings by collecting design parameters, calling the JXT mechanical parts workflow, and tracking guest production-sheet results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realsanyu](https://clawhub.ai/user/realsanyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and mechanical-design agents use this skill to collect steering-gear parameters, review calculated values, create a guest production sheet, and monitor generated CAD output from jixietools.com. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends steering-gear design parameters to jixietools.com. <br>
Mitigation: Proceed only when sharing those design parameters with jixietools.com is acceptable. <br>
Risk: Guest production-sheet URLs and codes can expose production progress and output links to anyone who has them. <br>
Mitigation: Treat guest codes and sheet URLs as private links and avoid sharing them publicly. <br>
Risk: Production-sheet creation depends on the user's reviewed calculated parameters. <br>
Mitigation: Review calculated input, debug, coefficient, and output parameters before creating the production sheet. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/realsanyu/steering-gear) <br>
- [JXT mechanical parts API](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Chinese Markdown with tables and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user prompts, parameter review tables, API request commands, guest production-sheet links, and status updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
