## Description: <br>
Skill Guard scans AI skill directories for keyword-based risk patterns before installation, use, or security review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HuaiBuer](https://clawhub.ai/user/HuaiBuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and security reviewers use this skill as a first-pass local scanner when evaluating unknown or third-party skills before installation or execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner is a first-pass keyword-based review aid and may miss unsafe behavior or report benign code as risky. <br>
Mitigation: Use its findings to prioritize manual review, and do not treat a clean scan as a security guarantee. <br>
Risk: Scanning broad private directories can expose sensitive filenames or code snippets in local scan output. <br>
Mitigation: Run it only on the specific skill or code folder being evaluated and avoid broad private directories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HuaiBuer/skill-guard-waai) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON-like scan results with human-readable security guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports aggregate severity counts and a bounded list of matching risk findings.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata; artifact frontmatter reports 1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
