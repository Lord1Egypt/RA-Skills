## Description: <br>
Searches Xiaohongshu trending notes by keyword, ranks popular posts by relevance, popularity, and timeliness, and returns Markdown results plus a local HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brands, MCN teams, and content operators use this skill to find high-engagement Xiaohongshu notes, compare topic trends, and generate benchmark reports for content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Redfox API key and sends Xiaohongshu search keywords to the Redfox API. <br>
Mitigation: Install only when this data flow is acceptable; keep REDFOX_API_KEY in environment or agent configuration and avoid exposing it in code, prompts, logs, or generated outputs. <br>
Risk: Each search may create a local HTML report that contains the query, Xiaohongshu result links, and retrieved content metadata. <br>
Mitigation: Review generated reports before sharing and retain or delete them according to the user's data-handling requirements. <br>
Risk: Optional calendar subscriptions can persist the selected keyword and time range. <br>
Mitigation: Create subscriptions only after explicit user choice, and record only the current search parameters needed for the reminder. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/if530770/xhs-explosive-content-detector) <br>
- [Xiaohongshu hot article format](references/xhs_hot_article_format.md) <br>
- [Redfox Hub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [Redfox Hub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown tables, plain text guidance, shell command snippets, JSON returned by the script, and local HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; sends Xiaohongshu search keywords to the Redfox API; creates local HTML reports; optional subscriptions retain the chosen keyword and time range.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
