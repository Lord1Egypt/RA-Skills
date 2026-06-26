## Description: <br>
Comprehensive website audit combining uptime checks, TLS certificate inspection, and security headers grading in one command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and security reviewers use this skill to audit websites they own or are authorized to test for uptime, HTTPS certificate status, response time, and common security header coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes HTTP and TLS requests to user-provided domains or URLs, which can contact external, internal, or sensitive services. <br>
Mitigation: Use the skill only against sites you own or are authorized to test, and avoid internal or sensitive targets unless that access is intentional. <br>
Risk: Website health and header grades are point-in-time checks and may not represent ongoing security posture. <br>
Mitigation: Treat results as a current audit signal and re-run checks when site configuration, certificates, or response behavior changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogue-agent1/siteaudit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain-text command output or JSON audit results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports status, response time, TLS certificate details, security header grade, detected issues, and process exit status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
