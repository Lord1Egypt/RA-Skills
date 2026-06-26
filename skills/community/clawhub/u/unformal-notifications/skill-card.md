## Description: <br>
Get notified when someone completes an Unformal Pulse via a scheduled Claude Code routine, a local desktop listener, or on-demand API polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonasboury](https://clawhub.ai/user/jonasboury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor Unformal Pulse completions, set up local or scheduled notifications, and summarize new response data when asked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Unformal API key and accesses Pulse response data. <br>
Mitigation: Use a scoped, rotatable API key, avoid sharing secrets in transcripts, and review where response data is stored. <br>
Risk: The local listener writes event JSON files to ~/.unformal/inbox, which may contain sensitive response content. <br>
Mitigation: Periodically clean or archive the inbox and apply local access controls appropriate for the data. <br>
Risk: The install flow downloads a shell listener from unformal.ai. <br>
Mitigation: Verify the downloaded listener against the bundled script or another trusted source before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jonasboury/unformal-notifications) <br>
- [Unformal website](https://unformal.ai) <br>
- [Unformal API settings](https://unformal.ai/studio/settings) <br>
- [Unformal SSE stream docs](https://unformal.ai/agents) <br>
- [Listener source](https://unformal.ai/unformal-listen.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local listener commands, scheduled routine instructions, notification setup, and response summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
