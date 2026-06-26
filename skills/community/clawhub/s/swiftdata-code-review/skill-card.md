## Description: <br>
Reviews SwiftData code for model design, queries, concurrency, and migrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review SwiftData-related Swift files for model design, query, concurrency, and migration issues. It guides reviewers toward scoped, reference-backed findings with file-line evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration guidance may be technically inconsistent with Apple SwiftData behavior in some cases. <br>
Mitigation: Verify migration recommendations against Apple SwiftData behavior before applying code changes. <br>
Risk: Review findings can be misleading when the target is outside SwiftData scope or lacks file-line evidence. <br>
Mitigation: Confirm SwiftData scope, open the matching reference or mark the area N/A, and cite each finding as [FILE:LINE] ISSUE_TITLE. <br>


## Reference(s): <br>
- [SwiftData Model Design](references/model-design.md) <br>
- [SwiftData Queries](references/queries.md) <br>
- [SwiftData Concurrency](references/concurrency.md) <br>
- [SwiftData Migrations](references/migrations.md) <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/swiftdata-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown review findings with file-line citations and checklist or severity grouping] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should use [FILE:LINE] ISSUE_TITLE citations and should only be reported after the skill's hard gates pass.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
