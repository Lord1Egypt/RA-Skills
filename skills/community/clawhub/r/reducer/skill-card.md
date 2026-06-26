## Description: <br>
Reducer helps agents guide users through generating reducer CAD drawings with the hosted JXT mechanical parts workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realsanyu](https://clawhub.ai/user/realsanyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and mechanical design practitioners use this skill to collect reducer parameters, run hosted calculations, review generated values, and create a no-login production sheet for CAD drawing generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reducer design parameters are sent to jixietools.com as part of the hosted CAD drawing workflow. <br>
Mitigation: Avoid confidential or proprietary designs unless the user understands the service's privacy and retention behavior. <br>
Risk: The workflow creates a no-login guest viewing link for production sheet status and results. <br>
Mitigation: Treat generated guest links as shareable access links and share them only with intended recipients. <br>
Risk: A production sheet is created from the calculated reducer parameters. <br>
Mitigation: Have the user confirm the displayed parameters before creating the production sheet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realsanyu/reducer) <br>
- [JXT mechanical tools API base](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides hosted API calls, parameter review, production sheet creation, status polling, and guest viewing link delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter declares 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
