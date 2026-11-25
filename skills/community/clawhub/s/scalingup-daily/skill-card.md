## Description:

Generates a structured Markdown daily report tracking recent search, advertising, and recommendation-system Scaling Up research, articles, open-source projects, and conference activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fandywang87](https://clawhub.ai/user/fandywang87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical operators use this skill to collect recent recommendation-system and advertising-model developments, assemble a daily Markdown report, and publish it to configured knowledge-sharing destinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill publishes generated reports through authenticated IMA and Tencent Docs accounts.

Mitigation: Make publication opt-in, verify destination IDs and document titles before upload, and use accounts scoped for this workflow.

Risk: The skill reads local IMA credentials and depends on Tencent Docs authorization.

Mitigation: Protect stored credentials, rotate them if exposed, and confirm tokens are valid only for the intended workspace or account.

Risk: The skill includes unsafe cross-skill helper discovery for upload support.

Mitigation: Replace recursive helper discovery with a fixed, reviewed helper path or an explicit user-provided path before production use.

Risk: The skill searches external sites and includes Sogou/WeChat scraping behavior.

Mitigation: Review whether this scraping is acceptable for the deployment environment and respect site access restrictions before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fandywang87/skills/scalingup-daily)
- [Known papers and project references](references/known_papers.md)
- [Daily report template](templates/daily_report_template.md)
- [Meta generative recommenders](https://github.com/meta-recsys/generative-recommenders)
- [Kuaishou OneRec OpenOneRec](https://github.com/Kuaishou-OneRec/OpenOneRec)
- [RecBole](https://github.com/RUCAIBox/RecBole)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with citations, plus supporting shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated Markdown report and may publish it to IMA and Tencent Docs when required accounts and credentials are configured.]

## Skill Version(s):

3.0.0 (source: server release metadata and artifact/_meta.json; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
