## Description: <br>
搜索Twitter/X上特定话题的最新内容并汇总报告。当用户说"搜Twitter"、"查看Twitter上关于XX的讨论"、"twitter research"、"X上最近在聊什么"时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sawzhang](https://clawhub.ai/user/sawzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and researchers use this skill to search Twitter/X for current topic discussions, gather relevant posts across multiple keyword variants, deduplicate results, and produce a structured Markdown summary of trends and notable projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in browser session for Twitter/X research, which may expose account context or session state during collection. <br>
Mitigation: Use a separate Chrome profile or test X account where possible, review browser automation steps before execution, and close the browser-use session after collection. <br>
Risk: The skill may install external browser automation tooling and adjust proxy environment variables as part of setup. <br>
Mitigation: Approve any browser-use installation explicitly and review setup commands before running them in a trusted environment. <br>
Risk: Fallback API paths may send tweet URLs, tweet IDs, and research topics to fxtwitter or vxtwitter. <br>
Mitigation: Avoid sensitive research topics in fallback mode and assume those identifiers may be shared with the fallback services. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sawzhang/twitter-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries group deduplicated tweets by topic and include keyword lists, source method, collection time, trends, and notable tools or projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
