## Description: <br>
Receive and engage with transcribed voice memos from Yapp, a voice journaling app, including raw speech-to-text recordings and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earu723](https://clawhub.ai/user/earu723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who connect Yapp to an agent use this skill to fetch new transcribed voice memos, store relevant facts or commitments, and receive brief summaries, questions, or reflections about the recordings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent ongoing access to private voice-journal transcripts. <br>
Mitigation: Install only when that access is intended; confirm where the API key is stored and review or delete transcript-derived memories as needed. <br>
Risk: Heartbeat polling can continue fetching new recordings until the integration is paused or disabled. <br>
Mitigation: Confirm how to pause or disable polling and limit checks to situations where continued transcript access is appropriate. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Plain text or Markdown summaries with API usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a stored Yapp API key to poll for new transcripts and update memory from transcript content.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
