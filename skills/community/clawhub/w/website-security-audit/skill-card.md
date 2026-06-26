## Description: <br>
Website Security Audit helps an agent assess a user-provided URL for trust and security signals, including HTTPS/TLS, site content, ICP and public security registration, domain age, and platform background. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[666-moonlight](https://clawhub.ai/user/666-moonlight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to check whether a public website or link appears trustworthy before interacting with it. It guides the agent through browser review, domain and certificate checks, public registration checks, and a structured risk report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opening untrusted or private URLs can expose sensitive systems or data. <br>
Mitigation: Use the workflow only for public sites or links the user is comfortable opening, and avoid internal systems, private URLs, login pages, or pages containing sensitive data. <br>
Risk: A website trust assessment can be incomplete or misleading when public signals are unavailable, stale, or ambiguous. <br>
Mitigation: Treat the report as advisory, preserve uncertainty in the findings, and verify important conclusions against authoritative public sources before acting. <br>
Risk: The optional ProSearch command is environment-specific and may not be available or appropriate in every runtime. <br>
Mitigation: Use it only when the local environment is configured for it; otherwise rely on browser inspection, WHOIS, and public registration checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/666-moonlight/website-security-audit) <br>
- [Known platforms reference](references/known-platforms.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Structured Markdown report with risk tables, checklists, and a short summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optional local search or WHOIS lookup suggestions; no credentials are required by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
