## Description: <br>
Detects delivery packages in surveillance images or videos and returns package counts, locations, stale-package status, and report output for package-area monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to analyze package-area camera images or videos for delivery package presence, counts, positions, stale-package alerts, and historical report lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package-area images or videos and open-id/user identifiers are sent to configured remote services. <br>
Mitigation: Use only with media and identifiers approved for those services; confirm retention, access controls, and data-handling terms before deployment. <br>
Risk: The security evidence reports under-disclosed account, token, and broader analysis/reporting behavior. <br>
Mitigation: Review the publisher documentation and configuration before installing; limit API keys, tokens, and report-query permissions to the minimum required. <br>
Risk: The skill package includes broader analysis/reporting components beyond the package-detection description. <br>
Mitigation: Keep deployment scoped to package detection and do not use it in sensitive surveillance settings unless the publisher clarifies what analysis is performed and whether face or health-related analysis is disabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-package-detection-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [Package detection API documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report text and JSON returned from remote analysis and history-report APIs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an image/video path or URL and an open-id/user identifier; output may include package counts, package locations, stale-package status, report links, and history records.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
