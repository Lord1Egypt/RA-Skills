## Description: <br>
Analyzes a Rakuten shop URL or shopCode by sending the shop input to a hosted analysis service and returning structured shop results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abca12a](https://clawhub.ai/user/abca12a) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to evaluate Rakuten shops for competitor research, shop structure analysis, popular item review, and quick report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shop URLs or shopCodes are sent to the disclosed hosted service for analysis. <br>
Mitigation: Use the skill only with Rakuten shop identifiers that are acceptable to send to that service, and avoid including unrelated confidential information. <br>
Risk: Server-resolved GitHub import provenance is unavailable for this version. <br>
Mitigation: Verify the publisher profile or repository separately when stronger provenance is required. <br>
Risk: Hosted analysis can be rate-limited, time out, or return no final result during a single invocation. <br>
Mitigation: Report incomplete runs clearly and ask the user to retry later instead of promising background monitoring or later proactive follow-up. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abca12a/rakuten-shop-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/abca12a) <br>
- [Disclosed hosted analysis service](https://rakuten.845817074.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Structured JSON from the runner, suitable for a human-facing analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns compact shop, catalog, bucket, degradation, summary, and bucket-detail fields for the requested shop input.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
