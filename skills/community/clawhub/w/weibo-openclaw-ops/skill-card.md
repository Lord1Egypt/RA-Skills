## Description: <br>
Weibo operations for OpenClaw via server-side browser automation. Use when the user asks to log in by QR, persist session state, read feed/messages/hot topics, summarize recent posts, publish posts, or run safe like/follow workflows with explicit limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiami2019](https://clawhub.ai/user/xiami2019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to operate Weibo through server-side browser automation, including QR login, persisted session checks, feed and message review, hot-topic scans, latest-post summaries, and explicitly scoped posting, liking, or following workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A reusable logged-in Weibo session is stored on a remote server. <br>
Mitigation: Install only if comfortable with remote session persistence, and delete the saved state or revoke the Weibo session when finished. <br>
Risk: Posting, commenting, reposting, liking, or following can mutate the Weibo account. <br>
Mitigation: Require explicit user intent, scope, and action limits before any mutating workflow. <br>
Risk: Recurring keepalive checks can keep the remote session active longer than intended. <br>
Mitigation: Use keepalive only when intentionally desired, keep it read-only, and stop it when session persistence is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with browser automation commands and concise audit summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include actions performed, success or skipped counts, skip reasons, and the next suggested action.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
