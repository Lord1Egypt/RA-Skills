## Description: <br>
Automatically accesses Xiaohongshu's Explore page via browser automation, inputs keywords into the search bar, and collects the list of related keywords from the auto-suggest dropdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content researchers use this skill to collect Xiaohongshu search suggestion terms for keyword research, SEO planning, content topic selection, and competitor analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Entered keywords are submitted to Xiaohongshu while collecting auto-suggest results. <br>
Mitigation: Avoid confidential personal or business terms when using the skill. <br>
Risk: Search activity may be associated with the active browser session or account. <br>
Mitigation: Use a logged-out or separate browser session when the activity should not be tied to a main account. <br>
Risk: Xiaohongshu may show captchas, restrictions, or incomplete suggestions depending on login state and anti-crawling controls. <br>
Mitigation: Pause automation and ask the user to handle manual challenges or login requirements before continuing. <br>


## Reference(s): <br>
- [Xiaohongshu Explore](https://www.xiaohongshu.com/explore) <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/xiaohongshu-keyword-collector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown keyword lists grouped by input keyword] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Suggestions are collected from Xiaohongshu's browser auto-suggest dropdown and may vary by session, login state, locale, and platform availability.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
