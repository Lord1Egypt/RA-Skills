## Description: <br>
Website vulnerability scanner and security audit toolkit for web application pentesting, bug bounty reconnaissance, and security audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p0lish](https://clawhub.ai/user/p0lish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security engineers, and authorized testers use this skill to run web reconnaissance and vulnerability checks against systems they own or have explicit permission to assess. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill actively probes web targets and can be dual-use. <br>
Mitigation: Run it only against systems you own or have explicit authorization to test, and review selected modules before starting a full scan. <br>
Risk: Optional Shodan enrichment and other network checks may send target details to third-party services. <br>
Mitigation: Avoid setting SHODAN_API_KEY unless Shodan enrichment is intended, and review network-facing modules before execution. <br>
Risk: Generated reports can contain discovered secrets, vulnerable endpoints, and infrastructure details. <br>
Mitigation: Treat the output directory as sensitive and restrict access to generated Markdown, JSON, screenshots, and raw scan files. <br>


## Reference(s): <br>
- [Tool Requirements](references/tools.md) <br>
- [SecLists Wordlist Reference](references/wordlists.md) <br>
- [ProjectDiscovery subfinder](https://github.com/projectdiscovery/subfinder) <br>
- [ProjectDiscovery nuclei](https://github.com/projectdiscovery/nuclei) <br>
- [Titus secrets scanner](https://github.com/AidenPearce369/titus) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Analysis, Files] <br>
**Output Format:** [Markdown reports, optional JSON reports, shell output, and saved scan artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports and scan artifacts are written under the configured reconnaissance output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
