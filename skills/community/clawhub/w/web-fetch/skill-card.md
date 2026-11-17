## Description:

web-fetch helps agents collect public web data from static or JavaScript-rendered pages, parse selected fields, and export structured JSON or CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to gather authorized public web data for market research, competitor monitoring, public data aggregation, and repeatable extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted URL fetching can reach private networks, cloud metadata endpoints, authenticated sessions, or sensitive local services.

Mitigation: Review targets before execution and run only in environments without access to private networks, cloud metadata, authenticated web sessions, or sensitive local paths.

Risk: Anti-bot bypass guidance and optional robots.txt bypass can be misused for unauthorized scraping.

Mitigation: Use only for authorized public scraping, respect site terms and robots.txt, and avoid anti-detection techniques unless explicit permission exists.

Risk: The learning script stores usage history and notes as persistent plaintext data.

Mitigation: Treat learned_patterns.json as local plaintext history and avoid recording sensitive URLs, credentials, personal data, or private operational details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/web-fetch)
- [ClawHub publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON/CSV data outputs from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write JSON, CSV, or learned_patterns.json files in the selected working directory when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
