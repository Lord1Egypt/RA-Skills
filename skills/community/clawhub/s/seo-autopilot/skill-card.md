## Description: <br>
Run local SEO autopilot for boll-koll.se or hyresbyte.se and return PR link plus summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamhjort](https://clawhub.ai/user/adamhjort) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and site operators use this skill to run allowlisted SEO automation for boll-koll.se or hyresbyte.se, then receive a PR URL and a short summary of reported findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper invokes a local seo-autopilot executable, so an unexpected executable on PATH could affect the SEO run. <br>
Mitigation: Install only in environments where the seo-autopilot executable is trusted and PATH is controlled. <br>
Risk: Automation may open pull requests against the wrong repository or account if the local tool is misconfigured. <br>
Mitigation: Confirm generated PR URLs target the expected repository and account before review or merge. <br>
Risk: The plain 'seo' trigger defaults to boll-koll.se, which could run unintentionally. <br>
Mitigation: Prefer the site-specific triggers when accidental execution would matter. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown summary containing a PR URL and top SEO findings when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Site input is restricted to boll-koll.se or hyresbyte.se and defaults to boll-koll.se.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
