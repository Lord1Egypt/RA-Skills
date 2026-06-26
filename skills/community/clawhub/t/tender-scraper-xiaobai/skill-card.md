## Description: <br>
Scrapes public tender and procurement announcements from ygcg.nbcqjy.org for business intelligence, competitor analysis, and government procurement tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahuishao](https://clawhub.ai/user/jiahuishao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect structured public tender notices, inspect fields such as title, source URL, publish date, tags, and tender type, and prepare date/type grouped summaries for procurement monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to a public third-party procurement site and may fail or return incomplete data if the site changes, throttles, or is unavailable. <br>
Mitigation: Review the target site terms and results before operational use, handle request failures, and validate returned notices against source links. <br>
Risk: Dependencies are unpinned, which can introduce supply-chain or compatibility drift. <br>
Mitigation: Install from a trusted package index and pin vetted versions of requests and beautifulsoup4 before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiahuishao/tender-scraper-xiaobai) <br>
- [Public tender announcement source](https://ygcg.nbcqjy.org) <br>
- [Bulletin list API endpoint](https://ygcg.nbcqjy.org/api/Portal/GetBulletinList) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [JSON returned by the Python/CLI scraper, with Markdown summary guidance for date and tender-type grouping.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outbound HTTPS POST requests to ygcg.nbcqjy.org; configurable item limit in Python API and documented CLI examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
