## Description: <br>
Check SSL certificate health, protocols, and cipher suites on domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect SSL certificate details, expiry, protocol support, cipher information, and certificate chains for domains they are authorized to test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local shell script that invokes OpenSSL against user-provided domains. <br>
Mitigation: Install and run it only in environments where local shell execution is acceptable, and use it only for domains you own or are authorized to test. <br>
Risk: Security evidence notes that current command examples may need fixing because the script appears to read the wrong argument position. <br>
Mitigation: Verify command behavior in a test environment before relying on results for audits or operational decisions. <br>
Risk: SSL checks can disclose target domains through outbound network connections. <br>
Mitigation: Avoid using the skill for sensitive domains unless network disclosure is acceptable under the user's assessment process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/ssl-checker) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OpenSSL and connects to user-provided domains; stores data under ~/.local/share/ssl-checker/.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
