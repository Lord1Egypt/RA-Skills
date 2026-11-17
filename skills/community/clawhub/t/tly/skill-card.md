## Description:

Create T.LY short links through the T.LY API for agents that need a shareable short_url and have access to a valid T.LY API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timleland](https://clawhub.ai/user/timleland)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to create T.LY short links, return short_url values, and surface T.LY API errors clearly when credentials, custom domains, or account limits block creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: T.LY API tokens can be exposed through command history, process arguments, logs, or generated files.

Mitigation: Prefer TLY_API_TOKEN in the environment, avoid embedding real keys in commands or files, and use a safer request method than the curl fallback when process arguments are observable.

Risk: The skill depends on the T.LY service and the optional tly-url-shortener-api package.

Mitigation: Confirm the user trusts T.LY and the package before use, and prefer installing the package in an isolated virtual environment.

## Reference(s):

- [T.LY Short Link API Reference](references/api.md)
- [T.LY homepage](https://t.ly/)
- [tly-url-shortener-api PyPI package](https://pypi.org/project/tly-url-shortener-api/)
- [ClawHub skill page](https://clawhub.ai/timleland/skills/tly)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or JSON short-link results with Markdown guidance and inline shell or Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid T.LY API key and network access to the T.LY API; may return API errors for invalid keys, unauthorized domains, or plan limits.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
