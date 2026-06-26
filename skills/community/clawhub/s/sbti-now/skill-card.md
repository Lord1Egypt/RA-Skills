## Description: <br>
Runs a self-contained SBTI personality test in English or Chinese using bundled questions, scoring scripts, and a manual fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fechin](https://clawhub.ai/user/fechin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent hosts use this skill to run an entertainment-first SBTI personality quiz, score responses, and summarize localized results. It supports scripted Python execution and a manual workflow for hosts that cannot execute Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release metadata includes broad capability tags that are not needed for the local quiz. <br>
Mitigation: Deny financial, crypto, purchase, account, and credential permissions if prompted. <br>
Risk: Quiz answers may be visible to or logged by the host environment. <br>
Mitigation: Avoid entering highly sensitive personal information while taking the quiz. <br>
Risk: Personality-test results could be mistaken for clinical or professional assessment. <br>
Mitigation: Present SBTI results as entertainment-first output, not clinical guidance. <br>


## Reference(s): <br>
- [Manual Workflow](references/manual-workflow.md) <br>
- [SBTI Now](https://sbti.now/) <br>
- [ClawHub skill page](https://clawhub.ai/fechin/sbti-now) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON personality-test results with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes localized personality code and name, similarity score, 15-dimension vector, top matches, dimension explanations, and shareable summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
