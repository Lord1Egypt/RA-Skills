## Description: <br>
Provides cyber and cognitive security threat intelligence by monitoring feeds, scoring items against user interests, and producing briefings and deep-dive analyses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mirai8888](https://clawhub.ai/user/Mirai8888) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security practitioners and operators use this skill to keep watch on cybersecurity and cognitive-security feeds, receive scheduled or on-demand briefings, and request deeper analysis of vulnerabilities, exploits, campaigns, and influence operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled external feed checks and on-demand lookups may reveal topic interests or retrieve untrusted content. <br>
Mitigation: Review configured sources and briefing schedules before enabling the skill, keep feeds to trusted sources, and validate important findings against original advisories. <br>
Risk: Persistent memory can store the operator's interests, briefing history, and study progress. <br>
Mitigation: Periodically review or clear stored profile and study-history data, especially before using the skill on shared or sensitive systems. <br>
Risk: Deep-dive outputs about vulnerabilities, exploits, or proof-of-concept code can be incomplete, outdated, or misused. <br>
Mitigation: Treat outputs as triage and education, verify technical details from authoritative sources, and use exploit or lab guidance only in authorized environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mirai8888/seithar-intel) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Mirai8888) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown briefings and structured analysis with occasional code or shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include relevance scores, source links, MITRE ATT&CK or DISARM mappings, public PoC discovery notes, and user-specific study recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
