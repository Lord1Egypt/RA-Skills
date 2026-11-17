## Description:

Website vulnerability scanner and security audit toolkit. Scan any website for security issues: open ports (nmap), exposed secrets, subdomain enumeration, directory bruteforce, security header scoring, CORS misconfigurations, SSL/TLS analysis, WordPress vulnerabilities, and more. One command, full report. Pentesting and OSINT reconnaissance for web applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p0lish](https://clawhub.ai/user/p0lish)

### License/Terms of Use:


## Use Case:

Developers, security engineers, and authorized testers use this skill to run web reconnaissance and security checks against websites they are permitted to assess. It helps collect DNS, port, fingerprinting, subdomain, directory, secrets, vulnerability, header, CORS, SSL/TLS, WordPress, screenshot, Markdown report, and optional JSON report outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs active web reconnaissance and vulnerability scanning that may be intrusive or unauthorized when used on systems outside the user's control.

Mitigation: Use it only on targets where testing is explicitly authorized, and review scan scope before running full, directory, port, WordPress, or template-based checks.

Risk: The scanner can send target data to third-party lookup services and tools, including Shodan and public reconnaissance utilities.

Mitigation: Review enabled lookups and environment variables before scanning confidential targets, and disable or omit external integrations that are not approved.

Risk: Screenshot capture may run a headless browser with reduced sandboxing.

Mitigation: Avoid the screenshot option unless browser sandboxing is fixed or the scanner runs in an isolated container or disposable environment.

Risk: Unpinned command-line dependencies and scanner templates can change behavior over time.

Mitigation: Prefer pinned, reviewed, or containerized dependencies and validate tool versions before production use.

## Reference(s):

- [ClawHub web-recon Skill Page](https://clawhub.ai/p0lish/skills/web-recon)
- [Required Tools](artifact/references/tools.md)
- [SecLists Wordlist Reference](artifact/references/wordlists.md)
- [ProjectDiscovery Subfinder](https://github.com/projectdiscovery/subfinder)
- [ffuf](https://github.com/ffuf/ffuf)
- [ProjectDiscovery Nuclei](https://github.com/projectdiscovery/nuclei)
- [Titus](https://github.com/AidenPearce369/titus)
- [ProjectDiscovery httpx](https://github.com/projectdiscovery/httpx)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands plus generated Markdown, JSON, text, and screenshot files in a recon output directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include prioritized scan findings and optional machine-readable JSON; available results depend on installed command-line tools and selected scan options.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
