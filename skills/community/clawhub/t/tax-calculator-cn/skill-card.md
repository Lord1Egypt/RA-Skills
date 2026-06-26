## Description: <br>
Chinese personal income tax calculator for salary, bonus, freelance income, deductions, annual settlement, tax refund estimates, tax optimization, and offer comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate Chinese personal income tax scenarios, including monthly salary, year-end bonus, freelance income, annual settlement, deductions, refund estimates, tax optimization, and offer comparisons. Results should be treated as estimates and checked against current tax policy or a qualified tax professional for decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks the release suspicious because it bundles an unrelated financial-tracking script that is under-disclosed and writes local history. <br>
Mitigation: Review before installing, verify that the installed command uses scripts/tax.sh for tax calculations, and avoid entering transaction details into scripts/script.sh unless local history writing is acceptable. <br>
Risk: Tax calculations and optimization guidance may become inaccurate as Chinese tax policy changes. <br>
Mitigation: Treat outputs as estimates and confirm material tax decisions against current official guidance or a qualified tax professional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/tax-calculator-cn) <br>
- [Tax optimization guide](artifact/tips.md) <br>
- [Declared project homepage](https://bytesagain.com) <br>
- [Declared source repository](https://github.com/bytesagain/ai-skills) <br>
- [Feedback and feature requests](https://bytesagain.com/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces tax estimates and optimization guidance; bundled scripts may also write local history under the user's data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
