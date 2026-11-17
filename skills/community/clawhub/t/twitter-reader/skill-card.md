## Description:

Extract complete data from X/Twitter tweets by URL, including text, author info, timestamps, engagement stats, media, quoted tweets, and thread context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iheardulkbtc](https://clawhub.ai/user/iheardulkbtc)

### License/Terms of Use:

MIT

## Use Case:

Agents and developers use this skill to read public X/Twitter status URLs, extract tweet or thread data, and present structured details such as author, timestamp, engagement, media, and quoted tweet context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tweet author and status ID are sent to FxTwitter and may be sent to Nitter fallback instances.

Mitigation: Use the skill only when sharing those public tweet identifiers with third-party tweet services is acceptable.

Risk: The thread reader accepts a max_depth argument that should not be treated as arbitrary user-controlled input.

Mitigation: Pass a bounded integer for thread depth and keep the default limit unless a larger value is explicitly needed.

Risk: Fallback results depend on public Nitter instances that may be unavailable or incomplete.

Mitigation: Prefer the FxTwitter reader and present fallback failures or limited data clearly to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iheardulkbtc/skills/twitter-reader)
- [FxTwitter API](https://api.fxtwitter.com)
- [Nitter fallback instance](https://nitter.net)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tweet and thread extraction results include public post metadata when available; fallback output can be limited when third-party services are unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
