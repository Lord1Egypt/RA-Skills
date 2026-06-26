## Description: <br>
Resume Context retrieves coding session briefings and developer notes through the resume CLI, with Redis caching for returned session output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickleodoen](https://clawhub.ai/user/nickleodoen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to catch up on recent coding sessions, project briefings, and developer notes for a named project. It is intended for agents that can run the resume CLI bridge and return the resulting session summary to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive developer-session data from local project history. <br>
Mitigation: Install only for trusted workspaces, avoid capturing secrets in resume sessions, and provide explicit project names or paths before invoking it. <br>
Risk: Session briefings may be processed through the user's configured resume LLM workflow. <br>
Mitigation: Use an approved LLM provider configuration and review session notes for sensitive content before relying on generated briefings. <br>
Risk: Raw briefing output may be cached in Redis. <br>
Mitigation: Use a private authenticated Redis database and keep the cache TTL short or disable caching where sensitive projects are involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickleodoen/resume-context) <br>
- [resume CLI](https://github.com/nickleodoen/resume) <br>
- [Redis Cloud](https://cloud.redis.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON envelope containing an output string; user-facing content may be plain text or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Redis caching when available and returns cached status metadata with cached responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
