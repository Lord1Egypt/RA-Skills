## Description: <br>
Post native X/Twitter threads by chaining reply-to calls through Twitter API v2 for multi-tweet content workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams and agents use this skill to preview, post, or schedule native X/Twitter threads from prepared markdown thread drafts when single-post schedulers are insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post and schedule public X/Twitter threads from an agent-controlled workflow. <br>
Mitigation: Run preview or dry-run first, confirm the target account, and require human approval before posting or scheduling. <br>
Risk: Security evidence notes a mismatch between the declared credential environment variable and the local credential store described by the artifact. <br>
Mitigation: Confirm which credential source is actually used, which account it controls, and limit or rotate credentials after use. <br>
Risk: Scheduled jobs and thread logs can persist after the agent session. <br>
Mitigation: Inspect or cancel queued jobs and remove queued post files or logs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/twitter-thread-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce preview checks, scheduled job instructions, and queue or log file guidance for thread posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
