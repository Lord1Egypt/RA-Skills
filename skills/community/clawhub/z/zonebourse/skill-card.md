## Description:

Fetch stock slugs, retrieve categorized ZoneBourse news article links, and read article metadata and content through local Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredguile](https://clawhub.ai/user/fredguile)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis agents use this skill to look up ZoneBourse stock slugs, collect categorized market-news links for a stock, and extract article dates, titles, content, and paywall status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscriber session cookies can expose account access if stored or shared insecurely.

Mitigation: Use only cookies for an account you control, treat cookies.txt as a password-equivalent secret, restrict file permissions, and never commit cookie files.

Risk: The article reader accepts a URL argument and sends the cookie header with the request.

Mitigation: Run read_article.py only with verified ZoneBourse HTTPS article links and add hostname allowlisting before relying on subscriber cookies.

Risk: Automated requests may be rate limited or blocked by the external site.

Mitigation: Follow the documented 2-5 second delay between requests and expect access failures or paywall-only teaser responses.

## Reference(s):

- [ClawHub Zonebourse skill page](https://clawhub.ai/fredguile/skills/zonebourse)
- [ZoneBourse](https://www.zonebourse.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article extraction may return full content or a teaser depending on subscriber access; full article content is truncated by the helper script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
