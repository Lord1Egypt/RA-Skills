## Description: <br>
Fact-check and attribution-check social media content such as tweets, LinkedIn posts, and blog excerpts before publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media writers, reviewers, and approval agents use this skill to audit drafts for verifiable claims, attribution needs, inaccurate statements, and must-fix edits before content is sent for approval or published. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow expects web research and may expose confidential unpublished content to external search tools. <br>
Mitigation: Use it only with drafts that are approved for external research, or remove sensitive details before checking. <br>
Risk: Fact-checking results can still contain stale, incomplete, or misleading source interpretations. <br>
Mitigation: Review cited sources and verdicts before relying on the report for publication approval. <br>
Risk: The skill writes a local markdown report in the workspace. <br>
Mitigation: Review the generated report path and contents before sharing or committing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/social-accuracy-checker) <br>
- [Publisher profile](https://clawhub.ai/user/nissan) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown accuracy and attribution report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report includes a summary, claim checks, attribution flags, and recommended edits.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
