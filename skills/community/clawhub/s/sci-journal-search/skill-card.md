## Description: <br>
Queries SCI journal information, including XinRui/CAS partition data, JCR category partitions, Top journal status, and optional LetPub metrics by journal name or ISSN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songxf1024](https://clawhub.ai/user/songxf1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and agents use this skill to look up SCI journal partitions and publication metrics while preparing literature reviews, publication plans, or journal comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Journal search terms are sent to disclosed external data sources. <br>
Mitigation: Use only when it is acceptable to submit the queried journal name or ISSN to XinRui and, when enabled, LetPub. <br>
Risk: Optional LetPub mode asks the agent to open a browser session. <br>
Mitigation: Use LetPub mode only in environments where browser automation is permitted and close the browser after the lookup as directed by the skill output. <br>
Risk: Journal metrics and partition data can become stale or differ across sources. <br>
Mitigation: Treat returned metrics as lookup results from the disclosed sources and verify against official publisher or index records before high-impact publication decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songxf1024/sci-journal-search) <br>
- [Partition system reference](references/partition-system.md) <br>
- [XinRui Journal Ranking](https://www.xr-scholar.com) <br>
- [LetPub journal search](https://www.letpub.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON produced by Python command-line scripts, with optional browser-action guidance for LetPub lookup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include journal partitions, ISSN/EISSN, publisher, Top status, impact-factor fields, citation metrics, review-cycle notes, and browser close instructions for optional LetPub mode.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata, package.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
