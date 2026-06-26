## Description: <br>
Audit any website across 8 quality signals to determine if it is outdated, broken, or neglected. Returns a structured audit dict used by the lead-scorer skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to audit public websites for liveness, freshness, technology, performance, mobile readiness, SSL status, and design-age signals. It produces structured findings that can feed lead scoring or follow-on enrichment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches target webpages and can return full page HTML into the agent workflow. <br>
Mitigation: Audit only URLs whose contents are appropriate for the workflow, avoid private or internal URLs, and treat returned HTML as untrusted input. <br>
Risk: PageSpeed checks can send audited URLs to Google PageSpeed when PAGESPEED_API_KEY is configured. <br>
Mitigation: Use a restricted PageSpeed API key and avoid submitting sensitive URLs. <br>
Risk: The skill depends on external Python packages for HTTP fetching, parsing, technology detection, and WHOIS behavior. <br>
Mitigation: Pin and review the listed dependencies before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/website-auditor) <br>
- [Google PageSpeed Insights API endpoint](https://www.googleapis.com/pagespeedonline/v5/runPagespeed) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and structured audit dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PAGESPEED_API_KEY for PageSpeed checks; returns raw HTML for live pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
