## Description: <br>
Provides a backward-compatible daily literature push workflow that retrieves recent arXiv papers for a research topic, summarizes them, rates relevance, and prepares push updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, engineers, and external users use this skill to monitor recent arXiv papers for a chosen field and receive concise daily Markdown reports with paper links, summaries, and relevance ratings. It can be triggered manually or scheduled as a recurring literature update. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Push-channel targets or messaging credentials may expose research topics, paper links, and generated summaries through the selected service. <br>
Mitigation: Provide only intended channel and target values, and review where generated reports are sent before enabling delivery. <br>
Risk: Recurring cron use can create scheduled network requests and repeated notifications. <br>
Mitigation: Review any cron job before adding it, keep the schedule scoped to the intended audience, and remove scheduled jobs when they are no longer needed. <br>
Risk: Paper summaries and relevance scores are generated from retrieved arXiv metadata and simple scoring logic, so they may omit nuance or overstate relevance. <br>
Mitigation: Treat the report as triage guidance and verify important claims against the linked paper or PDF before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jirboy/research-daily-push) <br>
- [Publisher Profile](https://clawhub.ai/user/jirboy) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [arXiv API Query Endpoint](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown literature report with paper tables, concise summaries, relevance ratings, PDF links, and scheduling or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Retrieves recent papers for a user-specified field, normally limited to 5-10 papers per run, with optional push-channel targets or saved Markdown output.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
