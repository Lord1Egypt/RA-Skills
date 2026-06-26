## Description: <br>
Xiaohongshu (RED) search suggestion keyword collection tool that uses browser automation to visit the Xiaohongshu Explore page, type keywords in the search bar, and collect auto-suggest keywords from the dropdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and content strategists use this skill to collect Xiaohongshu search suggestions for keyword research, SEO/GEO optimization, content planning, hashtag strategy, and competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes browser automation guidance for Xiaohongshu and evidence.security flags concern around bypassing CAPTCHA or other platform protections. <br>
Mitigation: Do not use the skill to bypass CAPTCHA or other platform protections; keep collection low-frequency and stop when platform controls appear. <br>
Risk: Submitted keywords plus browser and network metadata may be visible to Xiaohongshu, especially when using a logged-in browser session. <br>
Mitigation: Use an isolated browser profile and avoid logged-in sessions unless the account and privacy risk is intentionally accepted. <br>


## Reference(s): <br>
- [Xiaohongshu Search Suggest DOM Selectors](references/selectors.md) <br>
- [Xiaohongshu Explore](https://www.xiaohongshu.com/explore) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks, plus JSON-shaped keyword results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces seed-keyword to suggestion-list mappings; selector behavior may require adjustment when Xiaohongshu changes its DOM.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
