## Description: <br>
WAF Rule Validator helps agents guide testing and validation of WAF, API gateway, and IPS security rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realguoxiufeng](https://clawhub.ai/user/realguoxiufeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to plan and run authorized WAF validation against web application firewalls, API gateways, and IPS deployments. It supports workflows for protocol selection, test-case configuration, scanning commands, and report review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports generating WAF test traffic that may be disruptive or unauthorized if aimed at systems without permission. <br>
Mitigation: Run scans only against systems you own or are explicitly authorized to test, preferably in a controlled environment. <br>
Risk: Incorrect target URLs or high concurrency can send validation traffic to the wrong service or create avoidable load. <br>
Mitigation: Verify target, protocol, and concurrency settings before execution. <br>
Risk: Generated reports may contain security findings or sensitive target details. <br>
Mitigation: Keep reports local unless intentionally sharing them with authorized recipients. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe generated local reports in JSON, HTML, PDF, or DOCX when those formats are selected by the underlying tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
