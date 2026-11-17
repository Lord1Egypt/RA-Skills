## Description:

Helps agents use Scrapling-based tooling to search Boss Zhipin candidates, retrieve resumes, send batch greetings, and parse resume data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuritu](https://clawhub.ai/user/wuritu)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and recruiting-operations agents use this skill to search Boss Zhipin for candidates, retrieve resumes, send greetings, and convert resume text into structured recruiting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Boss Zhipin session cookies can grant authenticated account access.

Mitigation: Use a dedicated account or sanctioned API flow, avoid pasting full browser cookies into prompts or shared files, and rotate credentials if exposed.

Risk: Candidate resumes may contain personal data.

Mitigation: Process resume data only with appropriate consent, access controls, retention limits, and review before sending content to any remote LLM parser.

Risk: Batch outreach can contact candidates at scale.

Mitigation: Require manual review before any batch greeting or outreach action and keep daily limits conservative.

## Reference(s):

- [Boss Zhipin Configuration Guide](references/config.md)
- [Boss Zhipin Selector Reference](references/selectors.md)
- [Boss Zhipin](https://www.zhipin.com)
- [ClawHub Skill Listing](https://clawhub.ai/wuritu/skills/scrapling-boss-recruitment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code snippets, configuration examples, and structured resume data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce candidate and resume fields as JSON-like structured text.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
