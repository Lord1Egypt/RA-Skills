## Description:

Build comprehensive threat actor profiles using open-source intelligence (OSINT) techniques to document adversary motivations, capabilities, infrastructure, and TTPs for proactive defense.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling-qian](https://clawhub.ai/user/ling-qian)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, threat intelligence teams, and detection engineers use this skill to gather OSINT, map threat actor TTPs to MITRE ATT&CK, correlate infrastructure, and produce structured threat actor dossiers for defensive planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Threat actor names, indicators, and collection targets may be sent to third-party OSINT and threat-intelligence services.

Mitigation: Use the skill only for authorized threat-intelligence work, minimize sensitive query content, and review which external services are enabled before execution.

Risk: API keys for OTX, VirusTotal, Shodan, Malpedia, or related tools could be exposed if passed directly in prompts or command lines.

Mitigation: Store credentials in environment variables or a secret manager and avoid embedding keys in generated code, reports, or command history.

Risk: Collected OSINT and generated dossiers can include sensitive indicators, attribution assessments, or investigative targets.

Mitigation: Handle generated JSON and Markdown reports according to organizational data-handling rules and review them before sharing.

Risk: Collection from social media, paste sites, dark web forums, or similar sources may have legal, policy, or authorization constraints.

Mitigation: Confirm legal and organizational authorization before using the skill for those source categories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ling-qian/skills/threat-actor-osint)
- [API Reference: Threat Actor Profiling from OSINT](references/api-reference.md)
- [SpiderFoot OSINT Tool](https://github.com/smicallef/spiderfoot)
- [MITRE ATT&CK Groups](https://attack.mitre.org/groups/)
- [MITRE ATT&CK STIX data](https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json)
- [Huntress: Threat Actor Profiling](https://www.huntress.com/cybersecurity-101/topic/threat-actor-profiling)
- [CrowdStrike: OSINT in Cybersecurity](https://www.crowdstrike.com/en-us/cybersecurity-101/threat-intelligence/open-source-intelligence-osint/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with Python and shell examples; JSON report artifacts when running the bundled script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call MITRE ATT&CK, AlienVault OTX, VirusTotal, Shodan, Malpedia, or SpiderFoot depending on user configuration and API keys.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
