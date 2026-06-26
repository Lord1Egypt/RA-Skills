## Description: <br>
Generates concise meeting summaries with key decisions, action items with owners, follow-up dates, and a brief three-sentence overview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, project teams, and developers can use this skill to turn meeting transcripts into structured notes for follow-up planning and accountability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts are sent to Anthropic for summarization. <br>
Mitigation: Use only with transcripts whose confidentiality and data-flow requirements permit processing by Anthropic with the user's API key. <br>
Risk: The skill depends on local command-line prerequisites and an API key. <br>
Mitigation: Confirm bash, curl, python3, and ANTHROPIC_API_KEY are available before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claudiodrusus/shelly-meeting-summarizer) <br>
- [Example output](example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown with Summary, Key Decisions, Action Items, and Follow-up Dates sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcript text is sent to Anthropic for summarization and the response is capped at 1500 max tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
