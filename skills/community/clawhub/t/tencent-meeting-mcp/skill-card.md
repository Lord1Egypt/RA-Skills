## Description: <br>
Connects an agent to Tencent Meeting MCP tools for creating, updating, canceling, and querying meetings, managing participant lists, and retrieving recordings, transcripts, and AI summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris8265-cl](https://clawhub.ai/user/chris8265-cl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers with a Tencent Meeting token can use this skill to let an agent manage Tencent Meeting meetings, participants, recordings, transcripts, and summaries. It is most appropriate when the user has authority to access the relevant meeting content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive meeting information, including participant lists, recordings, transcript exports, recording links, meeting passwords, or host keys. <br>
Mitigation: Use a least-privilege Tencent Meeting token, confirm the user is authorized for the requested meeting content, and avoid sharing retrieved content outside approved contexts. <br>
Risk: The setup path registers an MCP endpoint with the user's Tencent Meeting token and may install mcporter globally if it is missing. <br>
Mitigation: Review the setup script before running it, install mcporter from a trusted source, and keep TENCENT_MEETING_TOKEN out of logs and shared shells. <br>
Risk: Meeting changes such as updates or cancellations can affect other participants. <br>
Mitigation: Require explicit user confirmation before modifying or canceling meetings, matching the behavior described in the artifact instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris8265-cl/tencent-meeting-mcp) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/chris8265-cl) <br>
- [Tencent Meeting MCP endpoint](https://mcp.meeting.tencent.com/mcp/wemeet-open/v1) <br>
- [Tencent Meeting AI skill token page](https://meeting.tencent.com/ai-skill) <br>
- [Tencent Meeting MCP tool reference](references/api_references.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON argument examples; MCP tool results may contain meeting details, participant data, recording links, transcript content, or summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TENCENT_MEETING_TOKEN and mcporter registration for the Tencent Meeting MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
