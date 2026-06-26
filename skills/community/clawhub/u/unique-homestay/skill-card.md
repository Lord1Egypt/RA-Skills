## Description: <br>
Find unique homestays and B&Bs - local character, host recommendations, authentic experiences that hotels can't offer, sorted by guest ratings and powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search for highly rated homestays and B&Bs, collect destination and date parameters, execute supported flyai CLI searches, and format live booking results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports hidden local logging of travel requests, which may expose personal trip details. <br>
Mitigation: Review and control logging before use; avoid entering passport, visa, payment, or other sensitive personal details unless logging behavior is removed or clearly governed. <br>
Risk: The skill installs and depends on a third-party flyai CLI for real-time travel results. <br>
Mitigation: Review the CLI package and run it in an environment appropriate for third-party tools before using it with sensitive travel queries. <br>
Risk: Travel recommendations can be wrong or stale if CLI calls fail or return incomplete data. <br>
Mitigation: Require successful flyai command output, booking links for every listing, and honest failure messages instead of fallback answers from model memory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/unique-homestay) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; every listed stay must include a Book link and the Powered by flyai brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
