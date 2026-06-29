## Description: <br>
Yufluentcn Comp Scrape performs batch competitor comparison from user-provided CSV exports or authorized API snapshots through Yufluent's cloud service; it is not an unauthorized web scraper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and ecommerce teams use this skill to compare batches of competitor listings from their own CSV exports or authorized API snapshots across supported commerce platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected competitor/export data and optional listing text to Yufluent's cloud service. <br>
Mitigation: Use it only when organizational policy permits that cloud processing, and avoid confidential business data unless approved. <br>
Risk: The skill requires an API token and supports a TOKENAPI_BASE_URL override. <br>
Mitigation: Keep TOKENAPI_KEY in a trusted environment and check any TOKENAPI_BASE_URL override before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-comp-scrape) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text competitor comparison report, with optional JSON returned by the cloud API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY; may read competitor data from inline text or a local CSV/text file and send it to Yufluent's cloud service.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
