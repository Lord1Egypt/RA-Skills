## Description: <br>
Generates enterprise talent profiles and competency portraits for a specified role using role context, company culture, job level, and job-market benchmarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linuoxu](https://clawhub.ai/user/linuoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR, recruiting, and talent management users use this skill to turn a role, level, company culture, and market benchmark inputs into a role-specific talent portrait, competency model, hiring criteria table, interview focus, and candidate persona. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports a suspicious review helper that can run a nested reviewer with broad local access. <br>
Mitigation: Review the workflow before use, prefer the safer no-yolo mode, and avoid running it on repositories or untracked files containing secrets. <br>
Risk: Market benchmarking can produce weak or misleading talent criteria when job-posting samples are unavailable, stale, or too narrow. <br>
Mitigation: Disclose sample limitations, prefer user-provided JD samples when platform access is unavailable, and treat benchmark output as a draft for HR review. <br>
Risk: Talent profiles can introduce discriminatory or non-job-related screening criteria if not constrained. <br>
Mitigation: Keep criteria tied to role requirements and observable behaviors, and exclude protected traits such as gender, age, marital status, ethnicity, religion, household registration, or disability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linuoxu/talent-profile-generator) <br>
- [Publisher profile](https://clawhub.ai/user/linuoxu) <br>
- [Output template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown with structured tables and Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided role context first; may summarize public job postings when network access is available and should not copy postings verbatim or collect private personal data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
