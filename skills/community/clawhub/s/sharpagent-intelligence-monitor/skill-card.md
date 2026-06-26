## Description: <br>
SharpAgent Intelligence Monitor is a multi-track intelligence aggregation skill that collects public AI and technology signals, scores candidates, applies five-factor trust checks, and produces structured daily briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and teams use this skill to monitor public AI, technology, research, GitHub, and China tech sources and turn them into concise briefings for trend tracking and competitive awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public web and API sources, so source availability, rate limits, or stale upstream content can affect briefing completeness. <br>
Mitigation: Configure trusted fetch scripts and review missing-source warnings before relying on a briefing for operational decisions. <br>
Risk: Archived briefings and ontology records may retain public-source intelligence longer than intended. <br>
Mitigation: Decide storage location, retention period, and access controls before enabling archival behavior. <br>
Risk: Scored business, funding, or competitive claims can still be incomplete or misleading. <br>
Mitigation: Verify important claims independently, especially before using them in business or customer-facing decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yezhaowang888-stack/sharpagent-intelligence-monitor) <br>
- [36kr hotlist endpoint](https://openclaw.36krcdn.com/media/hotlist/{date}/24h_hot_list.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with ranked sections, links, trust scores, signal summaries, and optional shell commands for source fetching.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports warm, professional, and deep briefing modes; may archive briefings and ontology records when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
