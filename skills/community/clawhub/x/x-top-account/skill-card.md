## Description:

Tracks daily influential X (Twitter) account rankings from RedFox data, with filtering by gender and industry, pagination, Markdown summaries, HTML report generation, and user-confirmed daily subscription support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brands, MCN and cross-border operations teams, and industry analysts use this skill to find benchmark X accounts, evaluate creator candidates, monitor competitor rankings, and generate shareable ranking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key stored in the agent environment.

Mitigation: Use an environment variable or agent secret configuration, verify the key source and revocability, and avoid hardcoding or exposing the key in prompts, logs, or output files.

Risk: The skill writes local JSON data and HTML report files.

Mitigation: Run it only in workspaces where local report generation is intended, and review generated files before sharing them externally.

Risk: Daily ranking subscriptions can create recurring automated pushes.

Mitigation: Create subscriptions only after explicit user confirmation and review OpenClaw automation settings to modify or stop scheduled pushes.

Risk: Generated HTML reports load html2canvas from a CDN for image export.

Mitigation: Open generated reports with awareness that image export depends on an external CDN script; use PDF export or disable external loading when required by policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/x-top-account)
- [X Hot Account API Documentation](references/api_docs.md)
- [Industry Category Mapping](references/category_map.md)
- [RedFox Ranking API Endpoint](https://redfox.hk/story/api/x/hotAccount/rankList)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Files, Configuration, Guidance]

**Output Format:** [Markdown ranking table and analysis, JSON data files, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; report and data files are written under the skill output directory unless an explicit output path is supplied.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
