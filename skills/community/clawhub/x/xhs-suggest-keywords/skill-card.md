## Description:

Xiaohongshu (RED) search suggestion keyword collection tool. Uses browser automation to visit the Xiaohongshu Explore page, type keywords in the search bar, and collect the auto-suggest keyword list from the dropdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content strategists use this skill to collect Xiaohongshu search suggestion keywords for keyword research, SEO/GEO planning, content strategy, hashtag planning, and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated collection from a third-party platform may violate Xiaohongshu's rules or applicable law if used without authorization.

Mitigation: Confirm that the intended collection is allowed before use and keep request rates conservative.

Risk: The artifact includes guidance that could be used for anti-bot or CAPTCHA-bypass behavior.

Mitigation: Do not use the skill to bypass CAPTCHA or access controls; stop collection when such controls appear.

Risk: Browser automation and npm dependencies can increase local execution risk.

Mitigation: Run Playwright in a limited environment and pin dependencies before installation.

Risk: Selectors for a React web client may change and produce incomplete or incorrect keyword results.

Mitigation: Validate selectors against the live page DOM before relying on collected suggestions.

## Reference(s):

- [Xiaohongshu Search Suggest DOM Selectors](references/selectors.md)
- [Xiaohongshu Explore](https://www.xiaohongshu.com/explore)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and shell command code blocks, plus sample JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a mapping from seed keywords to collected suggestion keyword lists.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
