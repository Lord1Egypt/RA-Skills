## Description: <br>
Automated lead generation pipeline that finds local businesses with weak/no websites, AI-generates custom demo sites, deploys to Vercel, and runs a 5-email cold outreach drip sequence via AgentMail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RazzleDazzleI](https://clawhub.ai/user/RazzleDazzleI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales operators, agencies, and developers use this skill to discover local business leads, generate custom demo websites, deploy them, and coordinate cold email follow-up after configuration and approval checkpoints. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run continuously, deploy public demo websites, and send cold outreach from user-controlled accounts. <br>
Mitigation: Run dry-runs first, keep manual approval checkpoints before sends and deployments, and monitor rate limits and run logs. <br>
Risk: The workflow requires API keys and a Google service-account key with access to lead data. <br>
Mitigation: Use dedicated least-privilege accounts, store credentials securely, and rotate keys if they are exposed or no longer needed. <br>
Risk: Cold outreach and lead processing can create email, privacy, and consent obligations. <br>
Mitigation: Confirm the campaign complies with applicable email and privacy rules before enabling automated sending. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/RazzleDazzleI/skill-package) <br>
- [Project homepage declared by artifact](https://github.com/RazzleDazzleI/lead-gen-pipeline) <br>
- [Environment Variables Reference](references/env-example.md) <br>
- [Google Sheet Setup](references/google-sheet-setup.md) <br>
- [5-Email Drip Sequence](references/drip-sequence.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands plus generated JSON, HTML, email text, screenshots, and status files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and external API credentials; per-lead runs may deploy public websites and send outreach email.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
