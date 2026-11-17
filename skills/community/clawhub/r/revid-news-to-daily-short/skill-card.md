## Description:

Generate a daily news short on a topic Revid researches itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and automation developers use this skill to generate recurring short-form daily news videos from a topic or niche. The skill is suited for scheduled news-of-the-day channels where Revid researches fresh news, writes the script, and produces the video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topics and prompts are sent to Revid through an outbound API request.

Mitigation: Install only when sharing those topics with Revid is acceptable for the intended workflow.

Risk: The skill uses REVID_API_KEY for rendering and status checks.

Mitigation: Store the key in managed configuration or secrets and avoid logging or committing it.

Risk: Scheduled or publish-now workflows can push generated videos to public social accounts without timely review.

Mitigation: Review generated videos before enabling cron jobs or public publishing, especially for regulated or sensitive topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/api00/skills/revid-news-to-daily-short)
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render)
- [Revid status API endpoint](https://www.revid.ai/api/public/v3/status)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with HTTP, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVID_API_KEY and sends the supplied topic or prompt to Revid for video generation.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
