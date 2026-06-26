## Description: <br>
A three-layer review and quick-capture system that connects current inputs, historical reviews, and daily context to identify deeper behavior patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jack-Yang-ai](https://clawhub.ai/user/Jack-Yang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and external users use this skill to capture quick notes, run daily, weekly, and monthly reviews, and receive structured coaching that connects recent inputs with historical patterns and daily summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect and persist broad local conversation history for behavioral analysis. <br>
Mitigation: Review the configured transcript and memory paths before enabling it, add source filters, and avoid using it around highly sensitive chats unless that data can be summarized and reused later. <br>
Risk: Persistent coaching memory may include review notes, commitments, daily summaries, and emotion signals. <br>
Mitigation: Keep the memory location access-restricted, use a retention and deletion process, and periodically review stored records for unnecessary sensitive data. <br>
Risk: Daily Digest and reminder workflows may run on a schedule and process recent session transcripts. <br>
Mitigation: Enable cron only after confirming the schedule, transcript directory, output directory, and deletion controls match the user's expectations. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Templates](references/templates.md) <br>
- [Reminders](references/reminders.md) <br>
- [Raw Input Extraction Script](scripts/extract-raw-inputs.py) <br>
- [Daily Digest Extraction Script](scripts/extract-daily-digest.py) <br>
- [Markdown to JSONL Migration Script](scripts/migrate-md-to-jsonl.py) <br>
- [Trigger Router Script](scripts/trigger-router.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and concise chat text, with JSONL memory records and optional shell command or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist review notes, captures, commitments, emotion labels, and daily summaries under local memory paths.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release metadata; artifact metadata shows 2.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
