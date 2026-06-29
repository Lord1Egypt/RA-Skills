## Description: <br>
Confirms or rejects review-llm-artifacts findings before deletions or risky refactors so agents can reduce false positives before applying fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code-review agents use this skill after review-llm-artifacts to verify reported LLM artifact findings, especially deletion, dead-code, and high-risk cases, before running follow-up fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect verification results could cause a follow-up fix step to remove or refactor code that is still required. <br>
Mitigation: Review the generated .beagle/llm-artifacts-verification.json before using any follow-up fix skill, especially for deletion, dead-code, or high-risk findings. <br>
Risk: A stale or mismatched findings report could produce misleading verdicts. <br>
Mitigation: Use the skill's parse, echo, id-lock, evidence-before-verdict, and output-validation gates so results map exactly to the source findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/skills/verify-llm-artifacts) <br>
- [Verification checklist](references/verification-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON verification report with markdown summary and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [.beagle/llm-artifacts-verification.json records one result per locked finding id with status, confidence, checks_performed, notes, and summary counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
