## Description: <br>
Queries and formats China social insurance and housing fund contribution bases and rates by area; current security evidence says the implementation returns limited static mock data rather than verified nationwide current policy data. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[elysiacwy](https://clawhub.ai/user/elysiacwy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and HR or payroll staff can ask an agent for area-specific Chinese social insurance and housing fund contribution tables. Results should be treated as illustrative unless the publisher replaces mock data with verified official sources and effective dates. <br>

### Deployment Geography for Use: <br>
China mainland <br>

## Known Risks and Mitigations: <br>
Risk: The release claims official nationwide current policy coverage, while security evidence says the implementation returns static mock data for only three cities. <br>
Mitigation: Treat outputs as illustrative and verify every result against official local human resources, social security, housing fund, or government sources before payroll, benefits, legal, or compliance use. <br>
Risk: Cached or stale policy data could be reused without clear source coverage or effective dates. <br>
Mitigation: Require source citations, effective dates, supported-region coverage, and documented cache/update behavior before relying on the data. <br>
Risk: Running the Python implementation may write a local cache file in the skill directory. <br>
Mitigation: Run it in an appropriate workspace and review retained cache data if query contents are sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elysiacwy/social-security-fund-query) <br>
- [Project homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown tables or JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local cache file when the Python implementation runs.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
