## Description: <br>
Skills Firewall scans skill directories for risky code patterns, applies allow, warn, block, or quarantine decisions, and generates security reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huzibbs](https://clawhub.ai/user/huzibbs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review skill folders before installation or execution, inspect pattern-based findings, and produce text, JSON, or HTML security reports for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact describes itself as a firewall, but server security evidence says it should be treated as a lightweight local pattern scanner rather than an enforcement boundary. <br>
Mitigation: Use scan and firewall decisions as advisory signals only; review findings manually before installing or running a skill. <br>
Risk: Server security evidence notes that generated HTML reports can render unescaped scanned names or fields. <br>
Mitigation: Be careful opening HTML reports generated from untrusted skill directories; prefer text or JSON output when reviewing untrusted inputs. <br>


## Reference(s): <br>
- [Malicious Patterns Reference](references/malicious_patterns.md) <br>
- [Security Rules Reference](references/security_rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/huzibbs/skills-firewall) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, plus text, JSON, or HTML security reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include threat levels, matched rules, warnings, recommendations, and risk summaries for manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
