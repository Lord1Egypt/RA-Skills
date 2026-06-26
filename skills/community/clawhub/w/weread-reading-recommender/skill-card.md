## Description: <br>
Use this skill when the user wants to export local WeRead records, normalize WeRead data, analyze reading preferences from WeRead history, or get book recommendations grounded in WeRead reading behavior and a current learning goal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CengSin](https://clawhub.ai/user/CengSin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to export and normalize their own WeRead reading records locally, then generate reading-profile analysis and book recommendations grounded in reading history and an optional current learning goal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local WeRead session cookie to fetch personal reading data. <br>
Mitigation: Keep the cookie local and private, prefer an environment variable or protected local file, and never paste it into shared files or responses. <br>
Risk: Exported and normalized JSON can reveal reading history and preferences. <br>
Mitigation: Store exported files carefully, share them only intentionally, and delete them when they are no longer needed. <br>
Risk: Recommendations may rely on stale or incomplete normalized data. <br>
Mitigation: Refresh the local export only when the user requests it, then base recommendation work on the normalized JSON file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CengSin/weread-reading-recommender) <br>
- [Data Schema](references/data-schema.md) <br>
- [Privacy Model](references/privacy-model.md) <br>
- [Recommendation Rubric](references/recommendation-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local raw and normalized WeRead JSON files; recommendation responses should use normalized JSON when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
