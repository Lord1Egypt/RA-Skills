## Description: <br>
Provides AI agents with web service health monitoring and quality assurance workflows for HTTP checks, response analysis, compliance validation, SSL certificate monitoring, API endpoint verification, and HTML reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guo5404](https://clawhub.ai/user/guo5404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, SREs, and authorized security professionals use this skill to monitor owned or explicitly authorized web services, validate response quality and compliance, check SSL status, verify APIs, and prepare health reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server metadata identifies the release as security-test-suite while the artifact describes web-health-suite, creating ambiguity about the intended package behavior. <br>
Mitigation: Confirm the intended release identity and scope before installing or relying on the skill. <br>
Risk: The artifact names Python scripts for monitoring, compliance checks, SSL monitoring, endpoint verification, and report generation, but the server security summary flags missing scripts. <br>
Mitigation: Verify the referenced scripts are present, reviewed, and expected before running any commands. <br>
Risk: Web monitoring or endpoint verification can affect systems outside the user's authority if pointed at unauthorized targets. <br>
Mitigation: Use only owned systems or targets with explicit written authorization, documented scope, agreed time windows, and rate limits. <br>
Risk: Default API verification methods may include state-changing requests such as POST, PUT, or DELETE. <br>
Mitigation: Restrict API verification to read-only methods unless testing in a controlled environment with explicit approval. <br>
Risk: Authenticated checks can expose sensitive production cookies or tokens. <br>
Mitigation: Avoid production session cookies and use least-privilege test credentials where authenticated checks are required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and references to JSON and HTML report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected outputs depend on external scripts named by the artifact; server security evidence says those scripts should be verified before use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
