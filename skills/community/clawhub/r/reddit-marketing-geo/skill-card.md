## Description: <br>
Spawns a specialized sub-agent to monitor Reddit and optimize for GEO, with a scheduled 9 AM and 6 PM default report cadence for lead drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muhammedilyasy](https://clawhub.ai/user/muhammedilyasy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketing operators and founders use this skill to monitor recent Reddit discussions, receive verified thread digests, and draft brand replies for human approval before posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A recurring Reddit-monitoring agent may continue producing reports after the user's needs or schedule change. <br>
Mitigation: Review the configured schedule, confirm the intended Reddit account before use, and disable or change the twice-daily schedule when it is no longer needed. <br>
Risk: Marketing digests could include inaccurate or stale Reddit thread references. <br>
Mitigation: Use the required URL verification pipeline, include the exact fetched URL, title, and comment count in each digest, and re-validate the thread immediately before posting. <br>
Risk: Drafted replies could be posted from the wrong account or without sufficient review. <br>
Mitigation: Require an explicit Go or Post approval for each draft before submitting any Reddit comment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muhammedilyasy/reddit-marketing-geo) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/muhammedilyasy) <br>
- [Author website](https://ilyasy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown digest with verified Reddit thread metadata and draft reply text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human approval before any browser-based Reddit post; default schedule is 9 AM and 6 PM daily.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
