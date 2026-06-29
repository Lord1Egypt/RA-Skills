## Description: <br>
Deep Weibo trending analysis that clusters topics, detects trend inflection points, and generates content angles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and social media analysts use this skill to monitor public Weibo trends, group hot topics, identify rapid movers, and produce daily trend reports with content angle suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may fetch or scrape public Weibo trend data. <br>
Mitigation: Use only public trend data, respect platform access limits, and avoid adding credentialed or account-mutating behavior without separate review. <br>
Risk: Monitoring may keep or compare trend snapshots during user-directed analysis. <br>
Mitigation: Scope snapshot retention to the monitoring task and avoid storing unnecessary personal or sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/weibo-trend-analyzer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown or JSON reports with clustered topics, trend status, heat metrics, and content suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include topic clusters, heat deltas, trend duration, related-topic maps, and user-filtered domains.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
