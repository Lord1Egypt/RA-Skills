## Description:

WHOOP Guru helps agents fetch WHOOP wearable data, analyze recovery, sleep, HRV, strain, and workouts, generate charts, and provide personalized fitness coaching and training plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effeceee](https://clawhub.ai/user/effeceee)

### License/Terms of Use:

MIT-0

## Use Case:

External users with WHOOP devices use this skill to sync wearable health data, review recovery and training trends, generate reports and charts, and receive fitness coaching or plans. Agents can also help configure OAuth, local data storage, optional LLM providers, check-ins, and scheduled reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive WHOOP recovery, sleep, workout, profile, and body data.

Mitigation: Install only when this data access is acceptable, review requested WHOOP scopes, and share the minimum data needed for coaching or reports.

Risk: AI analysis may transmit personal health data, goals, and check-ins to a user-configured LLM provider.

Mitigation: Use only trusted HTTPS LLM endpoints and review the provider's data handling terms before enabling LLM coaching.

Risk: WHOOP and LLM credentials are stored in local files, and one command can print the current access token.

Mitigation: Prefer the OAuth flow, restrict permissions on credential files, avoid printing or logging tokens, and delete local credential directories when access is no longer needed.

Risk: The server security verdict is suspicious because the skill is purpose-aligned but has weak controls around health data and credentials.

Mitigation: Review the skill before deployment, limit workspace and file-system exposure, and run it only in environments where local credential storage is acceptable.

Risk: Health and training recommendations may be inaccurate or unsuitable for a user's medical context.

Mitigation: Treat outputs as wellness guidance and seek qualified medical advice for health concerns, abnormal metrics, or injury decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/effeceee/skills/whoop-guru)
- [WHOOP API Reference](references/api.md)
- [Health Data Analysis Guide](references/health_analysis.md)
- [WHOOP API OAuth Guide](docs/whoop_api_guide.md)
- [WHOOP Developer Platform](https://developer.whoop.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML]

**Output Format:** [Markdown guidance, shell commands, local JSON state, and interactive HTML charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use WHOOP API data and user-configured LLM providers; generated advice should be reviewed as wellness guidance, not medical advice.]

## Skill Version(s):

8.4.12 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
