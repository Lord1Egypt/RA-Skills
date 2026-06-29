## Description: <br>
钟馗.Skill helps agents review other skills for security risks with static auditing, vulnerability-rule updates, scoring, and structured clean, suspicious, or malicious verdicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebandao777-oss](https://clawhub.ai/user/ebandao777-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to assess a ClawHub or agent skill before installation or release, inspect risk findings, and receive a structured safety verdict. It can also preview or apply local vulnerability-rule updates before running a review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The --update --apply path changes the local rule database without the normal confirmation step. <br>
Mitigation: Prefer --update --dry-run or interactive confirmation, and review generated rule changes before applying them. <br>
Risk: A clean automated scan is not a security guarantee for every install context. <br>
Mitigation: Use the verdict as triage, and add human review for sensitive, regulated, or high-impact deployments. <br>
Risk: Threat-intelligence updates may involve external services or optional credentials. <br>
Mitigation: Use scoped tokens only when needed, avoid pasting unrelated secrets, and keep network access limited to the documented update workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ebandao777-oss/zhongkui-skill) <br>
- [README.md](README.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>
- [REFERENCE.md](REFERENCE.md) <br>
- [Static Audit Checklist](references/static-audit.md) <br>
- [Risk Taxonomy](references/risk-taxonomy.md) <br>
- [Scoring and Verdict Rules](references/scoring.md) <br>
- [Capability Boundaries](references/capability-boundaries.md) <br>
- [Threat Intelligence Pipeline](references/threat-intel-pipeline.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown security review report with verdict, score, findings table, and remediation guidance; direct script mode prints Markdown to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional update mode can modify local vulnerability signatures; dry-run or interactive confirmation is safer than direct apply.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
