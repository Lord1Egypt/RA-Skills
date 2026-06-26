## Description: <br>
Reviews Remix v2 code for v1-shape meta exports, cookie security gaps, misplaced auth gates, and missing CSRF protection in meta/SEO, session, auth, or form-mutation code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review Remix v2 applications for SEO metadata regressions, insecure session cookie configuration, misplaced authentication checks, and missing CSRF validation before changes are accepted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide inspection of sensitive auth, session, CSRF, cookie configuration, environment examples, or relevant git history. <br>
Mitigation: Use it only in repositories where the agent is authorized to inspect those materials. <br>
Risk: Generated review findings could be incorrect or overstate a Remix security or SEO issue. <br>
Mitigation: Require human review of each finding, including the cited file location or quoted evidence, before acting on it. <br>


## Reference(s): <br>
- [Meta V2 Shape](references/meta-v2-shape.md) <br>
- [Cookie Security](references/cookie-security.md) <br>
- [Auth Gates](references/auth-gates.md) <br>
- [CSRF](references/csrf.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown review findings and guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to cite concrete file locations or quotes before recommending changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
