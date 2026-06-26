## Description: <br>
Guides a Chinese-language workflow for creating and monitoring guest CAD production sheets for a styrene distillation section through the JXT mechanical parts platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realsanyu](https://clawhub.ai/user/realsanyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect design parameters in Chinese, call jixietools.com endpoints, review calculated values, create a guest production sheet, and monitor drawing generation progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the advertised styrene-distillation CAD purpose does not match the mechanical parts API workflow the skill runs on an external site. <br>
Mitigation: Install only when the intended use is guest mechanical CAD production sheet creation through jixietools.com, and verify the selected product category and examples before relying on outputs. <br>
Risk: The skill instructs an agent to send user-provided design parameters to an external service and to create guest production sheets without authentication. <br>
Mitigation: Get user confirmation before remote API calls, avoid sending sensitive or proprietary parameters unless approved, and review returned links and files before purchase or downstream use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realsanyu/styrene) <br>
- [JixieTools API base](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown with tables and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser links to guest production sheet status and generated output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
