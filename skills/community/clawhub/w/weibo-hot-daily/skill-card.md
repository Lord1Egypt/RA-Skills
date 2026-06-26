## Description: <br>
Fetches current Weibo hot-search topics, prints them for review, and can export the results with a simple generated summary. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[qq853632587](https://clawhub.ai/user/qq853632587) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Weibo hot-search topics for personal monitoring, reporting, or lightweight analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes an undisclosed Weibo session cookie that should be treated as an exposed credential. <br>
Mitigation: Remove the bundled cookie before use, rotate any affected session, and require users to supply their own valid credentials only when needed. <br>
Risk: The release advertises AI summary, notification, and scheduling capabilities that the security evidence says are not clearly implemented. <br>
Mitigation: Verify the installed behavior locally and rely only on the script outputs that are actually implemented until later versions document those features clearly. <br>
Risk: The skill retrieves data from Weibo and its own documentation limits use to personal learning and technical research. <br>
Mitigation: Review Weibo's terms and the release disclaimer before use, and avoid illegal, unauthorized, or production uses outside the documented limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qq853632587/weibo-hot-daily) <br>
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, shell commands] <br>
**Output Format:** [Terminal text, JSON files, or CSV files produced by the Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and outbound access to Weibo endpoints; supports flags such as --top, --summary, --output, and --format.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
