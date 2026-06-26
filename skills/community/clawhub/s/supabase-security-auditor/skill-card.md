## Description: <br>
Audit Supabase projects for security by checking Row Level Security policies, auth configuration, API exposure, storage rules, and edge function security. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Supabase applications before launch, after configuration changes, or during security reviews. It helps identify weak RLS policies, unsafe auth settings, exposed API keys, storage misconfiguration, edge function issues, and database permission risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may surface Supabase secrets or API keys while checking project files and environment files. <br>
Mitigation: Run it only from the intended Supabase project root, redact secrets in reports, and avoid sharing raw audit output publicly. <br>
Risk: Security findings are advisory and may be incomplete or incorrect if the project structure, migrations, or configuration are missing from the agent context. <br>
Mitigation: Review findings against the live Supabase project, database policies, and deployment configuration before making security decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security audit report with findings, severity groupings, command examples, SQL examples, and remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include project security findings and should redact secrets before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
