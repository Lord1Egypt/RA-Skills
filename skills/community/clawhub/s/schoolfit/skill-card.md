## Description: <br>
Use for Hong Kong school admissions, school selection, secondary school, primary school, kindergarten, international school, and postsecondary advisory workflows with SchoolFit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djanngau](https://clawhub.ai/user/djanngau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External families and education advisors use this skill to search, compare, shortlist, and plan Hong Kong school admissions decisions using SchoolFit data. It supports advisory workflows for kindergartens, primary schools, secondary schools, international schools, and postsecondary options. <br>

### Deployment Geography for Use: <br>
Hong Kong <br>

## Known Risks and Mitigations: <br>
Risk: Live school-search queries send preference text to schoolfit.hk. <br>
Mitigation: Disclose this before live queries and ask users to remove student names, HKID, phone numbers, addresses, report-card details, and private documents. <br>
Risk: A SchoolFit sfhk_ access code could be exposed if copied into shared spaces, logs, or final answers. <br>
Mitigation: Keep the code only in a trusted one-to-one chat or current helper invocation, pass it only via --skill-code or active context, and never echo the full code. <br>
Risk: Vacancy and admissions results can become stale or be mistaken for guarantees. <br>
Mitigation: Present these results as time-limited leads, include source and freshness context when returned, and tell families to verify current status with the school. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/djanngau/schoolfit) <br>
- [SchoolFit Skill Repository](https://github.com/djanngau/schoolfit-skill) <br>
- [SchoolFit](https://schoolfit.hk/) <br>
- [SchoolFit Access Code](https://schoolfit.hk/skill-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and concise parent-facing text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live advisory commands call the SchoolFit API through the bundled helper; local parsing is available before live queries.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
