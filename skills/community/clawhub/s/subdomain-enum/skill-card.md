## Description: <br>
Enumerate subdomains for any domain using DNS brute-force and certificate transparency logs (crt.sh). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and authorized operators use this skill to discover subdomains, map exposed infrastructure, and audit known domain attack surface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subdomain enumeration can be unauthorized reconnaissance if run against domains the user does not control. <br>
Mitigation: Use the skill only for domains the user owns or is explicitly authorized to assess. <br>
Risk: Default runs send the target domain to crt.sh for certificate transparency lookup. <br>
Mitigation: Use the --no-crtsh option when target privacy or third-party network disclosure matters. <br>
Risk: The skill runs a local Python script that performs network lookups and can write output files. <br>
Mitigation: Review the target domain and output path before execution, and install only in environments where local Python reconnaissance tooling is acceptable. <br>


## Reference(s): <br>
- [crt.sh certificate transparency search](https://crt.sh/?q=%.{domain}&output=json) <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/subdomain-enum) <br>
- [Publisher profile](https://clawhub.ai/user/Johnnywang2001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; the bundled script can emit plain text reports or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write discovered subdomains to an output file when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
