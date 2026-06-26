## Description: <br>
Check subdomains for potential takeover vulnerabilities by detecting dangling DNS records pointing to unclaimed services such as GitHub Pages, Heroku, and AWS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hostilespider](https://clawhub.ai/user/hostilespider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to check owned or authorized subdomains for dangling DNS records and optionally verify potential takeover exposure with HTTP status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs DNS lookups and, unless run with --passive, HTTP requests against supplied domains. <br>
Mitigation: Use it only on domains you own or are authorized to test, and use --passive when HTTP verification is not appropriate. <br>
Risk: Takeover checks can produce false positives. <br>
Mitigation: Treat results as advisory and manually confirm ownership and service state before remediation. <br>
Risk: The security guidance notes curl is needed for active HTTP checks even though it is not listed in declared requirements. <br>
Mitigation: Ensure bash, dig, and curl are available before running non-passive scans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hostilespider/subdomain-takeover) <br>
- [Publisher profile](https://clawhub.ai/user/hostilespider) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text scan summary or JSON counts from shell execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write detailed findings to a file and exits nonzero when potential vulnerabilities are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
