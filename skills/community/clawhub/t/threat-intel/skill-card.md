## Description: <br>
Provides Arabic-first OSINT and threat intelligence workflows for monitoring public Telegram channels, generating bilingual reports, searching Tor-accessible dark web indexes, and passively enumerating subdomains through Certificate Transparency logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdullah944](https://clawhub.ai/user/Abdullah944) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SOC teams, OSINT investigators, journalists, security researchers, and enterprise security teams use this skill to gather passive threat intelligence from Arabic-language public sources, Tor-accessible indexes, and Certificate Transparency logs for reporting and triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OSINT queries, public channel names, and target domains may be sent to public or Tor-accessible services. <br>
Mitigation: Use only authorized targets and queries, avoid unnecessary sensitive identifiers, and review results before sharing. <br>
Risk: The skill declares broader local read/write permissions than its advertised passive lookup behavior appears to require. <br>
Mitigation: Run it with the least local file access available and avoid granting write access unless a workflow specifically needs it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abdullah944/threat-intel) <br>
- [Publisher profile](https://clawhub.ai/user/Abdullah944) <br>
- [Certificate Transparency search](https://crt.sh/) <br>
- [Telegram public channel preview format](https://t.me/s/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown-style threat intelligence summaries with command-line output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Arabic and English output is supported; dark web search depends on local Tor and torsocks availability.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
