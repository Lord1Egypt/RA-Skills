## Description: <br>
Checks whether a user's QA request includes a clear requirement, enough context, and readable supporting inputs before test design begins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, testers, and developer agents use this skill as an entry gate before requirement review or test design. It scores input quality, identifies missing requirement details, and asks focused clarification questions when the request is too vague. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may interrupt QA workflows if it is activated too broadly for requests that already contain enough context. <br>
Mitigation: Use it as the first QA workflow gate and continue once the validation result is pass or the user has answered the clarification questions. <br>
Risk: Fallback test cases may be weak when the user refuses or cannot provide missing requirement details. <br>
Mitigation: Review fallback output carefully and mark high-risk or uncovered areas before using it for test design. <br>
Risk: The skill may read supplied files or fetch supplied requirement URLs as part of input validation. <br>
Mitigation: Provide only requirement sources intended for the agent to inspect and paste inaccessible URL content directly when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kokxi/skills/qa-input-validation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kokxi) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance] <br>
**Output Format:** [Structured JSON or Markdown summaries with validation status, quality score, missing information, clarification questions, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the user to provide missing requirements, readable files, or accessible requirement URLs before continuing.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
