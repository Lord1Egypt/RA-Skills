## Description: <br>
Fetches current Zhihu hot-list topics from a public GitHub data source and outputs them as Markdown, JSON, or simple text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and content teams use this skill to inspect public Zhihu trending topics for content discovery, market research, public-opinion monitoring, or general awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes an outbound request to GitHub and returns third-party Zhihu hot-list content. <br>
Mitigation: Allow network access only where this data source is acceptable, and review returned topics and links before relying on them. <br>
Risk: Some advertised category filtering and trend-analysis commands are not present in the provided artifact. <br>
Mitigation: Use the reviewed get-hot.sh options only, or separately provide and review the missing scripts before use. <br>
Risk: The script can fail when the public data source is unavailable or its README format changes. <br>
Mitigation: Handle fetch or parsing failures in the calling workflow and verify the source format before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/zhihu-hot-cn) <br>
- [zhihu-hot-questions public data source](https://github.com/towelong/zhihu-hot-questions) <br>
- [SnailDev zhihu-hot-hub archive](https://github.com/SnailDev/zhihu-hot-hub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown, JSON, or simple newline-delimited text from a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports --limit and --format json|markdown|simple; category filtering and trend-analysis commands are not present in the provided artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
