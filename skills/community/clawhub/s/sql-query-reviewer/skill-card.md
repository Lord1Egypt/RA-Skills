## Description: <br>
Reviews SQL queries for correctness, security risks, and performance issues, then returns severity-rated findings and optimized rewrites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lnguyen1996](https://clawhub.ai/user/Lnguyen1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database engineers, and data teams use this skill to review raw SQL, ORM-generated SQL, and migration queries for correctness, security, performance, and maintainability before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SQL examples may contain secrets, production customer data, proprietary schemas, or sensitive business logic. <br>
Mitigation: Review and redact SQL, schema details, literals, and business logic before sharing them with an agent environment. <br>
Risk: The skill asks the agent to remember aggregate SQL issue patterns across reviews. <br>
Mitigation: Disable or avoid persistent memory when aggregate issue patterns should not be retained. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown report with severity sections, SQL snippets, explanations, and summary recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include corrected or optimized SQL rewrites and notes on correct query patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
