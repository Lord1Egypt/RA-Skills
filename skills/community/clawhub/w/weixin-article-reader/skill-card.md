## Description:

Extracts the title, author, publish date, and full body text from public Weixin official account article links on mp.weixin.qq.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricknote](https://clawhub.ai/user/ricknote)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch public Weixin article metadata and body text before returning the full article or summarizing it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted URL may cause the agent to fetch non-Weixin or internal network resources because URL validation can be bypassed.

Mitigation: Use only article links the user intends to fetch, and validate exact HTTPS hostnames and redirects before trusting the skill in environments with private-network access.

Risk: Extracted article text is untrusted content and may be incomplete.

Mitigation: Treat extracted content as user-supplied text, verify important details against the source page, and clearly report empty or partial extraction results.

## Reference(s):

- [Weixin Article Reader on ClawHub](https://clawhub.ai/ricknote/skills/weixin-article-reader)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON from the extraction script and human-readable text or Markdown in agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extracted article content is untrusted and may be partial or empty when pages block extraction or use unsupported structures.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
