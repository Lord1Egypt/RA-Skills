## Description: <br>
Search Viewer aggregates cyberspace search APIs such as FOFA, Hunter, Shodan, 360 Quake, Zoomeye, and Censys to support authorized reconnaissance and asset discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security researchers, penetration testers, and asset owners use this skill to install and run a GUI reconnaissance tool, configure provider API keys, query authorized targets across multiple cyberspace search platforms, and export results for assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored API credentials may be exposed if the local app directory or config.ini is shared or synchronized. <br>
Mitigation: Keep config.ini private, use an isolated workspace, and prefer limited-scope API keys. <br>
Risk: Reconnaissance queries and target identifiers may be logged by third-party search providers. <br>
Mitigation: Only run authorized searches and avoid entering sensitive target details unless provider logging and policy implications are acceptable. <br>
Risk: The tool can facilitate unauthorized reconnaissance if misused. <br>
Mitigation: Use it only for assets you own or are explicitly authorized to test, consistent with the artifact's lawful-use guidance and local rules. <br>


## Reference(s): <br>
- [ClawHub Search Viewer listing](https://clawhub.ai/adminlove520/search-viewer) <br>
- [FOFA](https://fofa.info) <br>
- [Hunter](https://hunter.qianxin.com) <br>
- [Shodan](https://www.shodan.io) <br>
- [360 Quake](https://quake.360.cn) <br>
- [Zoomeye](https://www.zoomeye.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash command blocks and provider query examples; the application can export CSV or JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied third-party API credentials and authorized target queries.] <br>

## Skill Version(s): <br>
4.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
