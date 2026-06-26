## Description: <br>
Review code with risk-first analysis, reproducible evidence, and patch-ready guidance for correctness, security, performance, and maintainability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to run code reviews, PR reviews, merge-readiness checks, and bug-risk audits before shipping. It helps structure findings by severity, confidence, evidence, impact, test coverage, and concrete fix direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional local review memory could retain sensitive project details if the user approves broad notes. <br>
Mitigation: Save only non-sensitive preferences, project constraints, and review summaries approved by the user; do not store secrets, tokens, private code, or confidential findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/review-code) <br>
- [Skill homepage](https://clawic.com/skills/review-code) <br>
- [Review workflow](review-workflow.md) <br>
- [Severity and confidence guide](severity-and-confidence.md) <br>
- [Test impact playbook](test-impact-playbook.md) <br>
- [Patch strategy](patch-strategy.md) <br>
- [Language and architecture risk checklists](language-risk-checklists.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown review findings with file references, severity and confidence labels, fix guidance, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optional user-approved local notes under ~/review-code/; no external network requests are made by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
