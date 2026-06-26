## Description: <br>
Collects high-ranking travel guide content from Xiaohongshu, Mafengwo, Ctrip, WeChat public accounts, and related platforms, then consolidates the findings into a weighted travel guide document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whhh1994](https://clawhub.ai/user/whhh1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel researchers, content operators, and agent users can use this skill to gather destination-specific travel posts from supported platforms, preserve source metrics, and produce a combined Markdown guide with weighted recommendations and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate a logged-in browser while scraping travel sites. <br>
Mitigation: Use a separate Chrome profile or disposable accounts, keep only the needed session open, and close the CDP-enabled browser after the task completes. <br>
Risk: The workflow references an external Xiaohongshu extraction helper for eval-based article extraction. <br>
Mitigation: Review the helper script before use and run it only from a trusted local skill path. <br>
Risk: Intermediate task, status, and data files can persist scraped content after the guide is generated. <br>
Mitigation: Review generated files, keep only the final guide when appropriate, and use the documented approval-based cleanup flow with trash instead of permanent deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whhh1994/tourism-guide-harvester) <br>
- [Publisher profile](https://clawhub.ai/user/whhh1994) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown travel guide with source tables, inline shell commands, and task/status/data file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces platform-specific intermediate task files and a consolidated destination guide with source links, mention counts, and freshness or seasonality weighting.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence and artifact version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
