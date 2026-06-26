## Description: <br>
Whois Toolkit helps agents query WHOIS data for domains, including registrar details, creation and expiry dates, nameservers, status, registrant information, raw responses, and JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and domain operators use this skill to look up domain registration details, check expiry dates, review nameservers and status, and export WHOIS results for monitoring or investigation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain names queried with this skill are sent to WHOIS servers. <br>
Mitigation: Query only domains you are comfortable disclosing to the selected WHOIS server. <br>
Risk: Custom WHOIS servers can observe queried domains and return raw response text. <br>
Mitigation: Use the custom server option only with WHOIS hosts you trust, especially when raw output is enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/whois-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown usage guidance with bash examples; command output is plain text, JSON, or raw WHOIS text depending on flags.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-domain and batch lookups, expiry-only output, raw WHOIS output, JSON output, and custom WHOIS server selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
