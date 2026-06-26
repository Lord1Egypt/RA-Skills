## Description: <br>
YoudaoNote News analyzes recent favorite Youdao Note entries, extracts topics of interest, searches for recent articles, and produces a dated news briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lephix](https://clawhub.ai/user/lephix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Youdao Note accounts use this skill to turn recent favorite notes into a concise news briefing and optionally schedule a recurring daily brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private Youdao note content and sends derived interests to configured search providers. <br>
Mitigation: Install only when that data flow is acceptable, keep API credentials scoped to the intended account, and avoid using the skill with sensitive note collections. <br>
Risk: The skill can create a recurring daily news brief in the background. <br>
Mitigation: Enable the schedule only when recurring briefs are desired, review existing cron jobs, and use the documented close or remove flow to disable it. <br>
Risk: Security evidence flags insecure temporary file handling. <br>
Mitigation: Run in an isolated environment and prefer an updated version that uses secure temporary file creation before handling sensitive notes. <br>
Risk: Broad activation phrases may trigger note retrieval and external searches unintentionally. <br>
Mitigation: Review trigger phrases before deployment and limit activation to users who understand the data access and search behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lephix/youdaonote-news) <br>
- [Publisher profile](https://clawhub.ai/user/lephix) <br>
- [Perplexity API settings](https://www.perplexity.ai/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown briefing with article links and a summary table; management flows use shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses recent favorite notes, caps extracted topics and articles, and can create or remove a daily OpenClaw cron schedule.] <br>

## Skill Version(s): <br>
1.7.8 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
