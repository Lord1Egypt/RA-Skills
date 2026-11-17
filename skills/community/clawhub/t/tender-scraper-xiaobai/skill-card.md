## Description:

Crawls tender and procurement announcements from ygcg.nbcqjy.org and returns structured records for business intelligence, competitor analysis, and government procurement tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahuishao](https://clawhub.ai/user/jiahuishao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to collect tender and procurement announcements from ygcg.nbcqjy.org, then summarize records by date and tender type for market intelligence and procurement monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes disclosed outbound network requests to ygcg.nbcqjy.org to retrieve live tender announcement data.

Mitigation: Run it in a virtual environment or container and allow network access only to the expected data source when possible.

Risk: Runtime dependencies are not pinned in the artifact requirements file.

Mitigation: Pin reviewed versions of requests and any retained parser dependency before production deployment.

Risk: beautifulsoup4 is listed as a dependency even though the artifact behavior does not require it.

Mitigation: Remove beautifulsoup4 unless a reviewed update introduces behavior that actually needs it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiahuishao/skills/tender-scraper-xiaobai)
- [Source Website](https://ygcg.nbcqjy.org)
- [Bulletin List API Endpoint](https://ygcg.nbcqjy.org/api/Portal/GetBulletinList)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands]

**Output Format:** [JSON records and Markdown summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned records include fetch_time, total_count, title, url, publish_time, tags, and tender_type.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
