## Description: <br>
Intelligent code security scanner with hybrid local-cloud detection that fingerprints packages, runs static behavioral analysis, and consults cloud threat intelligence for confidence scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yd-dev](https://clawhub.ai/user/yd-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to vet third-party code packages before installation by reviewing local behavioral findings, package fingerprints, and optional cloud threat intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud threat intelligence is enabled by default and sends redacted scan evidence to NetEase Yidun. <br>
Mitigation: For proprietary, personal, or regulated code, set YIDUN_SKILL_SEC_CLOUD=false before use. <br>
Risk: Local payload logging can retain redacted evidence on disk when explicitly enabled. <br>
Mitigation: Leave YIDUN_SKILL_SEC_LOG_PAYLOAD=false unless an audit log is required. <br>
Risk: The security review evidence flags the release as suspicious because cloud upload behavior and server-side retention deserve user review. <br>
Mitigation: Review the skill's security disclosure and environment settings before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yd-dev/yidun-skill-sec) <br>
- [Publisher profile](https://clawhub.ai/user/yd-dev) <br>
- [ClawHub homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown scan reports with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and openssl; cloud threat intelligence is enabled by default and can be disabled with YIDUN_SKILL_SEC_CLOUD=false.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
