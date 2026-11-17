## Description:

Checks the current version of the Yiri bookkeeping app by reading its Huawei AppGallery listing with Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taobaoaz](https://clawhub.ai/user/taobaoaz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese-language questions about the latest Yiri app version and update status. It returns concise version information, a source link, and the check timestamp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch Playwright/Chromium and make a network request when broad Yiri app-name triggers match.

Mitigation: Review trigger scope before deployment and tighten it if accidental browser launches or network requests would be a concern.

Risk: The returned version depends on the availability and page structure of a fixed Huawei AppGallery listing.

Mitigation: Treat failed or missing version responses as a signal to retry later or inspect the source listing before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taobaoaz/skills/yiri-app-monitor)
- [Huawei AppGallery listing for Yiri](https://appgallery.huawei.com/app/detail?id=com.ericple.onebill)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Concise text or JSON containing app name, app ID, version, URL, and checked_at timestamp.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, Playwright, and Chromium; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
