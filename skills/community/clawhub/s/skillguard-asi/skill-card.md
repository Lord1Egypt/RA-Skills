## Description: <br>
SkillGuard is a local Python command-line scanner that reviews agent skill ZIP packages for prompt injection, credential exposure, dangerous code execution, dependency risks, permission mismatches, sensitive file access, network whitelist issues, and memory-pollution patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thebuddha5566](https://clawhub.ai/user/thebuddha5566) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan agent skill packages before installation or release and generate JSON or Markdown security reports with TRACE scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner extracts and reads submitted ZIP packages, so malformed or untrusted archives could expose the local workspace to parser or extraction edge cases. <br>
Mitigation: Run scans in a constrained workspace or sandbox and only provide ZIP files intended for review. <br>
Risk: Marketplace capability tags list credential-related needs that are not supported by the security summary. <br>
Mitigation: Treat the tool as a local scanner and do not provide wallets, OAuth tokens, or sensitive credentials unless future reviewed evidence requires them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thebuddha5566/skillguard-asi) <br>
- [Publisher Profile](https://clawhub.ai/user/thebuddha5566) <br>
- [SkillGuard Source Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON and Markdown security reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include findings by severity, detector metadata, remediation guidance, and TRACE security scores.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
