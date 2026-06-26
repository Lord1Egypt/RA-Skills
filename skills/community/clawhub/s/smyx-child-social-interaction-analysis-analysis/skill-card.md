## Description: <br>
Analyzes kindergarten or early-education videos to report pairwise child social-interaction frequency, duration, initiators, low-interaction candidates, and heatmaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External educators, school operators, and their agents use this skill to analyze kindergarten, early-education, or playground video for child social-interaction statistics, heatmaps, report links, and historical report lookups. Outputs are educational support signals and should not be treated as psychological or medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes children's videos and historical reports through cloud services, creating sensitive minor-related data exposure risk. <br>
Mitigation: Use only after confirming the provider is authorized for the school or organization, guardian or school consent is in place, and retention, deletion, access-control, and export-handling terms are acceptable. <br>
Risk: The skill silently manages identity and authentication state and can retrieve broad historical report lists. <br>
Mitigation: Run it in a controlled environment, avoid shared machines unless local identity and token storage is acceptable, and review history outputs before sharing them. <br>
Risk: Low-interaction candidates or social-interaction statistics may be misread as clinical or autism diagnosis. <br>
Mitigation: Treat results as educational support and visual behavior statistics only; refer suspected developmental concerns to qualified professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-child-social-interaction-analysis-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown report text with structured JSON content, report/export links, and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local video files or video URLs; documented inputs include mp4, avi, and mov videos up to 10 MB.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
