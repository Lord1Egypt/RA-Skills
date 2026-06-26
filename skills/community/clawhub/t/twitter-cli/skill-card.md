## Description: <br>
twitter-cli helps agents read and manage Twitter/X timelines, tweets, profiles, searches, and account actions through a terminal CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackwener](https://clawhub.ai/user/jackwener) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to script Twitter/X reading workflows and explicit account actions such as posting, replying, liking, retweeting, bookmarking, and following from a local CLI session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use access equivalent to a logged-in Twitter/X session and includes account-changing commands. <br>
Mitigation: Run it only in a trusted local environment and require explicit user confirmation before posting, replying, deleting, liking, retweeting, bookmarking, following, or unfollowing. <br>
Risk: Browser cookies and Cookie headers can expose the user's Twitter/X session. <br>
Mitigation: Prefer local browser cookie extraction or local environment variables; do not paste full Cookie headers into chat, remote agents, logs, or shared terminals. <br>
Risk: Automated or high-volume account activity may create account safety or rate-limit issues. <br>
Mitigation: Keep request volumes low, review account-changing commands before execution, and avoid unattended write workflows. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jackwener/twitter-cli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jackwener) <br>
- [Structured Output Schema](SCHEMA.md) <br>
- [README](README.md) <br>
- [PyPI project](https://pypi.org/project/twitter-cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, YAML, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output in rich text, YAML, or JSON envelopes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured output uses an ok/schema_version/data envelope; compact mode can reduce returned tweet fields for agent context.] <br>

## Skill Version(s): <br>
0.5.1 (source: release evidence and pyproject.toml; SKILL.md frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
