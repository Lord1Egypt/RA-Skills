## Description: <br>
Helps detect supply chain poisoning in AI agent marketplace skills by scanning Gene/Capsule validation fields for shell injection, outbound requests, and encoded payloads that may indicate backdoors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and agent marketplace users use this skill to statically inspect skill definitions, validation commands, source code, or EvoMap asset URLs for supply-chain poisoning indicators before installation or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote artifacts or URLs supplied for review may reference untrusted code or commands. <br>
Mitigation: Verify URLs before fetching them and treat suspicious commands as text for review rather than executable instructions. <br>
Risk: Static analysis can miss sophisticated obfuscation, multi-stage payloads, or novel attack techniques. <br>
Mitigation: Use the report as a screening aid and manually review source code before installing or deploying uncertain skills. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andyxinweiminicloud/supply-chain-poison-detector) <br>
- [Publisher Profile](https://clawhub.ai/user/andyxinweiminicloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Structured Markdown report with risk ratings, suspicious pattern findings, line references, and recommended actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports classify findings as CLEAN, SUSPECT, or THREAT and are based on static review of the supplied artifact or URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
