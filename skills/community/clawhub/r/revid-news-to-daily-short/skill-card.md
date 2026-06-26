## Description: <br>
Generate a daily news short on a topic Revid researches itself for recurring news-of-the-day channels where the user supplies only the topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and automation teams use this skill to configure Revid to fetch fresh news for a topic, summarize it, and render a recurring short-form video. It is suited to daily channel workflows that schedule one render at a time and then review or publish the returned video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Revid API key and may be used with connected social accounts. <br>
Mitigation: Store REVID_API_KEY in a trusted secret manager, scope connected accounts deliberately, and install only where Revid is trusted with those credentials. <br>
Risk: Freshly generated news videos may contain inaccurate, stale, or off-brand summaries. <br>
Mitigation: Use the render/status flow first and review each generated video for accuracy and brand fit before publishing. <br>
Risk: Scheduled publishing can post generated videos without timely human review. <br>
Mitigation: Keep public posting behind a deliberate approval step unless the account scope, topic, and review process are already controlled. <br>


## Reference(s): <br>
- [Daily News Short on ClawHub](https://clawhub.ai/api00/revid-news-to-daily-short) <br>
- [Revid Render API endpoint](https://www.revid.ai/api/public/v3/render) <br>
- [Revid Status API endpoint](https://www.revid.ai/api/public/v3/status) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP, JSON, and Bash examples; Revid API responses are JSON and may include a videoUrl when rendering is ready.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVID_API_KEY. The default example renders a 9:16, 45-second news short and polls status until completion.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
