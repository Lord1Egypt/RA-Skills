## Description:

Search Viewer helps security researchers and penetration testers query multiple cyberspace mapping APIs for authorized reconnaissance, asset discovery, service enumeration, and fingerprint identification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

GPL-3.0 License

## Use Case:

Security researchers, penetration testers, and defenders use this skill to configure and run Search Viewer for authorized reconnaissance across FOFA, Hunter, Shodan, 360 Quake, Zoomeye, and related services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool stores third-party API credentials in a local plaintext config.ini file.

Mitigation: Use restricted API keys, avoid shared machines, and do not commit config.ini or exported results.

Risk: Searches and credentials are sent to third-party reconnaissance services.

Mitigation: Use the tool only for authorized targets and follow each service's terms and applicable law.

Risk: The release relies on unpinned external code and dependencies.

Mitigation: Prefer a reviewed installation path and pin dependencies before operational use.

## Reference(s):

- [Search Viewer ClawHub skill page](https://clawhub.ai/adminlove520/skills/search-viewer)
- [FOFA](https://fofa.info)
- [Hunter](https://hunter.qianxin.com)
- [Shodan](https://www.shodan.io)
- [360 Quake](https://quake.360.cn)
- [Zoomeye](https://www.zoomeye.org)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands, API key configuration notes, query examples, and export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying tool can export reconnaissance results as CSV or JSON files.]

## Skill Version(s):

4.3.0 (source: release metadata; artifact changelog lists 4.3 dated 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
