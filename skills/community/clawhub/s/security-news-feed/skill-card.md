## Description:

Collects and summarizes Korean security news hourly from 11 sources using Gemini API, then publishes to Notion and optionally to Tistory blog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rebugui](https://clawhub.ai/user/rebugui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to monitor Korean security advisories, filter relevant security news, summarize findings, and prepare publication-ready updates for Notion or Tistory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically create or update Notion records.

Mitigation: Use a dedicated Notion database and a least-privilege integration token scoped only to the intended workspace and database.

Risk: AI-generated summaries or posts may be inaccurate, misleading, or unsuitable for direct publication.

Mitigation: Require human review before publishing summaries or analysis to shared Notion pages or a public Tistory blog.

Risk: Automatic archival behavior may remove or hide records that still need operational review.

Mitigation: Disable or patch the 90-day archival cleanup until the retention policy is confirmed.

Risk: Tistory publishing uses browser-session automation.

Mitigation: Keep Tistory publishing disabled unless the runtime profile and account session are intentionally approved for automated posting.

Risk: Unpinned dependencies can change behavior or introduce new vulnerabilities.

Mitigation: Pin dependencies and review updates before deploying the skill in a scheduled workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rebugui/skills/security-news-feed)
- [KRCERT](https://www.krcert.or.kr)
- [NCSC](https://www.ncsc.go.kr)
- [Boho](https://www.boho.or.kr)
- [DailySecu](https://dailysecu.com)
- [KISA](https://www.kisa.or.kr)
- [K-shield](https://k-shield.or.kr)
- [Gemini API Key Setup](https://makersuite.google.com/app/apikey)
- [Notion Integrations](https://www.notion.so/my-integrations)
- [Tistory API Guide](https://www.tistory.com/guide/api/register)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown security-news summaries with source links, tags, and publication-ready Notion or Tistory content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured API credentials for summarization and publishing integrations.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
