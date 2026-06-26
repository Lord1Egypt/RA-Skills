## Description: <br>
Fetches the top 10 trending X.com results for a chosen keyword, translates titles to Chinese, generates a full-screen news poster, and sends it to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airbai](https://clawhub.ai/user/airbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create Chinese-language daily or on-demand X.com keyword briefings as poster files. It supports manual keyword requests and scheduled briefing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill browses X.com, creates local poster files, captures screenshots or PDFs, and sends the result through a messaging channel. <br>
Mitigation: Install only when that behavior is intended, review the generated file before sending when appropriate, and use the chosen messaging channel deliberately. <br>
Risk: Scheduled daily briefings can recur without fresh user intent. <br>
Mitigation: Keep scheduled runs disabled unless the user explicitly requests recurring briefings, and confirm ambiguous daily brief requests before execution. <br>
Risk: X.com results, translations, and summaries may omit context or misstate fast-moving news. <br>
Mitigation: Treat the poster as a briefing draft and verify important claims against the original posts or other reliable sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/airbai/x-news-daily) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with generated HTML poster files and Chrome screenshot or PDF commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs exactly 10 news items, with Chinese title translation and 1-2 sentence summaries for each item.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
