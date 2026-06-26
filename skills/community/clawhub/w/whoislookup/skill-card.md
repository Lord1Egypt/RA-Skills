## Description: <br>
Look up domain WHOIS registration info, including registrar, creation date, expiry date, nameservers, and domain status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and domain operators use this skill to check WHOIS registration details for one or more domains, including registrar, dates, nameservers, and status values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WHOIS queries disclose the queried domain name to the selected WHOIS server, including any custom server configured by the user. <br>
Mitigation: Query only domains that are acceptable to disclose to the relevant WHOIS service, and avoid untrusted custom WHOIS servers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogue-agent1/whoislookup) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text summaries, raw WHOIS text, or parsed JSON from the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries user-provided domains over WHOIS port 43; no external Python dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
