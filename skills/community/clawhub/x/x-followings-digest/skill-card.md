## Description:

Fetches recent tweets from X/Twitter followings and helps generate a structured AI digest from the collected tweet data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaima2022](https://clawhub.ai/user/kaima2022)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to fetch tweets from their X/Twitter followings and turn the collected posts into a concise AI-focused digest. It supports daily or weekly digest workflows with an analyst prompt template for English, Chinese, or bilingual output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide sensitive X/Twitter browser session credentials through AUTH_TOKEN and CT0.

Mitigation: Avoid storing these credentials in persistent shell profiles or logs, and consider rotating or revoking the X/Twitter session after use.

Risk: The skill depends on the external bird CLI to fetch following tweets.

Mitigation: Install bird only from a trusted source and review commands before execution.

Risk: The advertised time-range filtering may not reliably limit fetched tweets.

Mitigation: Treat the requested day range as approximate unless the filtering behavior is fixed and verified.

Risk: Tweets can contain prompt-injection text that may affect digest generation.

Mitigation: Run digest generation in a tool-limited context and review generated analysis before acting on it.

## Reference(s):

- [AI Digest Analyst Prompt Template](references/analyst_prompt_template.md)
- [X Followings Digest on ClawHub](https://clawhub.ai/kaima2022/skills/x-followings-digest)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON tweet data, and structured digest output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest output can be English, Chinese, or bilingual depending on the selected prompt template.]

## Skill Version(s):

1.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
